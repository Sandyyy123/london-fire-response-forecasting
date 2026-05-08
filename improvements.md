# Improvements: London Fire Brigade Response Time (Project #04)

Role: IMPROVER. Recommendations only. No files in the project folder were modified.

## Top recommendation (single highest-leverage change)

**Build the planned `modeling_3` station-level fixed-effects feature using the mobilisation file.** The manuscript explicitly forecasts that this single change would lift R squared from 0.08 to past 0.20. The brief lists the mobilisation dataset as a required resource, yet it is currently unused. Concrete next steps: (1) load `london-fire-brigade-mobilisation-records`, (2) for each `IncidentStationGround`, compute the train-window mean and median first-pump attendance time using a strict pre-split mask to avoid leakage, (3) join the station mean and station median onto the modelling table as two new numeric columns, (4) re-fit the baseline XGBoost. Expected outcome: R squared 0.20-0.30, MAE drop of 15-25 seconds, no privacy regression because station-level statistics are public.

This is the single change with the largest expected effect-to-effort ratio on the project.

---

## Weakness 1: Mobilisation dataset entirely unused [HIGH]

The brief mandates two datasets (incident records AND mobilisation records). The current pipeline only consumes the incident file. The mobilisation file holds the per-pump deployment-and-arrival timestamps that would let the team reconstruct turn-out time, travel time, and station-of-origin response time as separate components. Without it, the project under-delivers against the brief and leaves the strongest predictive signal on the table.

Action: load the mobilisation CSV in a new `02_mobilisation_join.ipynb`, key on `IncidentNumber`, derive (a) station-level historical mean response, (b) turn-out vs travel split, (c) borough-station crosswalk. Use these as engineered features in `modeling_3`.

## Weakness 2: Random rather than time-respecting split [HIGH]

The 60/20/20 split uses `random_state=42` on the 2009-2017 window, with no time stratification. Because the 1.96M-row dataset spans 2009-2024 and the manuscript itself notes regime changes (station consolidation post-2018, COVID disruption post-2020), a random split inflates test performance versus any realistic deployment scenario where the model predicts future incidents from past training data.

Action: switch to a chronological split (train = 2009-2018, validation = 2019-2021, test = 2022-2024) and re-report all four metrics. If R squared drops materially, retrain with year fixed effects or rolling-origin cross-validation (`TimeSeriesSplit` with 5 folds).

## Weakness 3: Right-censoring at 1200 s never modelled [HIGH]

Both modelling notes flag the hard 1200-second cap as an operational truncation, but no model accommodates it. OLS, RF and standard XGBoost all treat the cap as a real value, biasing predictions for genuinely long-attendance incidents downward. The log-target XGBoost partially compensates but still treats 1200 as observed.

Action: fit a Tobit regression (use `statsmodels` censored regression or `survival`-style accelerated failure time via `lifelines` / `scikit-survival`) treating 1200 s as right-censored. Compare to a quantile-regression XGBoost (`objective='reg:quantileerror'` at q=0.5 and q=0.9) which is robust to the truncation and produces calibrated intervals at the same time.

## Weakness 4: Sample is only 200k of 1.96M rows; xlsx files unused for modelling [HIGH]

The manuscript trains on the first 200k rows of the 2009-2017 CSV only. The 670k 2018-2023 rows and 305k 2024+ rows are loaded only for distributional checks. The team has 9.8x more data available than they use, which is the cheapest available accuracy lever after Weakness 1.

Action: convert all three release files to Parquet with a single pre-processing script (the manuscript already calls this scaffold "produced"; verify and execute), then sample 1M rows stratified by year and incident group. Even doubling the sample to 400k typically lowers RMSE by 3-5 percent on tabular regressors at this scale.

## Weakness 5: No predictive intervals, no calibration check [MEDIUM]

The system outputs only point predictions. For control-room ETA deployment, the dispatcher needs an interval ("first pump in 4-7 minutes") and the planner needs probability of breach against the LFB six-minute target. Neither is provided. Calibration is also unverified: the team should know whether the predicted distribution matches the observed distribution at each decile.

Action: wrap the strongest XGBoost in MAPIE conformal prediction (`MapieRegressor`, alpha=0.1) for 90 percent intervals, and produce a reliability diagram bucketing predictions into deciles versus realised mean. Add coverage and Winkler-score columns to `metrics.json`.

## Weakness 6: Borough effects are hard-encoded; no hierarchical pooling [MEDIUM]

One-hot encoding 33 boroughs in the present setup forces every borough mean to be estimated from its own rows alone. Outer boroughs with fewer incidents (Bromley, Havering, Hillingdon) get noisier estimates, which the random forest sees as feature importance but cannot stabilise. A hierarchical / partial-pooling approach would shrink small-sample borough effects toward the global mean.

Action: replace one-hot borough with target encoding (out-of-fold mean attendance, smoothed by `(n_borough * mean_borough + alpha * mean_global) / (n_borough + alpha)`, alpha tuned on validation). Or fit a mixed-effects baseline with `statsmodels.MixedLM` using random intercepts for borough and station-ground. Borough information value usually doubles after this change.

## Weakness 7: Feature engineering is shallow [MEDIUM]

Only seven raw features are kept (hour, weekday, month, year, borough, incident-group, property-category). Operational signals freely available at dispatch are missed: (a) hour-x-weekday interaction (Friday-night vs Tuesday-3am differ even after main effects), (b) bank-holiday flag (UK gov calendar API), (c) school-holiday flag, (d) major-event flag (Premier League home games, New Year's Eve), (e) weather lag (wind, rain, temperature from Met Office API at the call hour), (f) cyclical encoding of hour and weekday (`sin`, `cos`) instead of integers.

Action: add the six features above using public data only. Cyclical encodings alone typically lift tree models 0.5-1 R squared point. Met Office hourly weather over 15 years adds 1-2 R squared points on outdoor and road-vehicle incidents.

## Weakness 8: No reproducibility scaffold [MEDIUM]

The repository ships a `.pkl` model and a `metrics.json` but no `requirements.txt`, no `environment.yml`, no `pyproject.toml`, no Dockerfile, no run-all script, no documented seed beyond `random_state=42` mentioned in prose. A reviewer cannot rerun the manuscript-supporting numbers from a clean environment without guesswork.

Action: add (a) `requirements.txt` pinning pandas, numpy, scikit-learn, xgboost, openpyxl, matplotlib versions; (b) a top-level `Makefile` with `make eda`, `make train`, `make report` targets; (c) `random_state=42` propagated explicitly into every train/test split and every estimator constructor; (d) a `data/checksums.txt` with sha256 of the three release files so future runs can detect upstream changes.

## Weakness 9: Fairness / equity audit absent [MEDIUM]

LFB response time is a public-equity metric. Model errors that systematically run longer in the most deprived London boroughs (Newham, Tower Hamlets, Barking) versus the wealthiest (Westminster, Kensington) would matter politically and ethically, and reviewers from a public-sector client will ask. The manuscript does not stratify residuals by borough deprivation, ethnic composition, or property tenure.

Action: split the test-set MAE by IMD (Index of Multiple Deprivation) decile using the published 2019 lookup of London LSOA-to-IMD, and report a residual-equity table. If the gap exceeds 15 seconds across IMD deciles, flag in the discussion and propose mitigation (re-weight training rows by inverse propensity to under-served boroughs).

## Weakness 10: Presentation HTML lacks executive numbers up front [LOW]

The deliverables include a 180 KB self-contained HTML, but the audience for this brief is operational (dispatch managers and fleet planners) not academic. A business reader needs the headline numbers (median ETA error 72 s, p95 error 275 s, ceiling R squared 0.08) on the first slide, then the operational implication (which model for which use case), then methodology.

Action: re-order the HTML so slide 1 is "What you can expect from this model: median ETA wrong by 72 s, 5 percent of incidents off by 4.5 minutes or more"; slide 2 is "Use Model A for fleet planning, Model B for caller ETA"; slide 3 is the privacy argument; technical detail moves to an appendix section.

---

## Priority summary

- HIGH: weaknesses 1, 2, 3, 4 (mobilisation join, time-split, censoring, sample size). All four are straightforward execution items that the manuscript already telegraphs as "planned."
- MEDIUM: weaknesses 5, 6, 7, 8, 9 (intervals, hierarchical pooling, feature engineering, reproducibility, equity audit).
- LOW: weakness 10 (presentation re-ordering).

Tackling the four HIGH items in sequence delivers a credible v2 manuscript with R squared 0.20+, calibrated intervals, time-respecting evaluation, and a residual-equity audit, with no new privacy-redaction work needed.
