# Modeling 1 - Baseline (London Fire Brigade Response Time Regression)

## Task

Regression: predict first-pump attendance time in seconds (`FirstPumpArriving_AttendanceTime`) from incident metadata available at dispatch time. The target is right-skewed with median ~297 s and p95 ~588 s; values are truncated above at 1,200 s.

## Data scope

For tractability, this run uses the 2009-2017 CSV file only (988,279 rows full file). A **200,000-row stratified-by-time sample** was drawn (`random_state=42`) for training; future iterations should sweep across the xlsx files for 2018-2024+.

Target stats on the sample:

- Mean: 321.7 s
- Median: 297 s
- SD: 143.5 s
- Min / Max: 1 s / 1,200 s

After dropping rows with missing target: ~181,500 rows usable for the modeling table.

## Features

Pre-dispatch only. Post-event columns dropped to avoid label leakage:

- Dropped: `SecondPumpArriving_AttendanceTime`, `NumStationsWithPumpsAttending`, `NumPumpsAttending`, `Notional Cost`, `PumpHoursRoundUp`, `FirstPumpArriving_DeployedFromStation`
- Dropped (high-cardinality / privacy-redacted): `Postcode_full`, `UPRN`, `USRN`, `IncidentNumber`, exact lat/lon, easting / northing
- Numeric: `hour`, `weekday`, `month`, `CalYear` (4 features)
- Categorical: `IncGeo_BoroughName` (33 London boroughs), `IncidentGroup` (Fire / False Alarm / Special Service), `PropertyCategory` (~10 categories)

Total feature count after one-hot encoding: ~50.

## Split

Random 60/20/20 split with `random_state=42`:

- Train: 108,894
- Val: 36,299
- Test: 36,299

## Baselines (test set)

| Model | RMSE (s) | MAE (s) | R² | abs-resid p50 | abs-resid p95 |
|---|---|---|---|---|---|
| Linear Regression | 139.5 | 98.8 | 0.064 | 74.5 | 281.0 |
| Random Forest (100 trees, depth 15) | 139.7 | 99.0 | 0.062 | 74.3 | 280.3 |
| XGBoost baseline (400 trees, depth 6) | 138.0 | 97.5 | 0.084 | 72.2 | 274.7 |

The R² ceiling is intentionally low (~0.08) on dispatch-time features alone. **Most of the variance in attendance time is driven by spatial detail** (distance from the nearest available station) which we explicitly removed because the project goal is a privacy-respecting, dispatch-time predictor that does not depend on UPRN or exact geolocation.

## Top features (Random Forest, impurity-based)

| Feature | Importance |
|---|---|
| hour | 0.179 |
| month | 0.139 |
| CalYear | 0.126 |
| weekday | 0.102 |
| IncGeo_BoroughName_HILLINGDON | 0.040 |
| PropertyCategory_Outdoor | 0.040 |
| PropertyCategory_Road Vehicle | 0.036 |
| IncidentGroup_False Alarm | 0.033 |
| IncGeo_BoroughName_ENFIELD | 0.029 |
| IncGeo_BoroughName_LAMBETH | 0.020 |

Time-of-day, year, and month dominate. Borough effects are second-tier. False-alarm calls and outdoor / road-vehicle property categories carry distinct response-time distributions.

## Configuration details

- Linear Regression: `LinearRegression` defaults on standardised numeric features.
- Random Forest: `n_estimators=100`, `max_depth=15`, `min_samples_leaf=3`.
- XGBoost: `n_estimators=400`, `max_depth=6`, `learning_rate=0.07`, `subsample=0.9`, `colsample_bytree=0.8`, `tree_method='hist'`.

## Takeaways

- The information ceiling on dispatch-time, privacy-preserving features is ROC R² ~0.08 / RMSE ~138 s. Spatial detail (nearest station distance, UPRN-level routing) would push this much higher but at the cost of privacy and operational realism.
- Hour, month, year and borough together capture the dominant temporal-spatial structure of London response times.
- Median absolute residual is ~72 s; p95 absolute residual ~275 s. Roughly half of incidents are predicted within 72 s of actuals.
