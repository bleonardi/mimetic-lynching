"""
Compare spatial lag ρ across four W-matrix specifications.

For each W, estimates:
    Pr(L_it=1) = ρ·W·L_{j,t-1} + δ·BlackShare_it + λ·logPop_it + α_i + τ_t

via two-way demeaned OLS with HC3 robust SEs.

W matrices tested:
    Geographic adjacency  — county_adjacency.parquet
    Railroad network      — w_railroad.parquet
    Denomination (top-10) — w_denomination.parquet
    Newspaper co-coverage — w_newspaper.parquet

Outputs:
    data/processed/w_comparison_results.csv
    figures/fig5_w_comparison.png
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path
import warnings
warnings.filterwarnings("ignore")

PROC = Path(__file__).parent.parent / "data" / "processed"
FIG  = Path(__file__).parent.parent / "figures"
COTTON_STATES = {"01","05","12","13","22","28","37","40","45","47","48","51"}

# ── Load panel ────────────────────────────────────────────────────────────────
panel = pd.read_parquet(PROC / "county_year_panel.parquet")
panel["any_lynching"] = (panel["lynchings"] > 0).astype(float)
panel["log_pop"]      = np.log(panel["total_pop"].clip(lower=1))
panel["black_share"]  = panel["black_share"].fillna(0)
panel = panel.sort_values(["fips5","year"])
panel["lynching_lag1"] = panel.groupby("fips5")["any_lynching"].shift(1)

sample_base = panel[
    panel["fips5"].str[:2].isin(COTTON_STATES) &
    panel["year"].gt(1883) &
    panel["total_pop"].gt(0)
].copy()

base_rate = sample_base["any_lynching"].mean()

# Neighbor lag lookup table
lag_df = (sample_base[["fips5","year","lynching_lag1"]]
          .rename(columns={"fips5":"neighbor_fips","lynching_lag1":"nbr_lynch_lag"}))

CONTROLS = ["black_share","log_pop"]

# ── Two-way demean ────────────────────────────────────────────────────────────
def twoway_demean(df, yvars, xvars):
    out = df[["fips5","year"] + yvars + xvars].copy()
    cm  = out.groupby("fips5")[yvars+xvars].transform("mean")
    ym  = out.groupby("year")[yvars+xvars].transform("mean")
    gm  = out[yvars+xvars].mean()
    for c in yvars+xvars:
        out[c] = out[c] - cm[c] - ym[c] + gm[c]
    return out

# ── W specifications ──────────────────────────────────────────────────────────
W_SPECS = {
    "Geographic adjacency":   (PROC/"county_adjacency.parquet",  "neighbor_fips", None),
    "Newspaper co-coverage":  (PROC/"w_newspaper.parquet",        "neighbor_fips", None),
    "Denomination (top-10)":  (PROC/"w_denomination.parquet",     "neighbor_fips", "denom_similarity"),
    "Railroad network":       (PROC/"w_railroad.parquet",         "neighbor_fips", None),
}

results = {}

for w_name, (w_path, nbr_col, weight_col) in W_SPECS.items():
    print(f"Running {w_name}...", end=" ", flush=True)
    if not w_path.exists():
        print("SKIPPED (file not found — run 04_build_alternative_W.py first)")
        continue

    w = pd.read_parquet(w_path)
    w = w[w["fips5"].str[:2].isin(COTTON_STATES) &
          w[nbr_col].str[:2].isin(COTTON_STATES)].copy()

    w_lag = w.merge(lag_df, on="neighbor_fips", how="left")

    if weight_col and weight_col in w.columns:
        w_lag["wtd"] = w_lag["nbr_lynch_lag"] * w_lag[weight_col]
        num    = w_lag.groupby(["fips5","year"])["wtd"].sum()
        den    = w_lag.groupby(["fips5","year"])[weight_col].sum()
        sp_lag = (num/den).reset_index().rename(columns={0:"spatial_lag"})
    else:
        sp_lag = (w_lag.groupby(["fips5","year"])["nbr_lynch_lag"]
                  .mean().reset_index()
                  .rename(columns={"nbr_lynch_lag":"spatial_lag"}))

    samp = sample_base.merge(sp_lag, on=["fips5","year"], how="inner")
    samp = samp.dropna(subset=["spatial_lag"] + CONTROLS)

    xvars = ["spatial_lag"] + CONTROLS
    dm    = twoway_demean(samp, ["any_lynching"], xvars)
    X     = sm.add_constant(dm[xvars])
    fit   = sm.OLS(dm["any_lynching"], X).fit(cov_type="HC3")

    results[w_name] = {
        "rho":      fit.params["spatial_lag"],
        "se":       fit.HC3_se["spatial_lag"],
        "p":        fit.pvalues["spatial_lag"],
        "n":        int(len(dm)),
        "counties": int(samp["fips5"].nunique()),
        "r2":       fit.rsquared,
    }
    print(f"ρ={fit.params['spatial_lag']:+.4f}  "
          f"p={fit.pvalues['spatial_lag']:.3f}  "
          f"N={len(dm):,}")

# ── Print comparison table ────────────────────────────────────────────────────
def stars(p):
    return "***" if p<.01 else "**" if p<.05 else "*" if p<.1 else ""

print("\n" + "="*72)
print("TABLE 2. Mimetic Contagion by Transmission Channel")
print(f"Dependent variable: any lynching (t).  Base rate = {base_rate:.4f}")
print("LPM, two-way FE, HC3 SEs.  Controls: black share, log population.")
print("="*72)
print(f"{'W matrix':30s}  {'ρ':>8s}  {'SE':>7s}  {'p':>6s}  {'×base':>6s}  {'N':>7s}")
print("-"*72)
for w_name, r in results.items():
    print(f"  {w_name:28s}  {r['rho']:+8.4f}{stars(r['p']):3s}  "
          f"({r['se']:.4f})  {r['p']:6.3f}  "
          f"{r['rho']/base_rate:+5.0f}×  {r['n']:7,}")
print("="*72)
print("*** p<0.01  ** p<0.05  * p<0.10")

# Save CSV
pd.DataFrame(results).T.to_csv(PROC / "w_comparison_results.csv")
print(f"\nSaved → {PROC}/w_comparison_results.csv")

# ── Figure 5: coefficient plot ────────────────────────────────────────────────
ORDER  = ["Geographic adjacency","Newspaper co-coverage",
          "Denomination (top-10)","Railroad network"]
rhos   = [results[k]["rho"] for k in ORDER if k in results]
ses    = [results[k]["se"]  for k in ORDER if k in results]
ps     = [results[k]["p"]   for k in ORDER if k in results]
labels = [k for k in ORDER if k in results]
colors = ["#c0392b" if p < 0.05 else "#aaaaaa" for p in ps]

fig, ax = plt.subplots(figsize=(8, 4))
fig.patch.set_facecolor("#faf9f7")
ax.set_facecolor("#faf9f7")

y = np.arange(len(labels))
ax.barh(y, rhos, xerr=np.array(ses)*1.96, color=colors, height=0.55,
        error_kw=dict(ecolor="#555", lw=1.3, capsize=4))
ax.axvline(0, color="#333", lw=0.8, ls="--")

for i, (rho, p, se) in enumerate(zip(rhos, ps, ses)):
    star = "**" if p<.01 else "*" if p<.05 else ""
    if star:
        ax.text(rho + se*1.96 + 0.002, y[i], star,
                va="center", fontsize=11, color="#c0392b", fontweight="bold")

ax.set_yticks(y)
ax.set_yticklabels(labels, fontsize=10)
ax.set_xlabel("ρ  (spatial lag coefficient, LPM two-way FE, HC3 SEs)", fontsize=10)
ax.set_title(
    "Fig. 5 — Which transmission channel carries mimetic contagion?\n"
    "Spatial lag ρ by W-matrix specification, Cotton Belt 1884–1936",
    fontsize=10.5, fontfamily="serif")
ax.spines[["top","right"]].set_visible(False)

sig_p   = mpatches.Patch(color="#c0392b", label="p < 0.05")
insig_p = mpatches.Patch(color="#aaaaaa", label="p ≥ 0.05")
ax.legend(handles=[sig_p, insig_p], fontsize=8.5, loc="lower right")

plt.tight_layout()
out_path = FIG / "fig5_w_comparison.png"
plt.savefig(out_path, dpi=160, bbox_inches="tight")
plt.close()
print(f"Saved → {out_path}")
