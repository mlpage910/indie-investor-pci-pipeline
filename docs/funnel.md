---
layout: default
title: Funnel & filter catalog
---

# The funnel

| Stage | Titles | Developers |
|---|---:|---:|
| Raw scrape (October 2024) | **140,082** | **53,876** |
| Hygiene + structural cleanup | 64,320 | 38,524 |
| Cohort assignment (multi-title, non-AAA, active <5y) | — | 6,835 |
| PCI-resolvable (≥2 measurable titles) | — | 1,612 |
| Quality cleanup (port-shops, shovelware, audit R2) | — | 1,551 |
| Moderate + concentrated PCI | — | 1,210 |
| **Final investor candidates** | **457** | **146** |

A **99.7% title-level** and **99.7% developer-level** reduction.

## What the pipeline defines at each stage

| Stage | What it defines (positive) | What it filters out |
|---|---|---|
| **0 — Raw load** | Full Steam population | — |
| **1 — Hygiene** | A *real, shippable, paid* product | Empty metadata, future-dated, paid without price |
| **2 — Structural** | Competes in the English Steam market on standard terms | Demos, F2P, non-English, Early Access, no store listing |
| **2b — Activity cohort** | A *looser* view used only to measure dormancy | (Same as Stage 2 but keeps EA + demos) |
| **3 — Cohort assignment** | A *developer of investable scale*, not dormant (<5y) | Single-title devs, true-AAA studios, dormant devs |
| **4 — PCI** | HHI-style concentration of owners share across a dev's catalog | (Computational) |
| **5 — PCI-resolvable** | A dev whose PCI is *meaningful* (≥2 measurable-owners titles) | Single-title or all-zero-bucket catalogs |
| **6 — Quality cleanup** | Three audit-derived exclusion lists | Port-shops, translators, VN repackagers, shovelware, audit-flagged volume-flippers |
| **7 — Moderate + concentrated** | The two PCI categories where investment economics make sense | Diversified (portfolio-like) and one-hit (unrepeatable) studios |
| **8 — Suspect battery** | 9-test diagnostic score (annotates, doesn't filter) | (Tag only) |
| **9 — Trajectory** | 6 lifecycle labels (annotates) | (Tag only) |
| **10 — Country** | Jurisdiction estimator for **diligence sequencing** | (Tag only) |
| **11 — Investor candidates** | RISING or ANCHOR_RECENT + CLEAR on suspect battery | Falling, steady, mature, aging; any suspect flag |

## The two cohorts

**Cohort 1 — sub-AA+ multi-title indies.** `multi & NOT aa_plus`. **5,911 → 649 mod+conc → 53 final candidates.**

**Cohort 2 — AA+ studios below broad-AAA.** `aa_plus & NOT broad_aaa`. **924 → 561 mod+conc → 93 final candidates.**

Strict-AAA and broad-AAA studios are deliberately out of scope.

### Commercial-tier thresholds

| Tier | Min games | Min avg owners / game | Min max owners |
|---|---:|---:|---:|
| AA+ | 2 | 50,000 | — |
| Broad AAA | 5 | 100,000 | 500,000 |
| Strict AAA | 3 | 1,000,000 | 2,000,000 |

All thresholds use the **lower bound** of the owners band.
