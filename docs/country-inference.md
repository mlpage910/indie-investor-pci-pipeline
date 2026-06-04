---
title: "Country Inference — Framing"
permalink: /country-inference/
---

# Country-of-Origin Inference

<p class="lead">A triage estimator for diligence sequencing, not a quality or bias signal. No jurisdiction is treated as better or worse than another in the scoring.</p>

<div class="callout">
  <strong>This is sequencing, not selection.</strong> Every candidate that survives Stages 1–11 stays on the roster regardless of inferred country. The country tag only affects which candidates get reviewed in which order.
</div>

## Why jurisdiction is tracked at all (operational reasons only)

Investment and acquisition diligence is materially different across jurisdictions because of:

- **Regulatory and licensing differences** — game-ratings regimes, content classification, online-services licensing, app-store-style content gates
- **IP and contract-law differences** — assignability of copyright in employment agreements, work-for-hire treatment, moral-rights regimes, enforceability of standard buyout clauses
- **Tax structure and treaty differences** — withholding on royalties, transfer pricing, R&D incentive credits, capital-gains treatment on share sales
- **Sanctions and export-control exposure** — additional screening requirements; deal timelines and structures differ accordingly
- **Currency, banking, and payment-rail differences** — escrow availability, closing mechanics, cross-border settlement

A candidate in a jurisdiction with simple, predictable IP and tax treatment is *faster* to put through first-tier diligence — not better, just faster. A candidate flagged into a more complex jurisdictional bucket needs specialist counsel before the same depth of diligence can be completed, so they are routed differently in the work queue.

## Inference method

Country is not in the dataset. It is inferred from two conservative signals:

1. **Publisher-name suffixes** — UG/GmbH → Germany, S.r.l. → Italy, Sp. z o.o. → Poland, Co.,Ltd → Japan/Asia, etc.
2. **Steam language footprint** — developer ships a single non-English language dominantly on ≥70% of titles **AND** ships ≤2 dominant languages total. Developers that ship 8+ localizations are tagged "Global-localizer" because shipping a language as a localization tells you nothing about origin.

The second clause is critical — it is what keeps the inference from biasing on localization patterns rather than origin.

## Distribution of inferred signals

| Country signal | C1 | C2 | Total |
|---|---:|---:|---:|
| EN-default (no signal) | 426 | 224 | 650 |
| Global-localizer (3+ languages, no origin signal) | 200 | 360 | 560 |
| China (lang dominant + narrow footprint) | 68 | 44 | 112 |
| Russia/CIS (lang or personal name) | 64 | 21 | 85 |
| Japan (lang or Co.,Ltd) | 29 + 5 | 16 + 2 | 52 |
| Germany (UG/GmbH or lang) | 14 | 19 | 33 |
| Other (France, Brazil, UK, Italy, Poland, Turkey, Korea) | ≤16 each | — | — |

**78% of the roster lands in one of the two "Unknown" buckets** (EN-default + Global-localizer). The inference is intentionally conservative — when in doubt, no signal is fired.

## Cohort-level observation

Cohort 2 is dominated by global-localizers (51% of C2 vs 24% of C1). At AA+ scale, developers ship 4–8 localizations as a matter of course; at sub-AA+ scale, English-only or narrow-localization shipping is the norm. This is consistent with the broader cohort difference: C2 represents commercially-scaled studios that can afford full localization budgets.
