# -*- coding: utf-8 -*-
"""Subset Spectral and embed it in one CSS file as base64 woff2.

Spectral ships as static TrueType faces (not variable), so Chrome's
--print-to-pdf embeds it as real Type0 fonts. One family sets everything:
the book in Regular and Italic, headlines in Light and Medium, and the small
working type (labels, table heads) in SemiBold with letter-spacing.
"""
import base64
import io
import os

from fontTools import subset
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TTF = os.path.join(ROOT, "fonts", "ttf")

UNICODES = "U+0000-00FF,U+0100-017F,U+2000-206F,U+20AC,U+2122,U+2212,U+00D7"

FACES = [
    (300, "normal", "Spectral-Light.ttf"),
    (300, "italic", "Spectral-LightItalic.ttf"),
    (400, "normal", "Spectral-Regular.ttf"),
    (400, "italic", "Spectral-Italic.ttf"),
    (500, "normal", "Spectral-Medium.ttf"),
    (500, "italic", "Spectral-MediumItalic.ttf"),
    (600, "normal", "Spectral-SemiBold.ttf"),
    (600, "italic", "Spectral-SemiBoldItalic.ttf"),
    (700, "normal", "Spectral-Bold.ttf"),
]


def woff2(path):
    font = TTFont(path)
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = ["*"]
    opts.notdef_outline = True
    opts.name_IDs = ["*"]
    opts.drop_tables = ["DSIG"]
    sub = subset.Subsetter(options=opts)
    sub.populate(unicodes=subset.parse_unicodes(UNICODES))
    sub.subset(font)
    buf = io.BytesIO()
    font.flavor = "woff2"
    font.save(buf)
    return buf.getvalue()


def main():
    blocks = []
    for weight, style, fname in FACES:
        data = woff2(os.path.join(TTF, fname))
        b64 = base64.b64encode(data).decode("ascii")
        blocks.append(
            "@font-face{font-family:'Spectral';font-style:%s;font-weight:%d;"
            "font-display:block;src:url(data:font/woff2;base64,%s) format('woff2');}"
            % (style, weight, b64))
        print("  Spectral %3d %-6s %6.1f KB" % (weight, style, len(data) / 1024))
    out = os.path.join(ROOT, "fonts", "fonts.css")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(blocks) + "\n")
    print("fonts.css %.1f KB" % (os.path.getsize(out) / 1024))


if __name__ == "__main__":
    main()
