"""Compute title counts for each dev-level pipeline stage.

Use the pipeline's own loader + filters (so structural pool matches Stage 1-2 = 64,320)
and then count, for each downstream dev set, how many structural-pool titles
belong to those devs.
"""
import sys
from pathlib import Path
import pandas as pd

WS = Path("/home/user/workspace")
sys.path.insert(0, str(WS / "steam-threshold-app"))

# Use the SAME loader the pipeline uses
from loader import load
from filters import apply_all

# Match investor_pipeline.py HYGIENE + STRUCTURAL constants
HYGIENE = dict(
    require_developer=True,
    require_publisher=True,
    require_release_date=True,
    drop_paid_no_price=True,
    drop_future_release=True,
)
STRUCTURAL = dict(
    exclude_demos=True,
    exclude_free_to_play=True,
    require_english=True,
    require_us_available=True,
    exclude_early_access=True,
)

print("Loading base catalog via pipeline loader...")
base = load(str(WS / "steam-threshold-app" / "data"))
print(f"  base rows: {len(base):,}")
print(f"  base columns: {list(base.columns)[:15]} ...")

print("\nApplying HYGIENE + STRUCTURAL filters...")
clean, _ = apply_all(base, HYGIENE, STRUCTURAL, {})
clean['release_date'] = pd.to_datetime(clean['release_date'], errors='coerce')
clean = clean.dropna(subset=['release_date', 'owners_lower'])
print(f"  structural titles: {len(clean):,}  (target 64,320)")

# --- Load dev sets ---------------------------------------------------------
PIPE = WS / "pipeline_run"
cohorts = pd.read_csv(PIPE / "cohorts_full.csv")
pci_res = pd.read_csv(PIPE / "pci_resolvable.csv")
mod_conc = pd.read_csv(PIPE / "all_moderate_concentrated_scored.csv")
candidates = pd.read_csv(PIPE / "investor_candidates.csv")

# Stage 6 dev set = pci_resolvable MINUS the 3 exclusion lists
excl_devs = set()
for path in [
    WS / "moderate_indie_exclusions.csv",
    WS / "pci_resolvable_removed_shovelware.csv",
    WS / "pci_resolvable_excluded_round2.csv",
]:
    if path.exists():
        df = pd.read_csv(path)
        if "developer" in df.columns:
            n0 = len(excl_devs)
            excl_devs |= set(df["developer"].astype(str))
            print(f"  excl file {path.name}: {len(df)} rows, added {len(excl_devs)-n0} new devs")

stage6_devs = set(pci_res["developer"].astype(str)) - excl_devs
print(f"\nStage 6 devs reconstructed: {len(stage6_devs):,}  (target 1,551)")

# --- Count titles per dev set ----------------------------------------------
struct_dev = clean["developer"].astype(str)

def title_count(dev_set):
    return int(struct_dev.isin(dev_set).sum())

cohort_devs = set(cohorts["developer"].astype(str))
pci_devs = set(pci_res["developer"].astype(str))
mc_devs = set(mod_conc["developer"].astype(str))
cand_devs = set(candidates["developer"].astype(str))

print("\n" + "=" * 80)
print("STAGE-BY-STAGE FUNNEL — TITLES (in structural pool) and DEVELOPERS")
print("=" * 80)

rows = [
    ("Raw scrape (October 2024)",
        len(base), base["developer"].nunique() if "developer" in base.columns else None),
    ("Hygiene + structural cleanup",
        len(clean), clean["developer"].nunique()),
    ("Cohort assignment (multi, non-AAA, active <5y)",
        title_count(cohort_devs), len(cohort_devs)),
    ("PCI-resolvable (>=2 measurable titles)",
        title_count(pci_devs), len(pci_devs)),
    ("Quality cleanup (port-shops / shovelware / audit R2)",
        title_count(stage6_devs), len(stage6_devs)),
    ("Moderate + concentrated PCI",
        title_count(mc_devs), len(mc_devs)),
    ("Final investor candidates",
        title_count(cand_devs), len(cand_devs)),
]

print(f"{'Stage':<58}{'Titles':>10}{'Developers':>14}")
print("-" * 82)
for label, t, d in rows:
    tstr = f"{t:,}" if t is not None else "—"
    dstr = f"{d:,}" if d is not None else "—"
    print(f"{label:<58}{tstr:>10}{dstr:>14}")

print(f"\nSanity:")
print(f"  candidates count: {len(candidates)}  (target 146: {len(candidates)==146})")
print(f"  candidate titles in structural pool: {title_count(cand_devs)}  (target 457)")

out = pd.DataFrame(rows, columns=["stage", "titles", "developers"])
out.to_csv(WS / "funnel_title_counts.csv", index=False)
print(f"\nWrote funnel_title_counts.csv")
