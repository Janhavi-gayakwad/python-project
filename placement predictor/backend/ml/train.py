import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "placements.csv"
MODEL_PATH = Path(__file__).resolve().parent / "model.joblib"

# Load CSV
data = pd.read_csv(DATA_PATH)

# Features & target
X = data.drop("placed", axis=1)
y = data["placed"]

FEATURES = list(X.columns)

numeric_features = ["cgpa", "twelfth_percentage", "technical_score",
                    "soft_skill_score", "internships", "projects", "backlogs"]
categorical_features = ["branch"]

# ColumnTransformer WITHOUT scaling
preprocessor = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)
], remainder='passthrough')  # keep numeric features as-is

pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(n_estimators=200, random_state=42))
])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
pipeline.fit(X_train, y_train)

MODEL_BUNDLE = {
    "pipeline": pipeline,
    "features": FEATURES
}
joblib.dump(MODEL_BUNDLE, MODEL_PATH)
print("✅ Model saved correctly. Probabilities will now be realistic (0–100%).")
