#!/usr/bin/env python3
"""Publish the news-image-20261119 entry image.

The entry is a newspaper front page summing up Thursday
19 November 2026 in 35 stories, stored as entry.png next to
this script. This program copies that image into the make.fun
output directory and checks the copy is byte-for-byte identical
(size and SHA-256) before declaring success.
"""

import hashlib
import os
import shutil
import sys

BLOCK = 1024 * 1024


def digest(path):
    """SHA-256 of a file, read in blocks so large files stay cheap."""
    hasher = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            block = handle.read(BLOCK)
            if not block:
                break
            hasher.update(block)
    return hasher.hexdigest()


def fail(message):
    print("error: " + message, file=sys.stderr)
    sys.exit(1)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")

    shutil.copyfile(source, target)

    expected_size = os.path.getsize(source)
    copied_size = os.path.getsize(target)
    if copied_size != expected_size:
        fail(
            "size mismatch for %s: got %d bytes, expected %d bytes"
            % (target, copied_size, expected_size)
        )

    if digest(target) != digest(source):
        fail("sha256 mismatch for %s: copy differs from %s" % (target, source))

    print("wrote %s (%d bytes)" % (target, copied_size))


if __name__ == "__main__":
    main()
