# Steam Threshold Calibration (v1)

A small Streamlit app for finding noise-removal thresholds that make the Steam
marketplace legible enough to study discovery and traction patterns.

## What this is (and isn't)

- **Is:** a calibration workbench. Sliders set filters, graphs show what survives,
  a normality test on the Findings tab tells you when a filter combination has
  produced a well-behaved response distribution worth recording.
- **Isn't:** a shovelware classifier, a predictive model, or a polished public
  product. v1 is for the researcher, not the end user.

## Three filter layers (kept strictly separate)

1. **Data hygiene** — drop rows with missing/invalid fields (no release date,
   no SteamSpy band, paid title with no price, future-dated release, etc.).
2. **Structural exclusions** — drop populations that follow different rules
   (demos, free-to-play). Justified by Steam's own [demo docs](https://partner.steamgames.com/doc/store/application/demos).
3. **Analytical thresholds** — the actual research object: minimum owners band,
   minimum concurrent users, release-age window, price band, developer output,
   genre stratifier. These are the knobs you calibrate.

## Why `owners_range` is the primary anchor

Review counts conflate adoption with willingness-to-review. SteamSpy's owners
band is a revealed-acquisition signal — a player actually owns the title. We
treat it as ordinal (14 bands) and sweep cutoffs to find natural elbows rather
than committing to one number.

## Data

Source: [NewbieIndieGameDev/steam-insights](https://github.com/NewbieIndieGameDev/steam-insights)
(October 2024 scrape). Place these four CSVs in `data/`:

- `games.csv`
- `steamspy_insights.csv`
- `genres.csv`
- `tags.csv`

Files are gitignored — fetch them locally.

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Project layout

```
loader.py    # DuckDB → pandas, derived columns, owners-band ordering
filters.py   # Pure filter functions (hygiene / structural / analytical)
app.py       # Streamlit UI: sidebar filters + 5 tabs
data/        # CSVs (gitignored)
findings.log # JSONL of saved filter snapshots (gitignored)
```

## Tabs

1. **Survival curve** — population remaining as the owners-band cutoff tightens.
2. **Distribution profile** — histograms of owners, price, age, concurrent users
   for the filtered cohort.
3. **Threshold sweep** — how median / mean / IQR / skew of a chosen response
   variable shift across cutoffs. Stable moments across a band = robust threshold.
4. **Cohort table** — surviving titles, exportable to CSV.
5. **Findings** — Shapiro–Wilk + D'Agostino K² normality tests and a Q–Q plot
   on the current filtered cohort. When a filter combination produces a
   near-normal distribution, save the snapshot to `findings.log`.

## Roadmap (post-v1)

- Drop in scrape #2 → re-run the same filter snapshots → A/B stability test
  (Kolmogorov–Smirnov on response distributions, rank correlation on overlapping
  titles).
- Adapter for Kindle / self-publishing data: same filter-layer architecture,
  swap the loader. Acquisition anchor becomes sales-rank decay; reviews stay
  as conditional response.
