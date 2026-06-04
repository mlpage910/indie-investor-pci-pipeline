---
title: "Methodology"
permalink: /methodology/
---

# Methodology

<p class="lead">How the 11-stage filter chain is constructed, why each gate exists, and what each design decision is calibrated against. The <a href="{{ '/' | relative_url }}">Funnel</a> tab shows the stage counts; this page documents the reasoning behind them.</p>

<div class="callout">
  <strong>Reading order.</strong> §1 explains the data and the four questions the pipeline answers. §2 walks each stage in order, with the design choice and the finding(s) that justify it. §3 covers the audit work (port detection, suspect battery, country triage). §4 documents the known limitations the work does <em>not</em> resolve.
</div>

## 1. Design

### 1.1 Data source and vintage

The pipeline runs on a public Steam catalog snapshot from [NewbieIndieGameDev/steam-insights](https://github.com/NewbieIndieGameDev/steam-insights), dated **October 2024**. The snapshot contains ~140,082 store rows (titles, demos, software, Early Access, free-to-play, and paid) with owners banded (Steam never publishes exact owners), review counts, prices, release dates, languages, genres, tags, and publisher/developer strings.

Two characteristics of this data drive the entire design:

1. **Owners are banded, not continuous.** A title with "20K–50K owners" has a lower bound of 20,000 and an upper bound of 50,000. Every owners threshold in this pipeline uses the **lower bound** — the conservative reading. This means our AA+ floor of 50,000 avg owners is actually "lower-bound 50K," which is more stringent than it sounds.
2. **`release_date` is the Steam-listing date, not the original publish date** (Finding GG). Re-released games appear young; ports of decades-old IP appear as fresh launches. This is the single largest source of cohort-assignment noise and is the reason Stage 3 measures activity on a looser cohort than the structural one.

### 1.2 What the pipeline is trying to identify

The pipeline is built around four sequential questions:

| # | Question | Answered by |
|---|---|---|
| 1 | Is this a real, commercially-shipping product? | Stages 1–2 (hygiene + structural) |
| 2 | Is the developer at a scale and lifecycle where investment makes sense? | Stage 3 (cohort assignment) |
| 3 | Is their catalog focused enough to read as a coherent studio rather than a portfolio shop? | Stages 4–7 (PCI, resolvability, quality cleanup, mod+conc) |
| 4 | Are they moving in the right direction right now? | Stages 8–11 (suspect battery, trajectory, country triage, final candidates) |

Each question gates the next. A studio passing Question 2 but failing Question 3 (a port shop, a translator, a VN repackager) is excluded before the trajectory work even runs. This is a funnel of **conjunctions** — every gate must pass — not a union or a weighted score.

### 1.3 Why a deterministic filter chain rather than a model

We are not building a yield-curve forecaster or a "predict the next hit" classifier. We are building a **screening rule** that an analyst could in principle defend in writing. Every threshold maps to a finding (A–UU) and every exclusion list is documented. The output of a model run with hyperparameters is not the right artifact for an investment-screening process; the output of a documented filter chain is.

The trade-off is that the pipeline is **not adaptive**. It cannot learn from new data without thresholds being re-calibrated against the findings. That is intentional — the calibration step is a deliberate, auditable analyst action, not an opaque retraining loop.

## 2. Stages in order

### 2.1 Stages 1–2 — Hygiene and structural

The structural cohort is the answer to "is this a real, commercially-shipping product on the same terms as the rest of the paid Steam catalog?" It applies five filters in conjunction:

- **Paid.** Free-to-play is a fundamentally different business model — owners count does not mean what it means for paid titles. Cut.
- **English store listing.** Non-English-only listings are a small share of the catalog and behave anomalously in the owners distribution. Excluded to keep the comparison clean; this is not a quality judgment.
- **Not a demo.** Demos appear in the catalog but are not shipped products.
- **Not Steam Early Access.** EA titles can be commercially active but report owners that anticipate full release; their inclusion distorts the per-band shape. Kept for the activity cohort only (see 2.3).
- **Has a store listing.** Some catalog rows have no actual store page (delisted or never-launched). Cut.

**The dual-location trap (Finding LL).** Steam stores Early Access and Free-to-Play flags in **two different locations** in the data — once as a top-level flag and once buried inside the genres array (`"Free to Play"` and `"Early Access"` as genre tags). A single-location filter silently keeps both populations in. This is the trap that took the project through three pool-size revisions before landing at 1,331 moderate-indie devs the first correct time. The pipeline routes the structural filter through the same code path the calibration app uses, which checks both locations.

**Output: 64,320 titles** survive the structural filter (down from 140,082).

### 2.2 Stage 3 — Cohort assignment

The structural pool is split into three commercial tiers by per-dev aggregates, using the **lower-bound** owners value of each title:

| Tier | Min games | Min avg owners / game | Min max owners |
|---|---:|---:|---:|
| **AA+** | 2 | 50,000 | — |
| **Broad AAA** | 5 | 100,000 | 500,000 |
| **Strict AAA** | 3 | 1,000,000 | 2,000,000 |

From these, two cohorts are defined:

- **Cohort 1 (C1):** `multi & NOT aa_plus` — multi-title devs below AA+. The moderate-indie and emerging-studio universe. 5,911 devs.
- **Cohort 2 (C2):** `aa_plus & NOT broad_aaa` — AA+ studios below broad-AAA. The proven-commercial studio universe just below the AAA line. 924 devs.

**Strict-AAA and broad-AAA devs are deliberately excluded from both cohorts.** They are not the investment target. The pipeline is built for indie + AA+ acquirers, funders, and operators — not for studios looking to buy Bethesda.

**Why two cohorts and not one.** Findings J (C1 bimodality) and R (C2 left-skew in every band) showed that the two populations have **structurally different per-title owners shapes**. Pooling them would produce thresholds that fit neither group well. Treating them as separate cohorts means each set of band-level findings (E–P for C1, Q–CC for C2) can be calibrated independently.

**Why 50,000 avg owners and not 15,000.** Finding E showed the population's natural break starts at 15K. The pipeline uses **50K** anyway because (a) the question is "what is investable AA+?" not "where is the statistical kink?" and (b) the conservative reading on the lower bound (which is already the floor of a band) gives the AA+ definition real economic content. The 15K finding is preserved as a band-carve threshold inside C1, not as the AA+ line.

### 2.3 Activity measured on a *looser* cohort

This is the single most important non-obvious detail in the entire pipeline. **Dormancy** is measured on a separate `stage12_activity` cohort with `exclude_early_access=False, exclude_demos=False`. A dev who is still shipping EA content or demos counts as non-dormant even if their last paid release is older than 5 years.

The strict structural cohort would drop these devs entirely; the activity cohort lets them re-enter. Without this two-cohort trick the pipeline loses meaningful EA-active studios at Stage 3. The 5-year dormancy threshold is conservative; we tested 3 and 7 and the candidate set is stable across that range.

### 2.4 Stages 4–5 — PCI and PCI-resolvability

The **Portfolio Concentration Index (PCI)** is a Herfindahl-Hirschman-style index applied to a developer's catalog, weighting each title by its lower-bound owners share. A dev whose entire owners base comes from one title has PCI ≈ 1; a dev whose owners are spread evenly across many titles has PCI ≈ 1/n.

```
PCI(dev) = Σᵢ (owners_lower_i / Σⱼ owners_lower_j)²
```

**Restricting PCI to cohort devs.** PCI is computed only for the ~6,835 cohort devs, not for all 60K+ structural-pool devs. Including non-cohort devs would dilute the categorical mix and produce a misleading population-wide distribution. This is a correctness fix, not just a performance optimization.

**PCI-resolvability (Stage 5).** A dev's PCI is **meaningful** only if at least two of their titles have measurable owners (`owners_lower > 0`). Catalogs entirely in the zero-bucket read as "concentrated" by default — they have one or zero titles contributing to the index, so the result is mechanically high. The resolvability filter cuts 6,835 → 1,612 devs and removes the largest source of PCI artifact (Finding PP, the C1 zero-bucket floor effect).

**PCI mechanically drops with catalog size (Finding QQ).** A studio with 20 titles cannot easily score above 0.35 — there are simply too many denominator terms. PCI should always be read alongside `n_titles`; the moderate+concentrated band (Stage 7) is calibrated knowing this.

### 2.5 Stage 6 — Three audit-derived exclusion lists

After resolvability, three exclusion lists are applied in order:

- **6a — Port shops, translators, and VN repackagers.** Studios whose "catalog" is mostly other people's IP localized or ported. Their PCI looks like a studio's PCI but their economic identity is a service business. Detected by three converging methodologies: tag-based (Findings HH, JJ), iOS-first pattern (II), and trademark-clue (publisher strings ending in "Games" + suspicious title overlap with mobile catalogs).
- **6b — Round 1 shovelware.** A first-pass audit list built during the moderate-indie investigation. High-volume, low-engagement studios where >70% of the catalog sits in the zero bucket with zero reviews.
- **6c — Round 2 high-volume / low-engagement.** A targeted second-pass audit caught studios that pass 6a and 6b on tags but still show the structural pattern (median title age <12 months, median review count <5).

**Output: 1,612 → 1,551 devs.** The 61 removed devs are not edge cases; they are systematically catalog-as-distribution-business operators that the rest of the pipeline cannot distinguish from real studios on aggregate metrics alone.

### 2.6 Stage 7 — Moderate + concentrated

Of the four PCI categories — **diversified** (PCI < 0.35), **moderate** (0.35–0.65), **concentrated** (0.65–0.85), and **one-hit** (≥ 0.85) — only the middle two are retained:

- **Diversified** behaves like a portfolio, not a studio. There is no single thesis an investor can underwrite; the company is implicitly a fund.
- **One-hit** is unrepeatable. A studio whose entire owners base is one title is a single-asset bet, not a studio investment.
- **Moderate and concentrated** are the categories where a coherent studio-level thesis can exist: there is a hit (the anchor), there is supporting work (the catalog), and the relationship between the two is the investable structure.

**Output: 1,551 → 1,210 devs (649 C1 + 561 C2).**

### 2.7 Stage 8 — Suspect battery

A 9-test diagnostic that **annotates without filtering**. Each test contributes a flag; the aggregate is one of `CLEAR`, `LOW`, `MEDIUM`, `HIGH` suspect. The nine tests:

1. **Cadence anomaly** — release intervals are too uniform or too spiky for a real studio.
2. **Engagement collapse** — review-to-owners ratio falls off a cliff in recent titles.
3. **Dollar-store pricing** — entire catalog priced at the platform floor.
4. **Owners floor** — catalog floors at the lowest measurable band.
5. **Zero-review share** — high share of titles with zero reviews.
6. **Playtime collapse** — median playtime per owner is implausibly low.
7. **Uniform mediocrity** — every title scores between 60% and 70% review positive; suspiciously flat.
8. **Single-publisher factory** — publisher field is identical across most titles, suggesting a sub-label of a larger operator.
9. **Genre scattershot** — genre distribution has no coherent center.

The output (`HIGH`/`MEDIUM`/`LOW`/`CLEAR`) is **a tag, not a cut**, until the final stage. This lets analysts inspect why a studio is flagged before any exclusion is made.

### 2.8 Stage 9 — Trajectory

Each dev is assigned one of six trajectory labels based on anchor-title share, anchor age, and the late-vs-early-half owners split:

- **RISING** — owners are growing, anchor is recent, supporting catalog is contributing.
- **ANCHOR_RECENT** — the anchor is the dominant story but it is recent (< 24 months).
- **STEADY** — flat owners profile, no strong direction.
- **ANCHOR_MATURE** — the anchor is the dominant story and is 2–5 years old.
- **FALLING** — owners are declining; late half is less than the early half.
- **ANCHOR_AGING** — the anchor is the dominant story and is ≥ 5 years old.

### 2.9 Stage 10 — Country inference (triage, not bias)

A conservative estimator infers likely jurisdiction from two signals:

- **Publisher-name suffix.** "GmbH" → DE, "Pty Ltd" → AU, "S.A.S." → FR, etc. About 40+ suffix mappings, all unambiguous.
- **Steam-language dominance.** Titles published exclusively in one language (Russian-only, Japanese-only, Korean-only, Polish-only) get a soft regional tag.

When the two signals disagree, the dev is tagged **Unknown**. Roughly **78% of the mod+conc pool lands in Unknown by design** — this is conservative inference, not a confident classification.

**Why this exists.** The framing is explicit on the [Country Inference]({{ '/country-inference/' | relative_url }}) page: this is a **diligence-sequencing layer**, not a selection filter. Regulatory regimes, IP ownership conventions, corporate-tax treatment, sanctions exposure, and banking infrastructure all differ meaningfully by jurisdiction. A diligence team has finite first-week capacity; the country tag lets the team sequence the queue so the simplest jurisdictions get cleared first while the more complex ones are scheduled with the right counsel attached. **Triage, not bias.**

### 2.10 Stage 11 — Final candidate gate

A dev becomes a final investor candidate if and only if **all four** are true:

1. In C1 or C2 (Stage 3).
2. Moderate or concentrated PCI (Stage 7).
3. `CLEAR` on the suspect battery (Stage 8).
4. `RISING` or `ANCHOR_RECENT` on trajectory (Stage 9).

**Output: 146 developers (53 C1 + 93 C2), spanning 457 titles.** Of the 146, 82 are `RISING` and 64 are `ANCHOR_RECENT`. The country tag does not gate; it sequences.

## 3. Audit subsystems

### 3.1 Port-shop detection (HH–KK)

The work to identify port shops, translators, and VN repackagers is documented as Findings HH–KK in [Full Findings]({{ '/full-findings/' | relative_url }}). Three converging methodologies:

- **HH — Tag-based.** Catalogs whose tag mix is "Visual Novel + Anime + Adventure + Story Rich" with no original-game tags and no English-only-original publisher chain.
- **II — iOS-first pattern.** Steam release date is recent but `first_release_date` in metadata (when available) shows a 5+ year gap and the title's owners base on iOS/Android dwarfs Steam.
- **JJ — Trademark-clue.** Publisher chain ends in a generic LLC or "Games" suffix but every title in the catalog is a known IP from a different rights-holder.

These are case-study findings (not chart findings); the resulting exclusion list feeds Stage 6a.

### 3.2 The moderate-indie EA/F2P trap (LL)

Documented at length in Finding LL. The structural filter was originally applied to the top-level EA and F2P flags only. The second location — EA and F2P appearing **inside the genres array** — was silently keeping these titles in. Routing the structural filter through the calibration app's code path (which checks both locations) shrinks the moderate-indie pool from 1,610 → 1,331 the first correct time and shifts every downstream count.

The pipeline now uses the app's filter as the single source of truth, and the `investor_pipeline.py` script reproduces the canonical 146 deterministically. This is what Finding UU documents.

### 3.3 The suspect battery interpretation

The suspect battery is the most interpretive component of the pipeline and the one most likely to need re-tuning against future data. Two design choices worth flagging:

- **Composite, not single-test.** No single test is a knockout. A `HIGH` flag requires several signals to converge, which makes the rate of false positives empirically low (manual inspection of `HIGH` flags during development confirmed ~85% true positive rate on the sample we hand-audited).
- **Annotation throughout the pipeline.** The battery runs at Stage 8 but its outputs are visible everywhere downstream. Analysts can read `MEDIUM` flags as "look here second" and `LOW` as "look here third"; the `CLEAR` requirement at Stage 11 means the final 146 are the studios that passed all nine tests.

## 4. What this work does *not* do

These limitations are real and important. The pipeline is a screening tool, not a complete diligence stack.

1. **No financial data.** Steam does not publish revenue. Owners × price is a sales-equivalent estimate at best; refunds, sales discounts, and platform cuts are not modeled. Any "revenue" framing downstream of this pipeline must be marked as a sales-equivalent estimate.
2. **No private-sale/key-reseller leakage.** Direct-to-consumer Steam-key sales (Humble, Fanatical, indie store packages) bypass the on-Steam owners count. Studios with heavy off-Steam distribution will read smaller than they are.
3. **No console or mobile owners.** A studio that sells 90% of its units on console will look tiny in this data. The pipeline is **Steam-only** by design and should be paired with platform-mix evidence before any acquisition discussion.
4. **No timing of releases beyond `release_date`.** Re-releases distort age (Finding GG). The pipeline mitigates this with the looser activity cohort and the trajectory layer, but a deep historical re-release (a 2003 game re-listed in 2022) will appear as a 2022 launch and may slot into the wrong trajectory bucket.
5. **Country inference is conservative on purpose.** The 78% Unknown share is a feature, not a bug — but it does mean that geography-specific deal questions (export controls, country-specific tax structures) cannot be answered from this output alone.
6. **Single-snapshot vintage.** All findings are calibrated to the October 2024 scrape. The pipeline is rerunnable on any future scrape, but the thresholds may need re-calibration if Steam's banding scheme, owner-counting method, or genre taxonomy changes materially.
7. **No qualitative studio-stage signal.** The pipeline does not know whether a studio is fundraising, distressed, growing the team, or contemplating an exit. Those are signals only the diligence layer that follows can introduce.

## 5. References & further reading

- **The full filter chain** — [Funnel]({{ '/' | relative_url }})
- **Top-level findings** — [Findings — Highlights]({{ '/findings/' | relative_url }})
- **Every locked finding with chart appendix** — [Full Findings (A–UU)]({{ '/full-findings/' | relative_url }})
- **Pipeline reproducibility against locked roster** — [Reproducibility]({{ '/reproducibility/' | relative_url }})
- **Country triage framing in detail** — [Country Inference]({{ '/country-inference/' | relative_url }})
- **Upstream Steam data** — [NewbieIndieGameDev/steam-insights](https://github.com/NewbieIndieGameDev/steam-insights)
