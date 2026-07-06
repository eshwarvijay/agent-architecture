#!/usr/bin/env python3
"""Render clone-history.json as a cumulative-clones SVG line chart.

Usage: make-chart.py <history.json> <out.svg>
       make-chart.py --selftest
No deps — stdlib only. Committed SVG is embedded in the README.
"""
import json, sys

W, H = 720, 240
PAD_L, PAD_R, PAD_T, PAD_B = 48, 16, 28, 32
PLOT_W, PLOT_H = W - PAD_L - PAD_R, H - PAD_T - PAD_B
PURPLE = "#5436DA"


def build_svg(history: dict) -> str:
    days = sorted(history)
    # cumulative total over time — the "downloads going up" line.
    # lead with a 0 so the line visibly rises from the baseline.
    cum, running = [0], 0
    for d in days:
        running += history[d]
        cum.append(running)

    total = running or 1
    n = len(cum)

    def x(i):  # even spacing; single point sits mid-plot
        return PAD_L + (PLOT_W * i / (n - 1) if n > 1 else PLOT_W / 2)

    def y(v):
        return PAD_T + PLOT_H - (PLOT_H * v / total)

    pts = [(x(i), y(v)) for i, v in enumerate(cum)]
    line = " ".join(f"{px:.1f},{py:.1f}" for px, py in pts)
    area = f"{PAD_L},{PAD_T + PLOT_H} {line} {x(n - 1):.1f},{PAD_T + PLOT_H}"

    # y gridlines at 0, half, max
    grid = ""
    for v in (0, total // 2, total):
        gy = y(v)
        grid += (
            f'<line x1="{PAD_L}" y1="{gy:.1f}" x2="{W - PAD_R}" y2="{gy:.1f}" '
            f'stroke="#888" stroke-opacity="0.15"/>'
            f'<text x="{PAD_L - 8}" y="{gy + 4:.1f}" text-anchor="end" '
            f'font-size="11" fill="#888">{v}</text>'
        )

    dots = "".join(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="2.5" fill="{PURPLE}"/>' for px, py in pts)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="-apple-system,Segoe UI,sans-serif">
  <defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{PURPLE}" stop-opacity="0.35"/>
    <stop offset="1" stop-color="{PURPLE}" stop-opacity="0"/>
  </linearGradient></defs>
  <text x="{PAD_L}" y="18" font-size="13" font-weight="600" fill="{PURPLE}">plugin downloads over time — {total} total</text>
  {grid}
  <polygon points="{area}" fill="url(#g)"/>
  <polyline points="{line}" fill="none" stroke="{PURPLE}" stroke-width="2.5" stroke-linejoin="round"/>
  {dots}
  <text x="{PAD_L}" y="{H - 10}" font-size="11" fill="#888">{days[0]}</text>
  <text x="{W - PAD_R}" y="{H - 10}" text-anchor="end" font-size="11" fill="#888">{days[-1]}</text>
</svg>'''


def selftest():
    svg = build_svg({"2026-06-24": 95, "2026-06-25": 3, "2026-06-26": 7})
    assert "<polyline" in svg and "105 total" in svg, svg
    assert svg.count("<circle") == 4  # 3 days + leading zero baseline
    print("ok")


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        selftest()
    else:
        with open(sys.argv[1]) as f:
            history = json.load(f)
        with open(sys.argv[2], "w") as f:
            f.write(build_svg(history))
