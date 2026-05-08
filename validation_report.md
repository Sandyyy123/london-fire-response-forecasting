# Validation Report - Project #04 London Fire Brigade Response Time

## Compact Summary

**Overall: PASS-WITH-WARNINGS**

The project is technically sound and largely well-formed: both notebooks parse as valid JSON, the manuscript hits 4,099 words (inside the 4,000-5,000 target), full IMRaD structure is present, the presentation HTML is fully self-contained (zero external resources), no AI-tell phrases anywhere, and the saved XGBoost model plus metrics are in `deliverables/`. All 12 inline citations [1]-[12] map cleanly to `manuscripts/references.md`, and four of five randomly sampled DOIs resolve to the correct titles via CrossRef. Warnings: no `brief.md` (only `brief.pdf`), no `checkpoint.json`, no `data/README.md`, no `src/model_baseline.py` or `src/model_advanced.py` (the model code lives in `notebooks/03_modeling.ipynb`), reference [8] DOI `10.1007/s10694-018-0780-5` resolves to an unrelated barrier-failure paper rather than the cited Yang/Hu/Zhang London fire-service paper, and 6 em-dash characters remain (5 in `notebooks/01_eda.ipynb`, 1 in `src/eda_inspect.py`).

---

## Findings

### Task 1 - Notebook validity
- [PASS] `notebooks/01_eda.ipynb` parses as valid JSON.
- [PASS] `notebooks/03_modeling.ipynb` parses as valid JSON.

### Task 2 - Python script syntax
- [WARN] No `src/model_baseline.py` or `src/model_advanced.py` in this project. Model code is in `notebooks/03_modeling.ipynb` (executed earlier; this is a #1-#8 project where notebooks carry the modelling).
- [PASS] `src/count_csv.py` parses cleanly with `ast.parse`.
- [PASS] `src/eda_inspect.py` parses cleanly with `ast.parse`.

### Task 3 - Manuscript word count
- [PASS] `manuscripts/manuscript.md` = **4,099 words** (target 4,000-5,000).

### Task 4 - Self-contained HTML
- [PASS] `deliverables/presentation.html` has **0** `href="http` or `src="http` external resources.

### Task 5 - IMRaD completeness
- [PASS] All required sections present: Title (line 1), Abstract (line 3), Introduction (line 7), Data (line 19), Methods (line 64), Results (line 98), Discussion (line 144), Conclusion (line 168), References (line 172). Note: project uses an explicit "Data" section in addition to the standard IMRaD blocks; this strengthens, not weakens, completeness.

### Task 6 - Method drift
Methods named in manuscript Section 3.2: Ordinary Least Squares (`LinearRegression`), Random Forest, XGBoost, XGBoost log-target.
- [PASS] All four appear in `notebooks/03_modeling.ipynb` (the executed model script): `LinearRegression`, `RandomForestRegressor`, `XGBRegressor`, and a `log1p`/`expm1` log-target variant. No drift detected.
- [WARN] Manuscript states "standardised numeric features" for the OLS baseline but `StandardScaler` is not invoked in the notebook. Minor methodological-prose vs code mismatch.

### Task 7 - Citation drift
Numeric citations found in manuscript: [1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [11], [12].
- [PASS] All 12 inline citations map to a numbered entry in `manuscripts/references.md` (entries 1-12 present).

### Task 8 - DOI re-verification (5 random)
- [PASS] [1] `10.1023/A:1010933404324` -> HTTP 200, title "Random Forests" (match).
- [PASS] [2] `10.1145/2939672.2939785` -> HTTP 200, title "XGBoost" (match).
- [PASS] [3] `10.1214/aos/1013203451` -> HTTP 200, title "Greedy function approximation: A gradient boosting machine" (match).
- [PASS] [7] `10.1016/j.aap.2008.12.014` -> HTTP 200, title "Kernel density estimation and K-means clustering to profile road accident hotspots" (match).
- [FAIL] [8] `10.1007/s10694-018-0780-5` -> HTTP 200 but resolves to "A Monte Carlo-Based Probabilistic Barrier Failure Model for Arbitrary Fire Environment" (Fire Technology). The cited title in `references.md` and the manuscript is "A Spatio-Temporal Forecasting Framework for London Fire Service Demand" (Yang, Hu and Zhang 2018). DOI / title mismatch - the DOI on file points at a different paper. Either the DOI is wrong or the citation prose is wrong. Needs correction before client delivery.

### Task 9 - Em-dash scan
- [WARN] 6 em-dash characters total across project files:
  - `notebooks/01_eda.ipynb`: 5
  - `src/eda_inspect.py`: 1
  - All other files: 0
  - `manuscripts/manuscript.md`, `deliverables/presentation.html`, `notebooks/03_modeling.ipynb`, `reports/*.md`, `src/count_csv.py`: 0 each.

### Task 10 - AI-tell scan
- [PASS] Zero hits for "verified by N agents", "AI-verified", or "cross-checked by Claude" anywhere in the project tree.

### Task 11 - Checkpoint schema
- [WARN] `checkpoint.json` does not exist in the project root. Cannot verify required fields (project_number, title, methodology, status). This is a #1-#8 executed project so the absence is logged as a WARN per QA rules, not a FAIL.

### Additional artefact check (#1-#8 projects)
- [PASS] `deliverables/lfb_xgb.pkl` (saved XGBoost model) present.
- [PASS] `deliverables/metrics.json` present.
- [PASS] `deliverables/presentation.html` present.
- [PASS] `reports/borough_top15.png`, `reports/incident_group.png`, `reports/target_distribution.png` present.

### Other gaps observed
- [WARN] `brief.md` not present (only `brief.pdf`).
- [WARN] `data/README.md` not present.
- [WARN] `manuscripts/references.bib` exists alongside `references.md`; not part of the QA spec but worth noting for downstream LaTeX/bib consistency.

---

## Action items (for IMPROVER and the project owner)

1. **Fix reference [8]**: the DOI `10.1007/s10694-018-0780-5` does not resolve to Yang, Hu and Zhang's London fire-service forecasting paper. Locate the correct DOI for "A Spatio-Temporal Forecasting Framework for London Fire Service Demand" or remove the citation from Discussion 5.4.
2. **Strip em-dashes**: 5 in `01_eda.ipynb` and 1 in `eda_inspect.py`.
3. **Add `checkpoint.json`** at project root with at least `project_number`, `title`, `methodology`, `status` keys.
4. **Add `brief.md`** (a markdown extraction of the PDF) and `data/README.md`.
5. **Reconcile OLS standardisation**: either add `StandardScaler` to the OLS pipeline or drop the "standardised numeric features" claim from Section 3.2.

---

Role A (VALIDATOR) complete.
