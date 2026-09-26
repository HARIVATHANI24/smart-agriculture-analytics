import sqlite3
import pandas as pd
import os

# ============================================================
# SMART AGRICULTURE ANALYTICS
# SQL ANALYSIS ENGINE
# ============================================================

print("=" * 70)
print("SMART AGRICULTURE ANALYTICS - SQL ANALYSIS")
print("=" * 70)

# ------------------------------------------------------------
# PROJECT PATH
# ------------------------------------------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATABASE_FILE = os.path.join(
    BASE_DIR,
    "database",
    "agriculture.db"
)

OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "excel"
)

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

# ------------------------------------------------------------
# CONNECT DATABASE
# ------------------------------------------------------------

print("\nConnecting to database...")

connection = sqlite3.connect(
    DATABASE_FILE
)

print("Database connected successfully.")

# ============================================================
# QUERY 1 — KPI
# ============================================================

print("\n" + "=" * 70)
print("AGRICULTURE KPIs")
print("=" * 70)

kpi_query = """

SELECT

    COUNT(*) AS Total_Farms,

    COUNT(
        DISTINCT State
    ) AS Total_States,

    COUNT(
        DISTINCT Crop
    ) AS Total_Crops,

    ROUND(
        SUM(Area_Hectares),
        2
    ) AS Total_Area_Hectares,

    ROUND(
        SUM(Production_Tons),
        2
    ) AS Total_Production_Tons,

    ROUND(
        SUM(Revenue),
        2
    ) AS Total_Revenue,

    ROUND(
        AVG(Yield_Tons_Per_Hectare),
        2
    ) AS Average_Yield

FROM agriculture_data;

"""

kpi = pd.read_sql_query(
    kpi_query,
    connection
)

print(kpi.to_string(index=False))

# ============================================================
# QUERY 2 — CROP PERFORMANCE
# ============================================================

crop_query = """

SELECT

    Crop,

    ROUND(
        SUM(Production_Tons),
        2
    ) AS Total_Production,

    ROUND(
        AVG(Yield_Tons_Per_Hectare),
        2
    ) AS Average_Yield,

    ROUND(
        SUM(Revenue),
        2
    ) AS Total_Revenue

FROM agriculture_data

GROUP BY Crop

ORDER BY
    Total_Production DESC;

"""

crop_data = pd.read_sql_query(
    crop_query,
    connection
)

print("\n" + "=" * 70)
print("CROP PERFORMANCE")
print("=" * 70)

print(
    crop_data.to_string(
        index=False
    )
)

# ============================================================
# QUERY 3 — STATE PERFORMANCE
# ============================================================

state_query = """

SELECT

    State,

    ROUND(
        SUM(Production_Tons),
        2
    ) AS Total_Production,

    ROUND(
        AVG(Yield_Tons_Per_Hectare),
        2
    ) AS Average_Yield,

    ROUND(
        SUM(Revenue),
        2
    ) AS Total_Revenue

FROM agriculture_data

GROUP BY State

ORDER BY
    Total_Production DESC;

"""

state_data = pd.read_sql_query(
    state_query,
    connection
)

print("\n" + "=" * 70)
print("STATE PERFORMANCE")
print("=" * 70)

print(
    state_data.to_string(
        index=False
    )
)

# ============================================================
# QUERY 4 — SEASON PERFORMANCE
# ============================================================

season_query = """

SELECT

    Season,

    ROUND(
        SUM(Production_Tons),
        2
    ) AS Total_Production,

    ROUND(
        AVG(Yield_Tons_Per_Hectare),
        2
    ) AS Average_Yield,

    ROUND(
        SUM(Revenue),
        2
    ) AS Total_Revenue

FROM agriculture_data

GROUP BY Season

ORDER BY
    Total_Production DESC;

"""

season_data = pd.read_sql_query(
    season_query,
    connection
)

print("\n" + "=" * 70)
print("SEASON PERFORMANCE")
print("=" * 70)

print(
    season_data.to_string(
        index=False
    )
)

# ============================================================
# QUERY 5 — IRRIGATION PERFORMANCE
# ============================================================

irrigation_query = """

SELECT

    Irrigation,

    ROUND(
        AVG(Yield_Tons_Per_Hectare),
        2
    ) AS Average_Yield,

    ROUND(
        SUM(Production_Tons),
        2
    ) AS Total_Production

FROM agriculture_data

GROUP BY Irrigation

ORDER BY
    Average_Yield DESC;

"""

irrigation_data = pd.read_sql_query(
    irrigation_query,
    connection
)

print("\n" + "=" * 70)
print("IRRIGATION PERFORMANCE")
print("=" * 70)

print(
    irrigation_data.to_string(
        index=False
    )
)

# ============================================================
# SAVE EXCEL REPORT
# ============================================================

excel_file = os.path.join(
    OUTPUT_DIR,
    "agriculture_sql_analysis.xlsx"
)

print("\nCreating Excel analytics report...")

with pd.ExcelWriter(
    excel_file,
    engine="openpyxl"
) as writer:

    kpi.to_excel(
        writer,
        sheet_name="KPI",
        index=False
    )

    crop_data.to_excel(
        writer,
        sheet_name="Crop Analysis",
        index=False
    )

    state_data.to_excel(
        writer,
        sheet_name="State Analysis",
        index=False
    )

    season_data.to_excel(
        writer,
        sheet_name="Season Analysis",
        index=False
    )

    irrigation_data.to_excel(
        writer,
        sheet_name="Irrigation Analysis",
        index=False
    )

# ------------------------------------------------------------
# CLOSE DATABASE
# ------------------------------------------------------------

connection.close()

print("\n" + "=" * 70)

print(
    "SQL ANALYSIS COMPLETED SUCCESSFULLY!"
)

print("=" * 70)

print(
    f"\nExcel report created:"
    f"\n{excel_file}"
)

print("\nAnalysis sheets created:")

print("  ✓ KPI")

print("  ✓ Crop Analysis")

print("  ✓ State Analysis")

print("  ✓ Season Analysis")

print("  ✓ Irrigation Analysis")

print("=" * 70)