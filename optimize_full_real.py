import csv
import itertools
import json
import math
import os
from argparse import ArgumentParser
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from hashlib import sha256
from pathlib import Path

import numpy as np
from tqdm import tqdm

ROOT = Path(__file__).resolve().parent
WL_MIN = 380
WL_MAX = 700
D65_XY = (0.3127, 0.3290)
WEIGHTS = (0.95, 0.88, 0.80, 0.68, 0.55, 0.42)
ENVELOPE_WEIGHTS = (0.95, 0.80, 0.55, 0.42)
MAX_N = 12
OBJECTIVES = ("white", "envelope")
ENVELOPE_CACHE = {}
ENVELOPE_HELPER_WAVELENGTHS = (
    380,
    410,
    447,
    460,
    474,
    486,
    496,
    504,
    511,
    518,
    527,
    544,
    568,
    579,
    613,
    640,
    660,
    690,
    699,
    700,
)


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
    {
        "id": "nichia_uva",
        "text": "Nichia UV-A product page: 330, 365, 375, 385, 395, and 405 nm production UV-A LEDs.",
        "url": "https://led-ld.nichia.co.jp/en/product/uv_uva.html",
    },
    {
        "id": "nichia_515_ld",
        "text": "Nichia NDG4716 datasheet: 515 nm green laser diode, 150 mW CW typical.",
        "url": "https://led-ld.nichia.co.jp/api/data/spec/ld/NDG4716.pdf",
    },
    {
        "id": "osram_660_wpe",
        "text": "ams OSRAM 2023 OSLON Square Hyper Red: 660 nm horticulture LED, 78.8% WPE.",
        "url": "https://ams-osram.com/news/press-releases/oslon-square-hyper-red-led",
    },
    {
        "id": "osram_640_red",
        "text": "ams OSRAM OSLON Optimal adds 640 nm red to 450, 660, 730 nm horticulture family.",
        "url": "https://ams-osram.com/news/press-releases/oslon-optimal-red",
    },
]

SOURCE_MODEL_BANDS = [
    (380, 389, "led", [(380, 0.42), (385, 0.47), (389, 0.46)], 11, "Nichia-class UV-A LED; inferred WPE"),
    (390, 405, "led", [(390, 0.45), (405, 0.45)], 12, "violet InGaN LED / laser bin"),
    (406, 439, "led", [(406, 0.48), (439, 0.58)], 18, "violet-blue InGaN LED estimate"),
    (440, 459, "led", [(440, 0.62), (450, 0.68), (459, 0.62)], 20, "high-efficiency blue InGaN LED"),
    (440, 470, "laser", [(440, 0.30), (455, 0.48), (470, 0.38)], 2, "blue GaN laser diode"),
    (460, 480, "led", [(460, 0.58), (470, 0.50), (480, 0.38)], 22, "blue LED; docs cite 470 nm bins"),
    (481, 505, "led", [(481, 0.34), (505, 0.22)], 25, "cyan LED; green-gap shoulder"),
    (488, 521, "laser", [(488, 0.18), (515, 0.11), (521, 0.10)], 2, "cyan/green laser diode"),
    (506, 520, "led", [(506, 0.24), (520, 0.32)], 28, "cyan-green LED / display emitter"),
    (521, 540, "led", [(521, 0.38), (527, 0.54), (540, 0.36)], 30, "527 nm high-WPE green LED peak; optimistic"),
    (541, 579, "phosphor", [(541, 0.30), (565, 0.34), (579, 0.30)], 65, "lime/yellow phosphor or broad converter"),
    (580, 599, "led", [(580, 0.12), (590, 0.09), (599, 0.12)], 18, "amber/yellow AlInGaP LED; low WPE zone"),
    (600, 619, "oled_qd", [(600, 0.18), (614, 0.22), (619, 0.20)], 35, "orange-red OLED/QD research-class estimate"),
    (620, 639, "led", [(620, 0.38), (630, 0.52), (639, 0.58)], 20, "red LED / QD / 638 nm LD anchor"),
    (640, 649, "led", [(640, 0.62), (649, 0.68)], 18, "640 nm red horticulture LED helper"),
    (650, 669, "led", [(650, 0.72), (660, 0.788), (669, 0.68)], 18, "660 nm hyper-red horticulture LED"),
    (670, 700, "laser", [(670, 0.42), (690, 0.30), (700, 0.18)], 2, "deep/far red laser diode; product density thins near 700 nm"),
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
    return abs(
        0.5 * np.sum(p[:, 0] * np.roll(p[:, 1], -1) - p[:, 1] * np.roll(p[:, 0], -1))
    )


def area_for(xy, idx):
    return polygon_area(xy[sorted(idx)])


def d65_target():
    xw, yw = D65_XY
    return np.array([xw / yw, 1.0, (1.0 - xw - yw) / yw])


def source_profile(wl):
    rows = []
    for w in wl:
        choices = [
            (kind, interp(anchors, int(w)), f"{kind} source estimate", fwhm, note)
            for lo, hi, kind, anchors, fwhm, note in SOURCE_MODEL_BANDS
            if lo <= int(w) <= hi
        ]
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


def cache_key_for(mode, emit_xyz, point_xy, eff):
    h = sha256()
    h.update(mode.encode("ascii"))
    for arr in (emit_xyz, point_xy, eff):
        raw = np.ascontiguousarray(arr)
        h.update(str(raw.shape).encode("ascii"))
        h.update(raw.view(np.uint8))
    return h.hexdigest()


def triples_from_arrays(data, label="triples"):
    idx_arr = data["idx"]
    area_arr = data["area"]
    ideal_power_arr = data["ideal_power"]
    real_power_arr = data["real_power"]
    ideal_cost_arr = data["ideal_cost"]
    real_cost_arr = data["real_cost"]
    mat_arr = data["mat"]
    triples = []
    for i in tqdm(range(len(area_arr)), desc=f"Loading {label}", unit="triple"):
        triples.append(
            {
                "idx": tuple(int(x) for x in idx_arr[i]),
                "area": float(area_arr[i]),
                "ideal_power": float(ideal_power_arr[i]),
                "real_power": float(real_power_arr[i]),
                "ideal_cost": ideal_cost_arr[i],
                "real_cost": real_cost_arr[i],
                "mat": mat_arr[i],
            }
        )
    return triples


def scan_triple_chunk(args):
    start_i, end_i, emit_xyz, point_xy, locus_area, eff, target = args
    idx_rows = []
    area_rows = []
    ideal_power_rows = []
    real_power_rows = []
    ideal_cost_rows = []
    real_cost_rows = []
    mat_rows = []
    checked = 0
    n = len(eff)
    for i in range(start_i, end_i):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                checked += 1
                tri = (i, j, k)
                mat = emit_xyz[list(tri)].T
                try:
                    coeff = np.linalg.solve(mat, target)
                except np.linalg.LinAlgError:
                    continue
                if np.min(coeff) < -1e-10:
                    continue
                coeff = np.maximum(coeff, 0)
                idx_rows.append(tri)
                area_rows.append(area_for(point_xy, tri) / locus_area)
                ideal_power_rows.append(float(np.sum(coeff)))
                real_cost = 1.0 / eff[list(tri)]
                real_power_rows.append(float(np.sum(coeff * real_cost)))
                ideal_cost_rows.append((1.0, 1.0, 1.0))
                real_cost_rows.append(tuple(float(x) for x in real_cost))
                mat_rows.append(mat)
    return {
        "checked": checked,
        "idx": np.array(idx_rows, dtype=np.int32),
        "area": np.array(area_rows),
        "ideal_power": np.array(ideal_power_rows),
        "real_power": np.array(real_power_rows),
        "ideal_cost": np.array(ideal_cost_rows),
        "real_cost": np.array(real_cost_rows),
        "mat": np.array(mat_rows),
    }


def combo_count_for_first_range(start_i, end_i, n):
    return sum(math.comb(n - i - 1, 2) for i in range(start_i, end_i))


def scan_triples(wl, emit_xyz, point_xy, locus_area, eff, mode="triples", workers=1):
    cache_path = ROOT / f"triples_{mode}.npz"
    cache_key = cache_key_for(mode, emit_xyz, point_xy, eff)
    if cache_path.exists():
        print(f"Loading {len(eff)}-wavelength triples from {cache_path.name} ...", flush=True)
        data = np.load(cache_path)
        stored_key = str(data["cache_key"]) if "cache_key" in data.files else ""
        if stored_key == cache_key or (mode == "ideal" and not stored_key):
            triples = triples_from_arrays(data, mode)
            print(f"Loaded {len(triples)} triples from cache.", flush=True)
            data.close()
            return triples
        data.close()
        print(f"{cache_path.name} is stale for current source model; rebuilding.", flush=True)

    target = d65_target()
    worker_count = max(1, int(workers))
    n_wl = len(wl)
    chunk_size = max(1, math.ceil((n_wl - 2) / (worker_count * 8)))
    chunks = [
        (start, min(n_wl - 2, start + chunk_size), emit_xyz, point_xy, locus_area, eff, target)
        for start in range(0, n_wl - 2, chunk_size)
    ]
    total = math.comb(n_wl, 3)
    print(f"Scanning triples ({mode}) with {worker_count} worker(s); {total} combos.", flush=True)
    parts = []
    with tqdm(total=total, desc=f"Scanning triples ({mode})") as bar:
        if worker_count == 1:
            for chunk in chunks:
                part = scan_triple_chunk(chunk)
                parts.append(part)
                bar.update(part["checked"])
        else:
            with ProcessPoolExecutor(max_workers=worker_count) as pool:
                futures = [pool.submit(scan_triple_chunk, chunk) for chunk in chunks]
                for future in as_completed(futures):
                    part = future.result()
                    parts.append(part)
                    bar.update(part["checked"])

    idx_arr = np.concatenate([p["idx"] for p in parts if len(p["idx"])])
    area_arr = np.concatenate([p["area"] for p in parts if len(p["area"])])
    ideal_power_arr = np.concatenate([p["ideal_power"] for p in parts if len(p["ideal_power"])])
    real_power_arr = np.concatenate([p["real_power"] for p in parts if len(p["real_power"])])
    ideal_cost_arr = np.concatenate([p["ideal_cost"] for p in parts if len(p["ideal_cost"])])
    real_cost_arr = np.concatenate([p["real_cost"] for p in parts if len(p["real_cost"])])
    mat_arr = np.concatenate([p["mat"] for p in parts if len(p["mat"])])
    np.savez(
        cache_path,
        cache_key=cache_key,
        idx=idx_arr,
        area=area_arr,
        ideal_power=ideal_power_arr,
        real_power=real_power_arr,
        ideal_cost=ideal_cost_arr,
        real_cost=real_cost_arr,
        mat=mat_arr,
    )
    print(f"Saved {len(idx_arr)} triples to {cache_path.name}.", flush=True)
    return triples_from_arrays(
        {
            "idx": idx_arr,
            "area": area_arr,
            "ideal_power": ideal_power_arr,
            "real_power": real_power_arr,
            "ideal_cost": ideal_cost_arr,
            "real_cost": real_cost_arr,
            "mat": mat_arr,
        },
        mode,
    )


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


def target_xyz_from_xy(x, y):
    return np.array([x / y, 1.0, (1.0 - x - y) / y])


def best_power_for_target(idx, triple_map, mode, target):
    idx = sorted(idx)
    best = math.inf
    for tri in itertools.combinations(idx, 3):
        row = triple_map.get(tri)
        if not row:
            continue
        mat = row["mat"]
        try:
            coeff = np.linalg.solve(mat, target)
        except np.linalg.LinAlgError:
            continue
        if np.min(coeff) < -1e-9:
            continue
        coeff = np.maximum(coeff, 0)
        power = float(np.sum(coeff * row[f"{mode}_cost"]))
        best = min(best, power)
    return best


def make_envelope_grid(xy):
    grid = []
    for x in np.arange(0.04, 0.721, 0.08):
        for y in np.arange(0.04, 0.841, 0.08):
            if point_in_poly(float(x), float(y), xy):
                grid.append(target_xyz_from_xy(float(x), float(y)))
    return grid


def point_in_poly(x, y, poly):
    inside = False
    j = len(poly) - 1
    for i in range(len(poly)):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if ((yi > y) != (yj > y)) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            inside = not inside
        j = i
    return inside


def envelope_power_for_set(idx, xy, triple_map, mode, grid):
    key = (mode, tuple(sorted(idx)))
    if key in ENVELOPE_CACHE:
        return ENVELOPE_CACHE[key]
    points = xy[list(key[1])]
    total = 0.0
    count = 0
    for target in grid:
        tx = target[0] / np.sum(target)
        ty = target[1] / np.sum(target)
        if not point_in_poly(tx, ty, points):
            continue
        power = best_power_for_target(idx, triple_map, mode, target)
        if math.isfinite(power):
            total += power
            count += 1
    value = total / count if count else math.inf
    ENVELOPE_CACHE[key] = value
    return value


def score(xy, idx, locus_area, triple_map, mode, weight, objective, grid):
    area = area_for(xy, idx) / locus_area
    p = (
        envelope_power_for_set(idx, xy, triple_map, mode, grid)
        if objective == "envelope"
        else best_power_for_set(idx, triple_map, mode)
    )
    if not math.isfinite(p):
        return -math.inf, area, p
    return weight * area - (1 - weight) * math.log(p), area, p


def candidate_pool(xy, objective, fixed=()):
    if objective != "envelope":
        return range(len(xy))
    pool = {int(i) for i in fixed}
    pool.update(
        max(0, min(len(xy) - 1, w - WL_MIN)) for w in ENVELOPE_HELPER_WAVELENGTHS
    )
    pool.update(range(0, len(xy), 20))
    pool.add(len(xy) - 1)
    return sorted(pool)


def objective_weights(objective):
    return ENVELOPE_WEIGHTS if objective == "envelope" else WEIGHTS


def greedy_extend(xy, base, n, locus_area, triple_map, mode, weight, objective, grid):
    idx = set(base)
    while len(idx) < n:
        best = None
        for cand in candidate_pool(xy, objective, idx):
            if cand in idx:
                continue
            trial = tuple(sorted(idx | {cand}))
            val, area, p = score(
                xy, trial, locus_area, triple_map, mode, weight, objective, grid
            )
            if best is None or val > best[0]:
                best = (val, cand)
        idx.add(best[1])
    return tuple(sorted(idx))


def local_refine(
    xy, idx, locus_area, triple_map, mode, weight, objective, grid, passes=2
):
    idx = set(idx)
    for _ in range(passes):
        changed = False
        current = score(
            xy,
            tuple(sorted(idx)),
            locus_area,
            triple_map,
            mode,
            weight,
            objective,
            grid,
        )[0]
        for old in list(idx):
            best = (current, old)
            base = idx - {old}
            for cand in candidate_pool(xy, objective, idx):
                if cand in base:
                    continue
                trial = tuple(sorted(base | {cand}))
                val = score(
                    xy, trial, locus_area, triple_map, mode, weight, objective, grid
                )[0]
                if val > best[0] + 1e-12:
                    best = (val, cand)
            if best[1] != old:
                idx = base | {best[1]}
                changed = True
        if not changed:
            break
    return tuple(sorted(idx))


def optimize(wl, point_xy, locus_area, triples, mode, workers=1):
    triple_map = {tuple(t["idx"]): t for t in triples}
    grid = make_envelope_grid(point_xy)
    results = []
    max_by_n = {}

    # Pre-compute max-area gamut polygons (one per n)
    for n in range(3, MAX_N + 1):
        max_idx = max_area_dp(point_xy, n)
        max_by_n[n] = max_idx
        max_area = area_for(point_xy, max_idx) / locus_area
        max_power = best_power_for_set(max_idx, triple_map, mode)
        results.append(
            ("max_area", "gamut", mode, n, wl[list(max_idx)], max_area, max_power)
        )

    tasks = []
    for n in range(3, MAX_N + 1):
        for objective in OBJECTIVES:
            for weight in objective_weights(objective):
                tasks.append((n, objective, weight))

    def run_task(task):
        n, objective, weight = task
        max_idx = max_by_n[n]
        if objective == "envelope":
            idx = max_idx
        else:
            seed = max(
                triples,
                key=lambda t: (
                    weight * t["area"] - (1 - weight) * math.log(t[f"{mode}_power"])
                ),
            )["idx"]
            idx = greedy_extend(
                point_xy, seed, n, locus_area, triple_map, mode, weight, objective, grid
            )
        refine_passes = 1 if objective == "envelope" else 2
        idx = local_refine(
            point_xy,
            idx,
            locus_area,
            triple_map,
            mode,
            weight,
            objective,
            grid,
            refine_passes,
        )
        val, area, p = score(
            point_xy, idx, locus_area, triple_map, mode, weight, objective, grid
        )
        return (f"{objective}_{weight:.2f}", objective, mode, n, wl[list(idx)], area, p)

    worker_count = max(1, min(int(workers), len(tasks)))
    if worker_count == 1:
        for task in tqdm(tasks, desc=f"Optimizing ({mode})", unit="task"):
            results.append(run_task(task))
    else:
        print(f"Optimizing ({mode}) with {worker_count} worker threads.", flush=True)
        with ThreadPoolExecutor(max_workers=worker_count) as pool:
            futures = [pool.submit(run_task, task) for task in tasks]
            for future in tqdm(as_completed(futures), total=len(futures), desc=f"Optimizing ({mode})", unit="task"):
                results.append(future.result())
    return results


def choose_summary(results):
    best = {}
    for kind, objective, mode, n, waves, area, power in results:
        if not math.isfinite(power):
            continue
        key = (objective, mode, n)
        old = best.get(key)
        value = area / math.log(power + 1.0)
        if old is None or value > old[-1]:
            best[key] = (kind, objective, mode, n, waves, area, power, value)
    return sorted(best.values(), key=lambda r: result_sort_key(r[:7]))


def result_sort_key(row):
    objective_order = {"gamut": 0, "white": 1, "envelope": 2}
    kind, objective, mode, n, waves, area, power = row
    return (0 if mode == "ideal" else 1, objective_order.get(objective, 9), n, kind)


def write_csvs(source_rows, triples, results, summary):
    with open(ROOT / "source_scan.csv", "w", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=["wavelength", "kind", "efficiency", "name", "fwhm_nm", "note"],
        )
        w.writeheader()
        w.writerows(source_rows)

    with open(ROOT / "triple_scan.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["wavelengths_nm", "coverage", "ideal_power", "real_power"])
        for t in triples:
            waves = [WL_MIN + i for i in t["idx"]]
            w.writerow(
                [
                    " ".join(map(str, waves)),
                    f"{t['area']:.6f}",
                    f"{t['ideal_power']:.6f}",
                    f"{t['real_power']:.6f}",
                ]
            )

    with open(ROOT / "results_full.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(
            ["kind", "objective", "mode", "n", "wavelengths_nm", "coverage", "power"]
        )
        for kind, objective, mode, n, waves, area, power in results:
            w.writerow(
                [
                    kind,
                    objective,
                    mode,
                    n,
                    " ".join(map(str, waves)),
                    f"{area:.6f}",
                    f"{power:.6f}",
                ]
            )

    with open(ROOT / "summary_full.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "objective",
                "mode",
                "n",
                "choice",
                "wavelengths_nm",
                "coverage_pct",
                "power",
            ]
        )
        for kind, objective, mode, n, waves, area, power, _ in summary:
            w.writerow(
                [
                    objective,
                    mode,
                    n,
                    kind,
                    " ".join(map(str, waves)),
                    f"{100 * area:.2f}",
                    f"{power:.2f}",
                ]
            )


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
                "objective": objective,
                "mode": mode,
                "n": n,
                "wavelengths": waves.tolist(),
                "coverage": area,
                "power": power if math.isfinite(power) else None,
                "spectralReach": spectral_reach(waves, source_rows),
            }
            for kind, objective, mode, n, waves, area, power in results
        ],
        "summary": [
            {
                "kind": kind,
                "objective": objective,
                "mode": mode,
                "n": n,
                "wavelengths": waves.tolist(),
                "coverage": area,
                "power": power,
                "spectralReach": spectral_reach(waves, source_rows),
            }
            for kind, objective, mode, n, waves, area, power, _ in summary
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
:root{font-family:Segoe UI,Arial,sans-serif;background:#f5f6f8;color:#17202a}body{margin:0}main{max-width:1320px;margin:auto;padding:22px}h1{margin:0 0 6px;font-size:28px}p{margin:0;color:#586575}.top{display:flex;justify-content:space-between;gap:16px;align-items:end;margin-bottom:16px}.grid{display:grid;grid-template-columns:minmax(560px,1.3fr) minmax(340px,.7fr);gap:16px}.panel{background:#fff;border:1px solid #dfe5ec;border-radius:8px;padding:14px;box-shadow:0 1px 2px #0001}.chart{width:100%;aspect-ratio:1.08;min-height:540px}.mini{width:100%;aspect-ratio:1.45;min-height:240px}canvas{width:100%;height:100%;display:block}.controls{display:grid;gap:13px}label{display:grid;gap:6px;font-size:13px;font-weight:650}input[type=range],select{width:100%}select{padding:8px;border:1px solid #ccd5df;border-radius:8px;background:white;font-weight:650}.seg{display:grid;grid-template-columns:1fr 1fr;border:1px solid #ccd5df;border-radius:8px;overflow:hidden}.seg button{border:0;background:#f6f8fa;padding:9px;font-weight:650}.seg button.on{background:#17202a;color:white}.metrics{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px}.metric{background:#f7f9fb;border:1px solid #e2e8ef;border-radius:8px;padding:10px}.metric b{display:block;font-size:24px}.metric span,.small{font-size:12px;color:#687584}.pill{display:inline-block;margin:2px;padding:3px 8px;border-radius:999px;background:#edf2f7;border:1px solid #d7e0ea}.tables{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:16px}.wide{grid-column:1/-1}table{width:100%;border-collapse:collapse;font-size:13px}th,td{text-align:left;padding:7px 8px;border-bottom:1px solid #e8edf2;vertical-align:top}th{position:sticky;top:0;background:#f7f9fb;color:#47515e}.tablebox{max-height:380px;overflow:auto}a{color:#174ea6}@media(max-width:930px){main{padding:14px}.grid,.tables{grid-template-columns:1fr}.chart{min-height:370px}.top{display:block}.metrics{grid-template-columns:1fr}}
</style>
</head>
<body>
<main>
<div class="top"><div><h1>Wavelength Primary Optimizer</h1><p>CIE 1931, D65 white power, ideal 1 nm vs real source estimates.</p></div><div class="small">Real mode uses sourced wavelength availability plus WPE estimates. Phosphors are broad, shown as real sources but not true 1 nm emitters.</div></div>
<section class="grid">
<div class="panel"><canvas id="cie" class="chart"></canvas></div>
<div class="panel controls">
<div class="seg"><button id="idealBtn" class="on">Ideal radiant</button><button id="realBtn">Real source</button></div>
<label title="Pick what the optimizer should prefer. Envelope average uses a coarse xy grid inside the current gamut.">Optimize for <select id="objective"><option value="balanced">balanced</option><option value="gamut">max gamut</option><option value="white">D65 white power</option><option value="image">typical image power</option><option value="envelope">envelope average power</option></select></label>
<label>Primary count <input id="n" type="range" min="3" max="12" value="6"><span id="nText"></span></label>
<label>Gamut vs power <input id="bias" type="range" min="42" max="100" value="80"><span id="biasText"></span></label>
<div class="metrics"><div class="metric" title="Polygon area covered in CIE xy. This says how saturated colors can get, not how cheap they are."><b id="coverage"></b><span>locus area</span></div><div class="metric" title="Power to make D65 white at Y=1. Can explode if D65 needs a weak far-red or deep-blue primary."><b id="power"></b><span id="powerLabel"></span></div><div class="metric" title="Weighted average power for a small fixed typical-image sample set: gray/white, skin, sky, foliage, yellow, and saturated RGB."><b id="imagePower"></b><span id="imagePowerLabel"></span></div><div class="metric" title="Average power over a coarse grid of chromaticity points covered by the current source polygon. This catches expensive whole regions, not just D65."><b id="envelopePower"></b><span id="envelopePowerLabel"></span></div><div class="metric" title="Fraction of 380-700 nm intercepted by source bandwidths. Broad sources score better here but may reduce chromaticity gamut."><b id="reach"></b><span id="reachLabel"></span></div></div>
<div><div class="small">Chosen wavelengths</div><div id="waves"></div></div>
<canvas id="env" class="mini"></canvas>
<canvas id="mix" class="mini" title="Click inside the red gamut polygon to see the cheapest mix of selected primaries for that target color."></canvas>
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
    (ROOT / "index.html").write_text(
        html.replace("__DATA__", json.dumps(data)).replace("__APP_JS__", app_js),
        encoding="utf-8",
    )


def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        "--workers",
        type=int,
        default=max(1, min(8, (os.cpu_count() or 2) - 1)),
        help="process workers for stale triple scans",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    wl, xyz, xy = read_xyz()
    locus_area = polygon_area(xy)
    source_rows = source_profile(wl)
    real_xyz, real_xy = source_vectors(wl, xyz, source_rows)
    ideal_eff = np.ones(len(wl), dtype=float)
    real_eff = np.array([r["efficiency"] for r in source_rows], dtype=float)
    ideal_triples = scan_triples(wl, xyz, xy, locus_area, ideal_eff, "ideal", args.workers)
    real_triples = scan_triples(wl, real_xyz, real_xy, locus_area, real_eff, "real", args.workers)
    triples = ideal_triples + real_triples
    results = optimize(wl, xy, locus_area, ideal_triples, "ideal", args.workers) + optimize(
        wl, real_xy, locus_area, real_triples, "real", args.workers
    )
    results = sorted(results, key=result_sort_key)
    summary = choose_summary(results)
    write_csvs(source_rows, triples, results, summary)
    write_html(wl, xy, xyz, real_xy, source_rows, results, summary)
    print((ROOT / "summary_full.csv").read_text())
    print(f"ideal_triples={len(ideal_triples)} real_triples={len(real_triples)}")


if __name__ == "__main__":
    main()
