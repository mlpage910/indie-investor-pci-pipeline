---
layout: default
title: Notable findings
---

# Notable findings — highlights

The pipeline rests on 47+ individually-validated findings. The most surprising / actionable ones are grouped below. Each links into the [full findings reference](full-findings.html).

## Distribution & population structure

**[E]** The owners-distribution phase transition begins at **15K avg owners, not 50K** — the conventional AA+ line cuts above the real population break.

**[J]** Cohort 1 is **bimodal**: a zero-bucket floor and a niche-with-fans top, with structurally different economics.

**[R]** Per-title owners distributions are **left-skewed in every Cohort 2 band** — at AA+ scale, the top of the catalog stops being the long tail.

## Tag signals that actually predict scale

**[N]** **Great Soundtrack** is the strongest near-AA+ marker in Cohort 1 — a stronger predictor than any gameplay tag.

**[O]** **Turn-Based** is the only tag with strong floor lift in **both cohorts** — a rare cross-tier signal.

**[P]** **Visual Novel** is the most extreme **zero-wall** tag in Cohort 1: heavy concentration, heavy zero-bucket presence, near-zero promotion to higher bands.

**[M]** Niche-with-fans clusters (specific sims, narrative subsets) cluster at the **top** of Cohort 1, not the bottom.

## Band-specific genre fingerprints (Cohort 2)

| Tag cluster | Band it owns |
|---|---|
| Action | 1M+ ([W]) |
| Massively Multiplayer | 1M+ ([X]) — highest-tier-only |
| Vehicle / Party-game | 75K–100K ([Y]) |
| Builder / Educational | 100K–125K ([Z]) |
| Rogue-family / Shoot-'em-up | 125K–150K ([AA]) |
| Strategy / Base-building / Crafting | 150K–175K ([BB]) |
| Open World + Co-op | 500K+ ([CC]) |

## Methodological traps caught by the audit

**[GG]** `release_date` on Steam is the **Steam-listing date**, not the original publish date — re-releases distort age and cohort assignment.

**[LL]** Steam stores Early Access and Free-to-Play in **two different locations** in the data; a single-location filter silently keeps them in. *(This is the trap that took us from 1,610 → 1,551 → 1,210 → 146 the first correct time.)*

**[HH–JJ]** Three port-detection methodologies (tag-based, iOS-first pattern, trademark-clue) feed Stage 6a exclusions.

**[DD]** Adult content lifts **only at the AA+ floor band**, not across the whole AA+ tier — a narrower signal than usually assumed.

## Strategic takeaways

**[OO]** Cohort 2 is **genuinely more diversified** than Cohort 1 (not an artifact of catalog size).

**[PP]** Cohort 1's "concentrated" category is partly a **zero-bucket floor artifact** — read PCI alongside resolvable-title counts.

**[QQ]** PCI mechanically drops with catalog size — interpret with caution at large `n_titles`.

**[RR]** Moderate + concentrated is the investable PCI zone; diversified behaves like a portfolio, one-hit is unrepeatable.

**[TT]** Suspect battery + country inference operate as *triage layers*, not exclusions — annotation, not selection.

---

[→ Full findings reference (A–UU)](full-findings.html)
