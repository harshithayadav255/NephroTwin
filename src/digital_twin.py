
def build_digital_twin(patient_data, wearable_data, patient_id):
    """Combine synthetic lab and wearable measurements."""

    patient = patient_data[
        patient_data["patient_id"] == patient_id
    ].sort_values("date")

    wearable = wearable_data[
        wearable_data["patient_id"] == patient_id
    ].sort_values("timestamp")

    if patient.empty:
        raise ValueError("No historical data for this patient.")

    if wearable.empty:
        raise ValueError("No wearable data for this patient.")

    latest = patient.iloc[-1]

    return {
        "patient_id": patient_id,
        "latest_creatinine": float(latest["creatinine"]),
        "latest_egfr": float(latest["egfr"]),
        "latest_lab_date": latest["date"],
        "average_heart_rate": round(
            float(wearable["heart_rate"].mean()), 1
        ),
        "total_simulated_steps": int(wearable["steps"].sum()),
        "historical_data": patient,
        "wearable_data": wearable
    }
