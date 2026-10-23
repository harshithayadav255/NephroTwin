"""Generate reproducible synthetic NephroTwin data. Not real patient data."""
from pathlib import Path
import numpy as np
import pandas as pd

SEED = 42
OUT = Path("data")
OUT.mkdir(exist_ok=True)
rng = np.random.default_rng(SEED)

# Fictional profile for software demonstration only.
patient = pd.DataFrame([{
    "patient_id": "NT001",
    "age_years": 52,
    "ckd_stage_label": "G3a (fictional example)",
    "baseline_egfr_ml_min_1_73m2": 52.0,
    "baseline_creatinine_mg_dl": 1.4,
    "hypertension_history": 1,
    "diabetes_history": 0,
    "baseline_systolic_bp_mmhg": 132,
    "data_status": "SYNTHETIC - NOT A REAL PATIENT"
}])
patient.to_csv(OUT / "patient_static.csv", index=False)

timestamps = pd.date_range("2026-10-13 00:00:00", periods=7 * 24, freq="h")
rows = []
for i, ts in enumerate(timestamps):
    hour = ts.hour
    # A simple artificial daily cycle; not a validated weather model.
    temp = 31 + 5.0 * np.sin(2 * np.pi * (hour - 9) / 24) + rng.normal(0, 1.0)
    temp = float(np.clip(temp, 20, 43))
    humidity = float(np.clip(58 - 1.1 * (temp - 30) + rng.normal(0, 4), 20, 90))
    daytime = 7 <= hour <= 19
    steps = int(rng.integers(100, 900) if daytime else rng.integers(0, 150))
    hr = 69 + steps / 170 + max(0, temp - 32) * 1.1 + rng.normal(0, 3)
    hr = int(np.clip(hr, 48, 145))
    hydration = int(rng.integers(100, 301) if daytime else rng.integers(0, 101))
    rows.append({
        "patient_id": "NT001",
        "timestamp": ts,
        "heart_rate_bpm": hr,
        "steps": steps,
        "temperature_c": round(temp, 2),
        "humidity_percent": round(humidity, 2),
        "hydration_ml_simulated": hydration,
        "sleep_indicator_simulated": int(hour < 6 or hour >= 23),
        "data_status": "SYNTHETIC - NOT MEASURED"
    })
pd.DataFrame(rows).to_csv(OUT / "wearable_timeseries.csv", index=False)
print("Synthetic dataset created.")
print(f"Patient profiles: {len(patient)}")
print(f"Hourly sensor rows: {len(rows)}")
print(f"Files written to: {OUT.resolve()}")
