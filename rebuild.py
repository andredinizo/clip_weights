"""Reassemble ViT-B-32.pt from its split parts and verify integrity.

Usage (run from inside the model_parts/ directory, or pass --parts-dir):

    python rebuild.py                 # writes ../ViT-B-32.pt
    python rebuild.py -o /some/path/ViT-B-32.pt

Cross-platform (Windows / Linux / macOS), stdlib only. It concatenates
ViT-B-32.pt.part00 .. part19 in numeric order and checks the result's SHA-256
against the known-good hash of the official OpenAI CLIP ViT-B/32 checkpoint.
"""

from __future__ import annotations

import argparse
import glob
import hashlib
import os
import sys

EXPECTED_SHA256 = "40d365715913c9da98579312b702a82c18be219cc2a73407c4526f58eba950af"
PART_GLOB = "ViT-B-32.pt.part*"


def main() -> int:
    ap = argparse.ArgumentParser(description="Rebuild ViT-B-32.pt from split parts.")
    ap.add_argument("--parts-dir", default=os.path.dirname(os.path.abspath(__file__)),
                    help="Directory containing the .partNN files (default: this script's dir).")
    ap.add_argument("-o", "--output", default=None,
                    help="Output path (default: <parts-dir>/../ViT-B-32.pt).")
    args = ap.parse_args()

    parts = sorted(glob.glob(os.path.join(args.parts_dir, PART_GLOB)))
    if not parts:
        print(f"ERROR: no parts matching {PART_GLOB} in {args.parts_dir}", file=sys.stderr)
        return 1

    output = args.output or os.path.join(args.parts_dir, os.pardir, "ViT-B-32.pt")
    output = os.path.abspath(output)

    print(f"Found {len(parts)} parts. Reassembling into:\n  {output}")
    hasher = hashlib.sha256()
    with open(output, "wb") as out:
        for p in parts:
            with open(p, "rb") as fh:
                while True:
                    chunk = fh.read(1024 * 1024)
                    if not chunk:
                        break
                    out.write(chunk)
                    hasher.update(chunk)
            print(f"  + {os.path.basename(p)}")

    digest = hasher.hexdigest()
    print(f"\nSHA-256 of rebuilt file: {digest}")
    if digest == EXPECTED_SHA256:
        print("OK: hash matches the official OpenAI CLIP ViT-B/32 checkpoint.")
        return 0
    print(f"MISMATCH: expected {EXPECTED_SHA256}", file=sys.stderr)
    print("The rebuilt file is corrupt or parts are missing/out of order. Do NOT use it.",
          file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
