# -*- coding: utf-8 -*-
"""Chrome headless -> PDF. Chrome needs absolute Windows paths for both the
output file and the file:/// URL, or it answers "Access denied"."""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
from browser import CHROME, FLAGS  # noqa: E402

import build  # noqa: E402


def render(paper):
    src = build.html_path(paper)
    dst = build.pdf_path(paper)
    if os.path.exists(dst):
        os.remove(dst)
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                    "--run-all-compositor-stages-before-draw",
                    "--virtual-time-budget=30000", "--print-to-pdf=" + dst, *FLAGS,
                    "file:///" + src.replace("\\", "/").lstrip("/")], capture_output=True)
    if not os.path.exists(dst):
        raise SystemExit("chrome produced nothing for " + paper)
    import pymupdf
    doc = pymupdf.open(dst)
    print("%-7s %2d pages  %6.2f MB" % (paper, doc.page_count, os.path.getsize(dst) / 1048576))
    doc.close()


if __name__ == "__main__":
    for p in sys.argv[1:] or ["A4", "Letter"]:
        render(p)
