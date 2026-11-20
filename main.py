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

# The entry image this program publishes, pinned by size and SHA-256 so a
# swapped or truncated entry.png is refused instead of published.
EXPECTED_SIZE = 148733
EXPECTED_SHA256 = "e7ba2b932ad67032c83b0f8247020a5b85036ea59d50856117543bfb9fee062c"


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

    # The entry must be a PNG: refuse anything whose first bytes are not
    # the PNG signature, instead of copying and hashing unknown data.
    with open(source, "rb") as handle:
        signature = handle.read(8)
    if signature != b"\x89PNG\r\n\x1a\n":
        fail("entry.png is not a valid PNG: bad signature")

    # The entry must be the exact image pinned above: refuse any other
    # size or digest rather than publishing the wrong front page.
    source_size = os.path.getsize(source)
    if source_size != EXPECTED_SIZE:
        fail(
            "entry.png size mismatch: got %d bytes, expected %d bytes"
            % (source_size, EXPECTED_SIZE)
        )
    source_digest = digest(source)
    if source_digest != EXPECTED_SHA256:
        fail("entry.png sha256 mismatch: got %s, expected %s" % (source_digest, EXPECTED_SHA256))

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
