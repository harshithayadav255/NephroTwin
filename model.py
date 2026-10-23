"""Optional baseline ML demo on synthetic labels; not clinical prediction."""
from pathlib import Path
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.impute import SimpleImputer

FEATURES = [
    "temperature_c", "heart_rate_bpm", "steps", "humidity_percent",
    "hydration_ml_simulated"
]

def make_synthetic_training_rows(n=3000, seed=42):
    """Create artificial rows and artificial labels for pipeline demonstration."""
    rng = __import__("numpy").random.default_rng(seed)
    df = pd.DataFrame({
        "temperature_c": rng.uniform(22, 43, n),
        "heart_rate_bpm": rng.uniform(50, 140, n),
        "steps": rng.integers(0, 2500, n),
        "humidity_percent": rng.uniform(20, 90, n),
        "hydration_ml_simulated": rng.integers(0, 500, n),
    })
    # Artificial rule-generated labels. These are NOT real clinical outcomes.
    z = (
        0.20 * (df.temperature_c - 30)
        + 0.035 * (df.heart_rate_bpm - 75)
        + 0.001 * df.steps
        - 0.008 * df.hydration_ml_simulated
        + 0.015 * (df.humidity_percent - 50)
    )
    p = 1 / (1 + __import__("numpy").exp(-z / 3))
    df["synthetic_event_label"] = rng.binomial(1, p)
    return df

def train_demo_model():
    df = make_synthetic_training_rows()
    X, y = df[FEATURES], df["synthetic_event_label"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )
    clf = make_pipeline(
        SimpleImputer(strategy="median"),
        RandomForestClassifier(n_estimators=120, random_state=42, class_weight="balanced")
    )
    clf.fit(X_train, y_train)
    pred = clf.predict(X_test)
    prob = clf.predict_proba(X_test)[:, 1]
    return clf, classification_report(y_test, pred, zero_division=0), roc_auc_score(y_test, prob)
