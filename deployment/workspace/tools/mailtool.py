#!/usr/bin/env python3
"""Minimal Zoho mail tool for OpenClaw workspace.

Commands:
  - send: send email via SMTP with fallback hosts (plain + optional HTML)
  - list: list recent emails from a mailbox
  - read: read one email by sequence id
  - search: search emails by IMAP query (e.g., FROM "foo@bar.com")

Environment variables:
  ZOHO_EMAIL, ZOHO_PASSWORD
  ZOHO_IMAP_HOST (default: imap.zoho.com)
  ZOHO_IMAP_FALLBACK_HOST (default: imappro.zoho.com)
  ZOHO_SMTP_ENDPOINTS (optional CSV of host:port:mode)
    default: smtp.zoho.com:587:starttls,smtp.zoho.com:465:ssl,smtppro.zoho.com:465:ssl

TLS options:
  ZOHO_CA_FILE (optional PEM bundle path)
  ZOHO_CA_DIR (optional certificate directory)
  ZOHO_SSL_INSECURE=1 (optional emergency bypass; disables certificate verification)
"""

from __future__ import annotations

import argparse
import email
import imaplib
import os
import smtplib
import ssl
import sys
from email.header import decode_header, make_header
from email.message import EmailMessage
from email.utils import make_msgid


def getenv_required(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise SystemExit(f"Missing required environment variable: {name}")
    return value


def decode_mime(value: str | None) -> str:
    if not value:
        return ""
    try:
        return str(make_header(decode_header(value)))
    except Exception:
        return value


def read_utf8_file(path: str, flag_name: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as exc:
        raise SystemExit(f"Failed to read {flag_name} '{path}': {exc}") from exc


def smtp_endpoints() -> list[tuple[str, int, str]]:
    raw = os.getenv(
        "ZOHO_SMTP_ENDPOINTS",
        "smtp.zoho.com:587:starttls,smtp.zoho.com:465:ssl,smtppro.zoho.com:465:ssl",
    )
    out: list[tuple[str, int, str]] = []
    for item in raw.split(","):
        item = item.strip()
        if not item:
            continue
        parts = item.split(":")
        if len(parts) != 3:
            continue
        host, port_s, mode = parts
        mode = mode.strip().lower()
        if mode not in {"ssl", "starttls"}:
            continue
        try:
            out.append((host.strip(), int(port_s), mode))
        except ValueError:
            continue
    if not out:
        out.append(("smtp.zoho.com", 587, "starttls"))
    return out


def imap_hosts() -> list[str]:
    primary = os.getenv("ZOHO_IMAP_HOST", "imap.zoho.com").strip()
    fallback = os.getenv("ZOHO_IMAP_FALLBACK_HOST", "imappro.zoho.com").strip()
    hosts = [h for h in [primary, fallback] if h]
    return hosts or ["imap.zoho.com", "imappro.zoho.com"]


def is_truthy_env(name: str) -> bool:
    return os.getenv(name, "").strip().lower() in {"1", "true", "yes", "on"}


def certifi_cafile() -> str | None:
    try:
        import certifi  # type: ignore

        path = certifi.where()
        return path if path else None
    except Exception:
        return None


def ssl_contexts() -> list[tuple[str, ssl.SSLContext]]:
    contexts: list[tuple[str, ssl.SSLContext]] = []

    ca_file = os.getenv("ZOHO_CA_FILE", "").strip()
    ca_dir = os.getenv("ZOHO_CA_DIR", "").strip()
    if ca_file or ca_dir:
        try:
            ctx = ssl.create_default_context(cafile=ca_file or None, capath=ca_dir or None)
            contexts.append(("custom-ca", ctx))
        except Exception as exc:
            print(f"warning: invalid ZOHO_CA_FILE/ZOHO_CA_DIR: {exc}", file=sys.stderr)

    contexts.append(("system-default", ssl.create_default_context()))

    certifi_path = certifi_cafile()
    if certifi_path:
        try:
            contexts.append(("certifi", ssl.create_default_context(cafile=certifi_path)))
        except Exception as exc:
            print(f"warning: certifi context unavailable: {exc}", file=sys.stderr)

    if is_truthy_env("ZOHO_SSL_INSECURE"):
        insecure = ssl.create_default_context()
        insecure.check_hostname = False
        insecure.verify_mode = ssl.CERT_NONE
        contexts.append(("insecure-no-verify", insecure))
        print("warning: ZOHO_SSL_INSECURE=1 disables TLS certificate verification", file=sys.stderr)

    return contexts


def connect_imap(email_addr: str, password: str) -> tuple[imaplib.IMAP4_SSL, str]:
    errors: list[str] = []
    contexts = ssl_contexts()

    for host in imap_hosts():
        for ctx_name, ctx in contexts:
            try:
                conn = imaplib.IMAP4_SSL(host, 993, ssl_context=ctx)
                conn.login(email_addr, password)
                return conn, host
            except imaplib.IMAP4.error as exc:
                raise SystemExit(f"IMAP authentication failed on {host}: {exc}") from exc
            except ssl.SSLCertVerificationError as exc:
                errors.append(f"{host} [{ctx_name}] cert-verify-failed: {exc}")
            except ssl.SSLError as exc:
                errors.append(f"{host} [{ctx_name}] ssl-error: {exc}")
            except Exception as exc:
                errors.append(f"{host} [{ctx_name}] {exc}")

    hint = " Set ZOHO_CA_FILE to your CA bundle path (or ZOHO_SSL_INSECURE=1 for emergency testing only)."
    raise SystemExit("IMAP connection failed: " + " | ".join(errors) + hint)


def smtp_send(
    email_addr: str,
    password: str,
    to: str,
    subject: str,
    body: str,
    html_body: str | None = None,
    in_reply_to: str | None = None,
    references: str | None = None,
    message_id: str | None = None,
) -> str:
    msg = EmailMessage()
    msg["From"] = email_addr
    msg["To"] = to
    msg["Subject"] = subject
    if message_id:
        msgid = message_id.strip()
        if not msgid.startswith("<"):
            msgid = f"<{msgid}>"
    else:
        msgid = make_msgid()
    msg["Message-ID"] = msgid
    if in_reply_to:
        msg["In-Reply-To"] = in_reply_to
    if references:
        msg["References"] = references
    msg.set_content(body)
    if html_body:
        msg.add_alternative(html_body, subtype="html")

    errors: list[str] = []
    contexts = ssl_contexts()

    for host, port, mode in smtp_endpoints():
        for ctx_name, ctx in contexts:
            try:
                if mode == "ssl":
                    with smtplib.SMTP_SSL(host, port, context=ctx, timeout=30) as smtp:
                        smtp.login(email_addr, password)
                        smtp.send_message(msg)
                        print(f"sent via {host}:{port} ({mode}, {ctx_name})")
                        print(f"message_id={msgid}")
                        return msgid

                with smtplib.SMTP(host, port, timeout=30) as smtp:
                    smtp.ehlo()
                    smtp.starttls(context=ctx)
                    smtp.ehlo()
                    smtp.login(email_addr, password)
                    smtp.send_message(msg)
                    print(f"sent via {host}:{port} ({mode}, {ctx_name})")
                    print(f"message_id={msgid}")
                    return msgid

            except smtplib.SMTPAuthenticationError as exc:
                raise SystemExit(f"SMTP authentication failed on {host}:{port}: {exc}") from exc
            except ssl.SSLCertVerificationError as exc:
                errors.append(f"{host}:{port}/{mode} [{ctx_name}] cert-verify-failed: {exc}")
            except ssl.SSLError as exc:
                errors.append(f"{host}:{port}/{mode} [{ctx_name}] ssl-error: {exc}")
            except Exception as exc:
                errors.append(f"{host}:{port}/{mode} [{ctx_name}] {exc}")

    hint = " Set ZOHO_CA_FILE to your CA bundle path (or ZOHO_SSL_INSECURE=1 for emergency testing only)."
    raise SystemExit("SMTP send failed: " + " | ".join(errors) + hint)


def fetch_header(conn: imaplib.IMAP4_SSL, seq_id: str) -> dict[str, str]:
    status, data = conn.fetch(seq_id, "(BODY.PEEK[HEADER])")
    if status != "OK" or not data or not isinstance(data[0], tuple):
        return {"id": seq_id, "from": "", "subject": "", "date": ""}
    raw = data[0][1]
    msg = email.message_from_bytes(raw)
    return {
        "id": seq_id,
        "from": decode_mime(msg.get("From", "")),
        "subject": decode_mime(msg.get("Subject", "")),
        "date": decode_mime(msg.get("Date", "")),
    }


def print_list(conn: imaplib.IMAP4_SSL, mailbox: str, limit: int) -> None:
    status, _ = conn.select(mailbox, readonly=True)
    if status != "OK":
        raise SystemExit(f"Cannot open mailbox: {mailbox}")
    status, data = conn.search(None, "ALL")
    if status != "OK" or not data:
        print("no messages")
        return
    ids = data[0].decode().split()
    ids = ids[-limit:]
    for seq in reversed(ids):
        row = fetch_header(conn, seq)
        print(f"{row['id']}\t{row['date']}\t{row['from']}\t{row['subject']}")


def print_read(conn: imaplib.IMAP4_SSL, mailbox: str, seq_id: str) -> None:
    status, _ = conn.select(mailbox, readonly=True)
    if status != "OK":
        raise SystemExit(f"Cannot open mailbox: {mailbox}")
    status, data = conn.fetch(seq_id, "(RFC822)")
    if status != "OK" or not data or not isinstance(data[0], tuple):
        raise SystemExit(f"Message not found: {seq_id}")
    msg = email.message_from_bytes(data[0][1])
    print(f"From: {decode_mime(msg.get('From', ''))}")
    print(f"To: {decode_mime(msg.get('To', ''))}")
    print(f"Date: {decode_mime(msg.get('Date', ''))}")
    print(f"Subject: {decode_mime(msg.get('Subject', ''))}")
    print()

    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            disp = str(part.get("Content-Disposition", "")).lower()
            if ctype == "text/plain" and "attachment" not in disp:
                payload = part.get_payload(decode=True) or b""
                charset = part.get_content_charset() or "utf-8"
                print(payload.decode(charset, errors="replace"))
                return
        print("[no text/plain body found]")
    else:
        payload = msg.get_payload(decode=True) or b""
        charset = msg.get_content_charset() or "utf-8"
        print(payload.decode(charset, errors="replace"))


def print_search(conn: imaplib.IMAP4_SSL, mailbox: str, query: str, limit: int) -> None:
    status, _ = conn.select(mailbox, readonly=True)
    if status != "OK":
        raise SystemExit(f"Cannot open mailbox: {mailbox}")
    status, data = conn.search(None, query)
    if status != "OK" or not data:
        print("no matches")
        return
    ids = data[0].decode().split()
    ids = ids[-limit:]
    for seq in reversed(ids):
        row = fetch_header(conn, seq)
        print(f"{row['id']}\t{row['date']}\t{row['from']}\t{row['subject']}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Zoho mail tool for OpenClaw")
    sub = parser.add_subparsers(dest="cmd", required=True)

    s_send = sub.add_parser("send", help="Send an email")
    s_send.add_argument("--to", required=True)
    s_send.add_argument("--subject", required=True)
    body_group = s_send.add_mutually_exclusive_group(required=True)
    body_group.add_argument("--body")
    body_group.add_argument("--body-file")
    html_group = s_send.add_mutually_exclusive_group(required=False)
    html_group.add_argument("--html-body", help="Optional HTML body content")
    html_group.add_argument("--html-body-file", help="Optional path to UTF-8 HTML body file")
    s_send.add_argument("--in-reply-to", help="Optional Message-ID to thread this as a reply")
    s_send.add_argument("--references", help="Optional References header value for threading")
    s_send.add_argument("--message-id", help="Optional explicit Message-ID for this outbound email")

    s_list = sub.add_parser("list", help="List recent emails")
    s_list.add_argument("--mailbox", default="INBOX")
    s_list.add_argument("--limit", type=int, default=20)

    s_read = sub.add_parser("read", help="Read one email by IMAP sequence id")
    s_read.add_argument("--mailbox", default="INBOX")
    s_read.add_argument("--id", required=True)

    s_search = sub.add_parser("search", help="Search emails via IMAP query")
    s_search.add_argument("--mailbox", default="INBOX")
    s_search.add_argument("--query", required=True, help='IMAP query, e.g. FROM "x@y.com"')
    s_search.add_argument("--limit", type=int, default=20)

    args = parser.parse_args()

    email_addr = getenv_required("ZOHO_EMAIL")
    password = getenv_required("ZOHO_PASSWORD")

    if args.cmd == "send":
        if args.body_file:
            body = read_utf8_file(args.body_file, "--body-file")
        else:
            body = args.body or ""

        html_body: str | None = None
        if args.html_body_file:
            html_body = read_utf8_file(args.html_body_file, "--html-body-file")
        elif args.html_body is not None:
            html_body = args.html_body

        smtp_send(
            email_addr,
            password,
            args.to,
            args.subject,
            body,
            html_body=html_body,
            in_reply_to=args.in_reply_to,
            references=args.references,
            message_id=args.message_id,
        )
        return

    conn, host = connect_imap(email_addr, password)
    try:
        if args.cmd == "list":
            print(f"imap_host={host}")
            print_list(conn, args.mailbox, args.limit)
        elif args.cmd == "read":
            print(f"imap_host={host}")
            print_read(conn, args.mailbox, args.id)
        elif args.cmd == "search":
            print(f"imap_host={host}")
            print_search(conn, args.mailbox, args.query, args.limit)
    finally:
        try:
            conn.logout()
        except Exception:
            pass


if __name__ == "__main__":
    main()
