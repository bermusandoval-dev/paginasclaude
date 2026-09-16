# -*- coding: utf-8 -*-
"""Find the columns that are half empty.

fit.py measures fill as the height of .body's children over .body. That is
blind to the commonest way a finished page still looks empty: a two-column row
whose height is set by one column while the other stops half way down. Measured
on the FITTED file, because the fitter changes every picture's height.
"""
import io
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

FLOOR = 0.80
MIN_MM = 18.0

JS = """
<script>
window.addEventListener('load', function () {
  var out = [];
  var sel = '.g2,.g3,.g55,.g64,.g46,.g73,.g37';
  document.querySelectorAll('.page').forEach(function (pg, i) {
    var body = pg.querySelector('.body');
    if (!body) return;
    body.querySelectorAll(sel).forEach(function (row) {
      var rr = row.getBoundingClientRect();
      if (rr.height < 40) return;
      if (getComputedStyle(row).alignItems === 'center') return;
      // A grid with more cells than columns wraps onto several rows, and its
      // bounding box is then the height of ALL of them. Comparing a cell to
      // that reports every cell of a healthy 2x2 as half empty, which is how
      // the four position drawings on page 33 came back at 44%. Cells are
      // grouped by the line they actually sit on, and measured against their
      // own line.
      var lines = {};
      Array.prototype.forEach.call(row.children, function (cell, c) {
        var cr = cell.getBoundingClientRect();
        var key = Math.round(cr.top / 4);
        (lines[key] = lines[key] || []).push({cell: cell, c: c, r: cr});
      });
      Object.keys(lines).forEach(function (key) {
        var group = lines[key];
        if (group.length < 2) return;          // a full-width cell has no partner
        var lineTop = 1e9, lineBot = -1e9;
        group.forEach(function (g) {
          lineTop = Math.min(lineTop, g.r.top);
          lineBot = Math.max(lineBot, g.r.bottom);
        });
        var lineH = lineBot - lineTop;
        if (lineH < 40) return;
        group.forEach(function (g) {
          var kids = g.cell.children.length ? g.cell.children : [g.cell];
          var top = 1e9, bot = -1e9;
          Array.prototype.forEach.call(kids, function (k) {
            var r = k.getBoundingClientRect();
            if (r.height < 1) return;
            top = Math.min(top, r.top); bot = Math.max(bot, r.bottom);
          });
          if (bot < top) return;
          out.push({p: i + 1, col: g.c, cells: group.length,
                    row: +lineH.toFixed(1), used: +(bot - top).toFixed(1),
                    cls: (g.cell.className || g.cell.tagName).toString().slice(0, 26)});
        });
      });
    });
  });
  document.title = 'B' + JSON.stringify(out);
});
</script>
"""


def main():
    fitted = os.path.join(ROOT, "out", "routes-A4.html")
    if os.path.exists(fitted):
        html = io.open(fitted, encoding="utf-8").read()
        print("(measuring the fitted file)")
    else:
        html = build.build("A4")
        print("(no fitted file yet -- measuring the source)")
    html = html.replace("</head>", JS + "</head>")
    tmp = os.path.join(ROOT, "out", "_balance.html")
    with open(tmp, "w", encoding="utf-8") as fh:
        fh.write(html)
    dom = subprocess.run(
        [CHROME, "--headless", "--disable-gpu", "--dump-dom",
         "--run-all-compositor-stages-before-draw", "--virtual-time-budget=25000",
         *FLAGS, "file:///" + tmp.replace("\\", "/").lstrip("/")],
        capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
    m = re.search(r"<title>B(\[.*?\])</title>", dom, re.S)
    if not m:
        raise SystemExit("could not read the balance back from Chrome")
    rows = json.loads(m.group(1))
    print("=" * 74)
    print("half-empty columns (cell under %.0f%% of its row, hole over %.0f mm)"
          % (FLOOR * 100, MIN_MM))
    bad = 0
    for d in rows:
        frac = d["used"] / d["row"]
        gap = (d["row"] - d["used"]) / 3.7795
        if frac < FLOOR and gap >= MIN_MM:
            bad += 1
            print("   p%02d  column %d of %d  %-26s fills %3.0f%%  %5.1f mm of nothing"
                  % (d["p"], d["col"] + 1, d["cells"], d["cls"], frac * 100, gap))
    if not bad:
        print("   none")
    print("\n%d hole(s)" % bad)
    return bad


if __name__ == "__main__":
    main()
