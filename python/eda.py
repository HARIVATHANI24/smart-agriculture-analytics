import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ============================================================
# SMART AGRICULTURE ANALYTICS
# EXPLORATORY DATA ANALYSIS
# ============================================================

print("=" * 70)
print("SMART AGRICULTURE ANALYTICS - EDA")
print("=" * 70)

# ------------------------------------------------------------
# PROJECT PATHS
# ------------------------------------------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATASET_DIR = os.path.join(
    BASE_DIR,
    "dataset"
)

CHART_DIR = os.path.join(
    BASE_DIR,
    "charts"
)

INPUT_FILE = os.path.join(
    DATASET_DIR,
    "clean_agriculture_data.csv"
)

# Create charts folder if it doesn't exist
os.makedirs(
    CHART_DIR,
    exist_ok=True
)

# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------

print("\nLoading cleaned dataset...")

df = pd.read_csv(INPUT_FILE)

print(
    f"Dataset loaded: {df.shape[0]} rows "
    f"and {df.shape[1]} columns"
)

# ============================================================
# 1. BASIC DATA ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("1. BASIC DATA ANALYSIS")
print("=" * 70)

print("\nColumns:")

print(
    df.columns.tolist()
)

print("\nData types:")

print(
    df.dtypes
)

print("\nStatistical summary:")

print(
    df.describe()
)

# ============================================================
# 2. CROP ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("2. CROP ANALYSIS")
print("=" * 70)

crop_summary = (
    df.groupby("Crop")
    .agg(
        Total_Production=(
            "Production_Tons",
            "sum"
        ),
        Average_Yield=(
            "Yield_Tons_Per_Hectare",
            "mean"
        ),
        Total_Area=(
            "Area_Hectares",
            "sum"
        ),
        Total_Revenue=(
            "Revenue",
            "sum"
        )
    )
    .sort_values(
        "Total_Production",
        ascending=False
    )
)

print("\nCrop summary:")

print(
    crop_summary
)

# ------------------------------------------------------------
# CHART 1 — PRODUCTION BY CROP
# ------------------------------------------------------------

plt.figure(
    figsize=(12, 6)
)

crop_production = (
    df.groupby("Crop")["Production_Tons"]
    .sum()
    .sort_values(
        ascending=False
    )
)

crop_production.plot(
    kind="bar"
)

plt.title(
    "Total Agricultural Production by Crop"
)

plt.xlabel(
    "Crop"
)

plt.ylabel(
    "Production (Tons)"
)

plt.xticks(
    rotation=45
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        CHART_DIR,
        "01_production_by_crop.png"
    ),
    dpi=300
)

plt.close()

print(
    "\nChart 1 saved: "
    "01_production_by_crop.png"
)

# ============================================================
# 3. AVERAGE YIELD BY CROP
# ============================================================

average_yield = (
    df.groupby("Crop")[
        "Yield_Tons_Per_Hectare"
    ]
    .mean()
    .sort_values(
        ascending=False
    )
)

plt.figure(
    figsize=(12, 6)
)

average_yield.plot(
    kind="bar"
)

plt.title(
    "Average Yield by Crop"
)

plt.xlabel(
    "Crop"
)

plt.ylabel(
    "Yield (Tons per Hectare)"
)

plt.xticks(
    rotation=45
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        CHART_DIR,
        "02_average_yield_by_crop.png"
    ),
    dpi=300
)

plt.close()

print(
    "Chart 2 saved: "
    "02_average_yield_by_crop.png"
)

# ============================================================
# 4. PRODUCTION BY STATE
# ============================================================

print("\n" + "=" * 70)
print("3. STATE ANALYSIS")
print("=" * 70)

state_production = (
    df.groupby("State")[
        "Production_Tons"
    ]
    .sum()
    .sort_values(
        ascending=False
    )
)

print("\nProduction by state:")

print(
    state_production
)

plt.figure(
    figsize=(12, 6)
)

state_production.plot(
    kind="bar"
)

plt.title(
    "Total Agricultural Production by State"
)

plt.xlabel(
    "State"
)

plt.ylabel(
    "Production (Tons)"
)

plt.xticks(
    rotation=45,
    ha="right"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        CHART_DIR,
        "03_production_by_state.png"
    ),
    dpi=300
)

plt.close()

print(
    "Chart 3 saved: "
    "03_production_by_state.png"
)

# ============================================================
# 5. SEASONAL ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("4. SEASONAL ANALYSIS")
print("=" * 70)

season_summary = (
    df.groupby("Season")
    .agg(
        Production=(
            "Production_Tons",
            "sum"
        ),
        Average_Yield=(
            "Yield_Tons_Per_Hectare",
            "mean"
        ),
        Revenue=(
            "Revenue",
            "sum"
        )
    )
)

print("\nSeason summary:")

print(
    season_summary
)

plt.figure(
    figsize=(10, 6)
)

season_production = (
    df.groupby("Season")[
        "Production_Tons"
    ]
    .sum()
)

season_production.plot(
    kind="bar"
)

plt.title(
    "Agricultural Production by Season"
)

plt.xlabel(
    "Season"
)

plt.ylabel(
    "Production (Tons)"
)

plt.xticks(
    rotation=0
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        CHART_DIR,
        "04_production_by_season.png"
    ),
    dpi=300
)

plt.close()

print(
    "Chart 4 saved: "
    "04_production_by_season.png"
)

# ============================================================
# 6. RAINFALL VS YIELD
# ============================================================

plt.figure(
    figsize=(10, 6)
)

sns.scatterplot(
    data=df,
    x="Rainfall_mm",
    y="Yield_Tons_Per_Hectare",
    hue="Crop",
    alpha=0.6
)

plt.title(
    "Rainfall vs Crop Yield"
)

plt.xlabel(
    "Rainfall (mm)"
)

plt.ylabel(
    "Yield (Tons per Hectare)"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        CHART_DIR,
        "05_rainfall_vs_yield.png"
    ),
    dpi=300
)

plt.close()

print(
    "Chart 5 saved: "
    "05_rainfall_vs_yield.png"
)

# ============================================================
# 7. TEMPERATURE VS YIELD
# ============================================================

plt.figure(
    figsize=(10, 6)
)

sns.scatterplot(
    data=df,
    x="Temperature_C",
    y="Yield_Tons_Per_Hectare",
    hue="Crop",
    alpha=0.6
)

plt.title(
    "Temperature vs Crop Yield"
)

plt.xlabel(
    "Temperature (°C)"
)

plt.ylabel(
    "Yield (Tons per Hectare)"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        CHART_DIR,
        "06_temperature_vs_yield.png"
    ),
    dpi=300
)

plt.close()

print(
    "Chart 6 saved: "
    "06_temperature_vs_yield.png"
)

# ============================================================
# 8. IRRIGATION ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("5. IRRIGATION ANALYSIS")
print("=" * 70)

irrigation_summary = (
    df.groupby("Irrigation")
    .agg(
        Average_Yield=(
            "Yield_Tons_Per_Hectare",
            "mean"
        ),
        Total_Production=(
            "Production_Tons",
            "sum"
        )
    )
    .sort_values(
        "Average_Yield",
        ascending=False
    )
)

print(
    irrigation_summary
)

plt.figure(
    figsize=(10, 6)
)

irrigation_yield = (
    df.groupby("Irrigation")[
        "Yield_Tons_Per_Hectare"
    ]
    .mean()
    .sort_values(
        ascending=False
    )
)

irrigation_yield.plot(
    kind="bar"
)

plt.title(
    "Average Yield by Irrigation Method"
)

plt.xlabel(
    "Irrigation Method"
)

plt.ylabel(
    "Average Yield"
)

plt.xticks(
    rotation=30
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        CHART_DIR,
        "07_yield_by_irrigation.png"
    ),
    dpi=300
)

plt.close()

print(
    "Chart 7 saved: "
    "07_yield_by_irrigation.png"
)

# ============================================================
# 9. FERTILIZER VS YIELD
# ============================================================

plt.figure(
    figsize=(10, 6)
)

sns.scatterplot(
    data=df,
    x="Fertilizer_kg",
    y="Yield_Tons_Per_Hectare",
    alpha=0.6
)

plt.title(
    "Fertilizer Usage vs Crop Yield"
)

plt.xlabel(
    "Fertilizer (kg)"
)

plt.ylabel(
    "Yield (Tons per Hectare)"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        CHART_DIR,
        "08_fertilizer_vs_yield.png"
    ),
    dpi=300
)

plt.close()

print(
    "Chart 8 saved: "
    "08_fertilizer_vs_yield.png"
)

# ============================================================
# 10. CORRELATION HEATMAP
# ============================================================

print("\n" + "=" * 70)
print("6. CORRELATION ANALYSIS")
print("=" * 70)

numeric_data = df.select_dtypes(
    include=np.number
)

correlation = numeric_data.corr()

print("\nCorrelation with Yield:")

print(
    correlation[
        "Yield_Tons_Per_Hectare"
    ]
    .sort_values(
        ascending=False
    )
)

plt.figure(
    figsize=(14, 10)
)

sns.heatmap(
    correlation,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    center=0
)

plt.title(
    "Agricultural Feature Correlation Matrix"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        CHART_DIR,
        "09_correlation_heatmap.png"
    ),
    dpi=300
)

plt.close()

print(
    "Chart 9 saved: "
    "09_correlation_heatmap.png"
)

# ============================================================
# 11. REVENUE BY CROP
# ============================================================

revenue_by_crop = (
    df.groupby("Crop")[
        "Revenue"
    ]
    .sum()
    .sort_values(
        ascending=False
    )
)

plt.figure(
    figsize=(12, 6)
)

revenue_by_crop.plot(
    kind="bar"
)

plt.title(
    "Total Agricultural Revenue by Crop"
)

plt.xlabel(
    "Crop"
)

plt.ylabel(
    "Revenue"
)

plt.xticks(
    rotation=45
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        CHART_DIR,
        "10_revenue_by_crop.png"
    ),
    dpi=300
)

plt.close()

print(
    "Chart 10 saved: "
    "10_revenue_by_crop.png"
)

# ============================================================
# 12. TOP INSIGHTS
# ============================================================

print("\n" + "=" * 70)
print("7. AGRICULTURAL INSIGHTS")
print("=" * 70)

top_production_crop = (
    crop_production.idxmax()
)

top_production_value = (
    crop_production.max()
)

top_yield_crop = (
    average_yield.idxmax()
)

top_yield_value = (
    average_yield.max()
)

top_state = (
    state_production.idxmax()
)

top_state_value = (
    state_production.max()
)

best_irrigation = (
    irrigation_yield.idxmax()
)

best_irrigation_yield = (
    irrigation_yield.max()
)

print(
    f"\nHighest production crop: "
    f"{top_production_crop}"
)

print(
    f"Production: "
    f"{top_production_value:,.2f} tons"
)

print(
    f"\nHighest average yield crop: "
    f"{top_yield_crop}"
)

print(
    f"Average yield: "
    f"{top_yield_value:.2f} tons/hectare"
)

print(
    f"\nHighest production state: "
    f"{top_state}"
)

print(
    f"Production: "
    f"{top_state_value:,.2f} tons"
)

print(
    f"\nHighest average yield irrigation method: "
    f"{best_irrigation}"
)

print(
    f"Average yield: "
    f"{best_irrigation_yield:.2f}"
)

# ============================================================
# 13. SAVE SUMMARY FILES
# ============================================================

crop_summary.to_csv(
    os.path.join(
        CHART_DIR,
        "crop_summary.csv"
    )
)

season_summary.to_csv(
    os.path.join(
        CHART_DIR,
        "season_summary.csv"
    )
)

irrigation_summary.to_csv(
    os.path.join(
        CHART_DIR,
        "irrigation_summary.csv"
    )
)

# ============================================================
# COMPLETION
# ============================================================

print("\n" + "=" * 70)

print(
    "EDA COMPLETED SUCCESSFULLY!"
)

print("=" * 70)

print(
    f"\nAll charts saved in:\n{CHART_DIR}"
)

print(
    "\nTotal charts generated: 10"
)

print(
    "\nYou can now use these charts "
    "for your report and presentation."
)

print("=" * 70)