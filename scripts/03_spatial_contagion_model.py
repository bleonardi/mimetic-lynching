"""
Spatiotemporal contagion model for lynching.

Pr(L_it) = ρ·W·L_{j,t-1} + β·PostWeevil_it
           + γ·(PostWeevil × CottonPriceDecline)_it
           + δ·black_share_it + λ·log_pop_it
           + α_i + τ_t + ε_it

Estimation: Linear probability model with county + year FE, HC3 SEs.
IV robustness: instrument W·L_{j,t-1} with W·PostWeevil_{j,t-1}.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings("ignore")

PROC = Path(__file__).parent.parent / "data" / "processed"

# ── 1. Load and merge ─────────────────────────────────────────────────────────

panel = pd.read_parquet(PROC / "county_year_panel.parquet")
bw    = pd.read_parquet(PROC / "boll_weevil_arrival.parquet")
adj   = pd.read_parquet(PROC / "county_adjacency.parquet")

panel = panel.merge(bw, on="fips5", how="left")

# ── 2. Feature engineering ────────────────────────────────────────────────────

panel["post_weevil"] = (
    panel["arrival_year"].notna() &
    (panel["year"] >= panel["arrival_year"])
).astype(float)

# Cotton price decline: deviation below long-run mean (positive = bad shock)
mean_price = panel["cotton_price_annual_avg"].mean()
panel["cotton_price_decline"] = (mean_price - panel["cotton_price_annual_avg"]).clip(lower=0)

panel["weevil_x_price_decline"] = panel["post_weevil"] * panel["cotton_price_decline"]

panel["log_pop"] = np.log(panel["total_pop"].clip(lower=1))
panel["black_share"] = panel["black_share"].fillna(0)

# Binary outcome
panel["any_lynching"] = (panel["lynchings"] > 0).astype(float)

# ── 3. Spatial lag: W·L_{j,t-1} ──────────────────────────────────────────────

# Build adjacency lookup: fips5 → set of neighbor fips5
adj_dict = adj.groupby("fips5")["neighbor_fips"].apply(set).to_dict()

# Lag lynchings by 1 year within county
panel = panel.sort_values(["fips5", "year"])
panel["lynching_lag1"] = panel.groupby("fips5")["any_lynching"].shift(1)

# For each county-year, average neighbor's lagged lynching
panel_indexed = panel.set_index(["fips5", "year"])

def neighbor_lag(row):
    neighbors = adj_dict.get(row["fips5"], set())
    if not neighbors:
        return np.nan
    vals = []
    for n in neighbors:
        try:
            vals.append(panel_indexed.loc[(n, row["year"]), "lynching_lag1"])
        except KeyError:
            pass
    return np.nanmean(vals) if vals else np.nan

print("Computing spatial lag (this takes ~30s)...")
panel_reset = panel.reset_index(drop=True)
# Vectorized approach using merge
lag_df = panel[["fips5","year","lynching_lag1"]].rename(
    columns={"fips5":"neighbor_fips","lynching_lag1":"neighbor_lynch_lag1"}
)
adj_year = adj.merge(
    lag_df, on="neighbor_fips", how="left"
)
spatial_lag = (
    adj_year.groupby(["fips5","year"])["neighbor_lynch_lag1"]
    .mean()
    .reset_index()
    .rename(columns={"neighbor_lynch_lag1": "spatial_lag_lynch"})
)
panel = panel.merge(spatial_lag, on=["fips5","year"], how="left")

# IV: instrument = neighbor's post-weevil status (lagged 1 year)
panel["weevil_lag1"] = panel.groupby("fips5")["post_weevil"].shift(1)
lag_iv = panel[["fips5","year","weevil_lag1"]].rename(
    columns={"fips5":"neighbor_fips","weevil_lag1":"neighbor_weevil_lag1"}
)
adj_iv = adj.merge(lag_iv, on="neighbor_fips", how="left")
spatial_iv = (
    adj_iv.groupby(["fips5","year"])["neighbor_weevil_lag1"]
    .mean()
    .reset_index()
    .rename(columns={"neighbor_weevil_lag1": "spatial_iv"})
)
panel = panel.merge(spatial_iv, on=["fips5","year"], how="left")

print("Spatial lags done.")

# ── 4. Estimation sample ──────────────────────────────────────────────────────

# Cotton belt only; drop first year (need lag)
COTTON_STATES = {"01","05","12","13","22","28","37","40","45","47","48","51"}
sample = panel[
    panel["fips5"].str[:2].isin(COTTON_STATES) &
    panel["year"].gt(1883) &
    panel["total_pop"].gt(0)
].copy()

sample = sample.dropna(subset=["spatial_lag_lynch","black_share","log_pop","post_weevil"])
print(f"Estimation sample: {len(sample):,} county-years, "
      f"{sample['fips5'].nunique()} counties, "
      f"{sample['year'].nunique()} years")
print(f"Lynching rate: {sample['any_lynching'].mean():.4f} "
      f"({sample['any_lynching'].sum():.0f} county-years with lynching)")

# ── 5. OLS with county + year FE (within estimator) ─────────────────────────

import statsmodels.formula.api as smf

XVARS = ["spatial_lag_lynch", "post_weevil", "weevil_x_price_decline",
         "black_share", "log_pop"]

# Demean within county and year (two-way FE via demeaning)
def twoway_demean(df, yvars, xvars, county_var="fips5", year_var="year"):
    out = df[[county_var, year_var] + yvars + xvars].copy()
    # County means
    cmeans = out.groupby(county_var)[yvars+xvars].transform("mean")
    # Year means
    ymeans = out.groupby(year_var)[yvars+xvars].transform("mean")
    # Grand means
    gmeans = out[yvars+xvars].mean()
    # Within-transform
    for c in yvars+xvars:
        out[c] = out[c] - cmeans[c] - ymeans[c] + gmeans[c]
    return out

demeaned = twoway_demean(sample, ["any_lynching"], XVARS)

import statsmodels.api as sm

X = sm.add_constant(demeaned[XVARS])
y = demeaned["any_lynching"]
ols = sm.OLS(y, X).fit(cov_type="HC3")

print("\n" + "="*60)
print("OLS (Two-way FE, HC3): any_lynching ~ spatial_lag + weevil + controls")
print("="*60)
print(ols.summary2().tables[1].to_string())
print(f"\nN={len(y):,}  R²={ols.rsquared:.4f}")

# ── 6. IV-2SLS: instrument spatial_lag with spatial_iv ───────────────────────

try:
    from linearmodels.iv import IV2SLS
    sample_iv = sample.dropna(subset=["spatial_iv"])
    sample_iv = sample_iv.copy()
    # Absorb FE by demeaning
    iv_vars = ["spatial_lag_lynch","post_weevil","weevil_x_price_decline","black_share","log_pop","spatial_iv"]
    dm_iv = twoway_demean(sample_iv, ["any_lynching"], iv_vars)

    res_iv = IV2SLS(
        dependent=dm_iv["any_lynching"],
        exog=sm.add_constant(dm_iv[["post_weevil","weevil_x_price_decline","black_share","log_pop"]]),
        endog=dm_iv[["spatial_lag_lynch"]],
        instruments=dm_iv[["spatial_iv"]],
    ).fit(cov_type="robust")

    print("\n" + "="*60)
    print("IV-2SLS: spatial_lag instrumented by neighbor post-weevil")
    print("="*60)
    print(res_iv.summary.tables[1])

    # First-stage F
    from linearmodels.iv import compare
    print(f"\nFirst-stage F (approx): {res_iv.first_stage.diagnostics['f.stat'].values[0]:.2f}")
except ImportError:
    print("\nlinearmodels not installed — skipping IV. Run: pip install linearmodels")

# ── 7. Key results table ───────────────────────────────────────────────────────

print("\n" + "="*60)
print("GIRARDIAN INTERPRETATION")
print("="*60)
coefs = ols.params
ses   = ols.HC3_se
pvals = ols.pvalues

def fmt(var):
    return f"  {var:35s}  β={coefs[var]:+.5f}  SE={ses[var]:.5f}  p={pvals[var]:.3f}"

print("\nMimetic contagion (spatial spillover):")
print(fmt("spatial_lag_lynch"))
print("\nBoll weevil shock (economic crisis):")
print(fmt("post_weevil"))
print("\nWeevil × low cotton price (crisis amplifier):")
if "weevil_x_price_decline" in coefs.index:
    print(fmt("weevil_x_price_decline"))
print("\nBlack share (racial threat hypothesis):")
print(fmt("black_share"))
