# Wavelength Primary Optimizer

> **Disclaimer:** this is a quick modelling exercise made with Codex. It has had only basic sanity checks, not a careful color-science review. Do not use it for engineering, medical, safety, purchasing, display design, lighting design, or any other real decision. It is meant only as a toy to build some intuition about CIE color models, spectral primaries, eye sensitivity, and power trade-offs.

Interactive CIE 1931 primary wavelength optimizer.

Working site: https://cepera-ang.github.io/wavelength-opt/

This started from a Bluesky question:

> "what is the minimum number of pure wavelength lasers to cover most of the area ... extreme ends of spectrum will not cut it ... very blue/red is awful and it will require immense power"

Source: https://bsky.app/profile/tussles-shriek.bsky.social/post/3mp3smstlro24

## Color basics

### CIE 1931 chromaticity chart

![CIE 1931 chromaticity diagram](https://commons.wikimedia.org/wiki/Special:FilePath/CIExy1931.svg)

The CIE 1931 xy chart is a 2D map of visible color chromaticity. It ignores brightness and keeps only color direction. The curved outer edge is the spectral locus: pure single-wavelength light. The straight bottom edge is the line of purples, which cannot be made by one wavelength alone.

If you pick light sources as primaries, mixtures of those primaries land inside the polygon formed by their points. Three primaries make a triangle. More primaries make a larger polygon. This is why the app draws red polygons over the CIE chart.

Authoritative data source used here: [CIE 1931 colour-matching functions, 2 degree observer](https://cie.co.at/datatable/cie-1931-colour-matching-functions-2-degree-observer).

### Eye and retina sensitivity

![Human cone fundamentals](https://commons.wikimedia.org/wiki/Special:FilePath/Cone-fundamentals-with-srgb-spectrum.svg)

Human daylight color vision comes mostly from three cone classes: S, M, and L cones. They are often loosely called blue, green, and red cones, but their response curves are broad and overlap a lot.

The eye is much less sensitive at the deep blue and deep red ends of the visible spectrum. That means a primary near an extreme wavelength can be great for gamut area but bad for lumens per watt. A display or light engine may need a lot of radiant power there to produce the same perceived brightness.

Useful references:

- [CVRL cone fundamentals](https://www.cvrl.org/cones.htm)
- [CIE spectral luminous efficiency for photopic vision](https://cie.co.at/datatable/cie-spectral-luminous-efficiency-photopic-vision)
- [IES definition of CIE photopic luminous efficiency V(lambda)](https://ies.org/definitions/cie-photopic-luminous-efficiency-function/)

### Primaries and power

A primary is one source color used for mixing. In the ideal mode, a primary is a perfect 1 nm spectral line. In real-source mode, it is a rough model of available lasers, LEDs, or phosphor-converted sources.

Large gamut is not the same as low power. A set of primaries can cover a lot of area but still be inefficient if important colors, especially D65 white, require a weak deep-red or deep-blue source. The app therefore shows area, D65 white power, typical-image power, and spectral reach as separate numbers.

## What it does

The tool searches for sets of spectral primaries that cover a large part of the CIE 1931 chromaticity diagram without wasting huge power at wavelengths where the eye is weak.

It lets you compare:

- ideal 1 nm monochrome sources
- rough real-source estimates with broad spectra and wall-plug efficiency
- gamut area
- power to make D65 white
- average power for a small typical-image color sample set
- average power over a coarse grid inside the selected gamut envelope
- spectral reach from source bandwidth

## Why area alone is not enough

A triangle can cover a large part of the chart while still being terrible for white or normal images. If D65 white falls in a bad triangle, the solver may need a deep red or deep blue primary. Those wavelengths have poor luminous efficiency, so radiant power can explode.

That is why the app shows separate metrics instead of one "best" score.

The `envelope average power` objective tries to catch a different failure mode: a large polygon can hide a whole expensive corner where every clicked color is forced through one weak extreme primary. For each candidate set it samples a coarse grid of points inside the source polygon, solves the cheapest 3-primary mix for each point, and scores the Pareto trade-off between gamut area and average `log(power + 1)`. The raw average power is still shown as a metric, but the optimizer uses the log cost so one deep-red or deep-blue edge does not dominate the whole choice.

## Controls

- `Ideal radiant`: treat each source as a perfect 1 nm spectral line.
- `Real source`: use rough real-world source efficiency and bandwidth estimates.
- `Optimize for`: choose whether the picked set should prefer gamut, D65 white power, typical image power, envelope-average power, or a balanced mix.
- `Primary count`: choose how many primaries are allowed.
- `Gamut vs power`: steer the Pareto choice toward area or efficiency.

In ideal mode, the red points can be dragged inside the CIE locus. The app recomputes gamut area, D65 power, typical-image power, and approximate wavelength labels.

## Caveats

The real-source model is an estimate, not a parts database. Real LEDs, lasers, and phosphors vary by vendor, drive current, temperature, optics, binning, and bandwidth. Phosphor, OLED, and quantum-dot sources are broad and cannot be treated as true 1 nm primaries.

The current real-source model was revised from the notes in [`docs/`](docs/) and uses rough visible-band anchors: Nichia-class UV-A/violet LEDs, efficient blue InGaN LEDs/lasers, a 527 nm high-WPE green LED peak, broad phosphor/OLED/QD estimates through yellow-orange, and high-efficiency 640/660 nm red horticulture LEDs. These are deliberately approximate; the app is for intuition, not part selection.

The typical-image score is a simple fixed sample set, not a measured image corpus.

## Data

The optimizer uses CIE 1931 2 degree color matching functions and photopic luminous efficiency data from CIE tables included in this repo.

`optimize_full_real.py` caches expensive triple scans as local `triples_*.npz` files and prints progress bars. Those cache files are ignored by git because they are hundreds of MB. Use `uv run --with numpy --with tqdm python optimize_full_real.py --workers 8` to rebuild with multiple worker processes when a cache is stale.
