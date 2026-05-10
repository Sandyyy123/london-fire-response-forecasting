![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![LightGBM](https://img.shields.io/badge/LightGBM-regression-green) ![License](https://img.shields.io/badge/license-CC%20BY--NC%204.0-lightgrey)

# London Fire Brigade Response Time Forecasting

Time-series regression forecasting fire brigade first-response time from incident type, location, and temporal features.

---

## Task

**Time-series Regression**

---

## Architecture

```
LFB Incident Records → Spatio-temporal Feature Eng → LightGBM Regressor → SHAP Attribution
```

---

## Key Features

- Response time regression across 500K+ incidents
- Spatio-temporal feature engineering (ward, borough, hour, day-of-week)
- Incident type and property category encoding
- Time-of-day and seasonal demand patterns
- LightGBM with SHAP attribution for operational transparency

---

## Dataset

[London Fire Brigade Incident Records (data.london.gov.uk)](https://data.london.gov.uk/dataset/london-fire-brigade-incident-records)

---

## Project Structure

```
├── src/
│   ├── model_baseline.py      # Baseline model
│   └── model_advanced.py      # Advanced model
├── notebooks/
│   └── 01_EDA.ipynb           # Exploratory analysis
├── manuscripts/
│   └── manuscript.md          # IMRaD writeup
├── reports/
│   └── references.md          # Verified references
├── deliverables/
│   └── presentation.html      # Self-contained HTML
├── data/
│   └── README.md              # Dataset download instructions
└── requirements.txt
```

---

## Quick Start

```bash
git clone https://github.com/Sandyyy123/london-fire-response-forecasting.git
cd london-fire-response-forecasting
pip install -r requirements.txt

# See data/README.md for dataset download
jupyter notebook notebooks/01_eda.ipynb
# or run modeling:
jupyter notebook notebooks/03_modeling.ipynb
python src/model_advanced.py
```

---

## Tech Stack

`LightGBM · scikit-learn · pandas · geopandas`

---

## Author

**Dr. Sandeep Grover** — PhD Data Science, independent ML researcher, Mössingen, Germany.

---

## License

MIT
