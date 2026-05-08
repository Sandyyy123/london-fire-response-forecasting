# Changes - Project #04 London Fire Brigade Response Time

Date: 2026-05-08
Scope: documentation, citations, em-dash cleanup. No new modelling code.

## 1. Reference [8] removed (CrossRef DOI mismatch)

The previous reference [8] (Yang, Hu and Zhang 2018, "A Spatio-Temporal Forecasting Framework for London Fire Service Demand", DOI 10.1007/s10694-018-0780-5) could not be verified.

- The DOI on file resolves to a different paper: Li, Zhang and Hadjisophocleous (2018), "A Monte Carlo-Based Probabilistic Barrier Failure Model for Arbitrary Fire Environment", *Fire Technology*.
- CrossRef searches on the cited title, the cited author triplet (Yang/Hu/Zhang + London + fire), and on combinations of "spatio-temporal forecasting / London fire / fire-service demand" did not return any matching paper.
- Per the validator action item and the project no-fabrication rule, the citation has been REMOVED rather than re-attached to a guessed DOI.

Inline edits made in `manuscripts/manuscript.md`:
- Section 1 Introduction: dropped the Yang/Hu/Zhang sentence in the "Predictive modelling of urban fire-service activity..." paragraph; the surrounding paragraph still cites Asgary [8] (renumbered) and Anderson [7].
- Section 1 Introduction (contributions list): replaced "...closest London-specific prior work [8] and broader urban fire-risk modelling [9]" with "...broader urban fire-risk modelling [8]".
- Section 5.1: replaced the "mirrors the conclusion in Yang, Hu and Zhang [8]" sentence with a re-worded statement keyed to Asgary [8] only.
- Section 5.4: dropped the opening sentence "The closest prior work is Yang, Hu and Zhang [8]..." and the "two systems would compose naturally" sentence; the comparison-with-prior-work paragraph now starts with Asgary [8].

## 2. Citation renumbering

After removing [8], references [9] through [12] were renumbered to [8] through [11] across the manuscript prose, the manuscript References section, and `manuscripts/references.md`:

- [9] Asgary 2010 -> [8]
- [10] Chawla 2002 (SMOTE) -> [9]
- [11] Boyd 1987 (TRISS) -> [10]
- [12] LFB Open Data Portal -> [11]

All inline citations in `manuscript.md` were updated accordingly: [10] (intro property-loss link) -> [10] is Boyd; [11] (privacy redaction) -> [11] is the LFB portal; the SMOTE inline reference in section 5.4 is now [9]. After renumbering the unique inline citation set in the manuscript is {[1]...[11]}, with no gap and no orphan.

`manuscripts/references.bib` had its `@article{Yang2018, ...}` entry deleted to keep the bib file consistent with `references.md`.

A short note has been added at the top of `references.md` documenting why entry 8 was dropped, so a downstream reader is not surprised by the renumbering.

## 3. Em-dash cleanup (6 characters removed)

Per the validation report, the em-dash character is banned in deliverables. All 6 occurrences were replaced with a regular hyphen, parentheses, or a colon as the prose required.

`notebooks/01_eda.ipynb` (5 occurrences):
- Cell 779cee00 (title): "London Fire Brigade - Exploratory Data Analysis (Sampled)"
- Cell a7b4a2cd (section 3): "200k from CSV, 50k from each xlsx (enough for distribution shape and missingness)."
- Cell fc26e602 (chart title): "IncidentGroup - 2009-2017 sample (n=200k)"
- Cell 1a868bc0 (chart title): "Top 15 boroughs by incidents - 2009-2017 sample"
- Cell 3d989766 (summary): "pre-processing report (drop redacted/leakage columns, encode borough/incident group, derive datetime features, set up train/test split with year-stratified sampling for modeling)."

`src/eda_inspect.py` (1 occurrence):
- Module docstring: `"""Quick inspection: row counts, schema, target stats (sampled)."""`

Verification: a grep for the em-dash character (Unicode U+2014) over `notebooks/01_eda.ipynb`, `notebooks/03_modeling.ipynb`, `src/eda_inspect.py`, `src/count_csv.py`, `manuscripts/manuscript.md`, `manuscripts/references.md`, and `deliverables/presentation.html` returns 0 across every file.

## 4. Limitations section strengthened (mobilisation file + right-censoring)

`manuscripts/manuscript.md` Section 5.4 (Comparison with prior work and limitations) was rewritten so that the two highest-priority gaps flagged by the IMPROVER report are acknowledged explicitly as Phase 2 to-dos:

1. Mobilisation dataset entirely unused. The brief mandates two LFB datasets; the present study consumes only the incident file. The new text names the join key (`IncidentNumber`), the planned features (turn-out time, travel time, station-level mean/median attendance under a strict pre-split mask), and identifies this as the first Phase 2 task and the largest expected accuracy lever.
2. Right-censoring at 1,200 seconds. The cap visible in every release file is an administrative truncation rather than a measurement. The new text states that all four current models treat the cap as observed, and identifies a Tobit / accelerated-failure-time fit, or a quantile-regression XGBoost at q=0.5 and q=0.9, as the second Phase 2 task.
3. The modelling-sample-size and time-respecting-split caveats are kept and demoted to follow-up rather than primary limitations, because they unblock once the mobilisation join lands.

No new code, no new model fits, no new numbers in the manuscript prose. The only changes are documentation, citation hygiene, and em-dash removal, as scoped in the task brief.

## Files changed

- `manuscripts/manuscript.md`
- `manuscripts/references.md`
- `manuscripts/references.bib`
- `notebooks/01_eda.ipynb`
- `src/eda_inspect.py`
- `CHANGES.md` (new, this file)
