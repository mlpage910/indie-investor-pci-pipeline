"""
Build two parallel watchlist cohorts:
  Cohort 1: Non-AAA multi-release, non-dormant   (sub-AA+, ≥2 games, last release <5y)
  Cohort 2: AA+ but NOT AAA, multi-release, non-dormant (AA+ minus Broad AAA, last release <5y)
Both qualify on STRUCTURAL (EA-excluded) cohort.
Activity (latest_release) is measured against the LOOSER activity cohort (EA + demos allowed back).
"""
import sys
sys.path.insert(0, '/home/user/workspace/steam-threshold-app')
from loader import load
from filters import apply_all
import numpy as np
import pandas as pd

df = load('/home/user/workspace/steam-threshold-app/data')

# Qualifying (structural, EA excluded)
res_struct = apply_all(df, hyg={}, struct={}, ana={})
struct = res_struct[0] if isinstance(res_struct, tuple) else res_struct

# Activity cohort (EA + demos allowed back)
res_act = apply_all(df, hyg={}, struct={'exclude_early_access': False, 'exclude_demos': False}, ana={})
activity = res_act[0] if isinstance(res_act, tuple) else res_act

print(f"Qualifying (structural, no EA): {len(struct):,}")
print(f"Activity (EA + demos restored): {len(activity):,}")

# Aggregate per developer on qualifying cohort
def aggregate(d):
    g = d[d['developer'].notna()].groupby('developer').agg(
        games=('total_reviews','size'),
        sum_owners_lower=('owners_lower','sum'),
        max_owners_lower=('owners_lower','max'),
        sum_reviews=('total_reviews','sum'),
        max_reviews=('total_reviews','max'),
    ).reset_index()
    g['avg_owners_per_game'] = g['sum_owners_lower'] / g['games']
    g['avg_reviews_per_game'] = g['sum_reviews'] / g['games']
    return g

agg = aggregate(struct)
print(f"Distinct devs (qualifying): {len(agg):,}")

# Tier assignment (same as locked)
agg['strict_aaa'] = (agg['games']>=3) & (agg['avg_owners_per_game']>=1_000_000) & (agg['max_owners_lower']>=2_000_000)
agg['broad_aaa']  = (agg['games']>=5) & (agg['avg_owners_per_game']>=100_000)   & (agg['max_owners_lower']>=500_000)
agg['aa_plus']    = (agg['games']>=2) & (agg['avg_owners_per_game']>=50_000)
agg['multi']      = agg['games']>=2

print(f"\nTier counts on qualifying:")
print(f"  Strict AAA: {agg['strict_aaa'].sum():,}")
print(f"  Broad AAA:  {agg['broad_aaa'].sum():,}")
print(f"  AA+ total:  {agg['aa_plus'].sum():,}")
print(f"  Multi (≥2g):{agg['multi'].sum():,}")

# Define the two source pools (BEFORE activity filter)
# Cohort 2 source: AA+ AND NOT Broad AAA (exclude AAA tier from AA+ band)
aa_only_pool = agg[agg['aa_plus'] & ~agg['broad_aaa']].copy()
# Cohort 1 source: multi-release AND NOT AA+ (sub-AA+)
non_aaa_multi_pool = agg[agg['multi'] & ~agg['aa_plus']].copy()

print(f"\nCohort source pools (before activity filter):")
print(f"  AA+ only (excl Broad AAA): {len(aa_only_pool):,}")
print(f"  Non-AAA multi (sub-AA+):   {len(non_aaa_multi_pool):,}")

# Compute latest release per dev from activity cohort
SCRAPE_CUTOFF = pd.Timestamp('2024-10-28')
act = activity.copy()
act['release_date'] = pd.to_datetime(act['release_date'], errors='coerce')
latest = act.groupby('developer').agg(
    total_titles_seen=('release_date','size'),
    latest_release=('release_date','max'),
    earliest_release=('release_date','min'),
).reset_index()
latest['years_since_latest'] = (SCRAPE_CUTOFF - latest['latest_release']).dt.days / 365.25
latest['career_span_years']  = (SCRAPE_CUTOFF - latest['earliest_release']).dt.days / 365.25

# Merge and segment each pool
def build_cohort(pool, label):
    m = pool.merge(latest, on='developer', how='left')
    # career-stage segmentation (within non-dormant only)
    def stage(r):
        if pd.isna(r['years_since_latest']):
            return 'unknown'
        if r['years_since_latest'] >= 5:
            return 'dormant'
        # non-dormant: split by career length
        if r['career_span_years'] < 3:
            return 'up_and_coming'
        if r['career_span_years'] < 10:
            if r['years_since_latest'] < 2:
                return 'mid_career_active'
            return 'mid_zone'
        # career ≥10y
        if r['years_since_latest'] < 2:
            return 'established_active'
        return 'mid_zone'
    m['stage'] = m.apply(stage, axis=1)
    # Non-dormant cohort = everything that's not dormant and not unknown
    non_dormant = m[~m['stage'].isin(['dormant','unknown'])].copy()
    print(f"\n=== {label} ===")
    print(f"  Source pool: {len(m):,}")
    print(f"  Stage breakdown:")
    print(m['stage'].value_counts().to_string())
    print(f"  Non-dormant total: {len(non_dormant):,}  ({len(non_dormant)/len(m)*100:.1f}%)")
    return m, non_dormant

aa_full, aa_active = build_cohort(aa_only_pool, "Cohort 2: AA+ (excl Broad AAA), all stages")
nonaaa_full, nonaaa_active = build_cohort(non_aaa_multi_pool, "Cohort 1: Non-AAA multi-release, all stages")

# Save both full tables (with stage column) for follow-up
aa_full.to_csv('/home/user/workspace/cohort2_aaplus_only.csv', index=False)
nonaaa_full.to_csv('/home/user/workspace/cohort1_nonaaa_multi.csv', index=False)
aa_active.to_csv('/home/user/workspace/cohort2_aaplus_nondormant.csv', index=False)
nonaaa_active.to_csv('/home/user/workspace/cohort1_nonaaa_nondormant.csv', index=False)

# Summary stats per cohort
def stats_block(cohort, label):
    print(f"\n=== {label} — non-dormant stats ===")
    print(f"  n = {len(cohort):,}")
    print(f"  games/dev: median={cohort['games'].median():.0f}  mean={cohort['games'].mean():.1f}  max={int(cohort['games'].max())}")
    print(f"  career span: median={cohort['career_span_years'].median():.1f}y  p25={cohort['career_span_years'].quantile(.25):.1f}  p75={cohort['career_span_years'].quantile(.75):.1f}")
    print(f"  years since latest: median={cohort['years_since_latest'].median():.1f}y")
    print(f"  avg_owners/game: median={int(cohort['avg_owners_per_game'].median()):,}  mean={int(cohort['avg_owners_per_game'].mean()):,}")
    print(f"  avg_reviews/game: median={int(cohort['avg_reviews_per_game'].median()):,}  mean={int(cohort['avg_reviews_per_game'].mean()):,}")
    print(f"  Stage mix:")
    print(cohort['stage'].value_counts().to_string())

stats_block(aa_active,    "Cohort 2: AA+ only (excl Broad AAA), non-dormant")
stats_block(nonaaa_active,"Cohort 1: Non-AAA multi-release, non-dormant")

print('\nSaved:')
print('  /home/user/workspace/cohort1_nonaaa_multi.csv (all stages)')
print('  /home/user/workspace/cohort1_nonaaa_nondormant.csv')
print('  /home/user/workspace/cohort2_aaplus_only.csv (all stages)')
print('  /home/user/workspace/cohort2_aaplus_nondormant.csv')
