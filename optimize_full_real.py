import csv
import itertools
import json
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parent
WL_MIN = 380
WL_MAX = 700
D65_XY = (0.3127, 0.3290)
WEIGHTS = (0.95, 0.88, 0.80, 0.68, 0.55, 0.42)
MAX_N = 12


SOURCE_NOTES = [
    {
        "id": "osram_blue_laser_455",
        "text": "ams OSRAM PLPT9 450LC_E: 455 nm, 5.5 W optical, 43% WPE.",
        "url": "https://ams-osram.com/news/media-updates/introducing-the-new-high-efficiency-blue-laser-diode-with-455-nm-wavelength",
    },
    {
        "id": "blue_laser_record_455",
        "text": "Compound Semiconductor report: 455 nm blue laser, 7.11 W, 53.2% WPE record.",
        "url": "https://compoundsemiconductor.net/article/122870/Breakthroughs_in_blue_and_green_laser_diodes",
    },
    {
        "id": "green_led_527",
        "text": "Optics Express / PubMed: 527 nm InGaN green LED peak WPE 54.1%.",
        "url": "https://pubmed.ncbi.nlm.nih.gov/30645467/",
    },
    {
        "id": "green_gap_2025",
        "text": "2025 APL / Semiconductor Today: current green LED WPE near 19% at 100 A/cm2; DOE target 55%.",
        "url": "https://www.semiconductor-today.com/news_items/2025/jun/uiuc-120625.shtml",
    },
    {
        "id": "thorlabs_visible_lasers",
        "text": "Thorlabs visible laser diode catalog lists center wavelengths from 404 nm to 690 nm.",
        "url": "https://www.thorlabs.com/visible-laser-diodes-center-wavelengths-from-404-nm-to-690-nm",
    },
    {
        "id": "rpmc_gan_lasers",
        "text": "RPMC notes GaN laser technology covers 375 nm to 521 nm, with high power products.",
        "url": "https://www.rpmclasers.com/wavelength/635nm-lasers/",
    },
    {
        "id": "phosphor_amber_590",
        "text": "Phys.org: blue InGaN plus nitride phosphor at 590 nm amber, EQE 32%, 300% over direct AlGaInP.",
        "url": "https://phys.org/news/2009-07-yellow-gap-full-conversion-blue.html",
    },
    {
        "id": "laser_phosphor_broad",
        "text": "Laserline: blue laser phosphor creates broad 450-750 nm white spectrum at 230-300 lm/W optical conversion.",
        "url": "https://www.laserline.com/en-int/news-detail/from-blue-laser-to-high-power-white-light/",
    },
]


def interp(points, x):
    points = sorted(points)
    if x <= points[0][0]:
        return points[0][1]
    if x >= points[-1][0]:
        return points[-1][1]
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        if x0 <= x <= x1:
            t = (x - x0) / (x1 - x0)
            return y0 + t * (y1 - y0)
    raise AssertionError


def read_xyz():
    rows = []
    with open(ROOT / "CIE_xyz_1931_2deg.csv", newline="") as f:
        for wl, x, y, z in csv.reader(f):
            wl = int(wl)
            if WL_MIN <= wl <= WL_MAX:
                rows.append((wl, float(x), float(y), float(z)))
    arr = np.array(rows, dtype=float)
    xyz = arr[:, 1:4]
    xy = xyz[:, :2] / xyz.sum(axis=1, keepdims=True)
    return arr[:, 0].astype(int), xyz, xy


def polygon_area(points):
    p = np.asarray(points)
    return abs(0.5 * np.sum(p[:, 0] * np.roll(p[:, 1], -1) - p[:, 1] * np.roll(p[:, 0], -1)))


def area_for(xy, idx):
    return polygon_area(xy[sorted(idx)])


def d65_target():
    xw, yw = D65_XY
    return np.array([xw / yw, 1.0, (1.0 - xw - yw) / yw])


def source_profile(wl):
    rows = []
    for w in wl:
        laser_eff = None
        laser_name = ""
        led_eff = None
        led_name = ""
        phosphor_eff = None
        phosphor_name = ""

        if 404 <= w <= 690:
            if w <= 470:
                laser_eff = interp([(404, 0.18), (445, 0.40), (455, 0.48), (470, 0.38)], w)
                laser_name = "GaN blue/violet laser diode"
            elif w <= 521:
                laser_eff = interp([(471, 0.22), (500, 0.14), (521, 0.10)], w)
                laser_name = "GaN cyan/green laser diode"
            elif w >= 630:
                laser_eff = interp([(630, 0.30), (660, 0.38), (690, 0.30)], w)
                laser_name = "AlGaInP red laser diode"

        if 380 <= w <= 700:
            led_eff = interp(
                [
                    (380, 0.08),
                    (405, 0.22),
                    (448, 0.62),
                    (485, 0.30),
                    (505, 0.22),
                    (527, 0.38),
                    (555, 0.20),
                    (590, 0.14),
                    (608, 0.24),
                    (630, 0.48),
                    (660, 0.46),
                    (700, 0.18),
                ],
                w,
            )
            led_name = "narrow LED estimate"

        if 520 <= w <= 610:
            phosphor_eff = interp([(520, 0.24), (535, 0.32), (590, 0.32), (610, 0.24)], w)
            phosphor_name = "phosphor converted, broad band"

        choices = []
        if laser_eff is not None:
            choices.append(("laser", laser_eff, laser_name, 2, "laser diode"))
        if led_eff is not None:
            choices.append(("led", led_eff, led_name, 25, "LED"))
        if phosphor_eff is not None:
            choices.append(("phosphor", phosphor_eff, phosphor_name, 70, "phosphor"))
        best = max(choices, key=lambda x: x[1])
        rows.append(
            {
                "wavelength": int(w),
                "kind": best[0],
                "efficiency": round(best[1], 4),
                "name": best[2],
                "fwhm_nm": best[3],
                "note": best[4],
            }
        )
    return rows


def source_vectors(wl, xyz, source_rows):
    out_xyz = []
    out_xy = []
    grid = wl.astype(float)
    for row in source_rows:
        center = row["wavelength"]
        fwhm = max(1.0, float(row["fwhm_nm"]))
        sigma = fwhm / 2.354820045
        spd = np.exp(-0.5 * ((grid - center) / sigma) ** 2)
        spd = spd / np.sum(spd)
        vec = spd @ xyz
        out_xyz.append(vec)
        out_xy.append(vec[:2] / np.sum(vec))
    return np.array(out_xyz), np.array(out_xy)


def scan_triples(wl, emit_xyz, point_xy, locus_area, eff):
    target = d65_target()
    triples = []
    for tri in itertools.combinations(range(len(wl)), 3):
        mat = emit_xyz[list(tri)].T
        try:
            coeff = np.linalg.solve(mat, target)
        except np.linalg.LinAlgError:
            continue
        if np.min(coeff) < -1e-10:
            continue
        coeff = np.maximum(coeff, 0)
        ideal_power = float(np.sum(coeff))
        real_power = float(np.sum(coeff / eff[list(tri)]))
        area = area_for(point_xy, tri) / locus_area
        triples.append(
            {
                "idx": tri,
                "area": area,
                "ideal_power": ideal_power,
                "real_power": real_power,
            }
        )
    return triples


def max_area_dp(xy, n):
    start = 0
    end = len(xy) - 1
    dp = [[(-math.inf, None) for _ in range(n)] for _ in range(len(xy))]
    dp[start][0] = (0.0, None)
    for used in range(1, n):
        for j in range(start + used, end + 1):
            best = (-math.inf, None)
            for i in range(start + used - 1, j):
                prev = dp[i][used - 1][0]
                if not math.isfinite(prev):
                    continue
                a = xy[i] - xy[start]
                b = xy[j] - xy[start]
                val = prev - float(a[0] * b[1] - a[1] * b[0])
                if val > best[0]:
                    best = (val, i)
            dp[j][used] = best
    path = []
    cur = end
    used = n - 1
    while cur is not None:
        path.append(cur)
        cur = dp[cur][used][1]
        used -= 1
    return tuple(reversed(path))


def best_power_for_set(idx, triple_map, mode):
    idx = sorted(idx)
    best = math.inf
    for tri in itertools.combinations(idx, 3):
        row = triple_map.get(tri)
        if row:
            best = min(best, row[f"{mode}_power"])
    return best


def score(xy, idx, locus_area, triple_map, mode, weight):
    area = area_for(xy, idx) / locus_area
    p = best_power_for_set(idx, triple_map, mode)
    if not math.isfinite(p):
        return -math.inf, area, p
    return weight * area - (1 - weight) * math.log(p), area, p


def greedy_extend(xy, base, n, locus_area, triple_map, mode, weight):
    idx = set(base)
    while len(idx) < n:
        best = None
        for cand in range(len(xy)):
            if cand in idx:
                continue
            trial = tuple(sorted(idx | {cand}))
            val, area, p = score(xy, trial, locus_area, triple_map, mode, weight)
            if best is None or val > best[0]:
                best = (val, cand)
        idx.add(best[1])
    return tuple(sorted(idx))


def local_refine(xy, idx, locus_area, triple_map, mode, weight, passes=2):
    idx = set(idx)
    for _ in range(passes):
        changed = False
        current = score(xy, tuple(sorted(idx)), locus_area, triple_map, mode, weight)[0]
        for old in list(idx):
            best = (current, old)
            base = idx - {old}
            for cand in range(len(xy)):
                if cand in base:
                    continue
                trial = tuple(sorted(base | {cand}))
                val = score(xy, trial, locus_area, triple_map, mode, weight)[0]
                if val > best[0] + 1e-12:
                    best = (val, cand)
            if best[1] != old:
                idx = base | {best[1]}
                changed = True
        if not changed:
            break
    return tuple(sorted(idx))


def optimize(wl, point_xy, locus_area, triples, mode):
    triple_map = {tuple(t["idx"]): t for t in triples}
    results = []
    for n in range(3, MAX_N + 1):
        max_idx = max_area_dp(point_xy, n)
        max_area = area_for(point_xy, max_idx) / locus_area
        max_power = best_power_for_set(max_idx, triple_map, mode)
        results.append(("max_area", mode, n, wl[list(max_idx)], max_area, max_power))

        for weight in WEIGHTS:
            seed = max(
                triples,
                key=lambda t: weight * t["area"] - (1 - weight) * math.log(t[f"{mode}_power"]),
            )["idx"]
            idx = greedy_extend(point_xy, seed, n, locus_area, triple_map, mode, weight)
            idx = local_refine(point_xy, idx, locus_area, triple_map, mode, weight)
            val, area, p = score(point_xy, idx, locus_area, triple_map, mode, weight)
            results.append((f"pareto_{weight:.2f}", mode, n, wl[list(idx)], area, p))
    return results


def choose_summary(results):
    best = {}
    for kind, mode, n, waves, area, power in results:
        if not math.isfinite(power):
            continue
        key = (mode, n)
        old = best.get(key)
        value = area / math.log(power + 1.0)
        if old is None or value > old[-1]:
            best[key] = (kind, mode, n, waves, area, power, value)
    return list(best.values())


def write_csvs(source_rows, triples, results, summary):
    with open(ROOT / "source_scan.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["wavelength", "kind", "efficiency", "name", "fwhm_nm", "note"])
        w.writeheader()
        w.writerows(source_rows)

    with open(ROOT / "triple_scan.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["wavelengths_nm", "coverage", "ideal_power", "real_power"])
        for t in triples:
            waves = [WL_MIN + i for i in t["idx"]]
            w.writerow([" ".join(map(str, waves)), f"{t['area']:.6f}", f"{t['ideal_power']:.6f}", f"{t['real_power']:.6f}"])

    with open(ROOT / "results_full.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["kind", "mode", "n", "wavelengths_nm", "coverage", "power"])
        for kind, mode, n, waves, area, power in results:
            w.writerow([kind, mode, n, " ".join(map(str, waves)), f"{area:.6f}", f"{power:.6f}"])

    with open(ROOT / "summary_full.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["mode", "n", "choice", "wavelengths_nm", "coverage_pct", "power"])
        for kind, mode, n, waves, area, power, _ in summary:
            w.writerow([mode, n, kind, " ".join(map(str, waves)), f"{100*area:.2f}", f"{power:.2f}"])


def spectral_reach(waves, source_rows):
    covered = np.zeros(WL_MAX - WL_MIN + 1, dtype=bool)
    by_wl = {r["wavelength"]: r for r in source_rows}
    for w in waves:
        row = by_wl[int(w)]
        half = max(0.5, row["fwhm_nm"] / 2)
        lo = max(WL_MIN, int(math.floor(w - half)))
        hi = min(WL_MAX, int(math.ceil(w + half)))
        covered[lo - WL_MIN : hi - WL_MIN + 1] = True
    return float(np.sum(covered) / len(covered))


def write_html(wl, xy, xyz, real_xy, source_rows, results, summary):
    data = {
        "wavelengths": wl.tolist(),
        "ybar": xyz[:, 1].round(12).tolist(),
        "points": {
            "ideal": xy.round(8).tolist(),
            "real": real_xy.round(8).tolist(),
        },
        "locus": xy.round(8).tolist(),
        "sources": source_rows,
        "sourceNotes": SOURCE_NOTES,
        "results": [
            {
                "kind": kind,
                "mode": mode,
                "n": n,
                "wavelengths": waves.tolist(),
                "coverage": area,
                "power": power if math.isfinite(power) else None,
                "spectralReach": spectral_reach(waves, source_rows),
            }
            for kind, mode, n, waves, area, power in results
        ],
        "summary": [
            {
                "kind": kind,
                "mode": mode,
                "n": n,
                "wavelengths": waves.tolist(),
                "coverage": area,
                "power": power,
                "spectralReach": spectral_reach(waves, source_rows),
            }
            for kind, mode, n, waves, area, power, _ in summary
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
:root{font-family:Segoe UI,Arial,sans-serif;background:#f5f6f8;color:#17202a}body{margin:0}main{max-width:1320px;margin:auto;padding:22px}h1{margin:0 0 6px;font-size:28px}p{margin:0;color:#586575}.top{display:flex;justify-content:space-between;gap:16px;align-items:end;margin-bottom:16px}.grid{display:grid;grid-template-columns:minmax(560px,1.3fr) minmax(340px,.7fr);gap:16px}.panel{background:#fff;border:1px solid #dfe5ec;border-radius:8px;padding:14px;box-shadow:0 1px 2px #0001}.chart{width:100%;aspect-ratio:1.08;min-height:540px}.mini{width:100%;aspect-ratio:1.45;min-height:240px}canvas{width:100%;height:100%;display:block}.controls{display:grid;gap:13px}label{display:grid;gap:6px;font-size:13px;font-weight:650}input[type=range]{width:100%}.seg{display:grid;grid-template-columns:1fr 1fr;border:1px solid #ccd5df;border-radius:8px;overflow:hidden}.seg button{border:0;background:#f6f8fa;padding:9px;font-weight:650}.seg button.on{background:#17202a;color:white}.metrics{display:grid;grid-template-columns:1fr 1fr;gap:10px}.metric{background:#f7f9fb;border:1px solid #e2e8ef;border-radius:8px;padding:10px}.metric b{display:block;font-size:24px}.metric span,.small{font-size:12px;color:#687584}.pill{display:inline-block;margin:2px;padding:3px 8px;border-radius:999px;background:#edf2f7;border:1px solid #d7e0ea}.tables{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:16px}.wide{grid-column:1/-1}table{width:100%;border-collapse:collapse;font-size:13px}th,td{text-align:left;padding:7px 8px;border-bottom:1px solid #e8edf2;vertical-align:top}th{position:sticky;top:0;background:#f7f9fb;color:#47515e}.tablebox{max-height:380px;overflow:auto}a{color:#174ea6}@media(max-width:930px){main{padding:14px}.grid,.tables{grid-template-columns:1fr}.chart{min-height:370px}.top{display:block}}
</style>
</head>
<body>
<main>
<div class="top"><div><h1>Wavelength Primary Optimizer</h1><p>CIE 1931, D65 white power, ideal 1 nm vs real source estimates.</p></div><div class="small">Real mode uses sourced wavelength availability plus WPE estimates. Phosphors are broad, shown as real sources but not true 1 nm emitters.</div></div>
<section class="grid">
<div class="panel"><canvas id="cie" class="chart"></canvas></div>
<div class="panel controls">
<div class="seg"><button id="idealBtn" class="on">Ideal radiant</button><button id="realBtn">Real source</button></div>
<label>Primary count <input id="n" type="range" min="3" max="12" value="6"><span id="nText"></span></label>
<label>Gamut vs power <input id="bias" type="range" min="42" max="100" value="80"><span id="biasText"></span></label>
<div class="metrics"><div class="metric"><b id="coverage"></b><span>locus area covered</span></div><div class="metric"><b id="power"></b><span id="powerLabel"></span></div></div>
<div><div class="small">Chosen wavelengths</div><div id="waves"></div></div>
<canvas id="env" class="mini"></canvas>
</div>
</section>
<section class="tables">
<div class="panel tablebox"><h2>Best by count</h2><table id="summary"></table></div>
<div class="panel tablebox"><h2>Choices for selected count</h2><table id="choices"></table></div>
<div class="panel tablebox wide"><h2>Source scan</h2><table id="sources"></table></div>
<div class="panel tablebox wide"><h2>Source notes</h2><table id="notes"></table></div>
</section>
</main>
<script id="data" type="application/json">__DATA__</script>
<script>__APP_JS__</script>
</body>
</html>"""
    app_js = (ROOT / "app.js").read_text(encoding="utf-8")
    (ROOT / "index.html").write_text(html.replace("__DATA__", json.dumps(data)).replace("__APP_JS__", app_js), encoding="utf-8")


def main():
    wl, xyz, xy = read_xyz()
    locus_area = polygon_area(xy)
    source_rows = source_profile(wl)
    real_xyz, real_xy = source_vectors(wl, xyz, source_rows)
    ideal_eff = np.ones(len(wl), dtype=float)
    real_eff = np.array([r["efficiency"] for r in source_rows], dtype=float)
    ideal_triples = scan_triples(wl, xyz, xy, locus_area, ideal_eff)
    real_triples = scan_triples(wl, real_xyz, real_xy, locus_area, real_eff)
    triples = ideal_triples + real_triples
    results = optimize(wl, xy, locus_area, ideal_triples, "ideal") + optimize(wl, real_xy, locus_area, real_triples, "real")
    summary = choose_summary(results)
    write_csvs(source_rows, triples, results, summary)
    write_html(wl, xy, xyz, real_xy, source_rows, results, summary)
    print((ROOT / "summary_full.csv").read_text())
    print(f"ideal_triples={len(ideal_triples)} real_triples={len(real_triples)}")


if __name__ == "__main__":
    main()

