---
title: "Reproducibility"
permalink: /reproducibility/
---

# Reproducibility & the Locked Roster

<p class="lead">The pipeline is a single runnable module that reproduces the locked 146-developer candidate roster from a raw Steam dataset directory. Every locked checkpoint from Stage 6 onward matches exactly.</p>

## Reconciliation against the locked roster

| Stage | Actual | Target | Δ | Status |
|---|---:|---:|---:|---|
| 0 — Raw load | 140,082 | 140,082 | +0 | **MATCH** |
| 1-2 — Hygiene + Structural (strict) | 64,320 | 64,320 | +0 | **MATCH** |
| 1-2b — Activity cohort (looser) | 71,529 | — | — | — |
| 3 — Cohorts post-dormancy | 6,835 | 6,833 | +2 | CLOSE |
| 3 · Cohort 1 | 5,911 | 5,911 | +0 | **MATCH** |
| 3 · Cohort 2 | 924 | 924 | +0 | **MATCH** |
| 5 — PCI-resolvable | 1,612 | 1,610 | +2 | CLOSE |
| 6 — After exclusions | **1,551** | **1,551** | **+0** | **MATCH** |
| 7 — Moderate + concentrated | **1,210** | **1,210** | **+0** | **MATCH** |
| 7 · C1 mod+conc | 649 | — | — | — |
| 7 · C2 mod+conc | 561 | — | — | — |
| 11 — Final candidates | **146** | **146** | **+0** | **MATCH** |
| 11 · C1 / C2 split | 53 / 93 | 53 / 93 | +0 | MATCH |
| 11 · RISING / ANCHOR_RECENT | 82 / 64 | 82 / 64 | +0 | MATCH |

All 146 developer identities match the locked roster one-for-one.

## The two +2 deltas

Stage 3 picks up two extra Cohort 1 developers due to cleaner NaN handling on the dormancy join. Those two propagate to Stage 5. They are absorbed at Stage 6a (37 dropped vs locked 35). Net effect: zero impact on Stage 6 (1,551), Stage 7 (1,210), or Stage 11 (146).

## Canonical thresholds

```python
STRICT_AAA    = dict(min_games=3, min_avg_owners=1_000_000, min_max_owners=2_000_000)
BROAD_AAA     = dict(min_games=5, min_avg_owners=100_000,   min_max_owners=500_000)
AA_PLUS       = dict(min_games=2, min_avg_owners=50_000)
DORMANT_YEARS = 5.0
REF_DATE      = pd.Timestamp("2024-10-28")
```

## Cohort logic

```python
c1_mask = agg['multi'] & ~agg['aa_plus']       # sub-AA+ multi-title
c2_mask = agg['aa_plus'] & ~agg['broad_aaa']   # AA+ excluding broad-AAA
```

## The single most important non-obvious detail

Activity (dormancy) is measured on a **looser** cohort with EA + demos restored (`stage12_activity`). This lets a developer who is still shipping EA or demo content count as non-dormant even if their last paid release is older than 5 years.

Measuring dormancy on the strict cohort would silently drop a meaningful number of legitimate-but-EA-only developers.

## Running it yourself

```bash
python pipeline/investor_pipeline.py \
    --data steam-threshold-app/data \
    --out  pipeline_run
```

Output files:

- `pipeline_run/investor_candidates.csv` — final 146 with scores
- `pipeline_run/all_moderate_concentrated_scored.csv` — full 1,210 with annotations
- `pipeline_run/cohorts_full.csv` — 6,835 cohorted developers
- `pipeline_run/pci_resolvable.csv` — 1,612 PCI-resolvable developers
- `pipeline_run/pipeline_summary.csv` — the reconciliation table

The pipeline prints a stage-by-stage reconciliation table on every run.
