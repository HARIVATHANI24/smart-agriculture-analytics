import pandas as pd
import numpy as np
import os

# ============================================================
# SMART AGRICULTURE ANALYTICS
# DATA CLEANING MODULE
# ============================================================

print("=" * 70)
print("SMART AGRICULTURE ANALYTICS - DATA CLEANING")
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

INPUT_FILE = os.path.join(
    DATASET_DIR,
    "agriculture_data.csv"
)

OUTPUT_FILE = os.path.join(
    DATASET_DIR,
    "clean_agriculture_data.csv"
)

# ------------------------------------------------------------
# CHECK INPUT FILE
# ------------------------------------------------------------

if not os.path.exists(INPUT_FILE):

    print("\nERROR: agriculture_data.csv was not found.")

    print(
        f"\nExpected location:\n{INPUT_FILE}"
    )

    print(
        "\nRun data_generator.py first."
    )

    raise SystemExit

# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------

print("\n1. Loading agriculture dataset...")

df = pd.read_csv(INPUT_FILE)

print(
    f"Dataset loaded successfully: {df.shape[0]} rows, "
    f"{df.shape[1]} columns"
)

# ------------------------------------------------------------
# DISPLAY ORIGINAL INFORMATION
# ------------------------------------------------------------

print("\n2. Original dataset information")

print("-" * 70)

print(df.info())

# ------------------------------------------------------------
# CHECK DUPLICATES
# ------------------------------------------------------------

print("\n3. Checking duplicate records...")

duplicate_count = df.duplicated().sum()

print(
    f"Duplicate records found: {duplicate_count}"
)

if duplicate_count > 0:

    df = df.drop_duplicates()

    print(
        "Duplicate records removed."
    )

else:

    print(
        "No duplicate records found."
    )

# ------------------------------------------------------------
# CHECK MISSING VALUES
# ------------------------------------------------------------

print("\n4. Checking missing values")

print("-" * 70)

missing_values = df.isnull().sum()

print(missing_values)

total_missing = missing_values.sum()

print(
    f"\nTotal missing values: {total_missing}"
)

# ------------------------------------------------------------
# NUMERIC COLUMNS
# ------------------------------------------------------------

numeric_columns = [
    "Area_Hectares",
    "Rainfall_mm",
    "Temperature_C",
    "Humidity_Percent",
    "Soil_N",
    "Soil_P",
    "Soil_K",
    "Soil_pH",
    "Fertilizer_kg",
    "Pesticide_Liters",
    "Yield_Tons_Per_Hectare",
    "Production_Tons",
    "Market_Price_Per_Ton",
    "Revenue"
]

# ------------------------------------------------------------
# HANDLE MISSING NUMERIC VALUES
# USING MEDIAN
# ------------------------------------------------------------

print("\n5. Handling missing numeric values")

for column in numeric_columns:

    if column in df.columns:

        missing_before = df[column].isnull().sum()

        if missing_before > 0:

            median_value = df[column].median()

            df[column] = df[column].fillna(
                median_value
            )

            print(
                f"{column}: "
                f"{missing_before} missing values "
                f"filled with median "
                f"{median_value:.2f}"
            )

# ------------------------------------------------------------
# HANDLE MISSING CATEGORICAL VALUES
# ------------------------------------------------------------

categorical_columns = [
    "State",
    "District",
    "Crop",
    "Season",
    "Irrigation"
]

print("\n6. Handling missing categorical values")

for column in categorical_columns:

    if column in df.columns:

        missing_before = df[column].isnull().sum()

        if missing_before > 0:

            mode_value = df[column].mode()[0]

            df[column] = df[column].fillna(
                mode_value
            )

            print(
                f"{column}: "
                f"{missing_before} missing values "
                f"filled with mode '{mode_value}'"
            )

# ------------------------------------------------------------
# DATA TYPE CONVERSION
# ------------------------------------------------------------

print("\n7. Converting data types")

df["Record_ID"] = df["Record_ID"].astype(int)

df["Year"] = df["Year"].astype(int)

# ------------------------------------------------------------
# REMOVE INVALID VALUES
# ------------------------------------------------------------

print("\n8. Checking invalid values")

# Area cannot be zero or negative
df = df[
    df["Area_Hectares"] > 0
]

# Yield cannot be negative
df = df[
    df["Yield_Tons_Per_Hectare"] > 0
]

# Production cannot be negative
df = df[
    df["Production_Tons"] > 0
]

# Market price cannot be negative
df = df[
    df["Market_Price_Per_Ton"] > 0
]

# Soil pH should be within realistic range
df = df[
    (df["Soil_pH"] >= 4)
    &
    (df["Soil_pH"] <= 10)
]

print(
    f"Remaining records after validation: {len(df)}"
)

# ------------------------------------------------------------
# RE-CREATE RECORD ID
# ------------------------------------------------------------

df = df.reset_index(drop=True)

df["Record_ID"] = np.arange(
    1,
    len(df) + 1
)

# ------------------------------------------------------------
# ROUND NUMERIC VALUES
# ------------------------------------------------------------

rounding_columns = [
    "Area_Hectares",
    "Rainfall_mm",
    "Temperature_C",
    "Humidity_Percent",
    "Soil_N",
    "Soil_P",
    "Soil_K",
    "Soil_pH",
    "Fertilizer_kg",
    "Pesticide_Liters",
    "Yield_Tons_Per_Hectare",
    "Production_Tons",
    "Market_Price_Per_Ton",
    "Revenue"
]

for column in rounding_columns:

    if column in df.columns:

        df[column] = df[column].round(2)

# ------------------------------------------------------------
# FINAL MISSING VALUE CHECK
# ------------------------------------------------------------

print("\n9. Final missing value check")

remaining_missing = df.isnull().sum()

print(remaining_missing)

total_remaining_missing = remaining_missing.sum()

print(
    f"\nRemaining missing values: "
    f"{total_remaining_missing}"
)

# ------------------------------------------------------------
# SAVE CLEAN DATASET
# ------------------------------------------------------------

df.to_csv(
    OUTPUT_FILE,
    index=False
)

# ------------------------------------------------------------
# FINAL REPORT
# ------------------------------------------------------------

print("\n" + "=" * 70)

print(
    "DATA CLEANING COMPLETED SUCCESSFULLY!"
)

print("=" * 70)

print(
    f"\nOriginal dataset file:"
    f"\n{INPUT_FILE}"
)

print(
    f"\nClean dataset saved to:"
    f"\n{OUTPUT_FILE}"
)

print(
    f"\nFinal rows: {len(df)}"
)

print(
    f"Final columns: {len(df.columns)}"
)

print(
    f"\nFinal dataset size: {df.shape}"
)

print("\nSample cleaned data:")

print(
    df.head()
)

print("\n" + "=" * 70)