# Wavelength Primary Optimizer

Interactive CIE 1931 primary wavelength optimizer.

This started from a Bluesky question:

> "what is the minimum number of pure wavelength lasers to cover most of the area ... extreme ends of spectrum will not cut it ... very blue/red is awful and it will require immense power"

Source: https://bsky.app/profile/tussles-shriek.bsky.social/post/3mp3smstlro24

## What it does

The tool searches for sets of spectral primaries that cover a large part of the CIE 1931 chromaticity diagram without wasting huge power at wavelengths where the eye is weak.

It lets you compare:

- ideal 1 nm monochrome sources
- rough real-source estimates with broad spectra and wall-plug efficiency
- gamut area
- power to make D65 white
- average power for a small typical-image color sample set
- spectral reach from source bandwidth

## Why area alone is not enough

A triangle can cover a large part of the chart while still being terrible for white or normal images. If D65 white falls in a bad triangle, the solver may need a deep red or deep blue primary. Those wavelengths have poor luminous efficiency, so radiant power can explode.

That is why the app shows separate metrics instead of one "best" score.

## Controls

- `Ideal radiant`: treat each source as a perfect 1 nm spectral line.
- `Real source`: use rough real-world source efficiency and bandwidth estimates.
- `Optimize for`: choose whether the picked set should prefer gamut, D65 white power, typical image power, or a balanced mix.
- `Primary count`: choose how many primaries are allowed.
- `Gamut vs power`: steer the Pareto choice toward area or efficiency.

In ideal mode, the red points can be dragged inside the CIE locus. The app recomputes gamut area, D65 power, typical-image power, and approximate wavelength labels.

## Caveats

The real-source model is an estimate, not a parts database. Real LEDs, lasers, and phosphors vary by vendor, drive current, temperature, optics, binning, and bandwidth. Phosphor sources are broad and cannot be treated as true 1 nm primaries.

The typical-image score is a simple fixed sample set, not a measured image corpus.

## Data

The optimizer uses CIE 1931 2 degree color matching functions and photopic luminous efficiency data from CIE tables included in this repo.
