const data = JSON.parse(document.getElementById("data").textContent);
const wl = data.wavelengths;
let mode = "ideal";
let objective = "balanced";
let custom = null;
let drag = null;
let currentRow = null;
let targetPoint = null;
let movedDuringDrag = false;

const locus = data.locus.map((p, i) => ({ x: p[0], y: p[1], wl: wl[i] }));
const xMin = -0.02;
const xMax = 0.78;
const yMin = -0.04;
const yMax = 0.9;
const WL_MIN_JS = 380;
const WL_MAX_JS = 700;
const $ = (id) => document.getElementById(id);
const imageSamples = [
  { x: 0.3127, y: 0.3290, w: 0.35, name: "white/gray" },
  { x: 0.38, y: 0.35, w: 0.12, name: "skin/warm" },
  { x: 0.24, y: 0.27, w: 0.10, name: "sky" },
  { x: 0.30, y: 0.50, w: 0.10, name: "foliage" },
  { x: 0.36, y: 0.36, w: 0.10, name: "warm neutral" },
  { x: 0.44, y: 0.48, w: 0.08, name: "yellow" },
  { x: 0.64, y: 0.33, w: 0.05, name: "red" },
  { x: 0.30, y: 0.60, w: 0.05, name: "green" },
  { x: 0.15, y: 0.06, w: 0.05, name: "blue" },
];
const envelopeGrid = [];
for (let x = 0.04; x <= 0.72; x += 0.04) {
  for (let y = 0.04; y <= 0.84; y += 0.04) {
    if (inPoly(x, y, locus)) envelopeGrid.push({ x, y });
  }
}

function kindWeight(kind) {
  return kind === "max_area" ? 100 : Math.round(parseFloat(kind.split("_")[1]) * 100);
}

function objectiveRank(row) {
  return { gamut: 0, white: 1, envelope: 2 }[row.objective] ?? 9;
}

function rowOrder(a, b) {
  return objectiveRank(a) - objectiveRank(b) || a.n - b.n || a.kind.localeCompare(b.kind);
}

function rows() {
  return data.results.filter((r) => r.mode === mode && r.n === +$("n").value && r.power);
}

function pick() {
  const bias = +$("bias").value / 100;
  const scoreRow = (row) => {
    const stats = customStats(row);
    if (objective === "gamut") return stats.coverage;
    if (objective === "white") return stats.coverage / Math.log(stats.power + 1);
    if (objective === "image") return stats.imageCoverage / Math.log(stats.imagePower + 1);
    if (objective === "envelope") return stats.coverage / Math.log(stats.envelopePower + 1);
    const wanted = Math.abs(kindWeight(row.kind) / 100 - bias);
    return (stats.coverage * 0.35 + stats.imageCoverage * 0.25 + stats.envelopeCoverage * 0.25) / Math.log(stats.power + stats.imagePower + stats.envelopePower + 1) - wanted * 0.15;
  };
  return rows().reduce((best, row) => (scoreRow(row) > scoreRow(best) ? row : best), rows()[0]);
}

function fit(canvas) {
  const rect = canvas.getBoundingClientRect();
  const dpr = window.devicePixelRatio || 1;
  canvas.width = Math.max(1, Math.floor(rect.width * dpr));
  canvas.height = Math.max(1, Math.floor(rect.height * dpr));
}

function toPx(canvas, x, y) {
  return [
    ((x - xMin) / (xMax - xMin)) * canvas.width,
    canvas.height - ((y - yMin) / (yMax - yMin)) * canvas.height,
  ];
}

function fromEvent(event) {
  const canvas = $("cie");
  const rect = canvas.getBoundingClientRect();
  const dpr = window.devicePixelRatio || 1;
  const px = (event.clientX - rect.left) * dpr;
  const py = (event.clientY - rect.top) * dpr;
  return {
    x: xMin + (px / canvas.width) * (xMax - xMin),
    y: yMax - (py / canvas.height) * (yMax - yMin),
  };
}

function inPoly(x, y, poly) {
  let inside = false;
  for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {
    const a = poly[i];
    const b = poly[j];
    if ((a.y > y) !== (b.y > y) && x < ((b.x - a.x) * (y - a.y)) / (b.y - a.y) + a.x) {
      inside = !inside;
    }
  }
  return inside;
}

function closestPointOnSegment(point, a, b) {
  const vx = b.x - a.x;
  const vy = b.y - a.y;
  const len2 = vx * vx + vy * vy;
  const t = len2 === 0 ? 0 : Math.max(0, Math.min(1, ((point.x - a.x) * vx + (point.y - a.y) * vy) / len2));
  return { x: a.x + t * vx, y: a.y + t * vy };
}

function clampToLocus(point) {
  if (inPoly(point.x, point.y, locus)) return point;
  let best = null;
  for (let i = 0; i < locus.length; i++) {
    const candidate = closestPointOnSegment(point, locus[i], locus[(i + 1) % locus.length]);
    const dist = Math.hypot(candidate.x - point.x, candidate.y - point.y);
    if (!best || dist < best.dist) best = { ...candidate, dist };
  }
  return { x: best.x, y: best.y };
}

function nearestWavelength(point) {
  let best = locus[0];
  let bestDist = Infinity;
  for (const item of locus) {
    const dist = Math.hypot(item.x - point.x, item.y - point.y);
    if (dist < bestDist) {
      best = item;
      bestDist = dist;
    }
  }
  return best.wl;
}

function rgb(x, y) {
  if (y <= 0) return [255, 255, 255];
  const X = x / y;
  const Y = 1;
  const Z = (1 - x - y) / y;
  let r = 3.2406 * X - 1.5372 * Y - 0.4986 * Z;
  let g = -0.9689 * X + 1.8758 * Y + 0.0415 * Z;
  let b = 0.0557 * X - 0.204 * Y + 1.057 * Z;
  const m = Math.max(r, g, b, 1e-9);
  r = Math.max(0, Math.min(1, r / m));
  g = Math.max(0, Math.min(1, g / m));
  b = Math.max(0, Math.min(1, b / m));
  const enc = (v) => Math.round(255 * (v <= 0.0031308 ? 12.92 * v : 1.055 * Math.pow(v, 1 / 2.4) - 0.055));
  return [enc(r), enc(g), enc(b)];
}

function wavelengthColor(wave) {
  const index = Math.max(0, Math.min(wl.length - 1, wl.indexOf(wave)));
  const point = data.locus[index] || data.points.ideal[index];
  const color = rgb(point[0], point[1]);
  return `rgb(${color[0]},${color[1]},${color[2]})`;
}

function polyArea(points) {
  let sum = 0;
  for (let i = 0; i < points.length; i++) {
    const a = points[i];
    const b = points[(i + 1) % points.length];
    sum += a.x * b.y - a.y * b.x;
  }
  return Math.abs(sum / 2);
}

const locusArea = polyArea(locus);

function basePoint(wave) {
  const index = wl.indexOf(wave);
  const point = data.points[mode][index];
  return { x: point[0], y: point[1], wl: wave };
}

function chosenPoints(row) {
  return row.wavelengths.map((wave) => {
    const point = custom && custom[wave] ? custom[wave] : basePoint(wave);
    const effectiveWl = custom && custom[wave] ? nearestWavelength(point) : wave;
    return { ...point, wl: effectiveWl, originalWl: wave, luminousY: data.ybar[wl.indexOf(effectiveWl)] };
  });
}

function sourceEff(wave) {
  return data.sources[wl.indexOf(wave)].efficiency;
}

function xyzFromPoint(point) {
  const y = Math.max(0.001, point.y);
  const luminousY = point.luminousY || 1;
  return [luminousY * point.x / y, luminousY, luminousY * (1 - point.x - y) / y];
}

function solve3(matrix, target) {
  const a = matrix[0];
  const b = matrix[1];
  const c = matrix[2];
  const d = target;
  const det = a[0] * (b[1] * c[2] - b[2] * c[1]) - b[0] * (a[1] * c[2] - a[2] * c[1]) + c[0] * (a[1] * b[2] - a[2] * b[1]);
  if (Math.abs(det) < 1e-9) return null;
  const dx = d[0] * (b[1] * c[2] - b[2] * c[1]) - b[0] * (d[1] * c[2] - d[2] * c[1]) + c[0] * (d[1] * b[2] - d[2] * b[1]);
  const dy = a[0] * (d[1] * c[2] - d[2] * c[1]) - d[0] * (a[1] * c[2] - a[2] * c[1]) + c[0] * (a[1] * d[2] - a[2] * d[1]);
  const dz = a[0] * (b[1] * d[2] - b[2] * d[1]) - b[0] * (a[1] * d[2] - a[2] * d[1]) + d[0] * (a[1] * b[2] - a[2] * b[1]);
  return [dx / det, dy / det, dz / det];
}

function mixForTarget(points, row, targetPoint) {
  const target = xyzFromPoint(targetPoint);
  let best = Infinity;
  let bestMix = null;
  for (let i = 0; i < points.length; i++) {
    for (let j = i + 1; j < points.length; j++) {
      for (let k = j + 1; k < points.length; k++) {
        const coeff = solve3([xyzFromPoint(points[i]), xyzFromPoint(points[j]), xyzFromPoint(points[k])], target);
        if (!coeff || coeff.some((v) => v < -1e-7)) continue;
        const power = mode === "real"
          ? coeff[0] / sourceEff(row.wavelengths[i]) + coeff[1] / sourceEff(row.wavelengths[j]) + coeff[2] / sourceEff(row.wavelengths[k])
          : coeff[0] + coeff[1] + coeff[2];
        if (power < best) {
          best = power;
          bestMix = new Array(points.length).fill(0);
          bestMix[i] = coeff[0];
          bestMix[j] = coeff[1];
          bestMix[k] = coeff[2];
        }
      }
    }
  }
  return { power: best, mix: bestMix };
}

function powerForTarget(points, row, targetPoint) {
  return mixForTarget(points, row, targetPoint).power;
}

function imagePowerStats(points, row) {
  let coveredWeight = 0;
  let weightedPower = 0;
  for (const sample of imageSamples) {
    if (!inPoly(sample.x, sample.y, points)) continue;
    const power = powerForTarget(points, row, sample);
    if (!Number.isFinite(power)) continue;
    coveredWeight += sample.w;
    weightedPower += sample.w * power;
  }
  return {
    imageCoverage: coveredWeight,
    imagePower: coveredWeight > 0 ? weightedPower / coveredWeight : Infinity,
  };
}

function envelopePowerStats(points, row) {
  let count = 0;
  let total = 0;
  for (const sample of envelopeGrid) {
    if (!inPoly(sample.x, sample.y, points)) continue;
    const power = powerForTarget(points, row, sample);
    if (!Number.isFinite(power)) continue;
    count++;
    total += power;
  }
  return {
    envelopeCoverage: envelopeGrid.length ? count / envelopeGrid.length : 0,
    envelopePower: count ? total / count : Infinity,
  };
}

function customStats(row) {
  const points = chosenPoints(row);
  const image = imagePowerStats(points, row);
  const envelope = envelopePowerStats(points, row);
  if (!custom) return { coverage: row.coverage, power: row.power, spectralReach: row.spectralReach, points, ...image, ...envelope };
  const best = powerForTarget(points, row, { x: data.d65[0], y: data.d65[1] });
  const uniqueWaves = new Set(points.map((point) => point.wl));
  return { coverage: polyArea(points) / locusArea, power: best, spectralReach: uniqueWaves.size / wl.length, points, ...image, ...envelope };
}

function drawLine(ctx, canvas, points, close = true) {
  ctx.beginPath();
  points.forEach((point, i) => {
    const [x, y] = toPx(canvas, point.x, point.y);
    if (i) ctx.lineTo(x, y);
    else ctx.moveTo(x, y);
  });
  if (close) ctx.closePath();
  ctx.stroke();
}

function drawCie(row) {
  const canvas = $("cie");
  fit(canvas);
  const ctx = canvas.getContext("2d");
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const step = Math.max(4, Math.floor(canvas.width / 165));
  for (let py = 0; py < canvas.height; py += step) {
    for (let px = 0; px < canvas.width; px += step) {
      const x = xMin + ((px + step / 2) / canvas.width) * (xMax - xMin);
      const y = yMax - ((py + step / 2) / canvas.height) * (yMax - yMin);
      if (inPoly(x, y, locus)) {
        const color = rgb(x, y);
        ctx.fillStyle = `rgb(${color[0]},${color[1]},${color[2]})`;
        ctx.fillRect(px, py, step + 1, step + 1);
      }
    }
  }

  ctx.strokeStyle = "#000";
  ctx.lineWidth = 2;
  drawLine(ctx, canvas, locus);

  const chosen = customStats(row).points;
  ctx.fillStyle = "rgba(214,40,40,.15)";
  ctx.strokeStyle = "#d62828";
  ctx.lineWidth = 3;
  ctx.beginPath();
  chosen.forEach((point, i) => {
    const [x, y] = toPx(canvas, point.x, point.y);
    if (i) ctx.lineTo(x, y);
    else ctx.moveTo(x, y);
  });
  ctx.closePath();
  ctx.fill();
  ctx.stroke();

  ctx.fillStyle = "#d62828";
  ctx.font = `${12 * (window.devicePixelRatio || 1)}px Segoe UI`;
  chosen.forEach((point) => {
    const [x, y] = toPx(canvas, point.x, point.y);
    ctx.beginPath();
    ctx.arc(x, y, 7 * (window.devicePixelRatio || 1), 0, Math.PI * 2);
    ctx.fill();
    ctx.fillText(point.wl, x + 9, y - 6);
  });

  const [dx, dy] = toPx(canvas, data.d65[0], data.d65[1]);
  ctx.fillStyle = "#111";
  ctx.beginPath();
  ctx.arc(dx, dy, 4 * (window.devicePixelRatio || 1), 0, Math.PI * 2);
  ctx.fill();
  ctx.fillText("D65", dx + 7, dy + 14);

  if (targetPoint) {
    const [tx, ty] = toPx(canvas, targetPoint.x, targetPoint.y);
    ctx.strokeStyle = "#111";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.arc(tx, ty, 9 * (window.devicePixelRatio || 1), 0, Math.PI * 2);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(tx - 12, ty);
    ctx.lineTo(tx + 12, ty);
    ctx.moveTo(tx, ty - 12);
    ctx.lineTo(tx, ty + 12);
    ctx.stroke();
  }
}

function drawEnv(row) {
  const canvas = $("env");
  fit(canvas);
  const ctx = canvas.getContext("2d");
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const points = data.results.filter((r) => r.mode === mode && r.power);
  const maxPower = Math.max(...points.map((r) => r.power)) * 1.05;
  const sx = (x) => (Math.log(x) / Math.log(maxPower)) * (canvas.width - 54) + 38;
  const sy = (y) => canvas.height - 24 - (y / 1.02) * (canvas.height - 42);
  ctx.strokeStyle = "#d8dee6";
  for (let y = 0.2; y <= 1; y += 0.2) {
    ctx.beginPath();
    ctx.moveTo(34, sy(y));
    ctx.lineTo(canvas.width - 10, sy(y));
    ctx.stroke();
  }
  points.forEach((point) => {
    ctx.fillStyle = point === row ? "#d62828" : "#5b6776";
    ctx.beginPath();
    ctx.arc(sx(point.power), sy(point.coverage), point === row ? 6 : 3, 0, Math.PI * 2);
    ctx.fill();
  });
  ctx.fillStyle = "#53606e";
  ctx.font = `${11 * (window.devicePixelRatio || 1)}px Segoe UI`;
  ctx.fillText("coverage", 8, 14);
  ctx.fillText("power log", canvas.width - 76, canvas.height - 6);
}

function drawMix(row, stats) {
  const canvas = $("mix");
  fit(canvas);
  const ctx = canvas.getContext("2d");
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const points = stats.points;
  const target = targetPoint || { x: data.d65[0], y: data.d65[1] };
  const result = mixForTarget(points, row, target);
  const dpr = window.devicePixelRatio || 1;
  ctx.font = `${12 * dpr}px Segoe UI`;
  ctx.fillStyle = "#53606e";
  ctx.fillText(targetPoint ? `clicked x=${target.x.toFixed(3)} y=${target.y.toFixed(3)}` : "D65 mix preview; click chart for another color", 10 * dpr, 18 * dpr);
  if (!result.mix) {
    ctx.fillStyle = "#b42318";
    ctx.fillText("target is outside selected gamut", 10 * dpr, 42 * dpr);
    return;
  }
  ctx.fillText(`${mode === "real" ? "electric" : "radiant"} power ${result.power.toFixed(2)}x`, 10 * dpr, 40 * dpr);

  const left = 40 * dpr;
  const right = canvas.width - 14 * dpr;
  const bottom = canvas.height - 30 * dpr;
  const top = 56 * dpr;
  const barValues = result.mix.map((value, i) => mode === "real" ? value / sourceEff(row.wavelengths[i]) : value);
  const maxAmount = Math.max(...barValues, 1e-9);
  ctx.strokeStyle = "#d8dee6";
  ctx.beginPath();
  ctx.moveTo(left, top);
  ctx.lineTo(left, bottom);
  ctx.lineTo(right, bottom);
  ctx.stroke();

  points.forEach((point, i) => {
    const x = left + ((point.wl - WL_MIN_JS) / (WL_MAX_JS - WL_MIN_JS)) * (right - left);
    const h = (barValues[i] / maxAmount) * (bottom - top);
    ctx.fillStyle = barValues[i] > 0 ? wavelengthColor(point.wl) : "#9aa4b2";
    ctx.fillRect(x - 5 * dpr, bottom - h, 10 * dpr, h);
    ctx.strokeStyle = "rgba(15,23,42,.55)";
    ctx.strokeRect(x - 5 * dpr, bottom - h, 10 * dpr, h);
    ctx.fillStyle = "#334155";
    ctx.fillText(String(point.wl), x - 12 * dpr, bottom + 16 * dpr);
  });
}

function table(el, cols, rowsHtml) {
  el.innerHTML = `<thead><tr>${cols.map((c) => `<th>${c}</th>`).join("")}</tr></thead><tbody>${rowsHtml.join("")}</tbody>`;
}

function render() {
  const row = pick();
  currentRow = row;
  const stats = customStats(row);
  $("idealBtn").className = mode === "ideal" ? "on" : "";
  $("realBtn").className = mode === "real" ? "on" : "";
  $("nText").textContent = `${row.n} primaries`;
  $("biasText").textContent = `${$("bias").value}% area bias`;
  $("coverage").textContent = `${(100 * stats.coverage).toFixed(1)}%`;
  $("power").textContent = Number.isFinite(stats.power) ? `${stats.power.toFixed(2)}x` : "no D65";
  $("powerLabel").textContent = `${mode === "ideal" ? "radiant" : "electric"} D65 white`;
  $("imagePower").textContent = Number.isFinite(stats.imagePower) ? `${stats.imagePower.toFixed(2)}x` : "no image";
  $("imagePowerLabel").textContent = `typical image; ${(100 * stats.imageCoverage).toFixed(0)}% samples`;
  $("envelopePower").textContent = Number.isFinite(stats.envelopePower) ? `${stats.envelopePower.toFixed(2)}x` : "no grid";
  $("envelopePowerLabel").textContent = `envelope avg; ${(100 * stats.envelopeCoverage).toFixed(0)}% grid`;
  $("reach").textContent = `${(100 * stats.spectralReach).toFixed(1)}%`;
  $("reachLabel").textContent = "spectral reach";
  $("waves").innerHTML = stats.points.map((point) => `<span class="pill">${point.originalWl || point.wl} -> ${point.wl} nm</span>`).join(" ");
  drawCie(row);
  drawEnv(row);
  drawMix(row, stats);

  table($("summary"), ["Mode", "N", "Pick", "nm", "Cover", "Reach", "D65", "Image", "Envelope"], data.summary
    .filter((r) => r.mode === mode)
    .sort(rowOrder)
    .map((r) => {
      const s = customStats(r);
      return `<tr><td>${r.mode}</td><td>${r.n}</td><td>${r.kind}</td><td>${r.wavelengths.join(" ")}</td><td>${(100 * r.coverage).toFixed(1)}%</td><td>${(100 * r.spectralReach).toFixed(1)}%</td><td>${r.power.toFixed(2)}x</td><td>${s.imagePower.toFixed(2)}x</td><td>${s.envelopePower.toFixed(2)}x</td></tr>`;
    }));
  table($("choices"), ["Kind", "nm", "Cover", "Reach", "D65", "Image", "Envelope"], rows()
    .sort((a, b) => objectiveRank(a) - objectiveRank(b) || a.power - b.power)
    .map((r) => {
      const s = customStats(r);
      return `<tr><td>${r.kind}</td><td>${r.wavelengths.join(" ")}</td><td>${(100 * r.coverage).toFixed(1)}%</td><td>${(100 * r.spectralReach).toFixed(1)}%</td><td>${r.power.toFixed(2)}x</td><td>${s.imagePower.toFixed(2)}x</td><td>${s.envelopePower.toFixed(2)}x</td></tr>`;
    }));
  const chosen = new Set(row.wavelengths);
  table($("sources"), ["nm", "source", "WPE", "FWHM", "note"], data.sources
    .filter((s) => chosen.has(s.wavelength) || s.wavelength % 10 === 0)
    .map((s) => `<tr><td>${s.wavelength}</td><td>${s.kind}: ${s.name}</td><td>${(100 * s.efficiency).toFixed(1)}%</td><td>${s.fwhm_nm}</td><td>${s.note}</td></tr>`));
  table($("notes"), ["ID", "source"], data.sourceNotes
    .map((s) => `<tr><td>${s.id}</td><td><a href="${s.url}">${s.text}</a></td></tr>`));
}

$("cie").addEventListener("pointerdown", (event) => {
  if (!currentRow || mode !== "ideal") return;
  const canvas = $("cie");
  const dpr = window.devicePixelRatio || 1;
  let best = null;
  customStats(currentRow).points.forEach((point) => {
    const [x, y] = toPx(canvas, point.x, point.y);
    const dist = Math.hypot(x - event.offsetX * dpr, y - event.offsetY * dpr);
    if (dist < 18 * dpr && (!best || dist < best.dist)) best = { wave: point.originalWl || point.wl, dist };
  });
  if (best) {
    drag = best.wave;
    movedDuringDrag = false;
    $("cie").setPointerCapture(event.pointerId);
  }
});

$("cie").addEventListener("pointermove", (event) => {
  if (!drag) return;
  const point = clampToLocus(fromEvent(event));
  movedDuringDrag = true;
  custom = custom || {};
  custom[drag] = point;
  render();
});

$("cie").addEventListener("pointerup", () => {
  drag = null;
});

$("cie").addEventListener("click", (event) => {
  if (movedDuringDrag) {
    movedDuringDrag = false;
    return;
  }
  const point = fromEvent(event);
  targetPoint = inPoly(point.x, point.y, locus) ? point : clampToLocus(point);
  render();
});

$("idealBtn").onclick = () => {
  mode = "ideal";
  custom = null;
  targetPoint = null;
  render();
};
$("realBtn").onclick = () => {
  mode = "real";
  custom = null;
  targetPoint = null;
  render();
};
["n", "bias"].forEach((id) => $(id).addEventListener("input", () => {
  custom = null;
  render();
}));
$("objective").addEventListener("change", () => {
  objective = $("objective").value;
  custom = null;
  render();
});
window.addEventListener("resize", render);
render();
