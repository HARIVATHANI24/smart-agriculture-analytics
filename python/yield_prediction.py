# ============================================================
# SMART AGRICULTURE ANALYTICS
# YIELD PREDICTION MACHINE LEARNING MODEL
# ============================================================

import os
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


# ============================================================
# 1. PROJECT PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATA_PATH = os.path.join(
    BASE_DIR,
    "dataset",
    "clean_agriculture_data.csv"
)

MODEL_DIR = os.path.join(
    BASE_DIR,
    "models"
)

CHART_DIR = os.path.join(
    BASE_DIR,
    "charts"
)

os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(CHART_DIR, exist_ok=True)


# ============================================================
# 2. HEADER
# ============================================================

print("\n" + "=" * 70)
print("SMART AGRICULTURE ANALYTICS")
print("YIELD PREDICTION MACHINE LEARNING")
print("=" * 70)


# ============================================================
# 3. LOAD DATASET
# ============================================================

print("\nLoading dataset...")

df = pd.read_csv(DATA_PATH)

print("Dataset loaded successfully!")

print("Rows    :", df.shape[0])
print("Columns :", df.shape[1])


# ============================================================
# 4. FEATURES
# ============================================================

numeric_features = [
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
    "Market_Price_Per_Ton"
]

categorical_features = [
    "Crop",
    "Season",
    "Irrigation"
]

target = "Yield_Tons_Per_Hectare"


# ============================================================
# 5. CHECK REQUIRED COLUMNS
# ============================================================

required_columns = (
    numeric_features
    + categorical_features
    + [target]
)

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:

    print("\nERROR!")
    print("The following columns are missing:")

    for column in missing_columns:
        print("-", column)

    raise ValueError(
        "Required columns are missing from dataset."
    )


# ============================================================
# 6. PREPARE X AND Y
# ============================================================

X = df[
    numeric_features + categorical_features
].copy()

y = df[target].copy()

print("\nNumeric features:")

for feature in numeric_features:
    print("-", feature)

print("\nCategorical features:")

for feature in categorical_features:
    print("-", feature)

print("\nTarget:")
print("-", target)


# ============================================================
# 7. TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

print("\nTraining records:", len(X_train))
print("Testing records :", len(X_test))


# ============================================================
# 8. PREPROCESSING
# ============================================================

print("\nCreating preprocessing pipeline...")

preprocessor = ColumnTransformer(
    transformers=[
        (
            "numeric",
            "passthrough",
            numeric_features
        ),
        (
            "categorical",
            OneHotEncoder(
                handle_unknown="ignore"
            ),
            categorical_features
        )
    ]
)


# ============================================================
# 9. RANDOM FOREST REGRESSOR
# ============================================================

print("Creating Random Forest Regressor...")

regressor = RandomForestRegressor(
    n_estimators=300,
    max_depth=20,
    min_samples_split=4,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)


# ============================================================
# 10. COMPLETE PIPELINE
# ============================================================

model = Pipeline(
    steps=[
        (
            "preprocessor",
            preprocessor
        ),
        (
            "regressor",
            regressor
        )
    ]
)


# ============================================================
# 11. TRAIN MODEL
# ============================================================

print("\nTraining yield prediction model...")

model.fit(
    X_train,
    y_train
)

print("Model training completed!")


# ============================================================
# 12. PREDICTION
# ============================================================

print("\nGenerating predictions...")

y_pred = model.predict(
    X_test
)


# ============================================================
# 13. MODEL EVALUATION
# ============================================================

mae = mean_absolute_error(
    y_test,
    y_pred
)

mse = mean_squared_error(
    y_test,
    y_pred
)

rmse = np.sqrt(mse)

r2 = r2_score(
    y_test,
    y_pred
)


# ============================================================
# 14. DISPLAY PERFORMANCE
# ============================================================

print("\n" + "=" * 70)
print("YIELD PREDICTION MODEL PERFORMANCE")
print("=" * 70)

print(
    f"\nMean Absolute Error (MAE): "
    f"{mae:.4f}"
)

print(
    f"Root Mean Squared Error (RMSE): "
    f"{rmse:.4f}"
)

print(
    f"R² Score: "
    f"{r2:.4f}"
)

print(
    f"R² Percentage: "
    f"{r2 * 100:.2f}%"
)


# ============================================================
# 15. ACTUAL VS PREDICTED DATA
# ============================================================

results_df = pd.DataFrame({
    "Actual_Yield": y_test.values,
    "Predicted_Yield": y_pred
})

results_df["Difference"] = (
    results_df["Actual_Yield"]
    - results_df["Predicted_Yield"]
)

print("\nSample Predictions:")

print(
    results_df.head(10).to_string(
        index=False
    )
)


# ============================================================
# 16. ACTUAL VS PREDICTED CHART
# ============================================================

print("\nCreating actual vs predicted chart...")

plt.figure(
    figsize=(10, 7)
)

plt.scatter(
    y_test,
    y_pred,
    alpha=0.6
)

minimum = min(
    y_test.min(),
    y_pred.min()
)

maximum = max(
    y_test.max(),
    y_pred.max()
)

plt.plot(
    [minimum, maximum],
    [minimum, maximum],
    linestyle="--"
)

plt.xlabel(
    "Actual Yield (Tons/Hectare)"
)

plt.ylabel(
    "Predicted Yield (Tons/Hectare)"
)

plt.title(
    "Yield Prediction - Actual vs Predicted"
)

plt.tight_layout()

actual_predicted_path = os.path.join(
    CHART_DIR,
    "13_yield_actual_vs_predicted.png"
)

plt.savefig(
    actual_predicted_path,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(
    "Chart saved:"
)

print(
    actual_predicted_path
)


# ============================================================
# 17. SAVE PREDICTION RESULTS
# ============================================================

results_path = os.path.join(
    CHART_DIR,
    "yield_prediction_results.csv"
)

results_df.to_csv(
    results_path,
    index=False
)

print(
    "\nPrediction results saved:"
)

print(
    results_path
)


# ============================================================
# 18. SAVE MODEL
# ============================================================

model_path = os.path.join(
    MODEL_DIR,
    "yield_prediction_model.pkl"
)

joblib.dump(
    model,
    model_path
)

print("\n" + "=" * 70)
print("MODEL SAVED SUCCESSFULLY")
print("=" * 70)

print(
    "\nModel:"
)

print(
    model_path
)


# ============================================================
# 19. SAMPLE YIELD PREDICTION
# ============================================================

print("\n" + "=" * 70)
print("SAMPLE YIELD PREDICTION")
print("=" * 70)

sample_data = pd.DataFrame([
    {
        "Area_Hectares": 10,
        "Rainfall_mm": 180,
        "Temperature_C": 27,
        "Humidity_Percent": 75,
        "Soil_N": 90,
        "Soil_P": 45,
        "Soil_K": 40,
        "Soil_pH": 6.5,
        "Fertilizer_kg": 120,
        "Pesticide_Liters": 5,
        "Market_Price_Per_Ton": 25000,
        "Crop": "Rice",
        "Season": "Kharif",
        "Irrigation": "Canal"
    }
])

sample_prediction = model.predict(
    sample_data
)[0]

print("\nSample Conditions:")

for column in sample_data.columns:

    print(
        f"{column}: "
        f"{sample_data.iloc[0][column]}"
    )

print(
    f"\nPredicted Yield: "
    f"{sample_prediction:.2f} Tons/Hectare"
)


# ============================================================
# 20. COMPLETION
# ============================================================

print("\n" + "=" * 70)
print("YIELD PREDICTION MODEL COMPLETED!")
print("=" * 70)

print("\nFiles created:")

print(
    "1. models/yield_prediction_model.pkl"
)

print(
    "2. charts/13_yield_actual_vs_predicted.png"
)

print(
    "3. charts/yield_prediction_results.csv"
)

print("\nNext: Streamlit Dashboard")