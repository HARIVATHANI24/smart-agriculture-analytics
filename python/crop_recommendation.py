import os
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, ConfusionMatrixDisplay


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

print("\n" + "=" * 65)
print("SMART AGRICULTURE ANALYTICS")
print("CROP RECOMMENDATION MACHINE LEARNING")
print("=" * 65)


# ============================================================
# 3. LOAD DATASET
# ============================================================

print("\nLoading dataset...")

df = pd.read_csv(DATA_PATH)

print("Dataset loaded successfully!")
print("Rows    :", df.shape[0])
print("Columns :", df.shape[1])


# ============================================================
# 4. SELECT FEATURES
# ============================================================

features = [
    "Soil_N",
    "Soil_P",
    "Soil_K",
    "Temperature_C",
    "Humidity_Percent",
    "Rainfall_mm",
    "Soil_pH"
]

target = "Crop"


# ============================================================
# 5. CHECK COLUMNS
# ============================================================

required_columns = features + [target]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:

    print("\nERROR!")
    print("Missing columns:")

    for column in missing_columns:
        print("-", column)

    raise ValueError(
        "Required columns are missing."
    )


# ============================================================
# 6. PREPARE X AND Y
# ============================================================

X = df[features].copy()
y = df[target].copy()

print("\nFeatures used:")

for feature in features:
    print("-", feature)

print("\nTarget:")
print("-", target)


# ============================================================
# 7. ENCODE CROP NAMES
# ============================================================

print("\nEncoding crop names...")

label_encoder = LabelEncoder()

y_encoded = label_encoder.fit_transform(y)

print("\nCrop classes:")

for number, crop in enumerate(label_encoder.classes_):
    print(f"{number} -> {crop}")


# ============================================================
# 8. TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_encoded,
    test_size=0.20,
    random_state=42,
    stratify=y_encoded
)

print("\nTraining records:", len(X_train))
print("Testing records :", len(X_test))


# ============================================================
# 9. CREATE RANDOM FOREST MODEL
# ============================================================

print("\nCreating Random Forest model...")

model = RandomForestClassifier(
    n_estimators=300,
    max_depth=18,
    min_samples_split=4,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)


# ============================================================
# 10. TRAIN MODEL
# ============================================================

print("\nTraining model...")

model.fit(
    X_train,
    y_train
)

print("Model training completed!")


# ============================================================
# 11. PREDICTION
# ============================================================

print("\nGenerating predictions...")

y_pred = model.predict(X_test)


# ============================================================
# 12. ACCURACY
# ============================================================

accuracy = accuracy_score(
    y_test,
    y_pred
)

print("\n" + "=" * 65)
print("MODEL PERFORMANCE")
print("=" * 65)

print(
    f"\nAccuracy: {accuracy * 100:.2f}%"
)


# ============================================================
# 13. CLASSIFICATION REPORT
# ============================================================

print("\nClassification Report")
print("-" * 65)

print(
    classification_report(
        y_test,
        y_pred,
        target_names=label_encoder.classes_,
        zero_division=0
    )
)


# ============================================================
# 14. CONFUSION MATRIX
# ============================================================

print("\nCreating confusion matrix...")

fig, ax = plt.subplots(
    figsize=(12, 10)
)

ConfusionMatrixDisplay.from_predictions(
    y_test,
    y_pred,
    display_labels=label_encoder.classes_,
    xticks_rotation=45,
    cmap="Blues",
    ax=ax
)

plt.title(
    "Crop Recommendation - Confusion Matrix"
)

plt.tight_layout()

confusion_path = os.path.join(
    CHART_DIR,
    "11_crop_confusion_matrix.png"
)

plt.savefig(
    confusion_path,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(
    "Confusion matrix saved:"
)

print(confusion_path)


# ============================================================
# 15. FEATURE IMPORTANCE
# ============================================================

print("\nCalculating feature importance...")

importance_df = pd.DataFrame({
    "Feature": features,
    "Importance": model.feature_importances_
})

importance_df = importance_df.sort_values(
    by="Importance",
    ascending=False
)

print("\nFeature Importance")
print("-" * 65)

print(
    importance_df.to_string(index=False)
)


# ============================================================
# 16. FEATURE IMPORTANCE CHART
# ============================================================

plt.figure(figsize=(10, 6))

plt.barh(
    importance_df["Feature"],
    importance_df["Importance"]
)

plt.xlabel("Importance")
plt.ylabel("Feature")

plt.title(
    "Crop Recommendation - Feature Importance"
)

plt.gca().invert_yaxis()

plt.tight_layout()

importance_path = os.path.join(
    CHART_DIR,
    "12_crop_feature_importance.png"
)

plt.savefig(
    importance_path,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(
    "\nFeature importance chart saved:"
)

print(importance_path)


# ============================================================
# 17. SAVE MODEL
# ============================================================

model_path = os.path.join(
    MODEL_DIR,
    "crop_recommendation_model.pkl"
)

encoder_path = os.path.join(
    MODEL_DIR,
    "crop_label_encoder.pkl"
)

joblib.dump(
    model,
    model_path
)

joblib.dump(
    label_encoder,
    encoder_path
)

print("\n" + "=" * 65)
print("MODEL SAVED SUCCESSFULLY")
print("=" * 65)

print("\nModel:")
print(model_path)

print("\nLabel Encoder:")
print(encoder_path)


# ============================================================
# 18. TEST WITH SAMPLE INPUT
# ============================================================

print("\n" + "=" * 65)
print("SAMPLE CROP RECOMMENDATION")
print("=" * 65)

sample_data = pd.DataFrame([
    {
        "Soil_N": 90,
        "Soil_P": 45,
        "Soil_K": 40,
        "Temperature_C": 27,
        "Humidity_Percent": 75,
        "Rainfall_mm": 180,
        "Soil_pH": 6.5
    }
])

sample_prediction = model.predict(
    sample_data
)

recommended_crop = label_encoder.inverse_transform(
    sample_prediction
)[0]

print("\nSample Conditions:")

for column in features:

    print(
        f"{column}: "
        f"{sample_data.iloc[0][column]}"
    )

print(
    f"\nRecommended Crop: {recommended_crop}"
)


# ============================================================
# 19. TOP 3 RECOMMENDATIONS
# ============================================================

probabilities = model.predict_proba(
    sample_data
)[0]

top_indices = np.argsort(
    probabilities
)[::-1][:3]

print("\nTop 3 Recommendations")
print("-" * 65)

for rank, index in enumerate(
    top_indices,
    start=1
):

    crop_name = label_encoder.inverse_transform(
        [index]
    )[0]

    probability = probabilities[index] * 100

    print(
        f"{rank}. {crop_name:<20} "
        f"{probability:.2f}%"
    )


# ============================================================
# 20. COMPLETED
# ============================================================

print("\n" + "=" * 65)
print("CROP RECOMMENDATION MODEL COMPLETED!")
print("=" * 65)

print("\nFiles created:")

print(
    "1. models/crop_recommendation_model.pkl"
)

print(
    "2. models/crop_label_encoder.pkl"
)

print(
    "3. charts/11_crop_confusion_matrix.png"
)

print(
    "4. charts/12_crop_feature_importance.png"
)

print("\nNext: Yield Prediction ML Model")