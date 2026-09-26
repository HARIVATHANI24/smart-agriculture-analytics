import pandas as pd
import sqlite3
import os

# ============================================================
# SMART AGRICULTURE ANALYTICS
# SQLITE DATABASE CREATION
# ============================================================

print("=" * 70)
print("SMART AGRICULTURE ANALYTICS - DATABASE")
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

DATABASE_DIR = os.path.join(
    BASE_DIR,
    "database"
)

INPUT_FILE = os.path.join(
    DATASET_DIR,
    "clean_agriculture_data.csv"
)

DATABASE_FILE = os.path.join(
    DATABASE_DIR,
    "agriculture.db"
)

# ------------------------------------------------------------
# CREATE DATABASE FOLDER
# ------------------------------------------------------------

os.makedirs(
    DATABASE_DIR,
    exist_ok=True
)

# ------------------------------------------------------------
# CHECK DATASET
# ------------------------------------------------------------

if not os.path.exists(INPUT_FILE):

    print("\nERROR!")
    print(
        "clean_agriculture_data.csv was not found."
    )

    print(
        f"\nExpected location:\n{INPUT_FILE}"
    )

    raise SystemExit

# ------------------------------------------------------------
# LOAD CLEAN DATA
# ------------------------------------------------------------

print("\n1. Loading cleaned agriculture data...")

df = pd.read_csv(
    INPUT_FILE
)

print(
    f"Loaded {len(df)} records."
)

# ------------------------------------------------------------
# CONNECT TO SQLITE
# ------------------------------------------------------------

print("\n2. Connecting to SQLite database...")

connection = sqlite3.connect(
    DATABASE_FILE
)

print(
    f"Database connected:\n{DATABASE_FILE}"
)

# ------------------------------------------------------------
# CREATE MAIN TABLE
# ------------------------------------------------------------

print("\n3. Creating agriculture_data table...")

df.to_sql(
    "agriculture_data",
    connection,
    if_exists="replace",
    index=False
)

print(
    "agriculture_data table created successfully."
)

# ------------------------------------------------------------
# CREATE CROP SUMMARY TABLE
# ------------------------------------------------------------

print("\n4. Creating crop_summary table...")

crop_summary = (
    df.groupby("Crop")
    .agg(
        Total_Production_Tons=(
            "Production_Tons",
            "sum"
        ),
        Average_Yield=(
            "Yield_Tons_Per_Hectare",
            "mean"
        ),
        Total_Area_Hectares=(
            "Area_Hectares",
            "sum"
        ),
        Total_Revenue=(
            "Revenue",
            "sum"
        )
    )
    .reset_index()
)

crop_summary.to_sql(
    "crop_summary",
    connection,
    if_exists="replace",
    index=False
)

print(
    "crop_summary table created successfully."
)

# ------------------------------------------------------------
# CREATE STATE SUMMARY TABLE
# ------------------------------------------------------------

print("\n5. Creating state_summary table...")

state_summary = (
    df.groupby("State")
    .agg(
        Total_Production_Tons=(
            "Production_Tons",
            "sum"
        ),
        Average_Yield=(
            "Yield_Tons_Per_Hectare",
            "mean"
        ),
        Total_Area_Hectares=(
            "Area_Hectares",
            "sum"
        ),
        Total_Revenue=(
            "Revenue",
            "sum"
        )
    )
    .reset_index()
)

state_summary.to_sql(
    "state_summary",
    connection,
    if_exists="replace",
    index=False
)

print(
    "state_summary table created successfully."
)

# ------------------------------------------------------------
# CREATE SEASON SUMMARY TABLE
# ------------------------------------------------------------

print("\n6. Creating season_summary table...")

season_summary = (
    df.groupby("Season")
    .agg(
        Total_Production_Tons=(
            "Production_Tons",
            "sum"
        ),
        Average_Yield=(
            "Yield_Tons_Per_Hectare",
            "mean"
        ),
        Total_Revenue=(
            "Revenue",
            "sum"
        )
    )
    .reset_index()
)

season_summary.to_sql(
    "season_summary",
    connection,
    if_exists="replace",
    index=False
)

print(
    "season_summary table created successfully."
)

# ------------------------------------------------------------
# CREATE IRRIGATION SUMMARY TABLE
# ------------------------------------------------------------

print("\n7. Creating irrigation_summary table...")

irrigation_summary = (
    df.groupby("Irrigation")
    .agg(
        Average_Yield=(
            "Yield_Tons_Per_Hectare",
            "mean"
        ),
        Total_Production_Tons=(
            "Production_Tons",
            "sum"
        ),
        Total_Area_Hectares=(
            "Area_Hectares",
            "sum"
        )
    )
    .reset_index()
)

irrigation_summary.to_sql(
    "irrigation_summary",
    connection,
    if_exists="replace",
    index=False
)

print(
    "irrigation_summary table created successfully."
)

# ------------------------------------------------------------
# VERIFY TABLES
# ------------------------------------------------------------

print("\n8. Checking database tables...")

cursor = connection.cursor()

cursor.execute(
    """
    SELECT name
    FROM sqlite_master
    WHERE type='table'
    ORDER BY name
    """
)

tables = cursor.fetchall()

print("\nTables inside database:")

for table in tables:

    print(
        f"  ✓ {table[0]}"
    )

# ------------------------------------------------------------
# CHECK MAIN TABLE RECORD COUNT
# ------------------------------------------------------------

print("\n9. Checking agriculture_data record count...")

cursor.execute(
    """
    SELECT COUNT(*)
    FROM agriculture_data
    """
)

record_count = cursor.fetchone()[0]

print(
    f"Total agriculture records: {record_count}"
)

# ------------------------------------------------------------
# SAMPLE DATABASE QUERY
# ------------------------------------------------------------

print("\n10. Testing database query...")

query = """
SELECT
    Crop,
    ROUND(SUM(Production_Tons), 2)
        AS Total_Production
FROM agriculture_data
GROUP BY Crop
ORDER BY Total_Production DESC
LIMIT 5;
"""

result = pd.read_sql_query(
    query,
    connection
)

print("\nTop 5 crops by production:")

print(
    result.to_string(
        index=False
    )
)

# ------------------------------------------------------------
# CLOSE DATABASE
# ------------------------------------------------------------

connection.close()

print("\n" + "=" * 70)

print(
    "DATABASE CREATED SUCCESSFULLY!"
)

print("=" * 70)

print(
    f"\nDatabase location:"
    f"\n{DATABASE_FILE}"
)

print(
    f"\nTotal records: {record_count}"
)

print(
    "\nTables created:"
)

for table in tables:

    print(
        f"  ✓ {table[0]}"
    )

print("\n" + "=" * 70)