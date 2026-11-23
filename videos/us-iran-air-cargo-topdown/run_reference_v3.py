"""Run the original, code-drawn reference-style Advertio film.

The complete, editable six-scene Python source is stored as a losslessly packed
source file in this folder. Run `npm run unpack` to obtain film-reference-v3.py.
Its SHA256 is checked before lint, rendering, or extraction.

This packing is a transport mechanism for the GitHub connector's text upload;
NO image/reference pixels are bundled into the film.
"""
from pathlib import Path
import ast
import base64
import bz2
import hashlib
import sys

HERE = Path(__file__).resolve().parent
SOURCE_PACK = HERE / "reference-v3-source.bz2.b64"
UNPACKED = HERE / "film-reference-v3.py"
EXPECTED_SHA256 = "d4f5aefac864d3ab8c03dca0fd3fd64580a1fb1d6cf634fe8e8ce097b4c699bd"

def source_bytes():
    data = bz2.decompress(base64.b64decode(SOURCE_PACK.read_text(encoding="ascii")))
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        raise RuntimeError("Reference v3 source integrity mismatch: " + digest)
    return data

def main():
    src = source_bytes()
    ast.parse(src.decode("utf-8"), filename=str(UNPACKED))
    if "--lint" in sys.argv:
        print("Validated source Python syntax and checksum.")
        return
    if "--extract" in sys.argv:
        UNPACKED.write_bytes(src)
        print("Extracted readable source: " + str(UNPACKED))
        return
    # Use the final path to preserve asset roots and unchanged CLI options.
    namespace = {"__file__": str(UNPACKED), "__name__": "__main__", "__package__": None}
    exec(compile(src, str(UNPACKED), "exec"), namespace)

if __name__ == "__main__":
    main()
