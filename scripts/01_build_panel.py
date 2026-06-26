"""
Build county-year panel for mimetic lynching analysis.

Outputs: data/processed/county_year_panel.parquet
Columns: fips5, year, lynching, black_pop, white_pop, total_pop,
         black_share, cotton_acres, cotton_share_cropland
"""

import pandas as pd
import numpy as np
from pathlib import Path

RAW  = Path(__file__).parent.parent / "data" / "raw"
PROC = Path(__file__).parent.parent / "data" / "processed"
NHGIS = RAW / "nhgis" / "nhgis0003_csv"
PROC.mkdir(exist_ok=True)

# ── 1. Lynching data ────────────────────────────────────────────────────────

lynch = pd.read_csv(RAW / "seguin_rigby_lynching.csv")
lynch = lynch[lynch["race"] == "Black"].copy()

# Build 5-digit FIPS; full_fips is already 5-digit string in most cases
lynch["fips5"] = lynch["full_fips"].astype(str).str.zfill(5)

lynch_agg = (
    lynch.groupby(["fips5", "year"])
    .size()
    .reset_index(name="lynchings")
)

# ── 2. NHGIS population/race tables ─────────────────────────────────────────

def fips5_from_nhgis(df):
    """GISJOIN = G + state2 + 0 + county3 + 0  → FIPS = state2 + county3"""
    gj = df["GISJOIN"].astype(str)
    state = gj.str[1:3]
    county = gj.str[4:7]
    return state + county

pop_frames = []

# 1880 — two files: population (ds22) + race (ds23)
pop80 = pd.read_csv(NHGIS / "nhgis0003_ds22_1880_county.csv", usecols=["GISJOIN", "AOB001"])
race80 = pd.read_csv(NHGIS / "nhgis0003_ds23_1880_county.csv",
                     usecols=["GISJOIN", "APP001", "APP002"])
df80 = pop80.merge(race80, on="GISJOIN")
df80["fips5"] = fips5_from_nhgis(df80)
df80["year"] = 1880
df80["total_pop"] = df80["AOB001"]
df80["white_pop"] = df80["APP001"]
df80["black_pop"] = df80["APP002"]   # "Colored" in 1880 census
pop_frames.append(df80[["fips5", "year", "total_pop", "white_pop", "black_pop"]])

# 1890 — total pop (ds26) + race/nativity (ds27: AV0007+AV0008 = Colored M+F)
pop90 = pd.read_csv(NHGIS / "nhgis0003_ds26_1890_county.csv", usecols=["GISJOIN", "ASW001"])
race90 = pd.read_csv(NHGIS / "nhgis0003_ds27_1890_county.csv",
                     usecols=["GISJOIN"] + [f"AV0{i:03d}" for i in range(1, 9)])
df90 = pop90.merge(race90, on="GISJOIN")
df90["fips5"] = fips5_from_nhgis(df90)
df90["year"] = 1890
df90["total_pop"] = df90["ASW001"]
df90["white_pop"] = df90[["AV0001","AV0002","AV0003","AV0004","AV0005","AV0006"]].sum(axis=1)
df90["black_pop"] = df90[["AV0007","AV0008"]].sum(axis=1)
pop_frames.append(df90[["fips5", "year", "total_pop", "white_pop", "black_pop"]])

# 1900 — total pop + crop (ds30); race (ds31: AZ3003+AZ3004 = Negro)
pop00 = pd.read_csv(NHGIS / "nhgis0003_ds30_1900_county.csv", usecols=["GISJOIN", "AWS001"])
race00 = pd.read_csv(NHGIS / "nhgis0003_ds31_1900_county.csv",
                     usecols=["GISJOIN", "AZ3001", "AZ3002", "AZ3003", "AZ3004"])
df00 = pop00.merge(race00, on="GISJOIN")
df00["fips5"] = fips5_from_nhgis(df00)
df00["year"] = 1900
df00["total_pop"] = df00["AWS001"]
df00["black_pop"] = df00["AZ3003"] + df00["AZ3004"]
df00["white_pop"] = df00["total_pop"] - df00["black_pop"] - df00["AZ3001"] - df00["AZ3002"]
pop_frames.append(df00[["fips5", "year", "total_pop", "white_pop", "black_pop"]])

# 1910 — crop (ds36) + race (ds37: A30001+A30002=White, A30003+A30004=Negro)
race10 = pd.read_csv(NHGIS / "nhgis0003_ds37_1910_county.csv",
                     usecols=["GISJOIN", "A30001", "A30002", "A30003", "A30004"])
df10 = race10.copy()
df10["fips5"] = fips5_from_nhgis(df10)
df10["year"] = 1910
df10["white_pop"] = df10["A30001"] + df10["A30002"]
df10["black_pop"] = df10["A30003"] + df10["A30004"]
df10["total_pop"] = df10["white_pop"] + df10["black_pop"]
pop_frames.append(df10[["fips5", "year", "total_pop", "white_pop", "black_pop"]])

# 1920 — total pop + race (ds43: A8L005+A8L006=Negro; white = A8L001..A8L004)
df20 = pd.read_csv(NHGIS / "nhgis0003_ds43_1920_county.csv",
                   usecols=["GISJOIN", "A7L001", "A8L001","A8L002","A8L003","A8L004","A8L005","A8L006"])
df20["fips5"] = fips5_from_nhgis(df20)
df20["year"] = 1920
df20["total_pop"] = df20["A7L001"]
df20["white_pop"] = df20[["A8L001","A8L002","A8L003","A8L004"]].sum(axis=1)
df20["black_pop"] = df20["A8L005"] + df20["A8L006"]
pop_frames.append(df20[["fips5", "year", "total_pop", "white_pop", "black_pop"]])

# 1930 — total pop + race (ds54: BEP005+BEP006=Negro; white = BEP001..BEP004)
df30 = pd.read_csv(NHGIS / "nhgis0003_ds54_1930_county.csv",
                   usecols=["GISJOIN","BEP001","BEP002","BEP003","BEP004","BEP005","BEP006"])
pop30_extra = pd.read_csv(NHGIS / "nhgis0003_ds212_1930_county.csv",
                           usecols=["GISJOIN", "ACEE001"])
df30 = df30.merge(pop30_extra, on="GISJOIN")
df30["fips5"] = fips5_from_nhgis(df30)
df30["year"] = 1930
df30["total_pop"] = df30["ACEE001"]
df30["white_pop"] = df30[["BEP001","BEP002","BEP003","BEP004"]].sum(axis=1)
df30["black_pop"] = df30["BEP005"] + df30["BEP006"]
pop_frames.append(df30[["fips5", "year", "total_pop", "white_pop", "black_pop"]])

pop_panel = pd.concat(pop_frames, ignore_index=True)
pop_panel["black_share"] = pop_panel["black_pop"] / pop_panel["total_pop"].replace(0, np.nan)

# ── 3. Cotton acreage ────────────────────────────────────────────────────────

cotton_frames = []

# 1900 — Crop Acreage 1899 (ds30): need to find cotton column
# ds30 has many AXN columns; check codebook
cb30 = (RAW / "nhgis" / "nhgis0003_csv" / "nhgis0003_ds30_1900_county_codebook.txt").read_text()
# Find cotton line
cotton_col_1900 = None
for line in cb30.splitlines():
    if "cotton" in line.lower() and "AXN" in line:
        cotton_col_1900 = line.strip().split(":")[0].strip()
        break

crop00 = pd.read_csv(NHGIS / "nhgis0003_ds30_1900_county.csv", usecols=["GISJOIN"] + [c for c in pd.read_csv(NHGIS / "nhgis0003_ds30_1900_county.csv", nrows=0).columns if c.startswith("AXN")])
if cotton_col_1900:
    crop00["fips5"] = fips5_from_nhgis(crop00)
    crop00["year"] = 1900
    crop00 = crop00.rename(columns={cotton_col_1900: "cotton_acres"})
    cotton_frames.append(crop00[["fips5", "year", "cotton_acres"]])

# 1910 — Crop Production 1909 (ds36): find cotton
cb36 = (RAW / "nhgis" / "nhgis0003_csv" / "nhgis0003_ds36_1910_county_codebook.txt").read_text()
cotton_col_1910 = None
for line in cb36.splitlines():
    if "cotton" in line.lower() and "A2T" in line:
        cotton_col_1910 = line.strip().split(":")[0].strip()
        break

if cotton_col_1910:
    crop10 = pd.read_csv(NHGIS / "nhgis0003_ds36_1910_county.csv", usecols=["GISJOIN", cotton_col_1910])
    crop10["fips5"] = fips5_from_nhgis(crop10)
    crop10["year"] = 1910
    crop10 = crop10.rename(columns={cotton_col_1910: "cotton_acres"})
    cotton_frames.append(crop10[["fips5", "year", "cotton_acres"]])

# 1920 — ds210: AB43003 = Cotton acreage 1919
crop20 = pd.read_csv(NHGIS / "nhgis0003_ds210_1920_county.csv", usecols=["GISJOIN", "AB43003"])
crop20["fips5"] = fips5_from_nhgis(crop20)
crop20["year"] = 1920
crop20 = crop20.rename(columns={"AB43003": "cotton_acres"})
cotton_frames.append(crop20[["fips5", "year", "cotton_acres"]])

# 1930 — ds212: ACBD002 = Cotton lint acres 1929
crop30 = pd.read_csv(NHGIS / "nhgis0003_ds212_1930_county.csv", usecols=["GISJOIN", "ACBD002"])
crop30["fips5"] = fips5_from_nhgis(crop30)
crop30["year"] = 1930
crop30 = crop30.rename(columns={"ACBD002": "cotton_acres"})
cotton_frames.append(crop30[["fips5", "year", "cotton_acres"]])

cotton_panel = pd.concat(cotton_frames, ignore_index=True)

# ── 4. Cotton price (NBER annual) ─────────────────────────────────────────────

cotton_price = pd.read_csv(RAW / "cotton_price_annual.csv")  # columns: year, price_cents_lb

# ── 5. County adjacency → FIPS pairs ─────────────────────────────────────────

adj_rows = []
current = None
with open(RAW / "county_adjacency.txt", encoding="latin-1") as f:
    for line in f:
        parts = line.rstrip("\n").split("\t")
        if parts[0]:  # new county row: name, fips, neighbor_name, neighbor_fips
            current = parts[1].strip('"').zfill(5)
            neighbor = parts[3].strip('"').zfill(5)
        else:  # continuation: '', '', neighbor_name, neighbor_fips
            if len(parts) < 4:
                continue
            neighbor = parts[3].strip('"').zfill(5)
        if current and neighbor and current != neighbor:
            adj_rows.append((current, neighbor))

adj = pd.DataFrame(adj_rows, columns=["fips5", "neighbor_fips"])

# ── 6. Build full panel ───────────────────────────────────────────────────────

# Census years: interpolate decennially to fill annual gaps
# For lynching model: assign each lynching-year the nearest census pop
all_years = list(range(1883, 1937))
all_fips = pop_panel["fips5"].unique()

# Create skeleton: every county × every year
skeleton = pd.MultiIndex.from_product([all_fips, all_years], names=["fips5", "year"])
panel = pd.DataFrame(index=skeleton).reset_index()

# Merge lynchings
panel = panel.merge(lynch_agg, on=["fips5", "year"], how="left")
panel["lynchings"] = panel["lynchings"].fillna(0).astype(int)

# Merge census pop — forward-fill decennial to annual
panel = panel.merge(pop_panel, on=["fips5", "year"], how="left")

# For each county, sort by year and interpolate census vars
panel = panel.sort_values(["fips5", "year"])
for col in ["total_pop", "white_pop", "black_pop"]:
    panel[col] = panel.groupby("fips5")[col].transform(
        lambda s: s.interpolate(method="linear", limit_direction="both")
    )
panel["black_share"] = panel["black_pop"] / panel["total_pop"].replace(0, np.nan)

# Merge cotton (nearest census year — use left join on same decennial anchor)
panel = panel.merge(cotton_panel, on=["fips5", "year"], how="left")
panel["cotton_acres"] = panel.groupby("fips5")["cotton_acres"].transform(
    lambda s: s.interpolate(method="linear", limit_direction="both")
)

# Merge cotton price
panel = panel.merge(cotton_price, on="year", how="left")

# ── 7. Save ───────────────────────────────────────────────────────────────────

panel.to_parquet(PROC / "county_year_panel.parquet", index=False)
adj.to_parquet(PROC / "county_adjacency.parquet", index=False)

print(f"Panel: {len(panel):,} rows, {panel['fips5'].nunique():,} counties, {panel['year'].nunique()} years")
print(f"Lynching events: {panel['lynchings'].sum():,}")
print(f"Counties with any lynching: {(panel.groupby('fips5')['lynchings'].sum() > 0).sum()}")
print(f"Adjacency pairs: {len(adj):,}")
print(panel.head(3).to_string())
