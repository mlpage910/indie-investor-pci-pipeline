"""
INVESTOR CANDIDATE PIPELINE — end-to-end module
================================================

Runs any Steam-style dataset through the full filter/scoring chain that produced
our 146 investor candidates from ~140K raw titles.

Stages (in order, each documented + countable):
  Stage 0 : Load raw data (any directory with games/genres/categories/tags/steamspy/reviews CSVs)
  Stage 1 : Hygiene filter (drop rows with missing release_date, owners_band, dev, publisher, or paid-without-price)
  Stage 2 : Structural filter (drop demos, F2P, non-English, no Steam store listing, Early Access)
  Stage 3 : Cohort assignment (Cohort 1 = non-AA+ multi-title, Cohort 2 = AA+ multi-title)
  Stage 4 : PCI computation (HHI on owners shares per dev)
  Stage 5 : PCI-resolvable filter (>= 2 titles with measurable owners)
  Stage 6 : Quality cleanup
              6a — drop devs in the moderate-indie exclusion list (port shops, translators, VN repackagers)
              6b — drop additional shovelware identified in Round 1
              6c — drop high-volume low-engagement asset-flippers identified in Round 2
  Stage 7 : Restrict to moderate or concentrated PCI categories (drop diversified + one-hit)
  Stage 8 : Suspect-battery scoring (9 tests, score, bucket)
  Stage 9 : Trajectory classification (6 classes: RISING, ANCHOR_RECENT, STEADY, ANCHOR_MATURE, FALLING, ANCHOR_AGING)
  Stage 10: Country-of-origin inference (publisher suffix + Steam language dominance)
  Stage 11: Final investor-candidate selection:
              RISING or ANCHOR_RECENT
              + suspect_bucket == CLEAR
              + ranked by investor_score

Usage:
    from investor_pipeline import run_pipeline
    summary = run_pipeline(data_dir='/path/to/steam_csvs', out_dir='/path/to/output')
"""
from __future__ import annotations
import os
import sys
import pandas as pd
import numpy as np
from pathlib import Path

# ---------- Constants (all thresholds documented here in one place) ----------

REF_DATE = pd.Timestamp("2024-10-28")   # As-of date for age calculations

# Stage 1: hygiene
HYGIENE = dict(
    require_release_date=True,
    require_owners_band=True,
    require_developer=True,
    require_publisher=True,
    paid_requires_price=True,
    drop_future_release=True,
)

# Stage 2: structural
STRUCTURAL = dict(
    exclude_demos=True,
    exclude_free_to_play=True,    # via is_free flag
    require_english=True,
    require_us_available=True,    # operationalized as has_store_listing == 1
    exclude_early_access=True,    # via genres_list containing 'Early Access'
)

# Stage 3: cohort thresholds (faithfully reproduce two_cohorts.py)
# AA+ tier flags use AVG owners (not max) + game-count + max thresholds.
# Cohort 1 = multi-title AND NOT aa_plus    (sub-AA+)
# Cohort 2 = aa_plus AND NOT broad_aaa      (AA+ excluding AAA tier)
# Activity filter: drop devs whose latest release is >= DORMANT_YEARS old
#   (activity is measured against a LOOSER cohort: EA + demos restored)
STRICT_AAA = dict(min_games=3, min_avg_owners=1_000_000, min_max_owners=2_000_000)
BROAD_AAA  = dict(min_games=5, min_avg_owners=100_000,   min_max_owners=500_000)
AA_PLUS    = dict(min_games=2, min_avg_owners=50_000)
DORMANT_YEARS = 5.0   # drop devs whose latest release is older than this

# Stage 5: PCI categories (HHI bins)
PCI_BINS = {
    'diversified':  (0.00, 0.35),
    'moderate':     (0.35, 0.55),
    'concentrated': (0.55, 0.85),
    'one-hit':      (0.85, 1.01),
}

# Stage 8: Suspect battery
SUSPECT_BUCKET_THRESHOLDS = dict(HIGH_SUSPECT=6, MEDIUM_SUSPECT=3, LOW_SUSPECT=1)

# Stage 9: Trajectory classification
TRAJECTORY_ANCHOR_SHARE = 0.70  # >= this => ANCHOR_* class (else RISING/STEADY/FALLING)
TRAJECTORY_ANCHOR_AGE_BANDS = dict(recent=2.0, mature=5.0)  # years
TRAJECTORY_RISING_RATIO = 2.0   # late_half_owners / early_half_owners (smoothed)
TRAJECTORY_FALLING_RATIO = 0.5
TRAJECTORY_SMOOTH_K = 40_000    # additive smoothing on owners halves

# Stage 11: Final candidate selection
CANDIDATE_TRAJECTORIES = ['RISING', 'ANCHOR_RECENT']
CANDIDATE_SUSPECT_BUCKET = 'CLEAR'


# ============================================================================
# STAGE 0 — LOAD
# ============================================================================
def stage0_load(data_dir: str) -> pd.DataFrame:
    """Load raw Steam dataset; expects same CSV layout as steam-threshold-app/data."""
    sys.path.insert(0, str(Path(__file__).parent / 'steam-threshold-app'))
    from loader import load
    base = load(data_dir)
    return base


# ============================================================================
# STAGES 1+2 — HYGIENE + STRUCTURAL
# ============================================================================
def stage12_clean(base: pd.DataFrame) -> pd.DataFrame:
    """Apply hygiene and structural filters. Drops ~54% of rows."""
    sys.path.insert(0, str(Path(__file__).parent / 'steam-threshold-app'))
    from filters import apply_all
    clean, _ = apply_all(base, HYGIENE, STRUCTURAL, {})
    clean['release_date'] = pd.to_datetime(clean['release_date'], errors='coerce')
    return clean.dropna(subset=['release_date', 'owners_lower'])


def stage12_activity(base: pd.DataFrame) -> pd.DataFrame:
    """Looser activity cohort: hygiene + structural but with EA and demos restored.

    Used solely to measure dev activity (latest_release). This lets a dev who
    has shipped only EA/demo content in the past 5y count as non-dormant.
    """
    sys.path.insert(0, str(Path(__file__).parent / 'steam-threshold-app'))
    from filters import apply_all
    struct_loose = {**STRUCTURAL,
                    'exclude_early_access': False,
                    'exclude_demos': False}
    act, _ = apply_all(base, HYGIENE, struct_loose, {})
    act['release_date'] = pd.to_datetime(act['release_date'], errors='coerce')
    return act.dropna(subset=['release_date'])


# ============================================================================
# STAGE 3 — COHORT ASSIGNMENT
# ============================================================================
def stage3_cohorts(clean: pd.DataFrame, activity: pd.DataFrame) -> pd.DataFrame:
    """Faithful reproduction of two_cohorts.py logic.

    Steps:
      a) Aggregate per developer on the STRUCTURAL clean cohort
         (count rows via total_reviews to match the locked builder).
      b) Apply AA+ tier flags: strict_aaa / broad_aaa / aa_plus / multi.
      c) Compute latest_release / years_since_latest from the LOOSER activity
         cohort (EA + demos restored) — this lets a dormant-by-paid-game dev
         be re-activated if they're still shipping EA/demo content.
      d) Drop dormant devs (years_since_latest >= DORMANT_YEARS).
      e) Assign cohorts:
           Cohort 1 = multi AND NOT aa_plus
           Cohort 2 = aa_plus AND NOT broad_aaa
      f) (Strict AAA devs are dropped from both cohorts as out-of-scope.)
    """
    # a) per-dev aggregation on structural cohort
    agg = clean[clean['developer'].notna()].groupby('developer').agg(
        n_titles=('total_reviews', 'size'),
        sum_owners=('owners_lower', 'sum'),
        max_owners=('owners_lower', 'max'),
    ).reset_index()
    agg['avg_owners_per_game'] = agg['sum_owners'] / agg['n_titles']

    # b) tier flags
    agg['multi']      = agg['n_titles'] >= 2
    agg['strict_aaa'] = (
        (agg['n_titles']           >= STRICT_AAA['min_games']) &
        (agg['avg_owners_per_game'] >= STRICT_AAA['min_avg_owners']) &
        (agg['max_owners']         >= STRICT_AAA['min_max_owners'])
    )
    agg['broad_aaa'] = (
        (agg['n_titles']           >= BROAD_AAA['min_games']) &
        (agg['avg_owners_per_game'] >= BROAD_AAA['min_avg_owners']) &
        (agg['max_owners']         >= BROAD_AAA['min_max_owners'])
    )
    agg['aa_plus'] = (
        (agg['n_titles']           >= AA_PLUS['min_games']) &
        (agg['avg_owners_per_game'] >= AA_PLUS['min_avg_owners'])
    )

    # c) activity from looser cohort
    act = activity[activity['developer'].notna()].copy()
    act['release_date'] = pd.to_datetime(act['release_date'], errors='coerce')
    latest = act.groupby('developer').agg(
        latest_release=('release_date', 'max'),
        earliest_release=('release_date', 'min'),
    ).reset_index()
    latest['years_since_latest'] = (
        (REF_DATE - latest['latest_release']).dt.days / 365.25
    )
    latest['career_span_years'] = (
        (REF_DATE - latest['earliest_release']).dt.days / 365.25
    )

    agg = agg.merge(
        latest[['developer', 'latest_release', 'earliest_release',
                'years_since_latest', 'career_span_years']],
        on='developer', how='left'
    )

    # d) drop dormant + unknown
    not_dormant = (
        agg['years_since_latest'].notna() &
        (agg['years_since_latest'] < DORMANT_YEARS)
    )
    agg = agg[not_dormant].copy()

    # e) cohort assignment
    c1_mask = agg['multi'] & ~agg['aa_plus']
    c2_mask = agg['aa_plus'] & ~agg['broad_aaa']
    agg['cohort'] = np.where(c1_mask, 'C1', np.where(c2_mask, 'C2', None))
    cohorts = agg[agg['cohort'].notna()].copy()

    return cohorts[[
        'developer', 'cohort', 'n_titles',
        'sum_owners', 'max_owners', 'avg_owners_per_game',
        'strict_aaa', 'broad_aaa', 'aa_plus', 'multi',
        'latest_release', 'earliest_release',
        'years_since_latest', 'career_span_years',
    ]]


# ============================================================================
# STAGE 4 — PCI (HHI on owners shares per dev)
# ============================================================================
def stage4_pci(clean: pd.DataFrame, cohorts: pd.DataFrame) -> pd.DataFrame:
    """For each dev, PCI = sum((owners_g / total_owners)^2). HHI-style."""
    rows = []
    for dev, sub in clean.groupby('developer'):
        owners = sub['owners_lower'].fillna(0).values
        total = owners.sum()
        if total <= 0:
            continue
        shares = owners / total
        pci = float((shares ** 2).sum())
        n_resolvable = int((owners > 0).sum())
        rows.append({
            'developer': dev,
            'pci': pci,
            'n_titles_resolvable': n_resolvable,
            'total_owners': int(total),
        })
    pci_df = pd.DataFrame(rows)
    pci_df = pci_df.merge(cohorts[['developer', 'cohort']], on='developer', how='inner')

    def categorize(p):
        for cat, (lo, hi) in PCI_BINS.items():
            if lo <= p < hi:
                return cat
        return None
    pci_df['pci_category'] = pci_df['pci'].apply(categorize)
    return pci_df


# ============================================================================
# STAGE 5 — PCI-RESOLVABLE FILTER
# ============================================================================
def stage5_resolvable(pci_df: pd.DataFrame) -> pd.DataFrame:
    """Keep only devs with >= 2 measurable-owners titles (PCI is meaningful)."""
    return pci_df[pci_df['n_titles_resolvable'] >= 2].copy()


# ============================================================================
# STAGE 6 — QUALITY CLEANUP (3 exclusion lists)
# ============================================================================
def stage6_cleanup(pci_resolvable: pd.DataFrame,
                   exclusion_files: dict) -> tuple[pd.DataFrame, dict]:
    """Drop devs flagged in moderate-indie exclusions (6a), Round 1 shovelware (6b),
    Round 2 volume+engagement audit (6c). Returns cleaned df and step counts."""
    counts = {'before': len(pci_resolvable)}
    out = pci_resolvable.copy()

    for stage_name, path in exclusion_files.items():
        if not path or not os.path.exists(path):
            continue
        excl = pd.read_csv(path)
        devs_to_drop = set(excl['developer'])
        before = len(out)
        out = out[~out['developer'].isin(devs_to_drop)]
        counts[stage_name] = before - len(out)

    counts['after'] = len(out)
    return out, counts


# ============================================================================
# STAGE 7 — RESTRICT TO MODERATE + CONCENTRATED
# ============================================================================
def stage7_moderate_concentrated(pci_clean: pd.DataFrame) -> pd.DataFrame:
    """Drop diversified and one-hit categories; these aren't the testing targets."""
    return pci_clean[pci_clean['pci_category'].isin(['moderate', 'concentrated'])].copy()


# ============================================================================
# STAGE 8 — SUSPECT BATTERY (9 tests)
# ============================================================================
def _compute_dev_engagement_metrics(df_dev: pd.DataFrame) -> dict | None:
    """Compute the per-dev metrics used by the 9 suspect tests."""
    n = len(df_dev)
    if n < 2:
        return None
    span_days = (df_dev['release_date'].max() - df_dev['release_date'].min()).days
    span_years = max(span_days / 365.25, 1.0)
    titles_per_year = n / span_years

    reviews = df_dev['total_reviews'].fillna(0)
    pct_zero_rev = (reviews == 0).mean() * 100
    pct_lt5_rev = (reviews < 5).mean() * 100
    pct_ge100_rev = (reviews >= 100).mean() * 100
    median_rev = reviews.median()
    rev_cv = reviews.std() / max(reviews.mean(), 1)

    price = df_dev['price_usd'].fillna(0)
    median_price = price.median()
    pct_le199 = (price <= 1.99).mean() * 100
    pct_le099 = (price <= 0.99).mean() * 100

    owners = df_dev['owners_lower'].fillna(0)
    pct_owners_zero = (owners == 0).mean() * 100

    pt = pd.to_numeric(df_dev.get('playtime_median_forever', 0), errors='coerce').fillna(0)
    median_playtime_min = pt.median()

    n_publishers = df_dev['publisher'].nunique()

    if 'genres_list' in df_dev.columns:
        all_g = set()
        for g in df_dev['genres_list'].dropna():
            if isinstance(g, list):
                all_g.update(g)
        n_genres = len(all_g)
    else:
        n_genres = np.nan

    langs = df_dev.get('languages', pd.Series(['']*n)).fillna('').astype(str)
    def frac(token):
        return langs.str.contains(token, regex=False).sum() / max(n, 1)
    lang_fractions = {k: frac(k) for k in
                      ['Russian','Chinese','Japanese','Korean','Polish','German',
                       'French','Italian','Spanish','Portuguese - Brazil','Turkish']}
    lang_str = '; '.join(f"{k}:{v:.0%}" for k, v in lang_fractions.items() if v > 0)

    return dict(
        num_titles=n,
        career_span_years=round(span_years, 2),
        titles_per_year=round(titles_per_year, 2),
        median_price=round(median_price, 2),
        pct_price_le199=round(pct_le199, 1),
        pct_price_le099=round(pct_le099, 1),
        median_reviews=median_rev,
        pct_zero_reviews=round(pct_zero_rev, 1),
        pct_lt5_reviews=round(pct_lt5_rev, 1),
        pct_ge100_reviews=round(pct_ge100_rev, 1),
        reviews_cv=round(rev_cv, 2),
        pct_owners_zero=round(pct_owners_zero, 1),
        median_playtime_min=median_playtime_min,
        n_publishers=n_publishers,
        n_unique_genres=n_genres,
        languages_concat=lang_str,
    )


def _score_suspect(m: dict) -> tuple[int, str]:
    """9-test suspect battery. Returns (score, semicolon-separated flags)."""
    flags = []
    pts = 0
    # T1 cadence (>2/yr elevated)
    tpy = m['titles_per_year']
    if tpy >= 15:   flags.append('T1_extreme_cadence(>=15/yr)');     pts += 3
    elif tpy >= 8:  flags.append('T1_very_high_cadence(>=8/yr)');    pts += 3
    elif tpy >= 4:  flags.append('T1_high_cadence(>=4/yr)');         pts += 2
    elif tpy > 2:   flags.append('T1_elevated_cadence(>2/yr)');      pts += 1
    # T2 engagement collapse
    if m['pct_lt5_reviews'] >= 60:   flags.append('T2_severe_engagement_collapse(>=60%<5rev)'); pts += 3
    elif m['pct_lt5_reviews'] >= 40: flags.append('T2_engagement_collapse(>=40%<5rev)');        pts += 2
    # T3 price floor + low engagement
    if m['pct_price_le099'] >= 50 and m['median_reviews'] < 30:
        flags.append('T3_dollar_store_pricing'); pts += 2
    elif m['pct_price_le199'] >= 50 and m['median_reviews'] < 30:
        flags.append('T3_low_price_low_engagement'); pts += 1
    # T4 owners floor
    if m['pct_owners_zero'] >= 80: flags.append('T4_owners_floor(>=80%in0bucket)'); pts += 2
    # T5 zero-review share
    if m['pct_zero_reviews'] >= 30: flags.append('T5_high_zero_reviews(>=30%)'); pts += 2
    # T6 playtime collapse
    if 0 < m['median_playtime_min'] < 10: flags.append('T6_no_playtime(<10min median)'); pts += 1
    # T7 uniform mediocrity
    if m['reviews_cv'] < 0.5 and m['num_titles'] >= 10 and m['median_reviews'] < 30:
        flags.append('T7_uniform_low_engagement'); pts += 1
    # T8 single-publisher factory
    if m['n_publishers'] == 1 and m['num_titles'] >= 30 and m['median_reviews'] < 30:
        flags.append('T8_single_publisher_factory'); pts += 1
    # T9 genre scattershot
    if m['num_titles'] >= 10 and m['n_unique_genres'] >= 5 and m['median_reviews'] < 20:
        flags.append('T9_genre_scattershot'); pts += 1
    return pts, '; '.join(flags)


def _bucket(score: int) -> str:
    if score >= SUSPECT_BUCKET_THRESHOLDS['HIGH_SUSPECT']: return 'HIGH_SUSPECT'
    if score >= SUSPECT_BUCKET_THRESHOLDS['MEDIUM_SUSPECT']: return 'MEDIUM_SUSPECT'
    if score >= SUSPECT_BUCKET_THRESHOLDS['LOW_SUSPECT']: return 'LOW_SUSPECT'
    return 'CLEAR'


def stage8_suspect_battery(clean: pd.DataFrame, target_devs: pd.DataFrame,
                            spy_path: str | None = None) -> pd.DataFrame:
    """Score every dev in target_devs with the 9-test battery."""
    if spy_path and os.path.exists(spy_path):
        spy = pd.read_csv(spy_path, engine='python', on_bad_lines='skip')
        rename = {'median_forever': 'playtime_median_forever',
                  'average_forever': 'playtime_average_forever'}
        spy = spy.rename(columns={k: v for k, v in rename.items() if k in spy.columns})
        keep = [c for c in ['app_id', 'playtime_median_forever', 'languages'] if c in spy.columns]
        clean = clean.merge(spy[keep], on='app_id', how='left')
    if 'playtime_median_forever' not in clean.columns:
        clean['playtime_median_forever'] = np.nan
    if 'languages' not in clean.columns:
        clean['languages'] = ''

    devs = set(target_devs['developer'])
    sub = clean[clean['developer'].isin(devs)]
    rows = []
    for dev, gp in sub.groupby('developer'):
        m = _compute_dev_engagement_metrics(gp)
        if m is None:
            continue
        score, flags = _score_suspect(m)
        m.update(developer=dev, suspect_score=score, suspect_flags=flags,
                 suspect_bucket=_bucket(score))
        rows.append(m)
    return pd.DataFrame(rows)


# ============================================================================
# STAGE 9 — TRAJECTORY CLASSIFICATION
# ============================================================================
def _trajectory_metrics(df_dev: pd.DataFrame) -> dict | None:
    df = df_dev.sort_values('release_date').reset_index(drop=True)
    n = len(df)
    owners = df['owners_lower'].fillna(0).values
    total = owners.sum()
    if n < 2 or total <= 0:
        return None
    anchor_idx = int(np.argmax(owners))
    anchor_owners = owners[anchor_idx]
    anchor_age = (REF_DATE - df.loc[anchor_idx, 'release_date']).days / 365.25
    anchor_recency_rank = anchor_idx / (n - 1)
    anchor_share = anchor_owners / total

    span_days = (df['release_date'].max() - df['release_date'].min()).days
    if span_days < 30:
        early_half = late_half = total / 2
    else:
        mid = df['release_date'].min() + pd.Timedelta(days=span_days / 2)
        em = df['release_date'] <= mid
        early_half = owners[em.values].sum()
        late_half = owners[~em.values].sum()
    traj_ratio = (late_half + TRAJECTORY_SMOOTH_K) / (early_half + TRAJECTORY_SMOOTH_K)
    cutoff = REF_DATE - pd.Timedelta(days=2 * 365.25)
    rm = df['release_date'] >= cutoff
    velocity_pct = owners[rm.values].sum() / max(total, 1) * 100

    return dict(
        anchor_title=df.loc[anchor_idx, 'name'],
        anchor_age_years=round(anchor_age, 2),
        anchor_recency_rank=round(anchor_recency_rank, 3),
        anchor_share=round(anchor_share, 3),
        late_to_early_ratio=round(traj_ratio, 2),
        velocity_pct_last2yr=round(velocity_pct, 1),
        total_owners_traj=int(total),
    )


def _classify_trajectory(r: dict) -> str:
    if r['anchor_share'] >= TRAJECTORY_ANCHOR_SHARE:
        age = r['anchor_age_years']
        if age <= TRAJECTORY_ANCHOR_AGE_BANDS['recent']: return 'ANCHOR_RECENT'
        if age <= TRAJECTORY_ANCHOR_AGE_BANDS['mature']: return 'ANCHOR_MATURE'
        return 'ANCHOR_AGING'
    ratio = r['late_to_early_ratio']
    recency = r['anchor_recency_rank']
    if ratio >= TRAJECTORY_RISING_RATIO or (ratio >= 1.5 and recency >= 0.5): return 'RISING'
    if ratio <= TRAJECTORY_FALLING_RATIO or (ratio <= 0.66 and recency <= 0.5): return 'FALLING'
    return 'STEADY'


def stage9_trajectory(clean: pd.DataFrame, target_devs: pd.DataFrame) -> pd.DataFrame:
    devs = set(target_devs['developer'])
    sub = clean[clean['developer'].isin(devs)]
    rows = []
    for dev, gp in sub.groupby('developer'):
        m = _trajectory_metrics(gp)
        if m is None:
            continue
        m['developer'] = dev
        m['trajectory'] = _classify_trajectory(m)
        rows.append(m)
    return pd.DataFrame(rows)


# ============================================================================
# STAGE 10 — COUNTRY INFERENCE
# ============================================================================
RUSSIAN_NAME_PARTS = ['ovich', 'evich', 'ovna', 'evna', 'enko',
                      'dmitr', 'sergei', 'sergey', 'nikita', 'stas']
JAPANESE_HINTS = ['Co.,Ltd', 'Co., Ltd', 'Co.,Ltd.', 'Japan']
GERMAN_HINTS = [' UG', ' GmbH', ' UG ', ' UG)', 'UG (', 'e.K.', 'GbR']
ITALIAN_HINTS = ['S.r.l.', 'S.r.l', 'SRL ', ' s.r.l']
POLISH_HINTS = ['Sp. z o.o.', 'Sp. z o. o.', 'Sp z o.o.']
CHINESE_HINTS = ['(Beijing)', '(Shanghai)', '(Shenzhen)', 'Tencent', 'NetEase']
FRENCH_HINTS = ['SARL ', 'SAS ', ' SAS', 'Ubisoft']
SPANISH_HINTS = ['S.L.', 'S.L ', 'SL ']
UK_HINTS = ['Ltd', 'Ltd.', 'Limited']


def _infer_country(dev_name: str, languages_concat: str) -> str:
    if any(h in dev_name for h in GERMAN_HINTS): return 'Germany'
    if any(h in dev_name for h in ITALIAN_HINTS): return 'Italy'
    if any(h in dev_name for h in POLISH_HINTS): return 'Poland'
    if any(h in dev_name for h in CHINESE_HINTS): return 'China'
    if any(h in dev_name for h in JAPANESE_HINTS): return 'Japan/Korea/Asia'
    if any(h in dev_name for h in FRENCH_HINTS): return 'France'
    if any(h in dev_name for h in SPANISH_HINTS): return 'Spain'
    if any(p in dev_name.lower() for p in RUSSIAN_NAME_PARTS): return 'Russia/CIS'

    lf = {}
    for part in languages_concat.split('; '):
        if ':' in part:
            k, v = part.rsplit(':', 1)
            try: lf[k] = float(v.rstrip('%')) / 100
            except: pass
    dominant = {k: v for k, v in lf.items() if v >= 0.70}
    if len(dominant) > 2: return 'Unknown/Global-localizer'
    mapping = {'Russian':'Russia/CIS (lang only)', 'Chinese':'China (lang only)',
               'Japanese':'Japan (lang only)', 'Korean':'Korea (lang only)',
               'Polish':'Poland (lang only)', 'Portuguese - Brazil':'Brazil (lang only)',
               'Turkish':'Turkey (lang only)', 'German':'Germany (lang only)',
               'French':'France (lang only)', 'Italian':'Italy (lang only)'}
    if dominant:
        best = max(dominant, key=dominant.get)
        if best in mapping: return mapping[best]
    if any(h in dev_name for h in UK_HINTS): return 'UK/EN (Ltd suffix)'
    return 'Unknown/EN-default'


def stage10_country(merged: pd.DataFrame) -> pd.DataFrame:
    merged['country_guess'] = merged.apply(
        lambda r: _infer_country(r['developer'], r.get('languages_concat', '')), axis=1)
    return merged


# ============================================================================
# STAGE 11 — INVESTOR-CANDIDATE SCORING
# ============================================================================
def _investor_score(r) -> float:
    s = np.log10(r['total_owners'] + 1)
    s += r['velocity_pct_last2yr'] / 50
    age = r['anchor_age_years']
    if age <= 1: s += 1.5
    elif age <= 2: s += 1.0
    elif age <= 3: s += 0.5
    if r['trajectory'] == 'RISING' and r['late_to_early_ratio'] >= 3:
        s += 0.5
    return round(s, 2)


def stage11_candidates(merged: pd.DataFrame) -> pd.DataFrame:
    cand = merged[
        merged['trajectory'].isin(CANDIDATE_TRAJECTORIES) &
        (merged['suspect_bucket'] == CANDIDATE_SUSPECT_BUCKET)
    ].copy()
    cand['investor_score'] = cand.apply(_investor_score, axis=1)
    return cand.sort_values('investor_score', ascending=False)


# ============================================================================
# MAIN PIPELINE
# ============================================================================
def run_pipeline(data_dir: str, out_dir: str,
                 exclusion_files: dict | None = None,
                 spy_path: str | None = None,
                 verbose: bool = True) -> dict:
    """Run the full pipeline. Saves intermediate CSVs and returns step-count summary."""
    os.makedirs(out_dir, exist_ok=True)
    def log(msg):
        if verbose: print(msg)
    summary = {}

    # 0-2: load + clean (strict cohort + looser activity cohort)
    base = stage0_load(data_dir); summary['stage0_raw'] = len(base); log(f"[0] raw rows: {len(base):,}")
    clean = stage12_clean(base); summary['stage12_clean'] = len(clean); log(f"[1-2] hygiene+structural (strict): {len(clean):,}")
    activity = stage12_activity(base); summary['stage12_activity'] = len(activity)
    log(f"[1-2b] hygiene+structural (looser, EA+demos restored): {len(activity):,}")

    # 3: cohort assignment (faithful two_cohorts.py logic)
    cohorts = stage3_cohorts(clean, activity)
    n_c1 = int((cohorts['cohort'] == 'C1').sum())
    n_c2 = int((cohorts['cohort'] == 'C2').sum())
    summary['stage3_cohorted_devs'] = len(cohorts)
    summary['stage3_c1'] = n_c1
    summary['stage3_c2'] = n_c2
    log(f"[3] cohorted devs (post-dormancy): {len(cohorts):,}  ({n_c1} C1 / {n_c2} C2)")

    # 4: PCI for cohorted devs only (restrict clean to cohort devs first)
    cohort_devs = set(cohorts['developer'])
    clean_for_pci = clean[clean['developer'].isin(cohort_devs)]
    pci = stage4_pci(clean_for_pci, cohorts)
    summary['stage4_pci_devs'] = len(pci)
    log(f"[4] PCI computed: {len(pci):,}")

    # 5: PCI-resolvable (>=2 measurable-owners titles)
    resolvable = stage5_resolvable(pci)
    r_c1 = int((resolvable['cohort'] == 'C1').sum())
    r_c2 = int((resolvable['cohort'] == 'C2').sum())
    summary['stage5_resolvable'] = len(resolvable)
    summary['stage5_resolvable_c1'] = r_c1
    summary['stage5_resolvable_c2'] = r_c2
    log(f"[5] PCI-resolvable (>=2 measurable titles): {len(resolvable):,}  ({r_c1} C1 / {r_c2} C2)")

    # 6: cleanup
    if exclusion_files is None:
        exclusion_files = {
            'stage6a_mod_indie_excl': '/home/user/workspace/moderate_indie_exclusions.csv',
            'stage6b_shovelware_r1': '/home/user/workspace/pci_resolvable_removed_shovelware.csv',
            'stage6c_audit_r2':      '/home/user/workspace/pci_resolvable_excluded_round2.csv',
        }
    cleaned, ex_counts = stage6_cleanup(resolvable, exclusion_files)
    summary.update({f"stage6_{k}": v for k, v in ex_counts.items()})
    log(f"[6] After quality cleanup: {len(cleaned):,}  (dropped: 6a={ex_counts.get('stage6a_mod_indie_excl', 0)}, 6b={ex_counts.get('stage6b_shovelware_r1', 0)}, 6c={ex_counts.get('stage6c_audit_r2', 0)})")

    # 7: moderate + concentrated
    mc = stage7_moderate_concentrated(cleaned)
    mc_c1 = int((mc['cohort'] == 'C1').sum())
    mc_c2 = int((mc['cohort'] == 'C2').sum())
    summary['stage7_moderate_concentrated'] = len(mc)
    summary['stage7_mc_c1'] = mc_c1
    summary['stage7_mc_c2'] = mc_c2
    log(f"[7] Moderate + concentrated: {len(mc):,}  ({mc_c1} C1 / {mc_c2} C2)")

    # 8: suspect battery
    sus = stage8_suspect_battery(clean, mc, spy_path=spy_path)
    log(f"[8] Suspect battery scored: {len(sus):,}")

    # 9: trajectory
    traj = stage9_trajectory(clean, mc)
    log(f"[9] Trajectory classified: {len(traj):,}")

    # Merge mc + suspect + trajectory
    merged = mc.merge(sus, on='developer', how='left')
    merged = merged.merge(traj, on='developer', how='left')

    # 10: country
    merged = stage10_country(merged)
    log(f"[10] Country inferred for {merged['country_guess'].notna().sum():,}")

    # 11: candidates
    candidates = stage11_candidates(merged)
    cand_c1 = int((candidates['cohort'] == 'C1').sum())
    cand_c2 = int((candidates['cohort'] == 'C2').sum())
    cand_rising = int((candidates['trajectory'] == 'RISING').sum())
    cand_anchor = int((candidates['trajectory'] == 'ANCHOR_RECENT').sum())
    summary['stage11_candidates'] = len(candidates)
    summary['stage11_c1'] = cand_c1
    summary['stage11_c2'] = cand_c2
    summary['stage11_rising'] = cand_rising
    summary['stage11_anchor_recent'] = cand_anchor
    log(f"[11] Final investor candidates: {len(candidates):,}  ({cand_c1} C1 / {cand_c2} C2)")
    log(f"     {cand_rising} RISING / {cand_anchor} ANCHOR_RECENT")

    # Save
    merged.to_csv(f"{out_dir}/all_moderate_concentrated_scored.csv", index=False)
    candidates.to_csv(f"{out_dir}/investor_candidates.csv", index=False)
    cohorts.to_csv(f"{out_dir}/cohorts_full.csv", index=False)
    resolvable.to_csv(f"{out_dir}/pci_resolvable.csv", index=False)

    # Reconciliation table — stage-by-stage counts vs target
    target = {
        'stage0_raw': 140082,
        'stage12_clean': 64320,
        'stage3_cohorted_devs': 6833,
        'stage5_resolvable': 1610,
        'stage6_after': 1551,
        'stage7_moderate_concentrated': 1210,
        'stage11_candidates': 146,
    }
    recon_rows = []
    stage_labels = [
        ('stage0_raw',                  'Stage 0  — Raw load'),
        ('stage12_clean',               'Stage 1-2 — Hygiene + Structural (strict)'),
        ('stage12_activity',            'Stage 1-2b — Activity cohort (looser, for dormancy)'),
        ('stage3_cohorted_devs',        'Stage 3  — Cohorts (post-dormancy 5y)'),
        ('stage3_c1',                   '         · Cohort 1 (multi & NOT aa_plus)'),
        ('stage3_c2',                   '         · Cohort 2 (aa_plus & NOT broad_aaa)'),
        ('stage4_pci_devs',             'Stage 4  — PCI computed (devs with owners>0)'),
        ('stage5_resolvable',           'Stage 5  — PCI-resolvable (>=2 measurable titles)'),
        ('stage5_resolvable_c1',        '         · C1 resolvable'),
        ('stage5_resolvable_c2',        '         · C2 resolvable'),
        ('stage6_stage6a_mod_indie_excl', 'Stage 6a — Moderate-indie exclusions dropped'),
        ('stage6_stage6b_shovelware_r1',  'Stage 6b — Shovelware R1 dropped'),
        ('stage6_stage6c_audit_r2',       'Stage 6c — Volume+engagement R2 dropped'),
        ('stage6_after',                'Stage 6  — After all exclusions'),
        ('stage7_moderate_concentrated','Stage 7  — Moderate + concentrated only'),
        ('stage7_mc_c1',                '         · C1 mod+conc'),
        ('stage7_mc_c2',                '         · C2 mod+conc'),
        ('stage11_candidates',          'Stage 11 — Final candidates (RISING/ANCHOR_RECENT & CLEAR)'),
        ('stage11_c1',                  '         · C1 candidates'),
        ('stage11_c2',                  '         · C2 candidates'),
        ('stage11_rising',              '         · RISING'),
        ('stage11_anchor_recent',       '         · ANCHOR_RECENT'),
    ]
    for key, label in stage_labels:
        actual = summary.get(key)
        tgt = target.get(key, '')
        delta = ''
        status = ''
        if isinstance(actual, (int, float)) and tgt != '':
            d = int(actual) - int(tgt)
            delta = f"{d:+d}"
            status = 'MATCH' if d == 0 else ('CLOSE' if abs(d) <= max(5, int(tgt) * 0.01) else 'DIFF')
        recon_rows.append(dict(
            stage_key=key, stage=label,
            actual=actual, target=tgt, delta=delta, status=status,
        ))
    recon = pd.DataFrame(recon_rows)
    recon.to_csv(f"{out_dir}/pipeline_summary.csv", index=False)

    # Also print reconciliation table
    log("\n" + "=" * 92)
    log("RECONCILIATION TABLE — actual vs locked target")
    log("=" * 92)
    log(f"{'STAGE':<60} {'ACTUAL':>10} {'TARGET':>10} {'DELTA':>7}  STATUS")
    log("-" * 92)
    for r in recon_rows:
        a = '' if r['actual'] is None else f"{int(r['actual']):,}"
        t = '' if r['target'] == '' else f"{int(r['target']):,}"
        log(f"{r['stage'][:60]:<60} {a:>10} {t:>10} {r['delta']:>7}  {r['status']}")
    log("=" * 92)
    log(f"\nSaved to {out_dir}/")
    return summary


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(description="Run the investor-candidate pipeline on a Steam dataset.")
    p.add_argument('--data', default='/home/user/workspace/steam-threshold-app/data',
                   help='Directory with games/genres/tags/categories/steamspy_insights/reviews CSVs')
    p.add_argument('--out', default='/home/user/workspace/pipeline_run',
                   help='Output directory')
    p.add_argument('--spy', default='/home/user/workspace/steam-threshold-app/data/steamspy_insights.csv',
                   help='Path to steamspy_insights.csv (for playtime + languages)')
    args = p.parse_args()
    run_pipeline(data_dir=args.data, out_dir=args.out, spy_path=args.spy)
