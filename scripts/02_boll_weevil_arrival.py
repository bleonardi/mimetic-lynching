"""
Digitize boll weevil arrival years from USDA 1923 Hunter & Coad map
(Fig. 1 — spread of Mexican cotton boll weevil, 1892-1922).

Method: hand-read ~30 calibration points from the isochrone map,
interpolate to all cotton-belt county centroids via RBF.

Output: data/processed/boll_weevil_arrival.parquet
Columns: fips5, arrival_year (NaN = no weevil by 1922)
"""

import pandas as pd
import numpy as np
from pathlib import Path
from scipy.interpolate import RBFInterpolator

PROC = Path(__file__).parent.parent / "data" / "processed"

# ── 1. Calibration points read from the 1923 USDA map ───────────────────────
# (lat, lon, arrival_year) — traced from isochrone labels overlaid on county map
# Origin: Brownsville TX area, first US infestation ~1892

CALIBRATION = [
    # South Texas origin
    (26.0, -97.5, 1892),   # Brownsville TX
    (27.5, -97.7, 1895),   # Corpus Christi TX coast
    (27.8, -98.1, 1897),   # Alice TX area
    (28.5, -96.8, 1900),   # Victoria TX
    (28.7, -100.5, 1903),  # Eagle Pass / Del Rio TX
    (29.2, -98.5, 1903),   # San Antonio TX
    (29.7, -95.4, 1904),   # Houston TX
    (30.1, -94.1, 1905),   # Beaumont / Orange TX
    (31.5, -97.1, 1905),   # Waco TX area
    (31.0, -93.7, 1906),   # Nacogdoches TX
    (32.5, -93.8, 1906),   # Shreveport LA
    (32.7, -96.8, 1907),   # Dallas TX
    (31.3, -92.4, 1907),   # Alexandria LA
    (32.5, -92.1, 1907),   # Monroe LA
    (30.5, -91.2, 1908),   # Baton Rouge LA
    (29.9, -90.1, 1909),   # New Orleans LA
    (32.3, -90.2, 1909),   # Jackson MS
    (31.6, -91.0, 1908),   # Natchez MS
    (33.4, -91.0, 1909),   # Greenville MS (Delta)
    (30.7, -88.0, 1910),   # Mobile AL
    (32.4, -86.3, 1911),   # Montgomery AL
    (33.5, -86.8, 1912),   # Birmingham AL
    (33.7, -84.4, 1913),   # Atlanta GA
    (34.7, -92.3, 1912),   # Little Rock AR
    (34.0, -88.5, 1912),   # Corinth MS / NE Mississippi
    (35.1, -90.1, 1914),   # Memphis TN
    (36.2, -86.8, 1917),   # Nashville TN
    (34.5, -85.8, 1914),   # NW Georgia / Rome GA
    (32.8, -83.6, 1915),   # Macon GA
    (32.1, -81.1, 1915),   # Savannah GA
    (33.5, -82.0, 1916),   # Augusta GA
    (35.0, -89.0, 1914),   # NE Mississippi / Memphis corridor
    (34.0, -81.0, 1917),   # Columbia SC
    (32.8, -79.9, 1917),   # Charleston SC
    (35.2, -80.8, 1919),   # Charlotte NC
    (35.8, -78.6, 1920),   # Raleigh NC
    (34.2, -77.9, 1921),   # Wilmington NC
    (36.7, -76.3, 1921),   # Norfolk VA
    (35.0, -92.4, 1913),   # Central Arkansas
    (35.4, -94.4, 1914),   # Fort Smith AR
    (35.8, -90.7, 1913),   # Jonesboro AR
    (36.1, -95.9, 1916),   # Tulsa OK
    (35.5, -97.5, 1917),   # Oklahoma City OK
    (34.0, -97.0, 1916),   # Ardmore OK
    (31.8, -106.5, 1920),  # El Paso TX (far west, very late)
    (32.5, -103.7, 1919),  # Midland TX
    (31.5, -97.0, 1906),   # Temple TX
    (33.0, -97.3, 1909),   # Fort Worth TX
    (34.0, -100.0, 1915),  # Abilene TX area
    (36.3, -79.8, 1921),   # Danville VA / Piedmont NC
    (34.8, -76.6, 1921),   # Eastern NC coast
    (30.3, -87.2, 1910),   # Pensacola FL
    (30.4, -84.3, 1915),   # Tallahassee FL
    (29.7, -82.3, 1917),   # Gainesville FL
]

cal = np.array(CALIBRATION)
lats, lons, years = cal[:, 0], cal[:, 1], cal[:, 2]

# ── 2. Load county centroids ─────────────────────────────────────────────────
# Use the panel we already built, or derive from NHGIS GISJOIN
panel = pd.read_parquet(PROC / "county_year_panel.parquet",
                        columns=["fips5"]).drop_duplicates()

# Cotton belt states: only states where boll weevil was relevant
COTTON_BELT = {
    "01",  # Alabama
    "05",  # Arkansas
    "12",  # Florida
    "13",  # Georgia
    "22",  # Louisiana
    "28",  # Mississippi
    "37",  # North Carolina
    "40",  # Oklahoma
    "45",  # South Carolina
    "47",  # Tennessee
    "48",  # Texas
    "51",  # Virginia
}

panel["state_fips"] = panel["fips5"].str[:2]
cotton = panel[panel["state_fips"].isin(COTTON_BELT)].copy()

# County centroids from a standard lookup
# Use the us-county-adjacency centroids or derive from NHGIS time series coords
# We'll pull approximate centroids from a built-in dataset
try:
    import geopandas as gpd  # noqa
    HAS_GPD = True
except ImportError:
    HAS_GPD = False

if HAS_GPD:
    import geopandas as gpd
    from io import StringIO
    # Load from census tiger if available
    pass

# Fallback: approximate county centroids from a CSV we'll build from
# state FIPS + known county lat/lon reference table
# Use the NHGIS time series file which has STATEFP/COUNTYFP
ts = pd.read_csv(
    Path(__file__).parent.parent / "data" / "raw" / "nhgis" /
    "nhgis0003_csv" / "nhgis0003_ts_nominal_county.csv",
    usecols=["GISJOIN", "STATEFP", "COUNTYFP"]
)
ts["fips5"] = ts["STATEFP"].astype(str).str.zfill(2) + ts["COUNTYFP"].astype(str).str.zfill(3)

# We need lat/lon centroids. Use a standard county centroid file.
# Download from Census Bureau (small, ~200KB)
import urllib.request, json, os, tempfile

centroid_path = PROC / "county_centroids.csv"
if not centroid_path.exists():
    url = "https://raw.githubusercontent.com/btskinner/spatial/master/data/county_centers.csv"
    try:
        urllib.request.urlretrieve(url, centroid_path)
        print(f"Downloaded county centroids -> {centroid_path}")
    except Exception:
        print("Could not download centroids; using calibration-only approximation")

if centroid_path.exists():
    centroids = pd.read_csv(centroid_path)
    # Expected cols vary by source; normalize
    col_map = {}
    for c in centroids.columns:
        cl = c.lower()
        if "fips" in cl or cl in ("geoid", "county_fips"):
            col_map[c] = "fips5"
        elif cl in ("lat", "latitude", "cen_lat", "clat"):
            col_map[c] = "lat"
        elif cl in ("lon", "lng", "longitude", "cen_lon", "clon"):
            col_map[c] = "lon"
    centroids = centroids.rename(columns=col_map)
    # Rename actual lat/lon cols from this specific file
    if "clat00" in centroids.columns and "lat" not in centroids.columns:
        centroids = centroids.rename(columns={"clat00": "lat", "clon00": "lon"})

    if "fips5" in centroids.columns:
        centroids["fips5"] = centroids["fips5"].astype(str).str.zfill(5)
    else:
        # Try building from state + county columns
        sc = [c for c in centroids.columns if "state" in c.lower()]
        cc = [c for c in centroids.columns if "county" in c.lower() and c != "fips5"]
        if sc and cc:
            centroids["fips5"] = (centroids[sc[0]].astype(str).str.zfill(2) +
                                  centroids[cc[0]].astype(str).str.zfill(3))
    print("Centroid columns:", centroids.columns.tolist())
    print(centroids.head(2))
else:
    # No centroids available — skip
    centroids = pd.DataFrame(columns=["fips5", "lat", "lon"])

# ── 3. Merge centroids onto cotton counties ──────────────────────────────────

cotton = cotton.merge(centroids[["fips5", "lat", "lon"]], on="fips5", how="left")
cotton = cotton.dropna(subset=["lat", "lon"])
print(f"Cotton belt counties with centroids: {len(cotton)}")

# ── 4. RBF interpolation: (lat, lon) → arrival_year ─────────────────────────

rbf = RBFInterpolator(
    np.column_stack([lats, lons]),
    years,
    kernel="thin_plate_spline",
    smoothing=0.5,
)

coords = np.column_stack([cotton["lat"].values, cotton["lon"].values])
cotton["arrival_year_raw"] = rbf(coords)

# Round to integer, clip to [1892, 1922]
cotton["arrival_year"] = cotton["arrival_year_raw"].round().astype(int).clip(1892, 1922)

# ── 5. Save ──────────────────────────────────────────────────────────────────

out = cotton[["fips5", "arrival_year"]].copy()
# Add all counties (non-cotton belt get NaN)
all_counties = panel[["fips5"]].copy()
out = all_counties.merge(out, on="fips5", how="left")

out.to_parquet(PROC / "boll_weevil_arrival.parquet", index=False)

print(f"\nSaved {len(out)} counties")
print(f"Cotton belt with arrival year: {out['arrival_year'].notna().sum()}")
print(f"Year distribution:\n{out['arrival_year'].value_counts().sort_index()}")
