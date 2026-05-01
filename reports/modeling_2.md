# Modeling 2 - Log-Target XGBoost (LFB Response Time)

## What changed

Same features and split as `modeling_1.md`. Two changes:

1. Larger XGBoost: `n_estimators=600`, `max_depth=8`, `learning_rate=0.05`.
2. Target transformed with `log1p(seconds)` before fitting; predictions are inverse-transformed via `expm1` for evaluation in original (second) scale.

The motivation is that response-time distributions are right-skewed (median 297 s, p95 588 s, max truncated 1,200 s), so a log transform should pull large-residual incidents closer to a normal residual distribution and improve median absolute error.

## Test results

| Model | RMSE (s) | MAE (s) | R² | abs-resid p50 | abs-resid p95 |
|---|---|---|---|---|---|
| Linear Regression (modeling_1) | 139.5 | 98.8 | 0.064 | 74.5 | 281.0 |
| Random Forest (modeling_1) | 139.7 | 99.0 | 0.062 | 74.3 | 280.3 |
| XGBoost baseline (modeling_1) | 138.0 | 97.5 | 0.084 | 72.2 | 274.7 |
| **XGBoost log-target (this run)** | 143.3 | 97.9 | 0.012 | **68.5** | 289.8 |

The log-target model **wins on the median absolute residual** (68.5 s vs 72.2 s for the baseline XGBoost) but loses on RMSE (143.3 s vs 138.0 s) and R² (0.012 vs 0.084). This is the canonical median-vs-mean trade-off: `log1p` flattens large-residual incidents at the cost of a heavier RMSE penalty when the model under-predicts a long-attendance event.

## Operational interpretation

Two competing operational targets exist:

1. **Mean accuracy / fleet planning**: use the `modeling_1` XGBoost baseline (RMSE 138 s).
2. **Typical-call dispatch ETA shown to caller / control-room**: use the log-target variant (median residual 68.5 s) because callers care about the typical case, not the squared-error.

## Why ceiling is low

Both models plateau around 0.06-0.08 R² because:

- Spatial routing (distance from nearest available station) is excluded by design.
- Borough-level signal is weak compared to station-level routing.
- Time-of-day and month explain only the diurnal / seasonal demand modulation, not the routing bottleneck.

A `modeling_3` step would add station-level fixed effects (mean response per station) computed on a strict train-time-only window to avoid leakage. That should push R² past 0.20.

## Persisted artifacts

- `deliverables/lfb_xgb.pkl` - log-target XGBoost pipeline (600 trees, depth 8)
- `deliverables/metrics.json` - per-split metrics for all four models, top-15 RF features
