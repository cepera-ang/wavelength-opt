import csv
import itertools
import json
import math
import random
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import linprog


ROOT = Path(__file__).resolve().parent
D65_XY = (0.3127, 0.3290)
WL_MIN = 380
WL_MAX = 700
POWER_CACHE = {}


def cross2(a, b):
    return float(a[0] * b[1] - a[1] * b[0])


def read_xyz():
    rows = []
    with open(ROOT / "CIE_xyz_1931_2deg.csv", newline="") as f:
        for wl, x, y, z in csv.reader(f):
            wl = int(wl)
            if WL_MIN <= wl <= WL_MAX:
                rows.append((wl, float(x), float(y), float(z)))
    a = np.array(rows, dtype=float)
    xyz = a[:, 1:4]
    xy = xyz[:, :2] / xyz.sum(axis=1, keepdims=True)
    return a[:, 0].astype(int), xyz, xy


def polygon_area(points):
    p = np.asarray(points)
    return abs(0.5 * np.sum(p[:, 0] * np.roll(p[:, 1], -1) - p[:, 1] * np.roll(p[:, 0], -1)))


def hull_area_for_indices(xy, idx):
    idx = sorted(idx)
    return polygon_area(xy[idx])


def white_power(xyz, idx):
    key = tuple(sorted(idx))
    if key in POWER_CACHE:
        return POWER_CACHE[key]
    xw, yw = D65_XY
    target = np.array([xw / yw, 1.0, (1.0 - xw - yw) / yw])
    a_eq = xyz[list(key)].T
    res = linprog(
        c=np.ones(len(key)),
        A_eq=a_eq,
        b_eq=target,
        bounds=[(0, None)] * len(key),
        method="highs",
    )
    POWER_CACHE[key] = float(res.fun) if res.success else math.inf
    return POWER_CACHE[key]


def norm_power(power):
    return power


def max_area_dp(xy, n):
    m = len(xy)
    start = 0
    end = m - 1
    dp = [[(-math.inf, None) for _ in range(n)] for _ in range(m)]
    dp[start][0] = (0.0, None)
    for used in range(1, n):
        for j in range(start + used, end + 1):
            best_val = -math.inf
            best_prev = None
            for i in range(start + used - 1, j):
                prev = dp[i][used - 1][0]
                if not math.isfinite(prev):
                    continue
                val = prev - cross2(xy[i] - xy[start], xy[j] - xy[start])
                if val > best_val:
                    best_val = val
                    best_prev = i
            dp[j][used] = (best_val, best_prev)
    path = []
    cur = end
    used = n - 1
    while cur is not None:
        path.append(cur)
        cur = dp[cur][used][1]
        used -= 1
    return tuple(reversed(path))


def random_set(m, n):
    s = {0, m - 1}
    while len(s) < n:
        s.add(random.randrange(m))
    return tuple(sorted(s))


def mutate(idx, m):
    out = list(idx)
    pos = random.randrange(len(out))
    if random.random() < 0.7:
        out[pos] = min(m - 1, max(0, out[pos] + random.randint(-12, 12)))
    else:
        out[pos] = random.randrange(m)
    return tuple(sorted(set(out)))


def score(xy, xyz, idx, locus_area, area_weight):
    if len(idx) < 3:
        return -1e9, 0.0, math.inf
    area = hull_area_for_indices(xy, idx) / locus_area
    p = white_power(xyz, list(idx))
    if not math.isfinite(p):
        return -1e9, area, p
    return area_weight * area - (1.0 - area_weight) * math.log(norm_power(p)), area, p


def evolve(xy, xyz, n, locus_area, area_weight, rounds=1600, pop_size=42):
    m = len(xy)
    pop = [random_set(m, n) for _ in range(pop_size)]
    for _ in range(rounds):
        ranked = sorted((score(xy, xyz, p, locus_area, area_weight), p) for p in pop)
        pop = [p for _, p in ranked[-pop_size // 3 :]]
        while len(pop) < pop_size:
            parent = random.choice(pop)
            child = mutate(parent, m)
            while len(child) < n:
                child = tuple(sorted(set(child + (random.randrange(m),))))
            pop.append(child)
    return max(pop, key=lambda p: score(xy, xyz, p, locus_area, area_weight)[0])


def d65_target():
    xw, yw = D65_XY
    return np.array([xw / yw, 1.0, (1.0 - xw - yw) / yw])


def scan_base_triples(wl, xyz, xy, locus_area):
    target = d65_target()
    grid = list(range(0, len(wl), 2))
    if grid[-1] != len(wl) - 1:
        grid.append(len(wl) - 1)
    triples = []
    for tri in itertools.combinations(grid, 3):
        mat = xyz[list(tri)].T
        try:
            coeff = np.linalg.solve(mat, target)
        except np.linalg.LinAlgError:
            continue
        if np.min(coeff) < -1e-9:
            continue
        p = float(np.sum(np.maximum(coeff, 0)))
        area = hull_area_for_indices(xy, tri) / locus_area
        triples.append((tri, area, p))
    return triples


def best_base_for_weight(triples, area_weight):
    return max(
        triples,
        key=lambda t: area_weight * t[1] - (1.0 - area_weight) * math.log(norm_power(t[2])),
    )[0]


def greedy_extend(xy, xyz, base, n, locus_area, area_weight):
    idx = set(base)
    while len(idx) < n:
        best = None
        for cand in range(len(xy)):
            if cand in idx:
                continue
            trial = tuple(sorted(idx | {cand}))
            val, area, p = score(xy, xyz, trial, locus_area, area_weight)
            if best is None or val > best[0]:
                best = (val, cand)
        idx.add(best[1])
    return tuple(sorted(idx))


def write_html(wl, xy, results, best):
    data = {
        "wavelengths": wl.tolist(),
        "xy": xy.round(8).tolist(),
        "results": [
            {
                "kind": kind,
                "n": n,
                "wavelengths": waves.tolist(),
                "coverage": area,
                "power": norm_power(p) if math.isfinite(p) else None,
            }
            for kind, n, waves, area, p in results
        ],
        "summary": [
            {
                "n": n,
                "kind": row[0],
                "wavelengths": row[2].tolist(),
                "coverage": row[3],
                "power": norm_power(row[4]),
            }
            for n, row in sorted(best.items())
        ],
        "d65": D65_XY,
    }
    html = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Wavelength Primary Optimizer</title>
<style>
:root { color-scheme: light; font-family: Inter, Segoe UI, Arial, sans-serif; background:#f5f6f8; color:#18202a; }
body { margin:0; }
main { max-width:1280px; margin:0 auto; padding:24px; }
h1 { font-size:28px; margin:0 0 8px; }
p { margin:0; color:#54616f; }
.top { display:flex; justify-content:space-between; gap:18px; align-items:end; margin-bottom:18px; }
.grid { display:grid; grid-template-columns:minmax(520px, 1.3fr) minmax(320px, .7fr); gap:16px; }
.panel { background:white; border:1px solid #dfe4ea; border-radius:8px; padding:14px; box-shadow:0 1px 2px rgba(0,0,0,.04); }
.chart-wrap { position:relative; width:100%; aspect-ratio:1.08; min-height:520px; }
canvas { width:100%; height:100%; display:block; }
.controls { display:grid; gap:14px; }
label { display:grid; gap:7px; font-weight:650; font-size:13px; }
input[type=range] { width:100%; }
.readout { display:grid; grid-template-columns:repeat(2, 1fr); gap:10px; margin-top:12px; }
.metric { background:#f7f9fb; border:1px solid #e3e8ee; border-radius:8px; padding:10px; }
.metric b { display:block; font-size:22px; }
.metric span { color:#66717e; font-size:12px; }
table { width:100%; border-collapse:collapse; font-size:13px; }
th, td { text-align:left; padding:7px 8px; border-bottom:1px solid #e8edf2; vertical-align:top; }
th { color:#46515d; font-size:12px; background:#f7f9fb; position:sticky; top:0; }
.tables { display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-top:16px; }
.tablebox { max-height:360px; overflow:auto; }
.small { color:#6b7683; font-size:12px; }
.pill { display:inline-block; padding:2px 7px; border-radius:999px; background:#eef3f8; border:1px solid #d8e1ea; }
@media (max-width:900px) {
  main { padding:14px; }
  .grid, .tables { grid-template-columns:1fr; }
  .top { display:block; }
  .chart-wrap { min-height:360px; }
}
</style>
</head>
<body>
<main>
  <div class="top">
    <div>
      <h1>Wavelength Primary Optimizer</h1>
      <p>1 nm monochrome primaries, CIE 1931 2 deg, D65 white power test.</p>
    </div>
    <div class="small">Power is radiant watts for D65 per lumen, normalized to perfect 555 nm light.</div>
  </div>
  <section class="grid">
    <div class="panel">
      <div class="chart-wrap"><canvas id="cie"></canvas></div>
    </div>
    <div class="panel controls">
      <label>Primary count <input id="n" type="range" min="3" max="12" step="1" value="6"><span id="nText"></span></label>
      <label>Gamut vs power <input id="bias" type="range" min="42" max="100" step="1" value="84"><span id="biasText"></span></label>
      <label>Coverage floor <input id="floor" type="range" min="0" max="100" step="1" value="0"><span id="floorText"></span></label>
      <div class="readout">
        <div class="metric"><b id="coverage"></b><span>locus area covered</span></div>
        <div class="metric"><b id="power"></b><span>D65 power vs 555 nm</span></div>
      </div>
      <div>
        <div class="small">Chosen wavelengths</div>
        <div id="waves" style="margin-top:8px; line-height:1.9"></div>
      </div>
      <div class="chart-wrap" style="min-height:240px; aspect-ratio:1.35"><canvas id="env"></canvas></div>
    </div>
  </section>
  <section class="tables">
    <div class="panel tablebox">
      <h2 style="font-size:17px; margin:0 0 8px">Best by primary count</h2>
      <table id="summary"></table>
    </div>
    <div class="panel tablebox">
      <h2 style="font-size:17px; margin:0 0 8px">Choices for selected count</h2>
      <table id="choices"></table>
    </div>
  </section>
</main>
<script id="data" type="application/json">__DATA__</script>
<script>
const data = JSON.parse(document.getElementById("data").textContent);
const wl = data.wavelengths;
const xy = data.xy;
const locus = xy.map((p, i) => ({x:p[0], y:p[1], wl:wl[i]}));
const xMin = -0.02, xMax = 0.78, yMin = -0.04, yMax = 0.9;
const nEl = document.getElementById("n");
const biasEl = document.getElementById("bias");
const floorEl = document.getElementById("floor");

function kindWeight(kind) {
  if (kind === "max_area") return 100;
  return Math.round(parseFloat(kind.split("_")[1]) * 100);
}

function pick() {
  const n = +nEl.value;
  const b = +biasEl.value;
  const rows = data.results.filter(r => r.n === n && r.power);
  return rows.reduce((best, r) => {
    const d = Math.abs(kindWeight(r.kind) - b);
    const bd = Math.abs(kindWeight(best.kind) - b);
    if (d !== bd) return d < bd ? r : best;
    return r.coverage > best.coverage ? r : best;
  }, rows[0]);
}

function toPx(c, x, y) {
  return [(x - xMin) / (xMax - xMin) * c.width, c.height - (y - yMin) / (yMax - yMin) * c.height];
}

function pointInPoly(x, y, poly) {
  let inside = false;
  for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {
    const a = poly[i], b = poly[j];
    if (((a.y > y) !== (b.y > y)) && x < (b.x - a.x) * (y - a.y) / (b.y - a.y) + a.x) inside = !inside;
  }
  return inside;
}

function xyToRgb(x, y) {
  if (y <= 0) return [255,255,255];
  const Y = 1, X = x / y, Z = (1 - x - y) / y;
  let r =  3.2406 * X - 1.5372 * Y - 0.4986 * Z;
  let g = -0.9689 * X + 1.8758 * Y + 0.0415 * Z;
  let b =  0.0557 * X - 0.2040 * Y + 1.0570 * Z;
  const m = Math.max(r, g, b, 1e-9);
  r /= m; g /= m; b /= m;
  r = Math.max(0, Math.min(1, r));
  g = Math.max(0, Math.min(1, g));
  b = Math.max(0, Math.min(1, b));
  const enc = v => Math.round(255 * (v <= .0031308 ? 12.92 * v : 1.055 * Math.pow(v, 1/2.4) - .055));
  return [enc(r), enc(g), enc(b)];
}

function fitCanvas(c) {
  const r = c.getBoundingClientRect();
  const d = window.devicePixelRatio || 1;
  c.width = Math.max(1, Math.floor(r.width * d));
  c.height = Math.max(1, Math.floor(r.height * d));
}

function drawCie(row) {
  const c = document.getElementById("cie");
  fitCanvas(c);
  const ctx = c.getContext("2d");
  ctx.clearRect(0, 0, c.width, c.height);
  const step = Math.max(4, Math.floor(c.width / 160));
  for (let py = 0; py < c.height; py += step) {
    for (let px = 0; px < c.width; px += step) {
      const x = xMin + (px + step / 2) / c.width * (xMax - xMin);
      const y = yMax - (py + step / 2) / c.height * (yMax - yMin);
      if (pointInPoly(x, y, locus)) {
        const rgb = xyToRgb(x, y);
        ctx.fillStyle = `rgb(${rgb[0]},${rgb[1]},${rgb[2]})`;
        ctx.fillRect(px, py, step + 1, step + 1);
      }
    }
  }
  drawAxes(ctx, c);
  ctx.lineWidth = 2;
  ctx.strokeStyle = "#111";
  drawLine(ctx, c, locus);
  const chosen = row.wavelengths.map(w => locus[wl.indexOf(w)]);
  ctx.fillStyle = "rgba(220, 32, 44, .16)";
  ctx.strokeStyle = "#dc202c";
  ctx.lineWidth = 3;
  drawPoly(ctx, c, chosen, true);
  ctx.fillStyle = "#dc202c";
  ctx.font = `${12 * (window.devicePixelRatio || 1)}px Segoe UI`;
  chosen.forEach(p => {
    const [px, py] = toPx(c, p.x, p.y);
    ctx.beginPath(); ctx.arc(px, py, 5 * (window.devicePixelRatio || 1), 0, Math.PI * 2); ctx.fill();
    ctx.fillText(p.wl, px + 7, py - 6);
  });
  const [dx, dy] = toPx(c, data.d65[0], data.d65[1]);
  ctx.fillStyle = "#111";
  ctx.beginPath(); ctx.arc(dx, dy, 4 * (window.devicePixelRatio || 1), 0, Math.PI * 2); ctx.fill();
  ctx.fillText("D65", dx + 7, dy + 14);
}

function drawAxes(ctx, c) {
  const d = window.devicePixelRatio || 1;
  ctx.strokeStyle = "rgba(20,25,30,.22)";
  ctx.lineWidth = d;
  ctx.font = `${11 * d}px Segoe UI`;
  ctx.fillStyle = "#334";
  for (let x = 0; x <= .8; x += .1) {
    const [px] = toPx(c, x, 0);
    ctx.beginPath(); ctx.moveTo(px, 0); ctx.lineTo(px, c.height); ctx.stroke();
    ctx.fillText(x.toFixed(1), px + 2, c.height - 6);
  }
  for (let y = 0; y <= .9; y += .1) {
    const [, py] = toPx(c, 0, y);
    ctx.beginPath(); ctx.moveTo(0, py); ctx.lineTo(c.width, py); ctx.stroke();
    ctx.fillText(y.toFixed(1), 4, py - 2);
  }
}

function drawLine(ctx, c, points) {
  ctx.beginPath();
  points.forEach((p, i) => {
    const [x, y] = toPx(c, p.x, p.y);
    if (i) ctx.lineTo(x, y); else ctx.moveTo(x, y);
  });
  ctx.closePath();
  ctx.stroke();
}

function drawPoly(ctx, c, points, fill) {
  ctx.beginPath();
  points.forEach((p, i) => {
    const [x, y] = toPx(c, p.x, p.y);
    if (i) ctx.lineTo(x, y); else ctx.moveTo(x, y);
  });
  ctx.closePath();
  if (fill) ctx.fill();
  ctx.stroke();
}

function drawEnv(row) {
  const c = document.getElementById("env");
  fitCanvas(c);
  const ctx = c.getContext("2d");
  ctx.clearRect(0, 0, c.width, c.height);
  const rows = data.results.filter(r => r.power && r.coverage * 100 >= +floorEl.value);
  const minX = 1, maxX = Math.max(...rows.map(r => r.power)) * 1.08;
  const minY = 0, maxY = 102;
  const sx = x => Math.log(x / minX) / Math.log(maxX / minX) * (c.width - 56) + 42;
  const sy = y => c.height - 28 - (y - minY) / (maxY - minY) * (c.height - 44);
  ctx.strokeStyle = "#d7dee6"; ctx.lineWidth = 1;
  for (let y = 20; y <= 100; y += 20) { ctx.beginPath(); ctx.moveTo(36, sy(y)); ctx.lineTo(c.width - 14, sy(y)); ctx.stroke(); }
  rows.forEach(r => {
    ctx.fillStyle = r === row ? "#dc202c" : "rgba(24,32,42,.45)";
    ctx.beginPath(); ctx.arc(sx(r.power), sy(r.coverage * 100), r === row ? 6 : 3, 0, Math.PI * 2); ctx.fill();
  });
  ctx.fillStyle = "#46515d"; ctx.font = `${11 * (window.devicePixelRatio || 1)}px Segoe UI`;
  ctx.fillText("coverage %", 8, 14);
  ctx.fillText("power log scale", c.width - 104, c.height - 8);
}

function table(el, cols, rows) {
  el.innerHTML = `<thead><tr>${cols.map(c => `<th>${c}</th>`).join("")}</tr></thead><tbody>${rows.join("")}</tbody>`;
}

function render() {
  const row = pick();
  nEl.value = row.n;
  nText.textContent = `${row.n} primaries`;
  biasText.textContent = `${biasEl.value}% area bias`;
  floorText.textContent = `${floorEl.value}% min coverage on envelope`;
  coverage.textContent = `${(row.coverage * 100).toFixed(1)}%`;
  power.textContent = `${row.power.toFixed(2)}x`;
  waves.innerHTML = row.wavelengths.map(w => `<span class="pill">${w} nm</span>`).join(" ");
  drawCie(row);
  drawEnv(row);
  table(summary, ["N", "Pick", "nm", "Cover", "Power"], data.summary.map(r => `<tr><td>${r.n}</td><td>${r.kind}</td><td>${r.wavelengths.join(" ")}</td><td>${(r.coverage*100).toFixed(1)}%</td><td>${r.power.toFixed(2)}x</td></tr>`));
  const rows = data.results.filter(r => r.n === row.n && r.power).sort((a,b) => a.power - b.power);
  table(choices, ["Kind", "nm", "Cover", "Power"], rows.map(r => `<tr><td>${r.kind}</td><td>${r.wavelengths.join(" ")}</td><td>${(r.coverage*100).toFixed(1)}%</td><td>${r.power.toFixed(2)}x</td></tr>`));
}

[nEl, biasEl, floorEl].forEach(el => el.addEventListener("input", render));
window.addEventListener("resize", render);
render();
</script>
</body>
</html>
"""
    (ROOT / "index.html").write_text(html.replace("__DATA__", json.dumps(data)), encoding="utf-8")


def main():
    random.seed(7)
    wl, xyz, xy = read_xyz()
    locus_area = polygon_area(xy)
    results = []
    triples = scan_base_triples(wl, xyz, xy, locus_area)

    for n in range(3, 13):
        idx = max_area_dp(xy, n)
        area = hull_area_for_indices(xy, idx) / locus_area
        p = white_power(xyz, list(idx))
        results.append(("max_area", n, wl[list(idx)], area, p))

        for aw in (0.92, 0.84, 0.72, 0.58, 0.42):
            base = best_base_for_weight(triples, aw)
            idx = greedy_extend(xy, xyz, base, n, locus_area, aw)
            _, area, p = score(xy, xyz, idx, locus_area, aw)
            results.append((f"pareto_{aw:.2f}", n, wl[list(idx)], area, p))

    with open(ROOT / "results.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["kind", "n", "wavelengths_nm", "coverage", "d65_rel_power_vs_555"])
        for kind, n, waves, area, p in results:
            w.writerow([kind, n, " ".join(map(str, waves)), f"{area:.6f}", f"{norm_power(p):.3f}"])

    best = {}
    for kind, n, waves, area, p in results:
        if not math.isfinite(p):
            continue
        k = n
        old = best.get(k)
        if old is None or area / math.log(norm_power(p) + 1.0) > old[3] / math.log(norm_power(old[4]) + 1.0):
            best[k] = (kind, n, waves, area, p)

    with open(ROOT / "summary.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["n", "choice", "wavelengths_nm", "coverage_pct", "d65_rel_power_vs_555"])
        for n in sorted(best):
            kind, _, waves, area, p = best[n]
            w.writerow([n, kind, " ".join(map(str, waves)), f"{100*area:.2f}", f"{norm_power(p):.2f}"])

    fig, ax = plt.subplots(figsize=(8, 5))
    for kind in sorted(set(r[0] for r in results)):
        rows = [r for r in results if r[0] == kind and math.isfinite(r[4])]
        if not rows:
            continue
        ax.scatter([norm_power(r[4]) for r in rows], [100 * r[3] for r in rows], s=18, label=kind)
    ax.set_xscale("log")
    ax.set_xlabel("D65 radiant power, relative to ideal 555 nm lumen")
    ax.set_ylabel("CIE xy locus coverage, percent")
    ax.grid(True, alpha=0.25)
    ax.legend(fontsize=8, ncols=2)
    fig.tight_layout()
    fig.savefig(ROOT / "coverage_power_envelope.png", dpi=180)

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot(xy[:, 0], xy[:, 1], color="black", lw=1)
    kind, n, waves, area, p = best[6]
    idx = [int(np.where(wl == wv)[0][0]) for wv in waves]
    poly = np.vstack([xy[idx], xy[idx[0]]])
    ax.plot(poly[:, 0], poly[:, 1], color="red", lw=1.5)
    ax.scatter(xy[idx, 0], xy[idx, 1], color="red", s=22)
    for wv, point in zip(waves, xy[idx]):
        ax.text(point[0], point[1], str(wv), fontsize=8)
    ax.set_title("Chosen 6-primary tradeoff")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_aspect("equal", "box")
    fig.tight_layout()
    fig.savefig(ROOT / "six_primary_choice.png", dpi=180)

    write_html(wl, xy, results, best)

    print((ROOT / "summary.csv").read_text())


if __name__ == "__main__":
    main()
