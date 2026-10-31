#!/usr/bin/env python3
"""Decode a Gmail attachment, or the HTML body of a message, to a file.

Usage: decode_attachment.py <input.json> <output file>
<input.json> is either `gws gmail users messages attachments get` output (top-level
`data`) or `gws gmail users messages get ... format=full` output (the text/html part
of the payload is written). It may start with gws's "Using keyring backend" banner.
"""
import base64
import json
import sys


def html_part(part):
    """Depth-first search of a Gmail payload for the first text/html body."""
    if part.get("mimeType") == "text/html" and (part.get("body") or {}).get("data"):
        return part["body"]["data"]
    for child in part.get("parts") or []:
        found = html_part(child)
        if found:
            return found
    return None


def main():
    if len(sys.argv) != 3:
        print("usage: decode_attachment.py <attachment.json> <output file>")
        sys.exit(2)
    raw = open(sys.argv[1], encoding="utf-8").read()
    start = raw.find("{")
    if start < 0:
        print("error: no JSON object in input")
        sys.exit(1)
    obj = json.loads(raw[start:])
    data = obj.get("data") or html_part(obj.get("payload") or {})
    if not data:
        print("error: no attachment 'data' and no text/html part in the message (plain-text-only email: save it as PDF from the mail app instead)")
        sys.exit(1)
    blob = base64.urlsafe_b64decode(data + "=" * (-len(data) % 4))
    with open(sys.argv[2], "wb") as f:
        f.write(blob)
    print(f"wrote {sys.argv[2]} ({len(blob)} bytes)")


if __name__ == "__main__":
    main()
