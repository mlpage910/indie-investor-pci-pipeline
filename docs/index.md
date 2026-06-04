---
title: "Funnel"
---

# The Funnel

<p class="lead">A reproducible 11-stage filter chain that turns a raw Steam catalog into a ranked, audited shortlist of indie studios at investable scale. This page shows <em>what</em> the funnel produces and at <em>what counts</em>; the <a href="{{ '/methodology/' | relative_url }}">Methodology</a> tab covers <em>how and why</em> each stage is constructed.</p>

<div class="funnel-hero">
  <p class="funnel-numbers">
    From <span class="num">140,082</span> titles by <span class="num">53,876</span> developers
    <span class="arrow">→</span>
    <span class="num">457</span> titles by <span class="num">146</span> developers.
  </p>
  <p class="funnel-caption">
    A 99.7% title-level and 99.7% developer-level reduction through 11 calibrated stages, every threshold tied to a validated finding (A&ndash;UU).
  </p>
</div>

<div class="callout">
  <strong>Data is October 2024 vintage.</strong> The candidate roster is a point-in-time snapshot and is kept in a private companion repo. A new scrape with <a href="https://github.com/NewbieIndieGameDev/steam-insights">steam-insights</a> is needed to refresh.
</div>

<figure class="chart">
  <img src="{{ '/assets/charts/investor_candidates_map.png' | relative_url }}" alt="Final 146 investor candidates by inferred country">
  <figcaption>
    <span class="chart-title">The pipeline output — 146 candidates, by inferred jurisdiction</span>
    <strong>What the funnel produces.</strong> 146 developers across 457 titles. Country tags are a diligence-sequencing aid (regulatory, IP, tax, banking), not a selection filter. About 78% land in an Unknown bucket by design.
  </figcaption>
</figure>

## Stage-by-stage funnel

| Stage | Titles | Developers |
|---|---:|---:|
| Raw scrape (October 2024) | **140,082** | **53,876** |
| Hygiene + structural cleanup | 64,320 | 38,524 |
| Cohort assignment (multi-title, non-AAA, active &lt;5y) | — | 6,835 |
| PCI-resolvable (≥2 measurable titles) | — | 1,612 |
| Quality cleanup (port-shops, shovelware, audit R2) | — | 1,551 |
| Moderate + concentrated PCI | — | 1,210 |
| **Final investor candidates** | **457** | **146** |

## Filter catalog — what each stage defines

| Stage | What it defines (positive) | What it filters out |
|---|---|---|
| **0** — Raw load | Full Steam population | — |
| **1** — Hygiene | A *real, shippable, paid* product | Empty metadata, future-dated, paid without price |
| **2** — Structural | Competes in the English Steam market on standard terms | Demos, F2P, non-English, Early Access, no store listing |
| **2b** — Activity cohort | A *looser* view used only to measure dormancy | (Same as Stage 2 but keeps EA + demos) |
| **3** — Cohort assignment | A *developer of investable scale*, not dormant (&lt;5y) | Single-title devs, true-AAA studios, dormant devs |
| **4** — PCI | HHI-style concentration of owners share across a dev's catalog | (Computational) |
| **5** — PCI-resolvable | A dev whose PCI is *meaningful* (≥2 measurable-owners titles) | Single-title or all-zero-bucket catalogs |
| **6** — Quality cleanup | Three audit-derived exclusion lists | Port-shops, translators, VN repackagers, shovelware, audit-flagged volume-flippers |
| **7** — Moderate + concentrated | The two PCI categories where investment economics make sense | Diversified (portfolio-like), one-hit (unrepeatable) |
| **8** — Suspect battery | 9-test diagnostic score (annotates, doesn't filter) | (Tag only) |
| **9** — Trajectory | 6 lifecycle labels (annotates) | (Tag only) |
| **10** — Country | Jurisdiction estimator for **diligence sequencing** | (Tag only) |
| **11** — Investor candidates | RISING or ANCHOR\_RECENT + CLEAR on suspect battery | Falling, steady, mature, aging; any suspect flag |

## The two cohorts

<div class="stat-grid">
  <div class="stat-card">
    <p class="stat-label">Cohort 1 · sub-AA+</p>
    <p class="stat-value">5,911 → 53</p>
    <p class="stat-sub">Multi-title indies below AA+. <code>multi & NOT aa_plus</code></p>
  </div>
  <div class="stat-card">
    <p class="stat-label">Cohort 2 · AA+ &lt; AAA</p>
    <p class="stat-value">924 → 93</p>
    <p class="stat-sub">AA+ studios below broad-AAA. <code>aa_plus & NOT broad_aaa</code></p>
  </div>
  <div class="stat-card">
    <p class="stat-label">Excluded by design</p>
    <p class="stat-value">Broad &amp; strict AAA</p>
    <p class="stat-sub">Not the investment target — out of scope.</p>
  </div>
</div>

### Commercial-tier thresholds

| Tier | Min games | Min avg owners / game | Min max owners |
|---|---:|---:|---:|
| AA+ | 2 | 50,000 | — |
| Broad AAA | 5 | 100,000 | 500,000 |
| Strict AAA | 3 | 1,000,000 | 2,000,000 |

All thresholds use the **lower bound** of the owners band — the conservative reading.

## Why this construction

The pipeline answers four questions in sequence, each gating the next:

1. **Is this a real, commercially-shipping product?** (Stages 1–2)
2. **Is the developer at a scale and lifecycle where investment makes sense?** (Stage 3)
3. **Is their catalog focused enough to read as a coherent studio rather than a portfolio shop?** (Stages 4–7)
4. **Are they moving in the right direction right now?** (Stages 8–11)

The pipeline is a **funnel of conjunctions, not a union**. A candidate must satisfy every gate: real product → investable scale → not dormant → focused catalog → not flagged → moving up. Each gate is calibrated against the locked findings (A–UU); the 146 figure is the natural population that survives all of them, not a target that was tuned for.

## Running the pipeline

```bash
# 1. Fetch the upstream Steam scrape (October 2024 vintage)
cd data_fetch && ./fetch_upstream.sh

# 2. Run the full pipeline
python pipeline/investor_pipeline.py \
    --data steam-threshold-app/data \
    --out  pipeline_run

# 3. Read the reconciliation table
cat pipeline_run/pipeline_summary.csv
```

The pipeline prints a stage-by-stage reconciliation table on every run and saves four CSVs: the final candidates, the full mod+conc scored set, the cohort table, and the PCI-resolvable set. See [Reproducibility]({{ '/reproducibility/' | relative_url }}) for the locked-roster comparison.

<figure class="chart">
  <img src="{{ '/assets/charts/pci_distribution_both_cohorts.png' | relative_url }}" alt="PCI distribution for both cohorts">
  <figcaption>
    <span class="chart-title">PCI is the core mechanism — both cohorts shown</span>
    <strong>Why the funnel narrows where it does.</strong> The Portfolio Concentration Index (HHI-style on owners share) splits each cohort into diversified / moderate / concentrated / one-hit. Cohort 2 is genuinely more diversified than Cohort 1, and the moderate+concentrated zone is the investable PCI region. See <a href="{{ '/findings/' | relative_url }}">Findings</a> for the full reasoning.
  </figcaption>
</figure>
