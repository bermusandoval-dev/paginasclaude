# -*- coding: utf-8 -*-
"""Which characters used in the book are actually in the two typefaces?

A character a font does not carry raises nothing: Chrome swaps in Segoe UI or
Cambria for that glyph alone, and the PDF quietly grows two extra fonts.
"""
import html
import os
import re
import sys

from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
WIN = r"C:\Windows\Fonts"

import build  # noqa: E402


def cmap(path):
    return set(TTFont(path).getBestCmap().keys())


def main():
    ttf = os.path.join(os.path.dirname(HERE), "fonts", "ttf")
    gara = cmap(os.path.join(ttf, "Spectral-Regular.ttf"))
    georgia = cmap(os.path.join(ttf, "Spectral-SemiBold.ttf"))

    text = "".join(p[1] for p in build.render_pages())
    text = html.unescape(re.sub(r"<[^>]+>", " ", text))

    used = {}
    for ch in text:
        if ord(ch) < 0x20 or ch == " ":
            continue
        used[ord(ch)] = used.get(ord(ch), 0) + 1

    missing = []
    print("%-8s %-4s %-9s %-9s %s" % ("cp", "chr", "garamond", "georgia", "n"))
    for cp in sorted(used):
        a, b = cp in gara, cp in georgia
        if a and b:
            continue
        print("U+%04X   %-4s %-9s %-9s %d"
              % (cp, chr(cp).encode("ascii", "backslashreplace").decode(),
                 "yes" if a else "NO", "yes" if b else "NO", used[cp]))
        if not a or not b:
            missing.append(cp)
    print("\n%d codepoints used, %d missing from one of the two faces" % (len(used), len(missing)))
    if missing:
        raise SystemExit("missing: " + ", ".join("U+%04X" % c for c in missing))


if __name__ == "__main__":
    main()
