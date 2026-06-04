---
title: "Findings — Highlights"
permalink: /findings/
---

# Findings — Highlights

<p class="lead">The pipeline rests on 47+ individually validated findings (A–VV). The most surprising or actionable ones are organized here by theme, each grounded in a chart. Every entry links into the <a href="{{ '/full-findings/' | relative_url }}">full findings reference</a>.</p>

<figure class="chart">
  <img src="{{ '/assets/charts/investor_candidates_map.png' | relative_url }}" alt="Map of 146 final investor candidates by inferred country">
  <figcaption>
    <span class="chart-title">Final 146 investor candidates, by inferred jurisdiction</span>
    <strong>Headline</strong> 53,876 developers shipping on Steam → 146 candidates after the full 11-stage funnel. Country tags are a diligence-sequencing aid (regulatory, IP, tax, banking) — not a selection filter. ~78% land in "Unknown" by design.
  </figcaption>
</figure>

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

<figure class="chart">
  <img src="{{ '/assets/charts/cohort1_5k_bands_overview.png' | relative_url }}" alt="Cohort 1 5K-band overview showing bimodal distribution">
  <figcaption>
    <span class="chart-title">Cohort 1 — 5K-band carve [Finding E, J]</span>
    <strong>Bimodality is visible at the band level.</strong> Catalogs cluster near the zero-bucket floor and around the niche-with-fans top — not as a smooth power law. The "moderate indie" interior is genuinely thin, which justifies treating C1 as two populations.
  </figcaption>
</figure>

<figure class="chart">
  <img src="{{ '/assets/charts/cohort2_10k_bands_shape.png' | relative_url }}" alt="Cohort 2 distribution shape per band">
  <figcaption>
    <span class="chart-title">Cohort 2 — distribution shape across 10K bands [Finding R]</span>
    <strong>Left-skew in every band.</strong> At AA+ scale, a studio's top title is no longer the long tail — it sits at or above the band's median. This inverts the indie-tier intuition and is what makes Cohort 2 candidates structurally different from Cohort 1 candidates.
  </figcaption>
</figure>

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

<figure class="chart">
  <img src="{{ '/assets/charts/cohort1_tag_x_band_heatmap.png' | relative_url }}" alt="Cohort 1 tag-by-band lift heatmap">
  <figcaption>
    <span class="chart-title">Cohort 1 — tag × band lift heatmap [Findings M–P]</span>
    <strong>Where each tag concentrates.</strong> Great Soundtrack lifts strongly at the top bands; Visual Novel pins to the bottom; Turn-Based lifts across multiple bands — the rare cross-tier signal. Reading this heatmap is how the pipeline decides which tags warrant separate cohort treatment.
  </figcaption>
</figure>

<figure class="chart">
  <img src="{{ '/assets/charts/visual_novel_cohorts.png' | relative_url }}" alt="Visual novels behave differently in both cohorts">
  <figcaption>
    <span class="chart-title">Visual Novel zero-wall [Finding P]</span>
    <strong>Most extreme zero-bucket tag in C1.</strong> VN titles concentrate at the floor and show near-zero promotion into higher bands. This is what motivates VN-aware port-shop detection (HH–JJ) and the moderate-indie tag trend work (MM).
  </figcaption>
</figure>

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

<figure class="chart">
  <img src="{{ '/assets/charts/cohort2_genre_x_band_heatmap.png' | relative_url }}" alt="Cohort 2 genre by band lift heatmap">
  <figcaption>
    <span class="chart-title">Cohort 2 — genre × band lift heatmap [Findings W–CC]</span>
    <strong>Each band has a different genre signature.</strong> Action and Massively Multiplayer dominate the 1M+ tier; builder/educational anchors mid-bands; strategy/crafting anchors the 150K–175K interior. This is the structure the moderate+concentrated filter exploits when sequencing diligence by band.
  </figcaption>
</figure>

## Moderate-indie investigation (Cohort 1 5K band)

<figure class="chart">
  <img src="{{ '/assets/charts/moderate_indie_pool_size.png' | relative_url }}" alt="Moderate indie pool size after EA/F2P fix">
  <figcaption>
    <span class="chart-title">Moderate-indie pool size after the EA/F2P trap fix [Finding LL]</span>
    <strong>The dual-location trap shrinks the pool ~17%.</strong> A single-location EA/F2P filter silently keeps Early Access and Free-to-Play titles in. Applying the structural filter through the same path the app uses removes them and shifts every downstream count — this is the trap that took us to 1,331 devs, not 1,610.
  </figcaption>
</figure>

<figure class="chart">
  <img src="{{ '/assets/charts/moderate_indie_tag_trends.png' | relative_url }}" alt="Tag trend lines across moderate-indie bands">
  <figcaption>
    <span class="chart-title">Per-tag trend across moderate-indie bands [Finding MM]</span>
    <strong>Each tag has a directional shape.</strong> Some tags rise monotonically with band (real scale signal); others plateau or invert (saturated or zero-wall). Reading the slope, not the point estimate, is how moderate-indie tag signals get separated from noise.
  </figcaption>
</figure>

## Portfolio Concentration Index (PCI)

<figure class="chart">
  <img src="{{ '/assets/charts/pci_distribution_both_cohorts.png' | relative_url }}" alt="PCI distributions for both cohorts">
  <figcaption>
    <span class="chart-title">PCI distribution — both cohorts [Findings NN, OO]</span>
    <strong>Cohort 2 is genuinely more diversified than Cohort 1.</strong> The HHI-style concentration index falls right-shifted (concentrated) in C1 and left-shifted (diversified) in C2 — and the gap survives the catalog-size correction (QQ), making it a real cohort-level difference, not a measurement artifact.
  </figcaption>
</figure>

<figure class="chart">
  <img src="{{ '/assets/charts/pci_category_mix.png' | relative_url }}" alt="PCI category mix">
  <figcaption>
    <span class="chart-title">PCI category mix — diversified / moderate / concentrated / one-hit [Finding RR]</span>
    <strong>Moderate + concentrated is the investable zone.</strong> Diversified studios behave like portfolios (no signal to act on); one-hit studios are unrepeatable; the middle two categories are where a coherent studio thesis can exist. Filtering to these two is what turns 1,612 PCI-resolvable devs into 1,210.
  </figcaption>
</figure>

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

<div class="finding-card" style="border-left:3px solid var(--accent);background:#fbf6ed">
  <span class="finding-key">[VV]</span>
  <strong>Cohort 2 diversified + CLEAR is a separate research category</strong> — not lower-quality than the 146 roster, just a different shape. <strong>83 AA+ studios</strong> (4A Games, Tango Gameworks, SUPERHOT Team, Wolfire, Spiderweb Software, Revolution Software, Artifex Mundi, etc.) that the main pipeline drops at Stage 7 only because owners spread across many titles. The right starting point for <em>multi-IP acquirer theses</em>, <em>catalog roll-ups</em>, and <em>back-catalog cash-flow plays</em>. Future research needs a portfolio-appropriate momentum metric before any of the 83 can move to a candidate roster.
</div>

<figure class="chart">
  <img src="{{ '/assets/charts/trajectory_distribution.png' | relative_url }}" alt="Trajectory label distribution">
  <figcaption>
    <span class="chart-title">Trajectory labels — RISING and ANCHOR_RECENT carry the 146 [Finding TT]</span>
    <strong>The final gate is momentum.</strong> Of the 1,210 moderate+concentrated devs that pass the suspect battery, only those tagged RISING (82) or ANCHOR_RECENT (64) are kept — 146 in total. Falling, steady, mature, and aging studios are out of scope for active investment, by design.
  </figcaption>
</figure>

---

[→ Full findings reference (A–VV)]({{ '/full-findings/' | relative_url }})
