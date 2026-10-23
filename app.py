
import sys
from pathlib import Path

import streamlit as st
import pandas as pd

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from src.data_generator import (
    generate_patient_data,
    generate_wearable_data
)
from src.digital_twin import build_digital_twin
from src.risk_model import get_monitoring_context


st.set_page_config(
    page_title="NephroTwin",
    page_icon="🩺",
    layout="wide"
)

st.title("🩺 NephroTwin")
st.subheader("Kidney Health Digital Twin — Proof of Concept")

st.info(
    "Demonstration only: this prototype uses synthetic data. "
    "It is not a clinically validated prediction system."
)

# 1. Patient selection
st.sidebar.header("Patient Simulation")

patient_id = st.sidebar.selectbox(
    "Select synthetic patient",
    ["NT-001", "NT-002", "NT-003"]
)

seed = int(patient_id[-1])

patient_data = generate_patient_data(
    patient_id, seed=40 + seed
)

wearable_data = generate_wearable_data(
    patient_id, seed=50 + seed
)

# 2. Hypothetical patient inputs
st.sidebar.header("Explore a Hypothetical Scenario")

creatinine = st.sidebar.number_input(
    "Creatinine (mg/dL)",
    min_value=0.1,
    max_value=15.0,
    value=float(patient_data.iloc[-1]["creatinine"]),
    step=0.1
)

egfr = st.sidebar.number_input(
    "eGFR (mL/min/1.73 m²)",
    min_value=1.0,
    max_value=150.0,
    value=float(patient_data.iloc[-1]["egfr"]),
    step=1.0
)

bp = st.sidebar.slider(
    "Systolic blood pressure (mmHg)",
    min_value=70,
    max_value=220,
    value=120
)

# Update the latest synthetic measurements
patient_data.loc[
    patient_data.index[-1], "creatinine"
] = creatinine

patient_data.loc[
    patient_data.index[-1], "egfr"
] = egfr

# 3. Build the digital twin
twin = build_digital_twin(
    patient_data,
    wearable_data,
    patient_id
)

# 4. Patient overview
st.header("1. Patient Overview")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Patient ID", patient_id)
c2.metric("Creatinine", f"{creatinine:.2f} mg/dL")
c3.metric("eGFR", f"{egfr:.1f}")
c4.metric("Systolic BP", f"{bp} mmHg")

# 5. Historical lab measurements
st.header("2. Historical Lab Measurements")

left, right = st.columns(2)

with left:
    st.write("Creatinine Trend")
    st.line_chart(
        patient_data.set_index("date")["creatinine"]
    )

with right:
    st.write("eGFR Trend")
    st.line_chart(
        patient_data.set_index("date")["egfr"]
    )

with st.expander("View synthetic lab records"):
    st.dataframe(patient_data, use_container_width=True)

# 6. Wearable measurements
st.header("3. Wearable Measurements")

w1, w2 = st.columns(2)

with w1:
    st.write("Heart Rate — Simulated 48 Hours")
    st.line_chart(
        wearable_data.set_index("timestamp")["heart_rate"]
    )

with w2:
    st.write("Hourly Activity — Simulated Steps")
    st.bar_chart(
        wearable_data.set_index("timestamp")["steps"]
    )

m1, m2 = st.columns(2)

m1.metric(
    "Average Simulated Heart Rate",
    f"{twin['average_heart_rate']} bpm"
)

m2.metric(
    "Total Simulated Steps",
    f"{twin['total_simulated_steps']:,}"
)

# 7. Integrated digital twin
st.header("4. Integrated Digital Twin")

st.write(
    "The system combines synthetic lab measurements "
    "and wearable summaries for the selected patient."
)

st.json({
    "patient_id": twin["patient_id"],
    "latest_creatinine": twin["latest_creatinine"],
    "latest_egfr": twin["latest_egfr"],
    "average_heart_rate": twin["average_heart_rate"],
    "total_simulated_steps": twin["total_simulated_steps"]
})

# 8. Educational measurement context
st.header("5. Kidney Measurement Context")

context = get_monitoring_context(egfr)

st.subheader(context["category"])
st.write(context["message"])

# 9. What-if scenario
st.header("6. What-if Scenario Simulator")

change = st.slider(
    "Hypothetical eGFR change (%)",
    min_value=-30,
    max_value=30,
    value=0,
    step=5
)

scenario_egfr = egfr * (1 + change / 100)

a, b = st.columns(2)

a.metric("Current Entered eGFR", f"{egfr:.1f}")

b.metric(
    "Hypothetical eGFR",
    f"{scenario_egfr:.1f}",
    delta=f"{change:+d}%"
)

st.caption(
    "This is a mathematical illustration, not a forecast "
    "of an actual patient's health."
)

st.bar_chart(
    pd.DataFrame({
        "Scenario": ["Current Input", "Hypothetical"],
        "eGFR": [egfr, scenario_egfr]
    }).set_index("Scenario")
)

# 10. Download synthetic data
st.header("7. Export Demonstration Data")

csv_data = patient_data.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download Synthetic Lab Data (CSV)",
    data=csv_data,
    file_name=f"{patient_id}_synthetic_labs.csv",
    mime="text/csv"
)

st.success("NephroTwin demonstration dashboard is ready!")

st.caption(
    "NephroTwin PoC | Synthetic data only | "
    "Not for diagnosis or clinical decisions"
)
