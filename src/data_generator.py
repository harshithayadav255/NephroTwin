
import numpy as np
import pandas as pd


def generate_patient_data(patient_id="NT-001", seed=42):
    """Generate synthetic historical kidney measurements."""
    rng = np.random.default_rng(seed)

    dates = pd.date_range(
        end=pd.Timestamp.today().normalize(),
        periods=30,
        freq="D"
    )

    creatinine = np.clip(
        1.0 + np.cumsum(rng.normal(0, 0.015, 30)),
        0.4,
        4.0
    )

    egfr = np.clip(
        90 - np.cumsum(rng.normal(0.1, 0.8, 30)),
        5,
        150
    )

    return pd.DataFrame({
        "patient_id": patient_id,
        "date": dates,
        "creatinine": np.round(creatinine, 2),
        "egfr": np.round(egfr, 1)
    })


def generate_wearable_data(patient_id="NT-001", seed=43):
    """Generate synthetic wearable measurements."""
    rng = np.random.default_rng(seed)

    timestamps = pd.date_range(
        end=pd.Timestamp.now().floor("h"),
        periods=48,
        freq="h"
    )

    return pd.DataFrame({
        "patient_id": patient_id,
        "timestamp": timestamps,
        "heart_rate": rng.integers(60, 101, 48),
        "steps": rng.integers(0, 501, 48)
    })
