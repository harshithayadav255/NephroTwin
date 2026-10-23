# NephroTwin
**A Personalized Digital Twin Prototype for Heat-Associated Physiological Strain in Early-Stage Chronic Kidney Disease**

## Team details
- Team name: Twintechies
- College/incubator: G.Narayanamma institute of technology and sciences
- Team leader: G.Bhuvana sri
- Team members: G.Harshitha yadav

## Problem statement
People living with early-stage chronic kidney disease may respond differently to heat exposure and activity because of differences in baseline health. NephroTwin is a proof-of-concept virtual patient that combines a fictional historical clinical profile with synthetic hourly wearable and environmental inputs. It updates an illustrative physiological-strain index and lets users compare hypothetical 24-hour scenarios.

## Important scope boundary
This submission uses synthetic data and a hand-set illustrative index. It does **not** diagnose CKD, predict acute kidney injury, or estimate clinically validated risk. Synthetic labels or scores are not evidence of medical accuracy. Do not use for patient care.

## Features
- Static historical profile + hourly sensor/environment stream
- Reproducible synthetic data generation
- Transparent 0–100 illustrative strain index
- 24-hour hypothetical scenario simulation
- Streamlit dashboard with time-series charts and scenario controls
- Basic automated tests

## Architecture
1. `generate_data.py` creates `patient_static.csv` and `wearable_timeseries.csv`.
2. `app.py` loads the two streams.
3. `digital_twin.py` updates an illustrative index and simulates a hypothetical next 24 hours.
4. Streamlit displays trends and scenario comparisons.
5. `tests/` checks basic software behaviour.

## Setup (Windows PowerShell)
Install Python 3.12 (64-bit) from https://www.python.org/downloads/windows/ and enable **Add python.exe to PATH** during installation.

```powershell
python --version
cd C:\NephroTwin
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python generate_data.py
streamlit run app.py
```

If PowerShell blocks activation, use `.\.venv\Scripts\python.exe -m pip install -r requirements.txt`, then `.\.venv\Scripts\streamlit.exe run app.py`.

## Testing
```powershell
python -m pytest
```
Install pytest first with `python -m pip install pytest` if needed.

## Data dictionary
- `patient_static.csv`: fictional demographics and historical profile values.
- `wearable_timeseries.csv`: 168 synthetic hourly rows with timestamp, heart rate, steps, temperature, humidity, simulated hydration input, and a simulated sleep indicator.
- Every row is synthetic. No real patient information is included.

## Model and evaluation
The current index is an interpretable, hand-weighted demonstration function, not a trained or clinically validated model. No clinical accuracy claim is made. A future research version should use appropriately sourced labelled data, patient-level splits to prevent leakage, calibration, subgroup analysis, external validation, and clinical oversight.

## Submission files
- `docs/architecture.pdf`
- `docs/presentation.pdf`
- Source code and data-generation script
- Public repository URL: REPLACE

## License
MIT; see `LICENSE`.
