---
title: "Findings — Highlights"
permalink: /findings/
---

# Findings — Highlights

<p class="lead">The pipeline rests on 47+ individually validated findings (A–UU). The most surprising or actionable ones are organized here by theme. Every entry links into the <a href="full-findings.html">full findings reference</a>.</p>

## Distribution & population structure

<div class="finding-card">
  <span class="finding-key">[E]</span>
  The owners-distribution phase transition begins at <strong>15K avg owners, not 50K</strong>. The conventional AA+ line cuts above the real population break in the data.
</div>

<div class="finding-card">
  <span class="finding-key">[J]</span>
  Cohort 1 is <strong>bimodal</strong>: a zero-bucket floor and a niche-with-fans top, with structurally different economics. Treating C1 as homogeneous misreads it.
</div>

<div class="finding-card">
  <span class="finding-key">[R]</span>
  Per-title owners distributions are <strong>left-skewed in every Cohort 2 band</strong>. At AA+ scale, the top of the catalog stops being the long tail.
</div>

## Tag signals that actually predict scale

<div class="finding-card">
  <span class="finding-key">[N]</span>
  <strong>Great Soundtrack</strong> is the strongest near-AA+ marker in Cohort 1 — a stronger predictor than any gameplay tag.
</div>

<div class="finding-card">
  <span class="finding-key">[O]</span>
  <strong>Turn-Based</strong> is the only tag with strong floor lift in <em>both</em> cohorts. A rare cross-tier signal.
</div>

<div class="finding-card">
  <span class="finding-key">[P]</span>
  <strong>Visual Novel</strong> is the most extreme <strong>zero-wall</strong> tag in Cohort 1: heavy concentration, heavy zero-bucket presence, near-zero promotion to higher bands.
</div>

<div class="finding-card">
  <span class="finding-key">[M]</span>
  Niche-with-fans clusters (specific sims, narrative subsets) cluster at the <em>top</em> of Cohort 1, not the bottom.
</div>

## Band-specific genre fingerprints (Cohort 2)

| Cluster | Band it owns | Finding |
|---|---|:---:|
| Action | 1M+ | [W] |
| Massively Multiplayer | 1M+ (highest-tier-only) | [X] |
| Vehicle / Party-game | 75K–100K | [Y] |
| Builder / Educational | 100K–125K | [Z] |
| Rogue-family / Shoot-'em-up | 125K–150K | [AA] |
| Strategy / Base-building / Crafting | 150K–175K | [BB] |
| Open World + Co-op | 500K+ | [CC] |

## Methodological traps caught by the audit

<div class="finding-card">
  <span class="finding-key">[GG]</span>
  <code>release_date</code> on Steam is the <strong>Steam-listing date</strong>, not the original publish date. Re-releases distort age and cohort assignment.
</div>

<div class="finding-card">
  <span class="finding-key">[LL]</span>
  Steam stores Early Access and Free-to-Play in <strong>two different locations</strong> in the data; a single-location filter silently keeps them in.
  <em>This is the trap that took us from 1,610 → 1,551 → 1,210 → 146 the first correct time.</em>
</div>

<div class="finding-card">
  <span class="finding-key">[HH–JJ]</span>
  Three port-detection methodologies — tag-based, iOS-first pattern, trademark-clue — feed Stage 6a exclusions.
</div>

<div class="finding-card">
  <span class="finding-key">[DD]</span>
  Adult content lifts <strong>only at the AA+ floor band</strong>, not across the whole AA+ tier. A narrower signal than usually assumed.
</div>

## Strategic takeaways

<div class="finding-card">
  <span class="finding-key">[OO]</span>
  Cohort 2 is <strong>genuinely more diversified</strong> than Cohort 1, not an artifact of catalog size.
</div>

<div class="finding-card">
  <span class="finding-key">[PP]</span>
  Cohort 1's "concentrated" category is partly a <strong>zero-bucket floor artifact</strong>. Read PCI alongside resolvable-title counts.
</div>

<div class="finding-card">
  <span class="finding-key">[QQ]</span>
  PCI mechanically drops with catalog size. Interpret with caution at large <code>n_titles</code>.
</div>

<div class="finding-card">
  <span class="finding-key">[RR]</span>
  Moderate + concentrated is the investable PCI zone. Diversified behaves like a portfolio; one-hit is unrepeatable.
</div>

<div class="finding-card">
  <span class="finding-key">[TT]</span>
  Suspect battery and country inference operate as <em>triage layers</em>, not exclusions — annotation, not selection.
</div>

---

[→ Full findings reference (A–UU)](full-findings.html)
