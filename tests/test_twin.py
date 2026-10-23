import pandas as pd
from digital_twin import strain_index, simulate_next_24h

def test_score_bounded():
    score = strain_index(35, 90, 500, 55, 200, 52)
    assert 0 <= score <= 100

def test_forecast_has_24_rows():
    row = pd.Series({
        "timestamp": pd.Timestamp("2026-10-19 12:00"),
        "temperature_c": 34.0,
        "heart_rate_bpm": 80,
        "steps": 300,
        "humidity_percent": 50,
        "hydration_ml_simulated": 200,
    })
    result = simulate_next_24h(row, 52)
    assert len(result) == 24
    assert "simulated_strain_index" in result.columns
