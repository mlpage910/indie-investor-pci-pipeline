# indie-investor-pci-pipeline

> **From 140,082 titles by 53,876 developers → 457 titles by 146 developers.**
> A reproducible 11-stage filter chain that turns a raw Steam catalog into a ranked, audited shortlist of indie studios at investable scale.

[![Methodology site](https://img.shields.io/badge/docs-methodology%20site-blue)](https://mlpage910.github.io/indie-investor-pci-pipeline/)
[![Data](https://img.shields.io/badge/data-October%202024%20Steam%20scrape-orange)](https://github.com/NewbieIndieGameDev/steam-insights)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

## The funnel

| Stage | Titles | Developers |
|---|---:|---:|
| **Raw scrape (October 2024)** | **140,082** | **53,876** |
| Hygiene + structural cleanup | 64,320 | 38,524 |
| Cohort assignment (multi-title, non-AAA, active <5y) | — | 6,835 |
| PCI-resolvable (≥2 measurable titles) | — | 1,612 |
| Quality cleanup (port-shops, shovelware, audit R2) | — | 1,551 |
| Moderate + concentrated PCI | — | 1,210 |
| **Final investor candidates** | **457** | **146** |

A **99.7% title-level** and **99.7% developer-level** reduction through 11 calibrated, individually-validated stages. Every threshold is calibrated against a finding (A–UU) in [`findings/locked_findings.md`](findings/locked_findings.md), and the pipeline reconciles to the locked roster identity-for-identity.

> ⚠️ **Data is October 2024 vintage.** The candidate list is a point-in-time snapshot. A new scrape with [steam-insights](https://github.com/NewbieIndieGameDev/steam-insights) is needed to refresh. The pipeline itself is parameterless on dataset — drop new CSVs into `steam-threshold-app/data/` and re-run.

---

## What the pipeline defines at each stage

| Stage | What it defines (positive) | What it filters out |
|---|---|---|
| 0 — Raw load | Full Steam population | — |
| 1 — Hygiene | A *real, shippable, paid* product | Empty metadata, future-dated, paid without price |
| 2 — Structural | Competes in the English Steam market on standard terms | Demos, F2P, non-English, Early Access, no store listing |
| 2b — Activity cohort | A *looser* view used only to measure dormancy (EA + demos restored) | (Same as Stage 2 but keeps EA + demos) |
| 3 — Cohort assignment | A *developer of investable scale*, not dormant (<5y) | Single-title devs, true-AAA studios, dormant devs |
| 4 — PCI | HHI-style concentration of owners share across a dev's catalog | (Computational) |
| 5 — PCI-resolvable | A dev whose PCI is *meaningful* (≥2 measurable-owners titles) | Devs with single-title or all-zero-bucket catalogs |
| 6 — Quality cleanup | Three audit-derived exclusion lists | Port-shops, translators, VN repackagers, shovelware, audit-flagged volume-flippers |
| 7 — Moderate + concentrated | The two PCI categories where investment economics make sense | Diversified (portfolio-like) and one-hit (unrepeatable) studios |
| 8 — Suspect battery | 9-test diagnostic score (annotates, doesn't filter) | (Tag only — `HIGH`, `MEDIUM`, `LOW`, `CLEAR`) |
| 9 — Trajectory | 6 lifecycle labels (annotates) | (Tag only — `RISING`, `ANCHOR_RECENT`, `STEADY`, `ANCHOR_MATURE`, `FALLING`, `ANCHOR_AGING`) |
| 10 — Country | Jurisdiction estimator for **diligence sequencing** (not a quality signal) | (Tag only) |
| 11 — Investor candidates | RISING or ANCHOR_RECENT + CLEAR on suspect battery | Falling, steady, mature, aging; any suspect flag |

---

## The two cohorts

- **Cohort 1 — sub-AA+ multi-title indies.** Multi-game devs (≥2 titles) below AA+ commercial scale. **5,911 → 649 mod+conc → 53 final candidates.**
- **Cohort 2 — AA+ studios below broad-AAA.** Devs at AA+ scale (≥2 titles, avg owners ≥50K) but not broad-AAA. **924 → 561 mod+conc → 93 final candidates.**

Strict-AAA and broad-AAA studios are deliberately out of scope (not the investment target).

### Commercial-tier thresholds

| Tier | Min games | Min avg owners / game | Min max owners |
|---|---:|---:|---:|
| **AA+** | 2 | 50,000 | — |
| **Broad AAA** | 5 | 100,000 | 500,000 |
| **Strict AAA** | 3 | 1,000,000 | 2,000,000 |

All thresholds use the **lower bound** of the owners band (conservative reading).

---

## Notable findings — highlights

The pipeline rests on 47+ individually-validated findings. The most surprising / actionable ones:

### Distribution & population structure
- **[E]** The owners-distribution phase transition begins at **15K avg owners, not 50K** — the conventional AA+ line cuts above the real population break.
- **[J]** Cohort 1 is **bimodal**: a zero-bucket floor and a niche-with-fans top, with structurally different economics.
- **[R]** Per-title owners distributions are **left-skewed in every Cohort 2 band** — at AA+ scale, the top of the catalog stops being the long tail.

### Tag signals that actually predict scale
- **[N]** **Great Soundtrack** is the strongest near-AA+ marker in Cohort 1 — a stronger predictor than any gameplay tag.
- **[O]** **Turn-Based** is the only tag with strong floor lift in **both cohorts** — a rare cross-tier signal.
- **[P]** **Visual Novel** is the most extreme **zero-wall** tag in Cohort 1: heavy concentration, heavy zero-bucket presence, near-zero promotion to higher bands.
- **[M]** Niche-with-fans clusters (specific sims, narrative subsets) cluster at the **top** of Cohort 1, not the bottom.

### Band-specific genre fingerprints (Cohort 2)
- **[W]** **Action** becomes overwhelming at the **1M+** band.
- **[X]** **Massively Multiplayer** over-indexes hard at **1M+** — the highest-tier-only tag in the dataset.
- **[Y]** **Vehicle / Party-game** owns the **75K–100K** band.
- **[Z]** **Builder / Educational** owns **100K–125K**.
- **[AA]** **Rogue-family / Shoot-'em-up** owns **125K–150K**.
- **[BB]** **Strategy / Base-building / Crafting** owns **150K–175K**.
- **[CC]** **Open World + Co-op** define the **500K+** tiers.

### Methodological traps caught by the audit
- **[GG]** `release_date` on Steam is the **Steam-listing date**, not the original publish date — re-releases distort age and cohort assignment.
- **[LL]** Steam stores Early Access and Free-to-Play in **two different locations** in the data; a single-location filter silently keeps them in. *(This is the trap that took us from 1,610 → 1,551 → 1,210 → 146 the first correct time.)*
- **[HH–JJ]** Three port-detection methodologies (tag-based, iOS-first pattern, trademark-clue) feed Stage 6a exclusions.
- **[DD]** Adult content lifts **only at the AA+ floor band**, not across the whole AA+ tier.

### Strategic takeaways
- **[OO]** Cohort 2 is **genuinely more diversified** than Cohort 1 (not an artifact of catalog size).
- **[PP]** Cohort 1's "concentrated" category is partly a **zero-bucket floor artifact** — read PCI alongside resolvable-title counts.
- **[QQ]** PCI mechanically drops with catalog size — interpret with caution at large `n_titles`.
- **[RR]** Moderate + concentrated is the investable PCI zone; diversified behaves like a portfolio, one-hit is unrepeatable.

**Full reference:** every finding (A through UU) is documented in [`findings/locked_findings.md`](findings/locked_findings.md).

---

## Country-of-origin inference — important framing

Country inference is a **triage estimator for diligence sequencing**, not a quality or bias signal. No jurisdiction is treated as better or worse; every candidate that survives Stages 1–11 is a real candidate regardless of inferred country.

The reason jurisdiction matters at all is operational — investment and acquisition diligence is materially different across jurisdictions because of:

- **Regulatory and licensing differences** (ratings regimes, content classification, online-services licensing)
- **IP and contract-law differences** (copyright assignability, work-for-hire, moral rights)
- **Tax structure and treaty differences** (royalty withholding, transfer pricing, R&D credits)
- **Sanctions and export-control exposure**
- **Currency, banking, and payment-rail differences**

A candidate in a jurisdiction with simple, predictable IP and tax treatment is **faster** to put through first-tier diligence — not better, just faster. **This is sequencing, not selection.** All 146 candidates remain on the roster; the country tag only affects review order.

---

## Repository layout

```
indie-investor-pci-pipeline/
├── pipeline/
│   ├── investor_pipeline.py     # 11-stage pipeline, end-to-end
│   └── two_cohorts.py           # Canonical cohort builder
├── steam-threshold-app/         # Streamlit interactive explorer
│   ├── loader.py
│   ├── filters.py
│   ├── app.py
│   └── data/                    # ← put October 2024 CSVs here (not versioned)
├── findings/
│   └── locked_findings.md       # All 47+ findings (A–UU)
├── charts/                      # 45 PNGs (PCI, trajectory, cohort, tag/genre heatmaps)
├── docs/                        # Source for the GitHub Pages methodology site
├── data_fetch/
│   └── README.md                # How to pull the upstream scrape
└── STREAMLIT_DEPLOY.md          # One-click deploy guide for the live app
```

The **146-candidate roster, per-developer profiles, and exclusion lists** are kept in a separate private repo (`indie-investor-pci-pipeline-roster`) because the candidates are an active research workstream, not a finished public artifact.

---

## How to run the pipeline

```bash
# 1. Get the data (October 2024 vintage, ~1.5GB)
cd data_fetch && ./fetch_upstream.sh   # pulls from NewbieIndieGameDev/steam-insights

# 2. Run the full pipeline
python pipeline/investor_pipeline.py \
    --data steam-threshold-app/data \
    --out  pipeline_run

# 3. Inspect the reconciliation table
cat pipeline_run/pipeline_summary.csv

# 4. Optional — run the interactive explorer
streamlit run steam-threshold-app/app.py
```

The pipeline prints a stage-by-stage reconciliation table on every run, including which stages match the locked targets and which drift.

---

## Acknowledgments

Raw Steam scrape: **[NewbieIndieGameDev/steam-insights](https://github.com/NewbieIndieGameDev/steam-insights)**. This project is downstream analysis on that public dataset.

---

## License

MIT. See [LICENSE](LICENSE).
