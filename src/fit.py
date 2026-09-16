# -*- coding: utf-8 -*-
"""Measure every page in Chrome, then resize its pictures until no page is
clipped and none is half empty. Rewrites both HTML files at the end.

Two metrics, and only two:

* `slack` is the gap between the bottom of the footer and the bottom of the
  page box. `.body` is a flex item that cannot shrink below its content, so
  content that does not fit pushes the footer out of the page and `.page` clips
  it in silence. Negative slack is the only reliable sign of that.
* `fill` is the summed height of `.body`'s direct children over the height of
  `.body`. A page can have slack of zero and still be a third white.

Photographs move in height (they crop, so a taller box never leaves a white
band); drawings move in width (a fixed height on an SVG makes it scale down and
centre itself inside dead margins).
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(HERE)
from browser import CHROME, FLAGS  # noqa: E402

import build  # noqa: E402

TARGET = 0.96
MIN_SLACK = 0.0
PHOTO_MIN, PHOTO_MAX = 74.0, 460.0
FIGW_MIN, FIGW_MAX = 74.0, 100.0

MEASURE_JS = """
<script>
window.addEventListener('load', function () {
  var GRID = /(^| )(g2|g3|g55|g64|g46|g73|g37)( |$)/;
  // The hole this avoids: a picture that shares a two-column row with a block
  // of text is already as tall as its neighbour. Growing it to fill the page
  // makes the ROW taller, and the text column -- which cannot stretch -- ends
  // up beside a hand's width of nothing that the fitter itself just dug.
  // Such a picture is not counted as growable, and the page is left short
  // instead.
  function cellOf(el, pg) {
    var n = el;
    while (n && n !== pg) {
      var par = n.parentElement;
      if (!par) return null;
      if (GRID.test(' ' + par.className + ' ')) return {cell: n, row: par};
      n = par;
    }
    return null;
  }
  function contentHeight(el) {
    var kids = el.children.length ? el.children : [el];
    var top = 1e9, bot = -1e9;
    Array.prototype.forEach.call(kids, function (k) {
      var r = k.getBoundingClientRect();
      if (r.height < 1) return;
      top = Math.min(top, r.top); bot = Math.max(bot, r.bottom);
    });
    return bot < top ? 0 : bot - top;
  }
  var out = [];
  document.querySelectorAll('.page').forEach(function (pg, i) {
    var foot = pg.querySelector('.pf');
    var body = pg.querySelector('.body');
    if (!foot || !body) { out.push({i: i, hero: 1}); return; }
    var pr = pg.getBoundingClientRect(), fr = foot.getBoundingClientRect();
    var sum = 0;
    Array.prototype.forEach.call(body.children, function (c) {
      sum += c.getBoundingClientRect().height;
    });
    var growable = 0;
    Array.prototype.forEach.call(pg.querySelectorAll('.photo, .shot, .figw'), function (p) {
      var gc = cellOf(p, pg);
      if (!gc) { growable += 1; return; }          // full width: safe to grow
      var mine = gc.cell.getBoundingClientRect().height, other = 0;
      Array.prototype.forEach.call(gc.row.children, function (c) {
        if (c !== gc.cell) other = Math.max(other, contentHeight(c));
      });
      if (mine < other - 8) growable += 1;         // still filling toward its neighbour
    });
    out.push({
      i: i,
      slack: +(pr.bottom - fr.bottom).toFixed(2),
      fill: +(sum / body.clientHeight).toFixed(4),
      bh: +body.clientHeight.toFixed(2),
      sum: +sum.toFixed(2),
      growable: growable,
      ph: Array.prototype.map.call(pg.querySelectorAll('.photo, .shot'),
            function (e) { return +e.getBoundingClientRect().height.toFixed(2); }),
      fw: Array.prototype.map.call(pg.querySelectorAll('.figw'),
            function (e) { return +e.getBoundingClientRect().height.toFixed(2); })
    });
  });
  document.title = 'M' + JSON.stringify(out);
});
</script>
"""

PHOTO_RE = re.compile(r'(<div class="(?:photo|shot)" style="height:)(\d+(?:\.\d+)?)(pt")')
FIGW_RE = re.compile(r'(<div class="figw")( style="width:(\d+(?:\.\d+)?)%")?(>)')


def measure(pages):
    html = build.build("A4", pages).replace("</head>", MEASURE_JS + "</head>")
    tmp = os.path.join(ROOT, "out", "_measure.html")
    with open(tmp, "w", encoding="utf-8") as fh:
        fh.write(html)
    dom = subprocess.run(
        [CHROME, "--headless", "--disable-gpu", "--dump-dom",
         "--run-all-compositor-stages-before-draw", "--virtual-time-budget=25000",
         *FLAGS, "file:///" + tmp.replace("\\", "/").lstrip("/")],
        capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
    m = re.search(r"<title>M(\[.*?\])</title>", dom, re.S)
    if not m:
        raise SystemExit("could not read metrics back from Chrome")
    return json.loads(m.group(1))


def scale_page(src, k):
    def ph(m):
        v = max(PHOTO_MIN, min(PHOTO_MAX, float(m.group(2)) * k))
        return f"{m.group(1)}{v:.1f}{m.group(3)}"

    def fw(m):
        cur = float(m.group(3)) if m.group(3) else 100.0
        v = max(FIGW_MIN, min(FIGW_MAX, cur * k))
        return f'{m.group(1)} style="width:{v:.1f}%"{m.group(4)}'

    return FIGW_RE.sub(fw, PHOTO_RE.sub(ph, src))


def run(rounds=9):
    pages = build.render_pages()
    shrunk = set()

    def apply(i, k):
        pages[i] = (pages[i][0], scale_page(pages[i][1], k), pages[i][2], pages[i][3])

    for r in range(rounds):
        met = measure(pages)
        moved = 0
        for d in met:
            if d.get("hero") or d["slack"] >= MIN_SLACK - 0.5:
                continue
            i, scal = d["i"], sum(d["ph"]) + sum(d["fw"])
            if scal < 8:
                continue
            k = max(0.7, 1 - (-d["slack"] + 3) / scal)
            if abs(k - 1) < 0.004:
                continue
            before = pages[i][1]
            apply(i, k)
            shrunk.add(i)
            if pages[i][1] == before:
                continue
            moved += 1
        print("shrink round %d: %d pages" % (r + 1, moved))
        if not moved:
            break

    for r in range(rounds):
        met = measure(pages)
        moved = 0
        for d in met:
            if d.get("hero") or d["i"] in shrunk or d["fill"] >= TARGET:
                continue
            # a page whose only scalable pictures sit beside a column of text
            # that is already shorter than they are: growing them digs a hole
            if not d.get("growable"):
                continue
            i, scal = d["i"], sum(d["ph"]) + sum(d["fw"])
            if scal < 8:
                continue
            k = min(1.35, 1 + (TARGET * d["bh"] - d["sum"]) / scal)
            if abs(k - 1) < 0.004:
                continue
            base = pages[i]
            grown = False
            for stp in (k, 1 + (k - 1) / 2.0):
                if abs(stp - 1) < 0.004:
                    break
                pages[i] = base
                apply(i, stp)
                if pages[i][1] == base[1]:
                    break
                if measure(pages)[i]["slack"] >= MIN_SLACK - 0.5:
                    grown = True
                    break
            if not grown:
                pages[i] = base
                shrunk.add(i)
                continue
            moved += 1
        print("grow round %d: %d pages" % (r + 1, moved))
        if not moved:
            break

    met = measure(pages)
    clipped = [d["i"] + 1 for d in met if not d.get("hero") and d["slack"] < -0.5]
    short = [(d["i"] + 1, d["fill"], sum(d["ph"]) + sum(d["fw"]))
             for d in met if not d.get("hero") and d["fill"] < TARGET - 0.015]
    print("")
    print("clipped: %s" % (clipped or "none"))
    print("short:   %s" % (", ".join("%02d %.0f%%%s" % (i, f * 100, "" if sc >= 8 else " (no picture)")
                                     for i, f, sc in short) or "none"))
    if clipped:
        # by how much, and how much scalable picture is left on the page: a page
        # with nothing left to shrink needs a block of copy removed, not another
        # round of the fitter
        detail = ", ".join(
            "p%02d over by %.0f pt (%.0f pt of picture)"
            % (d["i"] + 1, -d["slack"], sum(d["ph"]) + sum(d["fw"]))
            for d in met if not d.get("hero") and d["slack"] < -0.5)
        raise SystemExit("REFUSING TO WRITE: %d page(s) still clipped -- %s"
                         % (len(clipped), detail))

    for paper in build.PAPERS:
        html = build.build(paper, pages)
        if html.count("<div") != html.count("</div>"):
            raise SystemExit("unbalanced divs in " + paper)
        path = build.html_path(paper)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(html)
        print("wrote %s (%.0f KB)" % (os.path.basename(path), len(html) / 1024))


if __name__ == "__main__":
    run()
