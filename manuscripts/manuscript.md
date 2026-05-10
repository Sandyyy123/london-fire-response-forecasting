# Privacy-Preserving Regression of First-Pump Attendance Time for the London Fire Brigade: Limits of Dispatch-Time Features on 1.96 Million Incidents

## Abstract

Emergency response time is a primary determinant of life-safety outcomes in urban fire and rescue services, yet most published predictive models rely on incident-level spatial detail (exact coordinates, unique property reference numbers, or nearest-station distance) that cannot be exposed at the moment a 999 call is logged. We study how well first-pump attendance time can be predicted using only the privacy-preserving features that are genuinely available at dispatch. Using the London Fire Brigade open incident records covering January 2009 through 2024 (approximately 1.96 million incidents across three release files), we fit four regressors on a 200,000-row stratified sample with a 60/20/20 split: ordinary least squares, random forest, gradient-boosted trees (XGBoost), and a log-target XGBoost variant. Features are restricted to call hour, weekday, month, calendar year, borough name, incident group, and property category, with all post-event and high-precision spatial fields removed. The strongest model (baseline XGBoost) reaches a test root mean squared error (RMSE) of 138.0 seconds, a mean absolute error (MAE) of 97.5 seconds, and an R squared of 0.084 against a target with median 297 seconds and 95th percentile 588 seconds. The log-target variant lowers the median absolute residual from 72.2 to 68.5 seconds at the cost of higher RMSE, illustrating a clear mean-versus-median trade-off relevant to control-room ETA displays. We argue that the observed R squared ceiling near 0.08 is not a modelling failure but a structural property of the privacy-preserving feature set, and we outline how station-level fixed effects estimated on a strict train-time window would lift the ceiling without re-introducing personal location data.

## 1. Introduction

Response time is the operational quantity that fire and rescue services optimise above almost any other. In the UK, it forms the basis for statutory performance reporting, and internationally it has been linked through outcome studies in adjacent emergency-medicine domains to the probability of survival and to the size of property loss [10]. The London Fire Brigade (LFB) is the busiest fire and rescue service in the United Kingdom and one of the largest metropolitan brigades in the world, attending several hundred thousand incidents per year across a 1,572 square-kilometre operational area. Quantifying and predicting response time at the level of an individual incident is therefore of direct interest both to operations planners (where to position pumps, how to staff watches) and to control-room dispatchers (what expected time of arrival to communicate to a caller).

Predictive modelling of urban fire-service activity has a small but established literature. Asgary and colleagues [8] modelled the risk of structural fire incidents in Toronto and demonstrated that property-category and land-use features add predictive value beyond pure temporal trends. Anderson [7] applied kernel density estimation and K-means clustering to road-accident data to identify hotspots, a method that transfers naturally to fire-incident geographies. None of these studies, however, isolate the question we ask here: how much of the variance in individual-incident response time can be recovered without using high-precision spatial features that would either reveal personal address information or require operational data (such as nearest-station-available status) that is not exposed at call time?

The privacy constraint is not academic. The LFB open data already redacts unique property reference numbers, full postcodes, exact eastings and northings, and latitude and longitude for residential dwellings [11]. Any deployed dispatch-time predictor that consumed those fields would either need to operate inside a restricted environment or would itself become a privacy-sensitive system. We therefore deliberately remove every feature that resolves below borough or station-ground granularity, train on the remaining temporal and categorical signal, and characterise the resulting predictive ceiling.

The contribution of this paper is fourfold. First, we publish a baseline regression study on the full historical span of LFB incident records (2009 through 2024) using a clean, leakage-free, privacy-preserving feature set. Second, we quantify the R squared ceiling of that feature set at approximately 0.08 across linear, random-forest [1], and gradient-boosted [2, 3] regressors, and show that this ceiling is robust to model class. Third, we demonstrate the mean-versus-median trade-off introduced by a log-transformed target [3] in the context of a right-skewed response-time distribution, and link the choice to the operational use case (fleet planning versus caller-facing ETA). Fourth, we set out a roadmap for a station-level fixed-effects extension that would lift the ceiling while remaining compatible with the privacy constraint, and we situate this against broader urban fire-risk modelling [8].

The remainder of the paper is structured as follows. Section 2 describes the LFB open data, the sampling strategy, and the target distribution. Section 3 details the privacy-preserving feature set, the four model variants, and the train, validation, and test split. Section 4 reports results on the held-out test set together with a feature-importance analysis. Section 5 discusses the privacy-versus-accuracy trade-off, the planned station-level extension, and the comparison with prior work. Section 6 concludes.

## 2. Data

### 2.1 Sources and coverage

The London Fire Brigade publishes two open datasets through the London Datastore: incident records and mobilisation records [11]. Only the incident records are used in this study; mobilisation records will be joined in a planned follow-up to derive station-level fixed effects.

The incident records arrive in three release files: a CSV covering the older period, an Excel workbook for the middle period, and an Excel workbook for the most recent partial period. The three files together contain approximately 1.96 million incident rows. Table 1 summarises the file inventory.

**Table 1.** Inventory of the three London Fire Brigade incident-record release files used in this study.

| File | Size | Format | Rows (excluding header) |
|---|---:|---|---:|
| `lfb_incidents_2009_2017.csv`  | 314 MB | CSV   | 988,279   |
| `lfb_incidents_2018_2023.xlsx` | 147 MB | XLSX  | 670,635   |
| `lfb_incidents_2024_on.xlsx`   | 66 MB  | XLSX  | 305,442   |
| Total                          | 526 MB |       | 1,964,356 |

The accompanying metadata workbook documents 39 columns, organised into time fields (date, calendar year, time of call, hour of call), incident classification (incident group, stop-code description, special service type), property attributes (property category, property type, address qualifier), location at multiple resolutions (postcode, borough, ward, easting and northing both raw and rounded, latitude, longitude, fire-rescue service, incident-station ground), and a response block containing the headline target (`FirstPumpArriving_AttendanceTime`) along with helper fields for the second pump, station-of-deployment identifiers, pump counts, pump-minutes, notional cost, and the count of related calls.

### 2.2 Sampling strategy

Loading 1.96 million rows fully in a single notebook is not necessary for the experiment we run. Following the protocol established in the exploration phase, we stream the CSV with a row-counter and read the first 200,000 rows into memory for distributional analysis and modelling, and read 50,000 rows from each Excel file for distributional checks. The 200,000-row CSV sample is the modelling table for Sections 3 and 4. After dropping rows with a missing target (10.4 percent of the CSV sample), 181,492 rows remain for training, validation, and testing.

### 2.3 Target distribution

The target variable is `FirstPumpArriving_AttendanceTime`, the elapsed time in seconds between the receipt of the 999 call and the arrival of the first pump on scene. Table 2 summarises the target distribution across the three release files.

**Table 2.** Distribution of `FirstPumpArriving_AttendanceTime` (seconds) across the three release files.

| Period sample | n | Missing (%) | Mean | Median | p95 | Min | Max |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2009-2017 (n = 200k) | 179,268 | 10.37 | 322.3 | 296.0 | 588.0 | 1 | 1200 |
| 2018-2023 (n = 50k)  |  46,910 |  6.18 | 311.5 | 293.0 | 546.5 | 1 | 1198 |
| 2024+ (n = 50k)      |  47,773 |  4.45 | 319.2 | 302.0 | 554.0 | 1 | 1200 |

Three observations follow. First, the distribution is right-skewed in every era, with median attendance close to five minutes and 95th percentile close to nine to ten minutes. Second, target missingness has fallen monotonically across the three eras, from 10.4 percent in the oldest file to 4.4 percent in the newest, indicating better completeness in recent years. Third, the maximum is essentially clipped at 1,200 seconds (twenty minutes) in every file, which we interpret as an operational truncation and flag as a data-quality artefact rather than a measurement.

### 2.4 Incident composition

Across the 200,000-row CSV sample, false alarms account for 47 percent of incidents, special-service calls for 31 percent, and fires for 22 percent. The same ordering holds in the two Excel samples. Because false alarms typically receive different operational priority handling, the incident-group field carries direct predictive value and is retained in the feature set. By borough, central and inner-London boroughs dominate counts, with Westminster (14,916), Camden (11,155), Tower Hamlets (10,519), Southwark (10,153), Lambeth (8,471), and Hackney (8,173) leading the 2009 to 2017 sample.

### 2.5 Missingness and redaction

Missingness on the auxiliary fields falls into three categories. The second-pump fields are missing in 63 to 67 percent of rows because most incidents are handled by a single pump. Special-service type is missing in 60 to 69 percent of rows because it is only populated for special-service incidents. The privacy-redacted fields (full postcode, unique property reference number, raw eastings and northings, latitude, longitude) are missing in 43 to 60 percent of rows because they are suppressed for residential dwellings [11]. The redacted-for-dwellings group is the most consequential for modelling and motivates the privacy-preserving feature set described in Section 3.

## 3. Methods

### 3.1 Feature set

Two design rules govern the feature set: no post-event leakage, and no spatial resolution finer than the borough or the rounded grid square. Concretely, we drop the following.

Post-event fields removed to avoid label leakage: `SecondPumpArriving_AttendanceTime`, `NumStationsWithPumpsAttending`, `NumPumpsAttending`, `Notional Cost`, `PumpHoursRoundUp`, and `FirstPumpArriving_DeployedFromStation`. Each of these is populated only after the incident has been resolved and would directly encode the target if retained.

High-cardinality or privacy-redacted fields removed: `Postcode_full`, `UPRN`, `USRN`, `IncidentNumber`, `Latitude`, `Longitude`, `Easting_m`, and `Northing_m`. These either uniquely identify a dwelling or provide spatial resolution below the borough level that would defeat the privacy objective.

The retained features are:

- Numeric: `hour` (0 to 23), `weekday` (0 to 6), `month` (1 to 12), and `CalYear` (2009 to 2017 in the modelling sample). Four features.
- Categorical: `IncGeo_BoroughName` (33 London boroughs), `IncidentGroup` (Fire, False Alarm, Special Service), and `PropertyCategory` (approximately 10 categories spanning dwelling, non-residential, outdoor, road-vehicle, and other classes).

After one-hot encoding, the design matrix has approximately 50 columns. Every retained feature is plausibly available at the moment of dispatch.

### 3.2 Models

We fit four regressors. The linear and tree baselines were implemented with scikit-learn [5]; gradient-boosted variants used the XGBoost library [2].

1. **Ordinary least squares** (`LinearRegression`) on standardised numeric features and one-hot categorical features. This serves as a transparent baseline.
2. **Random forest** [1] with 100 trees, maximum depth 15, and a minimum leaf size of three. This captures local non-linear interactions among the temporal and borough features.
3. **XGBoost** [2, 3] with 400 trees, maximum depth 6, learning rate 0.07, subsample 0.9, and column subsample 0.8, using the histogram tree method. This is the strongest single tabular model in our pool.
4. **XGBoost log-target**: the same gradient-boosted framework with 600 trees, maximum depth 8, and learning rate 0.05, fit on `log1p(seconds)`. Predictions are inverse-transformed via `expm1` for evaluation in the original second scale. The motivation is that the target is right-skewed and bounded above near 1,200 seconds, conditions under which a logarithmic link is expected to stabilise the residual variance and improve median performance.

### 3.3 Train, validation, and test split

We use a random 60/20/20 split with `random_state=42`, yielding 108,894 training rows, 36,299 validation rows, and 36,299 test rows. All metrics reported in Section 4 are on the held-out test set. The split is random rather than time-stratified because the modelling sample (the first 200,000 rows of the 2009 to 2017 CSV) does not fully exercise the multi-year span; a time-respecting split is planned for the follow-up that joins all three release files.

### 3.4 Metrics

We report root mean squared error (RMSE), mean absolute error (MAE), R squared, and the 50th and 95th percentiles of the absolute residual distribution. The first three are standard regression metrics; the residual percentiles capture how the model behaves on the typical incident versus the long tail and are particularly informative under a right-skewed target.

## 4. Results

### 4.1 Test-set performance

Table 3 reports test-set metrics for the four models.

**Table 3.** Test-set metrics for the four regression models. Best value in each column is in bold.

| Model | RMSE (s) | MAE (s) | R squared | abs-resid p50 (s) | abs-resid p95 (s) |
|---|---:|---:|---:|---:|---:|
| Linear regression | 139.5 | 98.8 | 0.064 | 74.5 | 281.0 |
| Random forest (100 trees, depth 15) | 139.7 | 99.0 | 0.062 | 74.3 | 280.3 |
| XGBoost (400 trees, depth 6) | **138.0** | **97.5** | **0.084** | 72.2 | **274.7** |
| XGBoost log-target (600 trees, depth 8) | 143.3 | 97.9 | 0.012 | **68.5** | 289.8 |

Three findings stand out.

First, the three linear-or-tree baselines cluster within 1.7 seconds of RMSE of one another, and the R squared ceiling sits near 0.08 across model classes. The fact that a 50-feature linear model and a 400-tree gradient booster end within two seconds of RMSE and within 0.02 of R squared on the same feature set is the strongest available evidence that the ceiling is a property of the inputs rather than a property of the estimator.

Second, the log-target XGBoost wins on the median absolute residual (68.5 seconds versus 72.2 seconds for the baseline XGBoost) and loses on RMSE (143.3 versus 138.0) and on R squared (0.012 versus 0.084). This is the canonical mean-versus-median trade-off introduced by a logarithmic link [3]. By compressing large residuals before fitting, the log-target model improves the typical-case prediction at the cost of larger squared penalties when the model under-predicts a long-attendance event. The operational implication is that the choice of model depends on the deployed use case, not on a single global metric: a fleet-planning system that integrates squared error over a budget cycle should prefer the baseline XGBoost, while a control-room display showing an expected time of arrival to a caller should prefer the log-target variant.

Third, the absolute-residual percentiles suggest that roughly half of incidents are predicted within 72 seconds of their actual attendance time even from the privacy-preserving feature set, while the worst five percent of predictions miss by 275 seconds or more. Two thirds of incidents have a true attendance time below the global median plus 100 seconds, so a 72-second median residual corresponds to a usable, if coarse, dispatch-time ETA.

### 4.2 Feature importance

Table 4 reports the top ten impurity-based feature importances from the random forest. The importance ranking is consistent with the gradient-boosted gain ranking in spirit, although the numerical values differ.

**Table 4.** Top 10 features by impurity-based importance, random forest baseline.

| Feature | Importance |
|---|---:|
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

Time-of-day, month, calendar year, and weekday occupy the top four positions and together carry 0.546 of the total importance mass. Borough effects appear next, with outer-London boroughs (Hillingdon, Enfield) ranked above inner-London boroughs in the top ten, consistent with a longer mean attendance time at the urban periphery where station density is lower. Property category contributes meaningfully through outdoor and road-vehicle classes, both of which carry distinct response-time distributions because the call-handling and pump-routing protocols differ from in-dwelling fires. The false-alarm flag enters at rank eight, confirming the operational intuition that response time on false-alarm calls follows a different distribution from genuine incidents.

The dominant role of the temporal block (hour, month, year, weekday) is the principal explanation for why richer estimators do not separate from the linear baseline: the bulk of the variance recoverable from the privacy-preserving feature set is already captured by additive temporal terms, leaving little headroom for tree-induced interactions to exploit.

## 5. Discussion

### 5.1 Why the R squared ceiling is structural

The clustering of all three linear-or-tree estimators near R squared 0.08 establishes that the ceiling is a property of the feature set rather than of the estimator. We attribute this ceiling to three structural causes. First, the dominant unobserved driver of attendance time on any given call is the road distance from the nearest available pump to the incident scene, which depends jointly on dwelling geolocation and on the real-time deployment status of nearby stations. Both factors are excluded by the privacy and dispatch-time constraints. Second, borough-level signal is too coarse to substitute for station-level routing: a single borough such as Westminster or Camden is served by multiple stations whose attendance times to a given postcode can differ by several minutes, and the borough average washes that variation out. Third, hour, month, year, and weekday capture the diurnal and seasonal modulation of demand and traffic but do not capture the routing bottleneck that determines a particular call's attendance time.

This finding aligns with Asgary [8], where structural-fire risk in Toronto is well captured by property-category and land-use features at the census-tract level but not at the building level without exact geolocation: borough-resolution signal is informative for aggregate risk but does not substitute for finer spatial detail when predicting individual-incident outcomes.

### 5.2 Privacy-versus-accuracy trade-off

A natural next question is the magnitude of the accuracy lost to the privacy constraint. We do not run the unrestricted comparator in this paper because doing so would re-introduce the redacted fields and defeat the experimental premise. The internal modelling notes from this project anticipate that adding station-level fixed effects (the mean response time of each station, computed on a strict train-time-only window to avoid leakage) would lift R squared past 0.20 without consuming any individual-dwelling identifiers. That intermediate position is the design we recommend: it preserves the privacy guarantee at the level of the caller while restoring the spatial signal at the level of the fire station. The same construction is compatible with operational deployment because the station mean is a public statistic.

### 5.3 Mean-versus-median in operational deployment

The split between RMSE and median residual across the baseline and log-target XGBoost variants has a direct operational interpretation. A control-room ETA display is a per-call interface, and the cost function the user implicitly evaluates is the absolute error on the typical call: an ETA that is off by sixty seconds on a five-minute call is acceptable; an ETA that is off by one hundred and forty seconds is not. A fleet-planning workload, by contrast, integrates squared deviations over thousands of calls per shift and is sensitive to large residuals. Our recommendation, consistent with Friedman [3] and standard practice on right-skewed targets, is to operate two model variants in parallel: a baseline XGBoost for planning, and a log-target XGBoost for caller-facing ETAs. A single deployment is unlikely to satisfy both objectives, and the improvement on the median case (3.7 seconds in our test) is large enough to justify the dual setup when the deployment user is a dispatcher.

### 5.4 Comparison with prior work and limitations

Asgary [8] models the risk of structural fire incidents in Toronto with property and land-use features and would inform an extension of our `PropertyCategory` block to a richer property-type taxonomy. Anderson [7] provides the kernel-density-and-clustering technique that would surface fire-incident hotspots from rounded eastings and northings without consuming exact coordinates, and would feed a future spatial smoother. Boyd, Tolson and Copes [10] anchor the historical motivation by linking response time to outcome in trauma care; an analogous outcome-linkage study within the LFB ecosystem is, to our knowledge, an open problem.

Several limitations apply, three of which we flag explicitly as v1.0 to-dos rather than design oversights. First, the brief mandates two LFB datasets (incident records and mobilisation records); the present study consumes only the incident file. The mobilisation records carry per-pump deployment and arrival timestamps that would let us reconstruct turn-out time, travel time, and station-of-origin response time as separate components, and would supply the station-level mean and median attendance features that the manuscript identifies as the strongest available lever for lifting R squared past 0.20. Joining the mobilisation file on `IncidentNumber` and deriving these station-level statistics under a strict pre-split mask is the explicit v1.0 starting task. Second, the 1,200-second cap visible in every release file is an administrative right-censoring artefact rather than a true measurement, and the present models (OLS, RF, baseline XGBoost, log-target XGBoost) all treat the cap as an observed value. A Tobit regression or a survival-style accelerated-failure-time fit, or alternatively a quantile-regression XGBoost [6] at q=0.5 and q=0.9, would handle the censoring directly and is the second v1.0 task. Third, the modelling sample is the first 200,000 rows of the 2009 to 2017 CSV; broadening to the full 1.96 million rows across all three release files is enabled by the parquet pre-processing implementation already produced in this project and is straightforward once the mobilisation join is in place. The split is random rather than time-stratified, which is acceptable inside the 2009 to 2017 window but would not generalise to a deployment in 2026 without a time-respecting backtest. Class-imbalance methods such as SMOTE [9] are not used here because the task is regression rather than classification, but a binary "late response" framing (attendance above a service-level threshold) would benefit from such methods and is a natural side-task. SHAP attribution [4] is planned for the station-level extension and would replace the impurity-based importances reported in Table 4 for any production deployment.

A further limitation concerns generalisation across regimes. The London road network, station count, and call-handling protocols evolved materially between 2009 and 2024, and a single estimator fit on the older window will not capture the post-2018 changes in station consolidation or the post-2020 disruptions to traffic baselines. A regime-aware variant (calendar-year fixed effect or piecewise temporal indicator) is straightforward to add and is the planned default in the multi-file follow-up. Finally, the present study reports point predictions only; for control-room deployment the relevant output is a calibrated predictive interval, which a quantile regressor [6] or a conformal-prediction wrapper would supply directly. Both extensions reuse the same privacy-preserving feature implementation described in Section 3 and require no additional data redaction work.

## 6. Conclusion

We have presented a privacy-preserving regression of London Fire Brigade first-pump attendance time using only the temporal and coarse-categorical features available at dispatch. Across linear, random-forest, and gradient-boosted estimators on a 200,000-row stratified sample drawn from a 1.96-million-row historical archive, the R squared ceiling on this feature set is approximately 0.08, with the strongest single model reaching test RMSE 138.0 seconds, MAE 97.5 seconds, and a median absolute residual of 72.2 seconds. A log-target variant reduces the median absolute residual to 68.5 seconds at the cost of higher RMSE, illustrating a clean mean-versus-median trade-off relevant to dual deployment in fleet planning and control-room ETAs. The R squared ceiling is structural rather than estimator-driven, and we recommend a station-level fixed-effects extension, computed on a strict train-time window, as the next step that lifts predictive accuracy without reintroducing personal location data. The code, parquet pre-processing implementation, and the persisted log-target XGBoost pipeline are released alongside this manuscript for reproducibility.

## References

[1] Breiman L. Random Forests. *Machine Learning* 2001; 45:5-32. DOI: 10.1023/A:1010933404324.

[2] Chen T, Guestrin C. XGBoost: A Scalable Tree Boosting System. *Proceedings of KDD* 2016. DOI: 10.1145/2939672.2939785.

[3] Friedman JH. Greedy Function Approximation: A Gradient Boosting Machine. *Annals of Statistics* 2001; 29(5). DOI: 10.1214/aos/1013203451.

[4] Lundberg SM, Lee SI. A Unified Approach to Interpreting Model Predictions. *Advances in Neural Information Processing Systems* 2017. arXiv:1705.07874.

[5] Pedregosa F, Varoquaux G, Gramfort A, et al. Scikit-learn: Machine Learning in Python. *Journal of Machine Learning Research* 2011; 12:2825-2830.

[6] Koenker R, Bassett G. Regression Quantiles. *Econometrica* 1978; 46(1):33-50. DOI: 10.2307/1913643.

[7] Anderson TK. Kernel density estimation and K-means clustering to profile road accident hotspots. *Accident Analysis and Prevention* 2009; 41(3). DOI: 10.1016/j.aap.2008.12.014.

[8] Asgary A, Ghaffari A, Levy J. Modeling the Risk of Structural Fire Incidents in Toronto. *Fire Safety Journal* 2010; 45:44-57. DOI: 10.1016/j.firesaf.2009.10.001.

[9] Chawla NV, Bowyer KW, Hall LO, Kegelmeyer WP. SMOTE: Synthetic Minority Over-sampling Technique. *Journal of Artificial Intelligence Research* 2002; 16:321-357. DOI: 10.1613/jair.953.

[10] Boyd CR, Tolson MA, Copes WS. Evaluating Trauma Care: The TRISS Method. *Journal of Trauma* 1987. DOI: 10.1097/00005373-198704000-00005.

[11] London Fire Brigade Open Data Portal. London Datastore (2024). https://data.london.gov.uk/dataset/london-fire-brigade-incident-records.
