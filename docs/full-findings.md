---
layout: default
title: Full findings reference
---

# Steam Investor-Candidate Pipeline — Locked Findings & Filter Catalog

All findings measured on the structural cohort (hygiene + English store listing + paid + no demos + no Steam Early Access). "EA" throughout means Steam Early Access, not Electronic Arts.

---

## Executive summary — what the pipeline does and what each filter defines

The pipeline takes a raw Steam catalog (~140K rows) and produces a ranked, audited shortlist of **146 acquisition-or-investment candidates**. It does this through 11 stages that progressively answer four questions: **(1) is this a real, commercially-shipping product? (2) is the developer at a scale and lifecycle where investment makes sense? (3) is their catalog focused enough to read as a coherent studio rather than a portfolio shop? (4) are they moving in the right direction right now?**

### Filter catalog — what each stage defines

| Stage | What it defines | What it filters out | Output count |
|---|---|---|---:|
| **0 — Raw load** | The full Steam population | — | 140,082 |
| **1 — Hygiene** | A *real, shippable, paid* product (has dev, publisher, release date, owners band, and a price if paid) | Empty metadata rows, unreleased / future-dated rows, paid titles missing price | (combined with Stage 2) |
| **2 — Structural** | A product that competes in the English Steam market on the same terms as the rest of the catalog (paid, English store page, not a demo, not Early Access, not Free-to-Play) | Demos, F2P, non-English-only titles, Early Access titles, titles with no store listing | 64,320 titles |
| **2b — Activity cohort** | A *looser* view used only to measure dormancy (EA + demos restored). Lets a dev who is still shipping EA content count as active even if their last paid release is old. | (Same as Stage 2 but keeps EA + demos) | 71,529 titles |
| **3 — Cohort assignment** | A *developer of investable scale* on one of two tiers, who is still active (latest release < 5y). Excludes the AAA tier as out-of-scope. | Single-title devs, true-AAA studios, dormant devs (≥5y since latest release) | 6,835 devs (5,911 C1 + 924 C2) |
| **4 — PCI** | The Herfindahl-style concentration of a dev's catalog by owners share. Tells us whether owners are spread across many titles or piled on one hit. | (Computational, no filtering) | 3,248 devs with owners > 0 |
| **5 — PCI-resolvable** | A dev whose PCI is *meaningful* — at least 2 of their titles have measurable owners (>0 lower bound) | Devs whose entire catalog is in the 0-bucket, or who only have one measurable title | 1,612 devs |
| **6 — Quality cleanup** | Three audit-derived exclusion lists removed: (6a) port-shops / translators / VN repackagers, (6b) Round-1 shovelware, (6c) Round-2 high-volume low-engagement audit | Studios whose catalogs look concentrated only because they don't ship their own IP | **1,551 devs** |
| **7 — Moderate + concentrated** | The two PCI categories where investment economics make sense: a dev with 35%–85% of owners in their top title. Diversified studios behave like portfolios; one-hit studios are unrepeatable. | Diversified (PCI < 0.35) and one-hit (PCI ≥ 0.85) studios | 1,210 devs (649 C1 + 561 C2) |
| **8 — Suspect battery** | A 9-test diagnostic score (cadence, engagement collapse, dollar-store pricing, owners floor, zero-review share, playtime collapse, uniform mediocrity, single-publisher factory, genre scattershot). Annotates, does not filter. | (Annotation only — flags `HIGH`, `MEDIUM`, `LOW`, `CLEAR`) | 1,210 scored |
| **9 — Trajectory** | One of 6 lifecycle labels based on anchor-title share, anchor age, and late-vs-early-half owners. | (Annotation only — `RISING`, `ANCHOR_RECENT`, `STEADY`, `ANCHOR_MATURE`, `FALLING`, `ANCHOR_AGING`) | 1,210 classified |
| **10 — Country** | A *triage estimator* for likely jurisdiction, inferred from publisher-name suffixes + Steam-language dominance. **Not a bias signal** — used to sort which candidates go to first-tier diligence first because regulatory, IP, tax, and deal-structure complexity vary by jurisdiction. Conservative: 78% land in an "Unknown" bucket. | (Annotation only) | 1,210 tagged |
| **11 — Investor candidates** | A developer who is **(a)** in C1 or C2 at investable scale, **(b)** focused (moderate/concentrated PCI), **(c)** clean on the suspect battery, and **(d)** showing positive momentum (RISING or ANCHOR_RECENT). | Falling, steady, mature, aging trajectories; anyone flagged on the suspect battery | **146 devs** (53 C1 + 93 C2) |

### What the two cohorts mean

- **Cohort 1 (C1) — sub-AA+ multi-title indies.** Multi-game devs (≥2 titles) who have *not* reached AA+ commercial scale. Definition: `multi & NOT aa_plus`. The moderate-indie and emerging-studio universe. **5,911 devs at cohort assignment → 649 in final mod+conc pool → 53 final candidates.**
- **Cohort 2 (C2) — AA+ studios below broad-AAA.** Devs who have hit AA+ scale (≥2 titles with avg owners ≥ 50K) but are *not* broad-AAA (broad-AAA = ≥5 titles, avg owners ≥ 100K, max owners ≥ 500K). The proven-commercial-studio universe just below the AAA line. **924 devs at cohort assignment → 561 in final mod+conc pool → 93 final candidates.**
- **Strict-AAA and broad-AAA tier devs are deliberately excluded from both cohorts** — they are not the investment target.

### The three commercial-tier thresholds (canonical, from `two_cohorts.py`)

| Tier | Min games | Min avg owners / game | Min max owners |
|---|---:|---:|---:|
| **AA+** | 2 | 50,000 | — |
| **Broad AAA** | 5 | 100,000 | 500,000 |
| **Strict AAA** | 3 | 1,000,000 | 2,000,000 |

All thresholds use the **lower bound** of the owners band (`owners_lower`), not the midpoint — this is the conservative reading.

### Why the final 146 is small but high-signal

The pipeline is deliberately a *funnel of conjunctions*, not a union. A candidate must satisfy every gate: real product → investable scale → not dormant → focused catalog → not flagged → moving up. Each gate is calibrated against the locked findings below (A–TT). The 146 figure is the natural population that survives all of them — not a target that was tuned for.

---

## Game-level findings

**A — Internal Consistency Rule (game-level symmetry)**
- Filter: `owners_lower ≥ total_reviews` AND `total_reviews ≥ 1`
- n = 17,422 games
- log10(total_reviews): skew = +0.006, kurt = −0.24
- Plain language: requiring lower-bound owners to be at least as large as review count produces a near-perfectly symmetric log distribution. This is the cleanest "real games with engaged audiences" filter we found.

**B — Floored Internal Consistency Rule (mesokurtic)**
- Filter: same as A plus `total_reviews ≥ 8`
- n = 15,694 games
- log10(total_reviews): skew = +0.338, kurt = +0.017
- Plain language: an 8-review floor gives near-normal tail behavior on top of the consistency rule.

## Developer-level findings

**C — Broad AAA tier is statistically a real population**
- Definition: ≥5 games AND avg_owners_per_game ≥ 100K AND max_owners_lower ≥ 500K
- n = 182 studios (or 161 on Cohort B data)
- log10(avg_reviews_per_game) per dev: skew = +0.145, kurt = 0.000
- Plain language: at this scale, studios form a well-formed statistical population — they are a real "class," not noise.

**D — Established & still active AA+ benchmark**
- 70 studios, career ≥10y, last release < 2y, AA+ tier (avg owners ≥ 50K, ≥2 games)
- Examples: Tango Gameworks, Freebird Games, Hopoo Games, Mossmouth
- Plain language: the working benchmark for "old guard but still kicking" at AA+ scale.

## Phase-transition findings (Cohort 1 5K-band carve)

**E — Distribution-shape phase transition begins at 15K avg owners, not 50K**
- In Cohort 1 (sub-AA+, multi-release, non-dormant), the per-title owners distribution flips from positive-skew zero-wall to symmetric/negative-skew between the 10K–15K and 15K–20K avg-owners bands.
- Median per-title owners flips 0 → 20K at the C1-04 (15K–20K) band.
- Distribution skew flips from +0.43 (C1-03) to −0.05 (C1-04).
- Plain language: the AA+ shape starts emerging at avg ≥ 15K. The 50K threshold is the visible end of a longer transition, not its starting point.

**F — Pre/Post-transition split of Cohort 1**
- Pre-transition: C1-Z through C1-03 (avg ≤ 15K) → 5,064 devs (85.7% of Cohort 1)
- Post-transition: C1-04 through C1-10 (avg > 15K, < 50K) → 847 devs (14.3% of Cohort 1)
- Within post-transition, the AA+ curve shape (negative skew, platykurtic) is already established despite still being labeled "Cohort 1."

**G — C1-10 (45K–<50K) is structurally AA+ near-miss**
- 27 devs, 14.8% established active rate (vs 0.1% in C1-Z, vs 7.8% in Cohort 2 baseline)
- Their per-title distribution shape matches Cohort 2 patterns.
- Plain language: indistinguishable from AA+ on every shape metric except the strict 50K threshold.

**H — Established-active rate climbs monotonically with band**
- C1-Z: 0.1% → C1-03: 5.2% → C1-08: 8.3% → C1-09: 9.4% → C1-10: 14.8%
- The single best predictor of 10+ year sub-AA+ survival is reaching even modest avg-owners ground (≥15K).
- Plain language: passing the visibility floor is what makes long-term survival possible at this scale.

**I — Up-and-coming is heavily Zero-band-dominated**
- 1,474 of 1,869 Cohort 1 up-and-coming devs (78.9%) sit in C1-Z.
- A more credible up-and-coming watchlist requires avg > 0 — i.e., at least one game registered a bucket.
- Plain language: the "up-and-coming" label is misleading without owner-band qualification.

**J — Bimodal population structure inside Cohort 1**
- 82.7% of Cohort 1 devs sit in bands C1-Z, C1-01, and C1-02 (avg ≤ 10K).
- The remaining 17.3% spreads thinly across the 10K-50K range.
- Plain language: Cohort 1 is really two populations stitched together — a massive zero/near-zero base and a thin upper tail.

## Genre-shift findings (within Cohort 1 bands)

**K — Genre mix shifts as bands climb**
- Casual: 25% (Zero) → 13% (Sub-AA) — over-represented at the bottom
- Action: ~26% steady across all bands
- Adventure: 15% (Zero) → 22% (Sub-AA) — climbs with band
- Strategy: grows with band, especially established-active share
- RPG: lowest Zero share of major genres (40%), broadest tail
- Niche-genre concentration: Gore (40.6%), Violent (35.6%), Nudity (55.6%) cluster in C1-02 (5K–10K)

## Tag-overindex findings (within Cohort 1 bands)

**L — Adult content concentrates at the floor**
- NSFW (1.63×), Mature (1.45×), Hentai (1.45×), Nudity (1.44×), Sexual Content (1.42×), Dating Sim (1.38×), Romance (1.35×) all over-indexed in C1-Z.
- Plain language: adult-content tagging is heavily associated with games that never crossed the visibility floor.

**M — Niche-with-fans clusters at the top of Cohort 1**
- C1-10 (45K–<50K, the AA+ doorstep) is most over-indexed on: Great Soundtrack (6.43×), Difficult (3.24×), Sci-fi (2.44×), Comedy (2.12×), Mystery (1.98×), Retro (1.73×)
- C1-07 (30K–35K) has Based On A Novel (28.86×), Classic (7.79×), Great Soundtrack (4.05×), Detective (3.55×)
- C1-09 (40K–45K) has RPGMaker (5.0×), Immersive Sim (3.63×), Horror (2.51×)
- Plain language: niche flavor tags with engaged audiences dominate near-AA+ work. Aesthetic tags do not.

**N — Great Soundtrack is the strongest near-AA+ marker**
- C1-10: 21.9% of titles tagged "Great Soundtrack" vs 3.4% cohort baseline (6.43× lift, n=37/169 titles)
- Also high lifts in C1-04 (2.06×), C1-06 (2.67×), C1-07 (4.05×), C1-08 (2.63×), C1-09 (3.16×)
- Plain language: of all tags in the sweep, Great Soundtrack travels with the most successful sub-AA+ work most consistently.

**O — Turn-Based is the only tag with strong floor lift in BOTH cohorts**
- Cohort 1: 55.9% zero rate vs 80% baseline (~24pp better)
- Cohort 2: 7.9% zero rate vs 22% baseline (~14pp better)
- Plain language: audience-driven tag rather than adoption-mode-driven.

## Visual Novel finding

**P — Visual Novel is the most extreme zero-wall tag in Cohort 1**
- 83.1% of VN titles by Cohort 1 devs read 0 owners (worse than Casual 87%, Indie 80.5%)
- AA+ VN devs (124 total) cluster in Adventure as primary genre
- 33 "pure VN" studios survive at AA+ — small but durable
- Plain language: VN is the canonical example of a niche where most titles never register but a few find durable audiences.

## Methodology note (owners are bucketed)

Owners data comes from Steam Spy in 14 fixed buckets ranging from 0–20K to 200M–500M. "owners_lower = 0" means a title is somewhere in the 0–20,000 bucket; it does NOT mean zero copies sold. All bucket-based findings are conservative lower bounds. Review counts are exact integers and are used wherever a continuous variable is needed.


---
# COHORT 2 FINDINGS (AA+ only, non-dormant, multi-release, excl Broad AAA — 25K bands)

Cohort 2 starts at the AA+ floor (avg_owners_per_game ≥ 50K). Bands are 25K wide from 50K up to 200K, then Steam Spy bucket-aligned above: 200K–300K, 300K–500K, 500K–1M, and 1M+. 10 bands total. All title-level stats use the structural filter (no Early Access, no demos).

**Note on band design:** an earlier 10K-wide sweep produced artifact clusters because devs with only 2 games can only land on certain arithmetic averages of bucket floors (e.g., 50K, 75K, 100K, 150K). 25K bands are wide enough to merge these arithmetic gravity wells into real economic groups while still resolving meaningful structure.

## Distribution shape of Cohort 2

**Q — The AA+ near-floor band C2-A1 holds 35% of Cohort 2**
- C2-A1 [50K–75K) = 325 devs (35.2%). This is the largest single band in Cohort 2.
- C2-A2 [75K–100K) = 107 (11.6%); C2-A3 [100K–125K) = 155 (16.8%).
- Plain language: more than a third of "active AA+" devs barely cleared the bucket boundary that defined them. The AA+ label captures a real distinction but a third of its members are right at the edge.

**R — Per-title owners distributions are LEFT-skewed for every Cohort 2 band**
- Every Cohort 2 band has negative skew on log10(owners) (range −3.69 to −0.61).
- Negative kurtosis only in the C2-A1 floor band (kurt = −1.57); all other bands have positive kurtosis with sharp central concentration.
- Plain language: Cohort 1's per-title distributions are positive-skewed (long upper tail above a near-zero mode). Cohort 2's per-title distributions are NEGATIVE-skewed (long lower tail below an upper-bucket mode). These are not the same population reflected at different scales.

**S — Per-title zero-rate decays sharply as band rises**
- C2-A1 [50K–75K): 34.4% of titles read 0 owners — the AA+ near-floor devs still have a third of their catalog in the floor bucket.
- C2-A2 [75K–100K): 17.8% zero
- C2-A3 [100K–125K): 18.0% zero
- C2-A4 [125K–150K): 12.0% zero
- C2-A7 [200K–300K): 12.2% zero
- C2-A8 [300K–500K): 4.6% zero
- C2-A10 [1M+]: 4.6% zero
- Plain language: devs in the lowest AA+ band are buoyed by a couple of breakthrough titles; their typical title still reads zero. Above 75K the typical title clears the floor; above 300K the typical title is solidly into AA+ territory.

**T — Review counts climb monotonically across bands (clean continuous signal)**
- C2-A1 median = 255 reviews per title.
- C2-A4 [125K–150K): median = 1,811. C2-A7 [200K–300K): median = 2,495. C2-A8 [300K–500K): median = 6,334.
- C2-A10 [1M+]: median = 26,219 reviews per title.
- Plain language: review counts (which aren't bucketed) confirm the band ordering is real — every step up in owners-band corresponds to a step up in review medians.

## Stage mix across Cohort 2

**U — "Mid zone" and "mid_career_active" dominate every Cohort 2 band**
- These two stages together account for ~70–85% of every band.
- established_active never exceeds 13% except in the small C2-A6 band (40%, n=10) where it's likely sample noise.
- up_and_coming starts at 13.5% (C2-A1) and falls to ~4% above C2-A4.
- Plain language: AA+ adoption sustains primarily via veteran devs in their working middle period, not via lateral arrivals.

**V — Up-and-coming AA+ devs heavily concentrate in C2-A1**
- C2-A1 holds 44 up-and-coming devs (52% of Cohort 2's total up-and-coming pool).
- C2-A2 + C2-A3 hold another 27 between them.
- Plain language: young AA+ devs almost always land just above the threshold. When they break out further, it's already past their "up and coming" career window.

## Genre by band — Cohort 2

**W — Action becomes overwhelming at C2-A10 [1M+)**
- C2-A1 Action share = 35%, Indie 25%.
- C2-A10 Action share = 67%, Indie = 5%.
- Plain language: at million-owner scale, the catalog is decisively Action-led. The Indie label largely drops off — these studios are no longer presenting as indie.

**X — Massively Multiplayer over-indexes hard at the 1M+ band**
- 14.6% of Cohort 2 MMO titles sit in C2-A10 [1M+) versus 4.7% baseline rate (3.1× lift).
- 26.8% of MMO titles still sit in C2-A1 (low end) — bimodal distribution.
- Plain language: MMO entries either disappear at the AA+ floor or break out into the 1M+ tier. Very little middle.

## Tag clusters by band — Cohort 2

**Y — Vehicle / Party-game cluster owns C2-A2 [75K–100K)**
- C2-A2 over-indexes on Motocross (5.66× lift), Motorbike (5.18×), Trivia (5.17×), Bikes (4.86×), Party (4.11×), Party Game (3.76×), Board Game (2.07×).
- Plain language: the band just above the AA+ floor has a distinctive identity — niche-vehicle sims and party-style games. These are tightly-clustered audience-size targets.

**Z — Builder/Educational tags cluster at C2-A3 [100K–125K)**
- Software (4.33× lift), Trading Card Game (4.10×), Game Development (3.71×), Satire (2.95×), Design & Illustration (2.57×), Capitalism (2.16×), Trading (2.15×), Education (2.01×).
- Plain language: the 100K–125K band is the canonical home of "tools, builders, and educational" content. Very different audience profile than the band immediately below it.

**AA — Rogue-family / Shoot-em-up cluster owns C2-A4 [125K–150K)**
- Shoot 'Em Up (3.07× lift), Side Scroller (2.72×), Post-apocalyptic (2.50×), Hack and Slash (2.28×), Roguelite (2.16×), Action Roguelike (1.93×), Roguelike (1.91×), Turn-Based Strategy (1.82×).
- Plain language: the "play-it-forever procedural" cluster lands in a tight band wider than its underlying genres would predict. Useful for benchmarking new roguelike releases.

**BB — Strategy / Base-building / Crafting cluster at C2-A5 [150K–175K)**
- Historical (3.03× lift), Strategy RPG (2.95×), Base Building (2.70×), Crafting (2.35×), Detective (2.33×), VR (2.07×), Resource Management (1.99×).
- Plain language: when AA+ devs are working in deep-system genres (strategy, builders, crafting), they tend to land in this 150K–175K band.

**CC — Open World + Co-op tags define the 500K+ tiers**
- C2-A8 [300K–500K): Crafting (2.42×), Online Co-Op (2.32×), Open World (2.26×), Turn-Based Combat (2.25×), Choices Matter (2.09×), Co-op (2.02×), Sandbox (2.00%).
- C2-A9 [500K–1M): Online Co-Op (3.14×), Third-Person Shooter (2.96×), Co-op (2.88×), Aliens (2.62×), Futuristic (2.33×), Cyberpunk (2.27×), Military (2.21×).
- C2-A10 [1M+]: Open World (3.67×), Moddable (3.40×), Online Co-Op (3.19×), Medieval (3.15×), Co-op (2.82×), Action RPG (2.79×), Multiplayer (2.74×).
- Plain language: the higher you go in Cohort 2, the more the catalog is defined by persistent-world + social-play tags. This is the most cohesive over-index pattern in either cohort.

**DD — Adult content lifts at the AA+ floor band only**
- C2-A1 [50K–75K) over-indexes on Hentai (1.40× lift, n=71).
- No adult-content tag over-indexes at any band above C2-A2.
- Plain language: adult content sorts to extremes — buried at C1-Z in Cohort 1 (zero band), barely clearing the AA+ floor in C2-A1. It does not progress further up.

**EE — Cohort 2 is densely-tagged**
- 50,791 title-tag rows across 3,065 titles → average 16.6 tags per title.
- 434 distinct tags vs Cohort 1's 392.
- Plain language: AA+ titles receive richer user-tag annotation. The tagging itself is a visibility signal.

## Cross-cohort comparison

**FF — Same threshold bucket, different distribution direction**
- Cohort 1 sits below the AA+ floor with positive-skewed per-title distributions (mode at zero, tail upward).
- Cohort 2 sits above the AA+ floor with negative-skewed per-title distributions (mode near band cap, tail downward).
- The 50K boundary is therefore a real phase transition in BOTH the dev-level structure AND the within-dev title distribution shape.
- Plain language: this is not a smooth gradient — devs cross into a qualitatively different operating regime at AA+, which is exactly what makes the 50K threshold defensible analytically.

## Methodology insights — port-shop detection (developed during C1-01/02/03 moderate-indie investigation)

**GG — Steam `release_date` is the Steam-listing date, not original publish date**
- The dataset has no field for "original release date." A 1992 visual novel relaunched on Steam in 2019 shows only "2019."
- Only 11 titles in the dataset pre-date 2003 (Steam's launch year), meaning all legacy ports show modern Steam dates.
- Plain language: we cannot use `release_date` to filter old games. Porting status must be inferred from tags, names, and cross-platform research.

**HH — Tag-based port detection: which tags actually signal porting**
- STRONG signals: `Classic`, `Cult Classic`, `Remaster`, `1980s`, `1990's` — these reliably indicate legacy IP being relaunched.
- WEAK signal: `Retro` alone — frequently used as a modern pixel-art aesthetic, NOT a port indicator unless paired with other strong signals.
- AMBIGUOUS signal: `Remake` — can mean (a) a true port, (b) a fully-rescripted modern rebuild from a legacy predecessor, or (c) misapplied to an entirely original modern game.
- Plain language: not all retro-flavored tags are equal. Aesthetic ≠ legacy IP.

**II — The hidden iOS-first port-shop pattern (Stefan Preuss case study)**
- A solo dev with a small Steam catalog (5 titles) can still be a port-shop if their primary publishing platform is mobile/iOS and Steam is the secondary channel.
- Cross-platform research on Stefan Preuss (Flensburg, Germany) revealed his entire iOS portfolio predates his Steam releases — "Hummingz - Retro Arcade action revised" (2018 Steam) followed iOS "Hummingz EVO HD"; "AcChen - Tile matching the Arcade way" (2017 Steam) followed iOS "AcChen - Solitaire Tiles Game"; "Fairy Fire" (2020 Steam) was a 2015 iOS port.
- Steam-only metadata could not detect this — only the `Remake` tag on Fairy Fire flagged this dev for review. The other 4 ports were invisible to Steam-based filters.
- Plain language: Steam-native filters undercount port-shops. Some catalogs that look like "genuine modern indie" on Steam are actually mobile catalogs being secondary-distributed. This is an acknowledged limitation of the moderate-indie pool.

**JJ — Trademark-clue port detection (HapGames / Qix case study)**
- HapGames' Steam title "Xonix Casual Edition" was tagged `Remake` but predecessor research initially returned UNCLEAR.
- The storefront listing on Green Man Gaming used the full title "Qix: Xonix Casual Edition" with the description "Remake of a classic old-school hit from 80s." Qix is a 1981 Taito arcade IP now owned by Square Enix.
- Use of a trademarked legacy IP name in the storefront title (even when the Steam page omits it) confirms the dev is licensing/branding around legacy IP, not creating original work.
- Plain language: storefront listings outside Steam can reveal IP relationships that the Steam page hides. Cross-storefront search is sometimes the only way to identify legacy-IP re-creations.

**KK — Final exclusion roster for C1-01/02/03 moderate-indie pool**
- Tier 1 port-shops (catalog ≥50% strict-port tags or name keywords): 122 devs
- Tier 3 confirmed PORTS (Remake-tagged with verified predecessor): 7 devs (Naps Team, Balio Studio, Screaming Villains, TERARIN GAMES, A Sharp, aNCHOR Inc./fuzz Inc., origamihero games)
- Tier 3 UNKNOWN re-classified as port: Stefan Preuss (iOS-first), HapGames (Qix licensee)
- Tier 4 TRANSLATOR_PORTERS: 19 devs (Zeiva Inc, Norn... [the J-VN localizer set])
- Shovelware outliers: Creobit (137-title Russian casual factory), Blessing Company (terminated by Valve Jan 2026 for review manipulation)
- Total unique exclusions: ~152 devs
- Net moderate-indie pool: ~1,325 devs across C1-01..C1-03
- ACKNOWLEDGED LIMITATION: The 1,325-dev pool is the BEST-EFFORT clean indie subset. Hidden iOS-first or mobile-first port-shops that escaped detection (no Remake tag, no Classic-tag co-tags) likely remain. The Stefan Preuss case proves these exist. Sensitivity analysis recommended.


**LL — Steam stores Early Access and Free-to-Play in TWO locations (dual-location filter trap)**
- DISCOVERED during moderate-indie genre analysis: an early "F2P and EA over-index in C1-02 (lifts 1.41, 1.24)" finding turned out to be a filtering artifact, not a real signal.
- Root cause: a downstream rebuild of the moderate-indie title pool filtered Early Access via `categories.csv` (string == "Early Access"), but on the Steam dataset these strings sit in `genres.csv` instead. The two columns do not overlap at all — `categories.csv` "Early Access" matched **zero** titles in our pool, while `genres.csv` "Early Access" matched 159. Free-to-Play has the same dual storage: 104 titles via the `genres.csv` "Free to Play" string AND 159 via the games-table `is_free=1` boolean flag (overlap, but neither is a superset).
- Total leak: **509 contaminated titles** in the 9,000-title moderate-indie pool (5.7%), concentrated in C1-02 (4.5% of its titles).
- The canonical app filter (`steam-threshold-app/filters.py → structural_mask`) handles this correctly: EA via `genres_list` contains "Early Access" AND F2P via `is_free != 1`. Cohort 1 and Cohort 2 band assignments built through `apply_all` were therefore unaffected.
- Post-fix totals: 8,491 titles (C1-01: 3,542 / C1-02: 3,885 / C1-03: 1,064). All five moderate-indie charts regenerated.
- After cleaning, **the genre-level F2P/EA lift disappears entirely** (those rows are gone). The tag-level signature got *stronger and more coherent*: C1-02 over-indexes on Colony Sim (1.65×), Loot (1.60×), Modern (1.50×), Isometric (1.44×), City Builder (1.41×), Dating Sim (1.38×), Life Sim (1.32×) — a coherent "systems-driven moderate indie" picture. C1-01 over-indexes on Text-Based (1.83×), Design & Illustration (1.67×), Solitaire (1.41×), NSFW, CYOA — "low-volume niche-fit indie." C1-03 over-indexes on Inventory Management (2.17×), Narration (1.98×), Crime (1.94×), RPGMaker (1.94×), Thriller (1.91×), Noir (1.91×), Cinematic (1.82×) — "narrative-mechanical hybrid indie."
- Plain language: when a dataset stores the same concept in two columns, a filter that catches only one will silently let half the contamination through. Always check both `categories.csv` AND `genres.csv` for structural exclusion strings, and check both the genre string AND the `is_free` flag for F2P. The canonical app filter is the source of truth — downstream pool rebuilds must go through it, not around it.

**MM — Per-tag trend shapes across the three moderate-indie bands**
- After classifying all 223 stable tags (n≥80 titles) by their lift trajectory across C1-01 → C1-02 → C1-03, four trajectory shapes emerge: 47 rising, 51 peak-middle, 10 falling, 9 valley-middle. The remaining 92 are mixed (no clean trend) and 14 are flat (no real movement).
- **Rising tags (lift climbs monotonically with owners band)** — these are tags that mark a moderate indie as more likely to break above 10K owners. Strongest movers: Level Editor (2.50× at C1-03), Inventory Management (2.17×), Narration (1.98×), RPGMaker (1.94×), Thriller (1.91×), Cinematic (1.82×). Reads as longer, deeper, more authored experiences — the kinds of mechanics where players stay long enough to leave a review and word-of-mouth has time to compound.
- **Middle-band champions (lift peaks at C1-02 and drops at C1-03)** — these tags own the 5K–10K band specifically. Strongest peakers: Colony Sim (1.65× at C1-02), Loot (1.60×), Modern (1.50×), Isometric (1.44×), City Builder (1.41×), Post-apocalyptic (1.39×). Reads as medium-complexity systems games — enough mechanical depth to hit moderate success, but genre-constraints cap audience before it crosses 10K. This is the "systems-driven moderate indie" archetype.
- **Falling tags (lift declines monotonically)** — concentrate at the 0–5K floor. Strongest fallers: Design & Illustration (1.67× at C1-01), Massively Multiplayer (1.39×), 3D Fighter (1.28×), Choose Your Own Adventure (1.28×), Mature (1.24×), Hentai (1.18×). Reads as either utility products (Design & Illustration), unrealistic genre expectations for indies (MMO/fighter), or NSFW which Steam algorithmically suppresses from discovery surfaces.
- **Valley tags (lift dips at C1-02 and recovers at C1-03)** — these tags skip the middle band; the 5K–10K zone is hostile terrain for them. Strongest skippers: Real Time Tactics (1.50× at C1-03 vs 0.85× at C1-02), Psychedelic (1.45×), 1980s (1.35×), Comic Book (1.32× at C1-01). Reads as bimodal niches — they either stay tiny or break out into cult-hit territory; the middle is unstable for them.
- **Two strategic takeaways:**
  1. The middle band is its own genre flavor, not just a halfway house. Colony Sim, Loot, City Builder, and Isometric peak specifically there with steep falloffs on both sides — this is a real population segment with a coherent mechanical identity, not statistical noise from band-edge titles drifting either direction.
  2. Author-driven mechanics rise as owners climb; niche-aesthetic commitment stays pinned at the floor. The cleanest cross-band signal in the dataset is that tags marking narrative-plus-mechanical depth (Thriller, Cinematic, Narration, Inventory Management, RPGMaker) climb steadily with band, while tags marking aesthetic/genre commitment with small target audiences (Hentai, Design & Illustration, MMO ambition, fighter) stay concentrated at the floor.
- Plain language: every tag in the dataset is moving in one of four ways across the bands. Knowing which way a tag moves tells you which band a game built around that tag is most likely to land in.

## Portfolio Concentration Index (PCI) — per-dev catalog dependency

**NN — PCI formula and intent**
- PCI is a Herfindahl-Hirschman-style index applied to a developer's own catalog of owners-shares. For each dev d with games g, PCI_d = Σ(owners_g / total_owners_d)². A perfectly even catalog (every game pulls equal weight) gives PCI = 1/N where N is the number of games with measurable owners. A "one-hit wonder" (one game = 100% of owners) gives PCI = 1.0.
- We computed PCI on the post-shovelware roster: Cohort 1 = 5,909 devs (excluded Creobit + Blessing Company; the two Tier-1 outliers we removed earlier), Cohort 2 = 924 devs (unaffected by the exclusions; both shovelware devs were sub-AA+).
- Source data: title-level `owners_lower` (bucket floor) from the canonical clean structural cohort (EA / F2P / demos excluded via `apply_all`). 27,654 titles in scope.
- Plain language: PCI tells us whether a dev's audience is spread across multiple titles or piled into a single hit. Higher = more dependent on one game.

**OO — PCI distribution: Cohort 2 is genuinely more diversified than Cohort 1**
- Restricted to devs with ≥2 games carrying measurable owners (the population where PCI is meaningfully defined):
  - C1: n=905, median PCI = 0.50, mean = 0.46 (range 0.05 to 0.83)
  - C2: n=705, median PCI = 0.56, mean = 0.56 (range 0.06 to 0.98)
- The C1 distribution has a sharp mode at PCI = 0.50 — devs with exactly 2 owners-bearing games where the split is close to 50/50. C2 has a bimodal-ish shape: mode at 0.50 plus a second hump near 0.70–0.85, meaning AA+ devs cluster into either "two-balanced-hits" or "anchor-title-plus-modest-followups" portfolios.
- C2's higher mean (0.56 vs 0.46) is largely a *bucket-resolution artifact* — AA+ devs land in higher owners buckets where one bucket can hold genuinely 5× the audience of another, so the share calculus produces wider gaps. C1 devs mostly sit in the 10K–20K bucket where two games landing there look identical share-wise.
- Plain language: AA+ developers really do rely more on a single anchor title than sub-AA+ developers. But part of that gap is the Steam owners-bucket coarseness — at lower owners levels, "the hit" and "the followups" both round to the same bucket.

**PP — PCI category mix and the "zero-bucket" floor in Cohort 1**
- 60.7% of C1 devs (3,587 of 5,909) have undefined PCI because every game in their catalog sits in the 0-owners bucket. This is not noise — it is a structural fact about sub-AA+ multi-release devs: most of their games genuinely fall below the lowest measurable owners threshold (20,000 owners or fewer in Steam's coarsest bucket, "0–20K" rounded to 0 in our scrape).
- Another 24% (1,417 devs) have exactly one game with measurable owners, which auto-assigns PCI = 1.0. So for 85% of Cohort 1, PCI is either undefined or trivially "one-hit by default" — and *only 15% (905 devs) have a meaningfully variable PCI*.
- Cohort 2 by contrast has 0% undefined (every AA+ dev has at least one well-populated title) and 23.7% single-owners-game; the remaining 76% have meaningfully variable PCI. The mix is 11.7% diversified (PCI<0.35), 21.9% moderate (0.35–0.55), 38.9% concentrated (0.55–0.85), 3.9% one-hit (≥0.85).
- Plain language: at lower owners levels Steam's data resolution hides most of the catalog signal — a sub-AA+ studio with 12 games that each sold 5,000 copies looks identical to one with 12 games that each sold 19,000 copies. We can only measure portfolio concentration meaningfully for studios with enough hits to land in resolvable buckets.

**QQ — PCI mechanically drops with catalog size — interpret with caution**
- Within both cohorts, median PCI drops as N (games with measurable owners) increases — from ~0.50 at N=2, ~0.40 at N=3, ~0.30 at N=4, and approaching the 1/N theoretical floor by N=8+. This is partly *mathematical* (the floor 1/N falls automatically as N rises) and partly *behavioral* (long-catalog devs are also more diversified than would be expected from chance alone — the C2 medians sit ~0.10 above 1/N at every N, indicating real anchor-title dependence even in big catalogs).
- Within Cohort 1, PCI varies modestly across the 5K bands: C1-01 through C1-04 medians sit at ~0.40–0.50, while C1-05 through C1-08 medians climb to ~0.50–0.56. The higher-owners moderate bands have slightly more concentrated catalogs than the lower-owners moderate bands — moderate-indie devs who break above 25K owners tend to do so on the back of one anchor title, not by climbing across the whole catalog.
- Plain language: a small studio with one hit and a long tail of zeros looks the same on PCI as a one-game shop. To distinguish them, always pair PCI with catalog size — the two together describe whether a dev is broad-but-thin or narrow-but-deep.

**RR — Strategic takeaway**
- PCI works as a portfolio-health signal *within* the resolvable population (the 905 C1 devs and 705 C2 devs with ≥2 games carrying measurable owners). The 60.7% C1 "all-zero" devs need a different framework — possibly a reviews-based concentration index, since reviews resolve to individual-title resolution while owners stay bucketed.
- For Cohort 2 specifically, PCI is a working tool — about 60% of AA+ devs (concentrated + one-hit categories) carry meaningful one-title dependency risk, while only ~12% have truly diversified portfolios. This matches the "anchor-title indie studio" pattern that dominates AA+ — most of these studios live on Hollow-Knight-style breakouts, not balanced multi-game catalogs.
- Recommended companion analysis: a *reviews-based* concentration index (PCI_rev) using the same formula but with `total_reviews` instead of `owners_lower`. Reviews resolve to single-title precision and would let us compute meaningful PCI for the 3,587 C1 devs currently locked at "undefined." That gives a complete portfolio picture across all 6,833 post-shovelware devs.

---

**SS — PCI category deep-dive: archetypes of each concentration class**

Restricted to the **resolvable PCI population** — devs with ≥2 games carrying measurable owners — and then further cleaned of port-shops, translators, VN repackagers, and shovelware/asset-flip operations identified via the moderate-indie exclusion list (round 1: 35 devs) and the volume+engagement audit (round 2: 24 devs). Net working roster: **846 C1 + 705 C2 = 1,551 devs**. The all-zero-owners floor (3,587 C1 devs) and the single-game-resolvable group (1,417 C1 + 219 C2) remain out of scope here — they are PCI-undefined or PCI-trivial. Reviews-based PCI is not pursued: paid-review contamination would dominate the signal.

**Studio profile per category (medians, 1,551-dev clean roster):**

| Cohort | Category | n devs | Catalog size | Median PCI |
|---|---|---:|---:|---:|
| C1 | diversified | 197 | 9 | 0.25 |
| C1 | moderate | 367 | 4 | 0.50 |
| C1 | concentrated | 282 | 3 | 0.59 |
| C1 | one-hit | 0 | — | — |
| C2 | diversified | 108 | 6 | 0.27 |
| C2 | moderate | 202 | 3 | 0.49 |
| C2 | concentrated | 359 | 2 | 0.68 |
| C2 | one-hit | 36 | 2 | 0.93 |

The PCI category boundaries (0.35 / 0.55 / 0.85) translate into very clean anchor-share medians (33% / 50% / 71–80% / 96%). That's a sanity check: the math behaves the way the labels claim.

**C1 has no "one-hit" devs** — to land in PCI≥0.85 you need a measurable hit *and* a population of measurable also-rans below it, but at sub-AA+ owners levels the also-rans usually round to 0 and therefore land in the "all-zero" group instead. AA+ devs always have enough resolvable titles to populate the one-hit category.

**Tag signatures per category (top tags by lift vs cohort baseline):**

- **C1 diversified — "catalog grinder":** Based On A Novel (1.73×), Trading Card Game (1.65), Cult Classic (1.50), Werewolves (1.43), Text-Based (1.39), Otome (1.37), Match 3 (1.37). Visual-novel / dating-sim / text-heavy niches. Broad-and-thin catalogs that earn audiences across multiple titles.
- **C1 moderate — "crafty middle":** Design & Illustration (2.14), Automation (2.07), Creature Collector (1.83), Wholesome (1.82), Experimental (1.73), Cozy (1.67), Comic Book (1.67), Auto Battler (1.65). Cozy/creative/automation studios with small catalogs of medium-success titles.
- **C1 concentrated — "genre-hit indie":** Transportation (2.96), Parody (2.81), Martial Arts (2.32), Combat Racing (2.19), Metroidvania (2.13), Level Editor (2.07), Base Building (2.01). One genre-defining title carrying most of the catalog.
- **C2 diversified — "mature/niche specialist":** Motorbike (2.46), Party Game (2.04), NSFW (1.65), Classic (1.64), Hentai (1.61), Fast-Paced (1.61), Minimalist (1.51), Fighting (1.40). Two distinct sub-archetypes: adult-content publishers with broad catalogs, and arcade/classic-style multi-genre studios.
- **C2 moderate — "vehicle / sim specialist":** Automobile Sim (1.97), Driving (1.73), Action RPG (1.55), Moddable (1.55), City Builder (1.49), War (1.46). Genuine sim and management studios — driving and city-builder communities are deep and repeat-purchase-friendly.
- **C2 concentrated — "anchor-title roguelike studio" (the dominant AA+ archetype):** Deckbuilding (1.87), Dark Comedy (1.71), Psychological (1.62), Perma Death (1.60), Resource Management (1.58), Team-Based (1.56), Roguelite (1.50), Post-apocalyptic (1.50). This is the Hollow-Knight / Slay-the-Spire pattern — one breakout in roguelike/deckbuilding territory + a thinner followup catalog.
- **C2 one-hit — "multiplayer breakout":** Multiplayer (1.77), Exploration (1.54), Atmospheric (1.25), Action (1.15). Singleplayer and generic Indie/Adventure/Casual tags sit at lift ≈ 1.0 (no distinctive signal). The lift is concentrated in *Multiplayer* — these are the studios whose entire catalog runs on one viral co-op title.

**Band × category cross-tab (Cohort 1):** the category mix systematically shifts as you climb the 5K bands. At C1-01 (5K–10K owners) the mix is 35% diversified / 63% moderate / 2% concentrated. By C1-07 (35K–40K owners) it has flipped to 14% / 16% / 70%. **Higher bands within sub-AA+ are dominated by concentrated portfolios** — devs who escape the lowest moderate-indie tier usually do so on the back of one anchor title, not by lifting their whole catalog uniformly. Pure broad-and-thin diversification rarely produces a 30K+ owners outcome at sub-AA+ scale.

**Plain-language takeaway:**
- The four PCI categories aren't just statistical buckets — they capture genuinely different studio business models. Diversified devs run catalog-grinder shops (text/visual-novel/cozy niches at C1; mature/sim niches at C2). Concentrated devs are anchor-title operations (one metroidvania / roguelike / vehicle-sim that earned most of the audience).
- For Cohort 2, ~60% of resolvable AA+ devs are concentrated or one-hit, confirming that "single-game studio" is the modal AA+ pattern, not the exception.
- For Cohort 1, the "concentrated" share grows with band: the path from moderate-indie band to upper-moderate-indie band runs through one breakout title, not through whole-catalog growth.

---

**TT — Suspect-Dev Battery + Country-of-Origin Inference**

Built a 9-test scoring battery to flag potentially suspect devs (asset-flipper vs incubator) on the 1,551-dev clean roster, plus a conservative country-of-origin inference. Findings:

**Battery design.** Nine tests, scored 1–3 points each, bucketed: HIGH_SUSPECT (≥6), MEDIUM (3–5), LOW (1–2), CLEAR (0). Cadence tier widened per user direction so that anything above 2 titles/year is treated as elevated — empirically every dev above 2/yr now carries at least one flag.

| Test | What it catches | Tiers (points) |
|---|---|---|
| T1 cadence | Title throughput | >2/yr=1, ≥4=2, ≥8=3, ≥15=3 |
| T2 engagement collapse | % titles with <5 reviews | ≥40%=2, ≥60%=3 |
| T3 dollar-store pricing | Price floor + low reviews | conditional 1–2 |
| T4 owners floor | ≥80% titles in 0-owners bucket | 2 |
| T5 zero-review share | ≥30% titles with 0 reviews | 2 |
| T6 playtime collapse | Median playtime <10 min | 1 |
| T7 uniform mediocrity | Review CV<0.5 + low median | 1 |
| T8 publisher factory | 1 publisher + ≥30 titles + low rev | 1 |
| T9 genre scattershot | ≥5 genres + low rev | 1 |

**Suspect bucket × PCI category × cohort:**

| | C1 dev | C1 mod | C1 conc | C2 dev | C2 mod | C2 conc | C2 1-hit |
|---|---:|---:|---:|---:|---:|---:|---:|
| HIGH_SUSPECT | 7 | 12 | 5 | 1 | 0 | 1 | 0 |
| MEDIUM | 22 | 48 | 23 | 4 | 1 | 1 | 0 |
| LOW | 80 | 71 | 34 | 20 | 7 | 11 | 3 |
| CLEAR | 88 | 236 | 220 | 83 | 194 | 346 | 33 |
| **% any suspect** | **55%** | **36%** | **22%** | **23%** | **4%** | **4%** | **8%** |

**The cohort gap is the headline.** Cohort 1 devs are suspect-flagged at ~5–10× the rate of Cohort 2 devs in the same PCI category. C1 diversified is the worst bucket (55% flagged) — that's where the catalog-grinder shops live and where genuine asset-flippers blend in most easily. C2 categories are nearly clean (≤8% flagged across the board, single-digit HIGH counts).

**The PCI-category gradient inside C1 is also informative.** Inside C1, suspect rate falls as concentration rises: diversified 55% → moderate 36% → concentrated 22%. Bottom line: **catalog-grinder behavior at sub-AA+ scale carries disproportionate suspect risk**; broad-and-thin output without anchor performance is exactly the asset-flipper / shovelware factory signature. Concentrated devs at the same scale earned their PCI through one resolvable hit, which is much harder to fake than catalog volume.

**HIGH_SUSPECT top cases (n=26).** Three archetypes visible:

1. *Likely asset-flippers / shovelware* (low engagement + price floor): Ammonite Design Studios Ltd, Seven Sails Games, Nacks Soft, Michael Richard Lannon, XSGames, Sprovieri Games, Brewsterland Studios.
2. *Probable legitimate incubators / collectives* (high cadence but real engagement): Choice of Games (163 titles, median 20 reviews), Hosted Games (109 titles, median 23 reviews), Sokpop Collective (95 titles, median 26 reviews), EpiXR Games UG (71 titles, median 19 reviews, 91.5% positive). These pass the engagement tests but fail volume tests — manual review confirms they're real CYOA/experimental publishers.
3. *Mixed / requires further review*: Follow the fun, Exe Create Inc., eSolutions, Tamashii, e-FunSoft Games, Afil Games, Boomzap Inc, Hede, PUNKCAKE Delicieux, Ready To Play, Gamma Ray Chamber, celikgames, SoteroApps, SEGA (C2 — likely legacy re-issues), Konnichiwa Games & Media.

The HIGH bucket is **not** the same as "asset-flipper" — it's "warrants a closer look". Devs are kept in the roster with a flag (`suspect_bucket`, `suspect_flags`, `manual_note`) rather than excluded.

**Why country-of-origin matters here — and what it is not.** Country inference is a **triage estimator**, not a quality or bias signal. No jurisdiction is treated as "better" or "worse" than another in the scoring; every candidate that survives Stages 1–11 is a real candidate regardless of inferred country. The reason we estimate jurisdiction at all is purely operational: **investment and acquisition diligence is materially different across jurisdictions** because of:
- **Regulatory and licensing differences** (game-ratings regimes, content-classification rules, online-services licensing, app-store-style content gates that apply in some countries and not others)
- **IP and contract-law differences** (assignability of copyright in employment agreements, work-for-hire treatment, moral-rights regimes, enforceability of standard buyout clauses)
- **Tax structure and treaty differences** (withholding on royalties, transfer-pricing rules, R&D incentive credits, capital-gains treatment on share sales)
- **Sanctions and export-control exposure** (some jurisdictions require additional screening; deal timelines and structures differ accordingly)
- **Currency, banking, and payment-rail differences** (escrow availability, closing mechanics, cross-border settlement)

A candidate in a jurisdiction with simple, predictable IP and tax treatment is **faster** to put through first-tier diligence — not better, just faster. A candidate flagged into a more complex jurisdictional bucket needs specialist counsel before the same depth of diligence can be completed, so we route them differently in the work queue. **This is sequencing, not selection.** All 146 candidates remain on the roster; the country tag only affects which ones get reviewed in which order.

**Country-of-origin inference method.** Country is not in the dataset. Inferred from two conservative signals: (1) publisher-name suffixes (UG/GmbH→Germany, S.r.l.→Italy, Sp. z o.o.→Poland, Co.,Ltd→Japan/Asia, etc.); (2) Steam language footprint where dev ships a single non-English language dominantly on ≥70% of titles AND ships ≤2 dominant languages total. The second clause is critical — devs that ship 8+ localizations are excluded as "Global-localizer" because shipping Russian or Chinese as a localization tells you nothing about origin.

| Country signal | C1 | C2 | Total |
|---|---:|---:|---:|
| EN-default (no signal) | 426 | 224 | 650 |
| Global-localizer (3+ languages, no origin signal) | 200 | 360 | 560 |
| China (lang dominant + narrow footprint) | 68 | 44 | 112 |
| Russia/CIS (lang or personal name) | 64 | 21 | 85 |
| Japan (lang or Co.,Ltd) | 29 + 5 | 16 + 2 | 52 |
| Germany (UG/GmbH or lang) | 14 | 19 | 33 |
| France / Brazil / UK / Italy / Poland / Turkey / Korea | ≤16 each | | |

**Key country observation:** C2 is dominated by global-localizers (51% of C2 vs 24% of C1). At AA+ scale, devs ship 4–8 localizations as a matter of course; at sub-AA+ scale, English-only or narrow-localization shipping is the norm. This is consistent with the broader cohort difference — C2 represents commercially-scaled studios that can afford full localization budgets.

**Plain-language takeaway:**
- C1 diversified is the highest-risk PCI category — 55% of its devs carry at least one suspect flag. If you build moderate-indie market estimates from C1 diversified without filtering, you are absorbing a large amount of asset-flipper noise into your baseline.
- C2 is essentially clean across the board (≤8% flagged). The AA+ commercial filter that puts a dev in C2 already screens out the asset-flipper population — they simply don't accumulate enough owners to register.
- The 26 HIGH_SUSPECT devs split into roughly two camps: ~7 likely-real asset-flippers/shovelware that survived earlier rounds, and the rest are high-cadence legitimate operations (incubators, collectives, CYOA publishers). The flag is a triage signal, not an exclusion criterion.
- Country inference is intentionally conservative — 78% of the roster lands in one of the two "Unknown" buckets. The signals that do fire (China, Russia/CIS, Japan, Germany) are consistent with what we'd expect from the publisher-name suffix patterns and language-dominance heuristics. **The tag is a diligence-routing aid, not a quality judgment** — it tells us which candidates can move through standard first-tier review and which ones need jurisdiction-specialist counsel queued up first, because regulatory, IP, tax, and deal-structure complexity vary by country.

---

## Finding UU — End-to-end pipeline is reproducible and reconciles to the locked roster

**What we built.** `investor_pipeline.py` (656 lines, 11 stages) takes a raw Steam dataset directory and produces the same 146-developer candidate roster the manual pipeline produced. Running it on the original `steam-threshold-app/data` reproduces every locked checkpoint exactly from Stage 6 onward.

**Reconciliation against locked roster (run on 2026-06-04):**

| Stage | Actual | Target | Δ | Status |
|---|---:|---:|---:|---|
| 0 — Raw load | 140,082 | 140,082 | +0 | MATCH |
| 1-2 — Hygiene + Structural (strict) | 64,320 | 64,320 | +0 | MATCH |
| 1-2b — Activity cohort (looser) | 71,529 | — | — | — |
| 3 — Cohorts post-dormancy | 6,835 | 6,833 | +2 | CLOSE |
| 3 · Cohort 1 | 5,911 | 5,911 | +0 | MATCH |
| 3 · Cohort 2 | 924 | 924 | +0 | MATCH |
| 5 — PCI-resolvable | 1,612 | 1,610 | +2 | CLOSE |
| 6 — After exclusions | **1,551** | **1,551** | **+0** | **MATCH** |
| 7 — Moderate + concentrated | **1,210** | **1,210** | **+0** | **MATCH** |
| 7 · C1 mod+conc | 649 | — | — | — |
| 7 · C2 mod+conc | 561 | — | — | — |
| 11 — Final candidates | **146** | **146** | **+0** | **MATCH** |
| 11 · C1 / C2 split | 53 / 93 | 53 / 93 | +0 | MATCH |
| 11 · RISING / ANCHOR_RECENT | 82 / 64 | 82 / 64 | +0 | MATCH |

**All 146 developer identities match the original roster one-for-one** (verified: 146 in both, 0 only-locked, 0 only-pipeline).

**The two +2 deltas in Stages 3 and 5.** The new pipeline picks up 2 extra C1 devs at cohort assignment (cleaner handling of `years_since_latest` NaN on the dormancy join). Those 2 extras propagate to Stage 5 PCI-resolvable. They are then absorbed at Stage 6a (37 dropped vs locked 35), which catches them via the moderate-indie exclusion list. Net effect: zero impact on Stage 6 (1,551), Stage 7 (1,210), or Stage 11 (146).

**Canonical thresholds in code (must match `two_cohorts.py`):**
```python
STRICT_AAA    = dict(min_games=3, min_avg_owners=1_000_000, min_max_owners=2_000_000)
BROAD_AAA     = dict(min_games=5, min_avg_owners=100_000,   min_max_owners=500_000)
AA_PLUS       = dict(min_games=2, min_avg_owners=50_000)
DORMANT_YEARS = 5.0   # drop devs whose latest release is older than this
REF_DATE      = pd.Timestamp("2024-10-28")
```

**Cohort logic in code:**
```python
c1_mask = agg['multi'] & ~agg['aa_plus']       # sub-AA+ multi-title
c2_mask = agg['aa_plus'] & ~agg['broad_aaa']   # AA+ excluding broad-AAA
```

**Activity (dormancy) measured on a LOOSER cohort.** Stage 3 uses a separate `stage12_activity` cohort with `exclude_early_access=False, exclude_demos=False`. This lets a dev who is still shipping EA or demo content count as non-dormant even if their last paid release is >5 years old. This is the single most important non-obvious detail in the pipeline — measuring activity on the strict cohort would drop a meaningful number of legitimate-but-EA-only devs.

**PCI restricted to cohort devs.** Stage 4 only computes PCI for the ~6,835 cohorted devs (not all 60K+ devs in the structural pool). This is a correctness fix, not just an optimization — including non-cohort devs in the PCI population would dilute the categorical mix.

**Plain-language takeaway.** The pipeline is now a single runnable module that any new Steam dataset can flow through and reach the same canonical roster. The audit findings A–TT calibrate every threshold and exclusion list it uses; the reconciliation table above is the proof that the code faithfully implements them. The 146-candidate output is no longer a one-off artifact of a notebook session — it is the deterministic output of a documented filter chain.
