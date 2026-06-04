# Data fetch — October 2024 Steam scrape

The pipeline expects six CSVs in `steam-threshold-app/data/`:

- `games.csv`
- `genres.csv`
- `categories.csv`
- `tags.csv`
- `steamspy_insights.csv`
- `reviews.csv`

These come from **[NewbieIndieGameDev/steam-insights](https://github.com/NewbieIndieGameDev/steam-insights)**, the public Steam scrape this project is downstream of.

## Why we don't commit the data

- The full scrape is ~1.5 GB
- The upstream repo is the canonical source and is updated periodically
- Pinning to a specific commit is cleaner than freezing CSVs in our repo

## Fetch (one of three options)

### Option 1 — git submodule (recommended)

```bash
git submodule add https://github.com/NewbieIndieGameDev/steam-insights \
    steam-threshold-app/data/upstream
ln -sf upstream/games.csv  steam-threshold-app/data/games.csv
ln -sf upstream/genres.csv steam-threshold-app/data/genres.csv
# ... repeat for the other CSVs
```

### Option 2 — direct download

```bash
cd steam-threshold-app/data
for f in games genres categories tags steamspy_insights reviews; do
  curl -L -o ${f}.csv \
    https://raw.githubusercontent.com/NewbieIndieGameDev/steam-insights/main/${f}.csv
done
```

### Option 3 — pin to the October 2024 commit

The locked roster in this repo was built on a specific October 2024 snapshot of `steam-insights`. To reproduce the 146-candidate roster identity-for-identity, pin to that commit:

```bash
git clone https://github.com/NewbieIndieGameDev/steam-insights /tmp/steam-insights
cd /tmp/steam-insights
git checkout <commit-sha-for-Oct-2024>   # see SCRAPE_PIN.md when published
cp *.csv /path/to/this/repo/steam-threshold-app/data/
```

## Refreshing for a new analysis

The pipeline is **parameterless on dataset** — drop newer CSVs into `steam-threshold-app/data/` and re-run:

```bash
python pipeline/investor_pipeline.py --data steam-threshold-app/data --out pipeline_run_fresh
```

All thresholds (AA+ at 50K, broad-AAA at 100K/500K, dormancy at 5 years, PCI bins, suspect-battery cutoffs) are constants in `pipeline/investor_pipeline.py` — change them in one place if calibration needs updating.
