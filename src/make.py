# -*- coding: utf-8 -*-
"""Build The Combined Routes end to end, and refuse to lie about the result.

    python src/make.py            full build, then every check
    python src/make.py --checks   checks only, against whatever is in out/

The order is not arbitrary. The fitter measures real pages in Chrome, so the
photographs have to be on disk before it runs; and page 15 shows a picture of
the rendered route 05, so the book is built, rendered, snapped, and then built
and rendered again with that snapshot in place.
"""
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PHOTOS = os.path.join(ROOT, "assets", "photos")

# (label, argv, needs_photos)
STEPS = [
    ("fonts      subset Spectral into fonts.css", ["prep_fonts.py"], False),
    ("photos     fetch the Higgsfield renders", ["fetch_photos.py"], False),
    ("build      assemble both HTML files", ["build.py"], True),
    ("fit        measure and resize until nothing clips", ["fit.py"], True),
    ("render     Chrome -> PDF (A4, for the snapshot)", ["render.py", "A4"], True),
    ("snap       photograph route 05 out of that PDF", ["snap.py"], True),
    ("build      reassemble, now with the snapshot", ["build.py"], True),
    ("fit        refit", ["fit.py"], True),
    ("render     Chrome -> PDF (both sizes)", ["render.py"], True),
    ("finalize   exact page boxes and metadata", ["finalize.py"], True),
]

CHECKS = [
    ("routes_text  30 routes agree with the builder", ["routes_text.py"]),
    ("arcs         360 sessions, columns valid", ["arcs.py"]),
    ("check_figs   every number re-derived a second way", ["check_figs.py"]),
    ("check_glyphs nothing falls outside Spectral", ["check_glyphs.py"]),
    ("check_pdf    fonts, margins, page references", ["check_pdf.py"]),
    ("check_balance no half-empty columns", ["check_balance.py"]),
    ("check_color  saturated colour budget", ["check_color.py"]),
    ("inventory    every asset used, none repeated", ["inventory.py"]),
]


def run(argv):
    t0 = time.time()
    p = subprocess.run([sys.executable] + argv, cwd=HERE)
    return p.returncode, time.time() - t0


def have_photos():
    if not os.path.isdir(PHOTOS):
        return 0
    return len([f for f in os.listdir(PHOTOS) if f.endswith(".jpg")])


def phase(title, items):
    print("\n" + "=" * 68)
    print(title)
    print("=" * 68)
    failed = []
    for label, argv in items:
        script = os.path.join(HERE, argv[0])
        if not os.path.exists(script):
            print("\n-- %s\n   SKIPPED: %s is not in the repo" % (label, argv[0]))
            failed.append((label, "missing"))
            continue
        print("\n-- %s" % label)
        code, secs = run(argv)
        if code:
            print("   FAILED (exit %d, %.1fs)" % (code, secs))
            failed.append((label, "exit %d" % code))
        else:
            print("   ok (%.1fs)" % secs)
    return failed


def main():
    checks_only = "--checks" in sys.argv
    if not checks_only:
        n = have_photos()
        steps = []
        for label, argv, needs in STEPS:
            steps.append((label, argv))
        failed = phase("BUILD", steps)
        if failed:
            print("\nBUILD INCOMPLETE:")
            for label, why in failed:
                print("   %-52s %s" % (label.split()[0], why))
            got = have_photos()
            if got < 57:
                print("\n   Only %d of 58 photographs are on disk." % got)
                print("   fetch_photos.py needs https://d8j0ntlcm91z4.cloudfront.net;")
                print("   if the egress policy blocks it, no PDF can be produced here.")
            return 1

    failed = phase("CHECKS", CHECKS)
    print("\n" + "=" * 68)
    if failed:
        print("%d CHECK(S) FAILED -- do not ship this build:" % len(failed))
        for label, why in failed:
            print("   %-52s %s" % (label.split()[0], why))
        return 1
    print("all checks green")
    for name in sorted(os.listdir(os.path.join(ROOT, "out"))):
        if name.endswith(".pdf"):
            p = os.path.join(ROOT, "out", name)
            print("   %-44s %6.2f MB" % (name, os.path.getsize(p) / 1048576))
    return 0


if __name__ == "__main__":
    sys.exit(main())
