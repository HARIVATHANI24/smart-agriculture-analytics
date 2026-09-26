import pandas as pd
import numpy as np
import os

# ============================================================
# SMART AGRICULTURE ANALYTICS
# DATASET GENERATOR
# ============================================================

np.random.seed(42)

# ------------------------------------------------------------
# PROJECT PATH
# ------------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(BASE_DIR, "dataset")

os.makedirs(DATASET_DIR, exist_ok=True)

# ------------------------------------------------------------
# AGRICULTURE INFORMATION
# ------------------------------------------------------------

states = [
    "Tamil Nadu",
    "Karnataka",
    "Andhra Pradesh",
    "Telangana",
    "Kerala",
    "Maharashtra",
    "Punjab",
    "Haryana",
    "Uttar Pradesh",
    "West Bengal"
]

districts = {
    "Tamil Nadu": [
        "Thanjavur", "Madurai", "Coimbatore",
        "Trichy", "Salem"
    ],
    "Karnataka": [
        "Mysore", "Mandya", "Bangalore",
        "Belgaum", "Hassan"
    ],
    "Andhra Pradesh": [
        "Guntur", "Krishna", "Nellore",
        "Kurnool", "Chittoor"
    ],
    "Telangana": [
        "Hyderabad", "Warangal", "Nalgonda",
        "Karimnagar", "Khammam"
    ],
    "Kerala": [
        "Kochi", "Thrissur", "Palakkad",
        "Kollam", "Kannur"
    ],
    "Maharashtra": [
        "Pune", "Nashik", "Nagpur",
        "Kolhapur", "Satara"
    ],
    "Punjab": [
        "Amritsar", "Ludhiana", "Patiala",
        "Bathinda", "Jalandhar"
    ],
    "Haryana": [
        "Karnal", "Hisar", "Rohtak",
        "Panipat", "Ambala"
    ],
    "Uttar Pradesh": [
        "Lucknow", "Kanpur", "Agra",
        "Varanasi", "Meerut"
    ],
    "West Bengal": [
        "Kolkata", "Hooghly", "Nadia",
        "Murshidabad", "Burdwan"
    ]
}

crops = [
    "Rice",
    "Wheat",
    "Maize",
    "Cotton",
    "Sugarcane",
    "Groundnut",
    "Tomato",
    "Potato",
    "Onion",
    "Millet"
]

seasons = [
    "Kharif",
    "Rabi",
    "Zaid"
]

irrigation_types = [
    "Drip",
    "Sprinkler",
    "Canal",
    "Rainfed",
    "Borewell"
]

# ------------------------------------------------------------
# GENERATE RECORDS
# ------------------------------------------------------------

records = []

number_of_records = 5000

for i in range(number_of_records):

    state = np.random.choice(states)

    district = np.random.choice(
        districts[state]
    )

    crop = np.random.choice(crops)

    season = np.random.choice(seasons)

    year = np.random.randint(
        2018,
        2026
    )

    # --------------------------------------------------------
    # WEATHER
    # --------------------------------------------------------

    temperature = round(
        np.random.uniform(18, 38),
        2
    )

    humidity = round(
        np.random.uniform(40, 95),
        2
    )

    rainfall = round(
        np.random.uniform(300, 1800),
        2
    )

    # --------------------------------------------------------
    # SOIL PARAMETERS
    # --------------------------------------------------------

    soil_n = round(
        np.random.uniform(20, 140),
        2
    )

    soil_p = round(
        np.random.uniform(10, 100),
        2
    )

    soil_k = round(
        np.random.uniform(10, 150),
        2
    )

    soil_ph = round(
        np.random.uniform(5.0, 8.5),
        2
    )

    # --------------------------------------------------------
    # FARM INFORMATION
    # --------------------------------------------------------

    area = round(
        np.random.uniform(1, 100),
        2
    )

    irrigation = np.random.choice(
        irrigation_types
    )

    fertilizer = round(
        np.random.uniform(20, 250),
        2
    )

    pesticide = round(
        np.random.uniform(2, 80),
        2
    )

    # --------------------------------------------------------
    # CROP BASE YIELD
    # --------------------------------------------------------

    crop_yield_base = {
        "Rice": 4.2,
        "Wheat": 3.8,
        "Maize": 4.5,
        "Cotton": 2.8,
        "Sugarcane": 7.5,
        "Groundnut": 2.4,
        "Tomato": 5.5,
        "Potato": 6.0,
        "Onion": 4.8,
        "Millet": 2.2
    }

    base_yield = crop_yield_base[crop]

    # --------------------------------------------------------
    # ENVIRONMENT EFFECT
    # --------------------------------------------------------

    rainfall_effect = (
        rainfall / 1000
    )

    fertilizer_effect = (
        fertilizer / 100
    )

    soil_effect = (
        (soil_n / 100)
        + (soil_p / 100)
        + (soil_k / 150)
    ) / 3

    temperature_effect = (
        1 - abs(
            temperature - 27
        ) / 30
    )

    irrigation_effect = {
        "Drip": 1.15,
        "Sprinkler": 1.10,
        "Canal": 1.08,
        "Borewell": 1.05,
        "Rainfed": 0.90
    }

    irrigation_factor = irrigation_effect[
        irrigation
    ]

    # --------------------------------------------------------
    # CALCULATE YIELD
    # --------------------------------------------------------

    yield_value = (
        base_yield
        * (
            0.65
            + rainfall_effect * 0.12
            + fertilizer_effect * 0.10
            + soil_effect * 0.10
            + temperature_effect * 0.08
        )
        * irrigation_factor
    )

    # Add natural variation
    yield_value += np.random.normal(
        0,
        0.25
    )

    yield_value = max(
        yield_value,
        0.5
    )

    yield_value = round(
        yield_value,
        2
    )

    # --------------------------------------------------------
    # PRODUCTION
    # --------------------------------------------------------

    production = round(
        area * yield_value,
        2
    )

    # --------------------------------------------------------
    # MARKET PRICE
    # --------------------------------------------------------

    crop_price = {
        "Rice": 2400,
        "Wheat": 2200,
        "Maize": 1900,
        "Cotton": 6500,
        "Sugarcane": 3500,
        "Groundnut": 5800,
        "Tomato": 2500,
        "Potato": 1800,
        "Onion": 2200,
        "Millet": 3000
    }

    base_price = crop_price[crop]

    market_price = round(
        base_price
        * np.random.uniform(
            0.85,
            1.20
        ),
        2
    )

    # --------------------------------------------------------
    # REVENUE
    # --------------------------------------------------------

    revenue = round(
        production
        * market_price,
        2
    )

    # --------------------------------------------------------
    # ADD RECORD
    # --------------------------------------------------------

    records.append({

        "Record_ID": i + 1,

        "State": state,

        "District": district,

        "Crop": crop,

        "Season": season,

        "Year": year,

        "Area_Hectares": area,

        "Rainfall_mm": rainfall,

        "Temperature_C": temperature,

        "Humidity_Percent": humidity,

        "Soil_N": soil_n,

        "Soil_P": soil_p,

        "Soil_K": soil_k,

        "Soil_pH": soil_ph,

        "Irrigation": irrigation,

        "Fertilizer_kg": fertilizer,

        "Pesticide_Liters": pesticide,

        "Yield_Tons_Per_Hectare": yield_value,

        "Production_Tons": production,

        "Market_Price_Per_Ton": market_price,

        "Revenue": revenue
    })

# ------------------------------------------------------------
# CREATE DATAFRAME
# ------------------------------------------------------------

df = pd.DataFrame(records)

# ------------------------------------------------------------
# ADD SOME MISSING VALUES
# FOR DATA CLEANING PRACTICE
# ------------------------------------------------------------

missing_columns = [
    "Rainfall_mm",
    "Soil_N",
    "Soil_P",
    "Soil_K",
    "Humidity_Percent"
]

for column in missing_columns:

    random_indexes = np.random.choice(
        df.index,
        size=20,
        replace=False
    )

    df.loc[
        random_indexes,
        column
    ] = np.nan

# ------------------------------------------------------------
# SAVE DATASET
# ------------------------------------------------------------

output_file = os.path.join(
    DATASET_DIR,
    "agriculture_data.csv"
)

df.to_csv(
    output_file,
    index=False
)

# ------------------------------------------------------------
# DISPLAY INFORMATION
# ------------------------------------------------------------

print("=" * 60)

print(
    "SMART AGRICULTURE ANALYTICS"
)

print(
    "Dataset generation completed successfully!"
)

print("=" * 60)

print(
    f"Total records: {len(df)}"
)

print(
    f"Total columns: {len(df.columns)}"
)

print(
    f"Dataset saved at:\n{output_file}"
)

print("=" * 60)

print("\nFirst 5 records:")

print(
    df.head()
)

print("\nDataset shape:")

print(
    df.shape
)

print("\nCrop distribution:")

print(
    df["Crop"].value_counts()
)

print("\nMissing values:")

print(
    df.isnull().sum()
)

print("=" * 60)