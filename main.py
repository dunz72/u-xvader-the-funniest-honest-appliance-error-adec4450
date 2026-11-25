"""Copy entry.txt to the make.fun output directory, byte-identical.

Stdlib only: the grader's pinned Python image has no third-party packages.
Reads entry.txt next to this file, validates it (exists, non-empty, exactly
one line, at most 200 characters), writes it byte-identical to
$MAKEFUN_OUTPUT_DIR/entry.txt (default ./output/entry.txt), and verifies
SHA-256 before and after the copy.
"""

import hashlib
import os
import sys

MAX_CHARS = 200


def sha256_hex(data):
    return hashlib.sha256(data).hexdigest()


def read_entry(path):
    if not os.path.isfile(path):
        raise SystemExit("entry.txt not found next to main.py: %s" % path)
    with open(path, "rb") as f:
        data = f.read()
    if not data.strip():
        raise SystemExit("entry.txt is empty")
    text = data.decode("utf-8")
    lines = text.strip().splitlines()
    if len(lines) != 1:
        raise SystemExit("entry.txt must contain exactly one line, got %d" % len(lines))
    if len(lines[0]) > MAX_CHARS:
        raise SystemExit(
            "entry line is %d characters, over the %d limit" % (len(lines[0]), MAX_CHARS)
        )
    if any(ord(ch) < 32 and ch not in "\t" for ch in lines[0]):
        raise SystemExit("entry line contains control characters")
    return data, lines[0]


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.txt")
    data, line = read_entry(src)
    before = sha256_hex(data)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.path.join(here, "output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.txt")
    with open(dst, "wb") as f:
        f.write(data)

    with open(dst, "rb") as f:
        written = f.read()
    after = sha256_hex(written)
    if after != before:
        raise SystemExit("SHA-256 mismatch after copy: %s != %s" % (after, before))

    print("entry: %s" % line)
    print("characters: %d / %d" % (len(line), MAX_CHARS))
    print("sha256: %s" % after)
    print("wrote: %s" % dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
