"""
Build three alternative spatial weight matrices for mimetic contagion analysis.

1. Railroad W   — counties sharing a railroad company (Atack shapefiles ≤1900)
2. Denomination W — top-10 most denominationally similar county pairs (cosine,
                    1890 Census of Religious Bodies)
3. Newspaper W  — counties sharing newspaper co-coverage zone (ICPSR 35513,
                  pub county + geographic neighbors, 1880–1896)

Outputs (data/processed/):
    w_railroad.parquet       — fips5, neighbor_fips
    w_denomination.parquet   — fips5, neighbor_fips, denom_similarity
    w_newspaper.parquet      — fips5, neighbor_fips
"""

import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity

RAW  = Path(__file__).parent.parent / "data" / "raw"
PROC = Path(__file__).parent.parent / "data" / "processed"

COTTON_STATES = {"01","05","12","13","22","28","37","40","45","47","48","51"}

STATE_FIPS = {"AL":"01","AR":"05","FL":"12","GA":"13","LA":"22",
              "MS":"28","NC":"37","OK":"40","SC":"45","TN":"47",
              "TX":"48","VA":"51"}

# ── 1. RAILROAD W ─────────────────────────────────────────────────────────────
print("Building railroad W...")

try:
    import geopandas as gpd

    rr = gpd.read_file(RAW / "railroad" / "RR1826-1911Modified103123.shp")
    rr = rr[rr["InOpBy"].fillna(9999) <= 1900].copy()

    # Load cotton-belt county boundaries
    counties = gpd.read_file(
        "https://www2.census.gov/geo/tiger/GENZ2018/shp/cb_2018_us_county_20m.zip"
    )
    counties["fips5"] = counties["STATEFP"] + counties["COUNTYFP"]
    counties = counties[counties["STATEFP"].isin(COTTON_STATES)].to_crs(rr.crs)

    # Spatial join: which railroad lines pass through each county
    rr_county = gpd.sjoin(
        rr[["geometry","RRname"]].reset_index(drop=True),
        counties[["fips5","geometry"]],
        how="inner", predicate="intersects"
    )[["RRname","fips5"]].drop_duplicates()

    # W_ij = 1 if counties share a railroad company
    rr_edges = (rr_county
                .merge(rr_county, on="RRname", suffixes=("_i","_j"))
                .query("fips5_i != fips5_j")
                [["fips5_i","fips5_j"]]
                .drop_duplicates()
                .rename(columns={"fips5_i":"fips5","fips5_j":"neighbor_fips"}))

    rr_edges.to_parquet(PROC / "w_railroad.parquet", index=False)
    print(f"  Railroad W: {len(rr_edges):,} edges, "
          f"{rr_edges['fips5'].nunique()} counties, "
          f"avg_k={rr_edges.groupby('fips5').size().mean():.1f}")

except Exception as e:
    print(f"  Railroad W skipped (geopandas/shapefile error): {e}")
    print("  Using cached w_railroad.parquet if present.")

# ── 2. DENOMINATION W ─────────────────────────────────────────────────────────
print("Building denomination W...")

relig = pd.read_csv(
    RAW / "nhgis" / "nhgis0004_csv" / "nhgis0004_csv" /
    "nhgis0004_ds28_1890_county.csv"
)
# Derive FIPS5 from GISJOIN = G + state2 + 0 + county3 + 0
gj = relig["GISJOIN"].astype(str)
relig["fips5"] = gj.str[1:3] + gj.str[4:7]
relig = relig[relig["fips5"].str[:2].isin(COTTON_STATES)].copy()

DENOM_COLS = {
    "AWD004": "Baptist_South",     "AWD005": "Baptist_Colored",
    "AWD042": "Methodist_South",   "AWD038": "AME",
    "AWD039": "AME_Zion",          "AWD043": "Methodist_Colored",
    "AWD051": "Presbyterian_S",    "AWD010": "Catholic",
    "AWD047": "Cumberland_Presb",  "AWD037": "Methodist_N",
    "AWD046": "Presbyterian_N",    "AWD003": "Baptist_N",
}
all_awd = [c for c in relig.columns if c.startswith("AWD")]
relig["total_members"] = relig[all_awd].fillna(0).sum(axis=1)
share_cols = list(DENOM_COLS.values())
for col, name in DENOM_COLS.items():
    relig[name] = relig[col].fillna(0) / relig["total_members"].replace(0, np.nan)

denom_shares = relig[["fips5"] + share_cols].dropna().copy()
denom_shares[share_cols] = denom_shares[share_cols].fillna(0)

X    = denom_shares[share_cols].values
fips = denom_shares["fips5"].values
sim  = cosine_similarity(X)

# Top-K most similar neighbors (K=10) — avoids fully-connected near-uniform W
K = 10
edges = []
for i in range(len(fips)):
    top_j = np.argsort(sim[i])[::-1][1:K+1]
    for j in top_j:
        edges.append((fips[i], fips[j], float(sim[i, j])))

denom_w = pd.DataFrame(edges, columns=["fips5","neighbor_fips","denom_similarity"])
denom_w.to_parquet(PROC / "w_denomination.parquet", index=False)
print(f"  Denomination W: {len(denom_w):,} edges, "
      f"{denom_w['fips5'].nunique()} counties, "
      f"avg_k={denom_w.groupby('fips5').size().mean():.1f}, "
      f"mean_sim={denom_w['denom_similarity'].mean():.3f}")

# ── 3. NEWSPAPER W ────────────────────────────────────────────────────────────
print("Building newspaper W...")

geo_adj = pd.read_parquet(PROC / "county_adjacency.parquet")

news = pd.read_csv(RAW / "newspaper" / "ICPSR_35513" / "DS0001" /
                   "35513-0001-Data.tsv", sep="\t")
news = news[news["state"].isin(STATE_FIPS)].copy()
news = news[(news["year"] >= 1880) & (news["year"] <= 1896)].copy()
news["state_fips"] = news["state"].map(STATE_FIPS)

# Match city_recode → county FIPS via county name lookup (county seats)
county_lu = relig[["fips5","COUNTY"]].copy()
county_lu["state_fips"]   = county_lu["fips5"].str[:2]
county_lu["county_clean"] = county_lu["COUNTY"].str.upper().str.strip()

def city_to_fips(city, state_fips):
    city_up = city.upper().strip()
    sub = county_lu[county_lu["state_fips"] == state_fips]
    exact = sub[sub["county_clean"] == city_up]
    if not exact.empty:
        return exact.iloc[0]["fips5"]
    partial = sub[sub["county_clean"].str.startswith(city_up)]
    if not partial.empty:
        return partial.iloc[0]["fips5"]
    partial2 = sub[sub.apply(lambda r: r["county_clean"] in city_up, axis=1)]
    if not partial2.empty:
        return partial2.iloc[0]["fips5"]
    return None

cities = news[["state_fips","city_recode"]].drop_duplicates()
cities["fips5"] = cities.apply(
    lambda r: city_to_fips(r["city_recode"], r["state_fips"]), axis=1)
news = news.merge(cities, on=["state_fips","city_recode"], how="left")

pub_fips = news.dropna(subset=["fips5"])["fips5"].unique()
print(f"  {len(pub_fips)} matched publication counties "
      f"({cities['fips5'].notna().mean():.1%} city match rate)")

# Zone = publication county + its geographic neighbors
direct   = pd.DataFrame({"pub_fips": pub_fips, "covered_fips": pub_fips})
adj_zone = (geo_adj[geo_adj["fips5"].isin(pub_fips)]
            .rename(columns={"fips5":"pub_fips","neighbor_fips":"covered_fips"}))
zones = pd.concat([direct, adj_zone], ignore_index=True)

news_w = (zones.merge(zones, on="pub_fips")
          .query("covered_fips_x != covered_fips_y")
          .rename(columns={"covered_fips_x":"fips5","covered_fips_y":"neighbor_fips"})
          [["fips5","neighbor_fips"]].drop_duplicates())
news_w = news_w[
    news_w["fips5"].str[:2].isin(COTTON_STATES) &
    news_w["neighbor_fips"].str[:2].isin(COTTON_STATES)]

news_w.to_parquet(PROC / "w_newspaper.parquet", index=False)
print(f"  Newspaper W: {len(news_w):,} edges, "
      f"{news_w['fips5'].nunique()} counties, "
      f"avg_k={news_w.groupby('fips5').size().mean():.1f}")

# ── Summary ───────────────────────────────────────────────────────────────────
geo_w = geo_adj[geo_adj["fips5"].str[:2].isin(COTTON_STATES) &
                geo_adj["neighbor_fips"].str[:2].isin(COTTON_STATES)]

print("\n" + "="*58)
print("W MATRIX SUMMARY")
print("="*58)
for name, w in [("Geographic adjacency", geo_w),
                ("Railroad network",     pd.read_parquet(PROC/"w_railroad.parquet")
                 if (PROC/"w_railroad.parquet").exists() else pd.DataFrame()),
                ("Denomination (top-10)",denom_w),
                ("Newspaper co-coverage",news_w)]:
    if w.empty:
        print(f"  {name:30s}  (not built)")
        continue
    k = w.groupby("fips5").size()
    print(f"  {name:30s}  {len(w):6,} edges  "
          f"{w['fips5'].nunique():4} counties  avg_k={k.mean():.1f}")
