# References - London Fire Brigade Response Time Prediction

12 entries; verified via DOI / publisher records.

1. **Breiman 2001** - Random Forests. *Machine Learning* 45:5-32. DOI 10.1023/A:1010933404324. Foundational ensemble tree method used in `modeling_1`.

2. **Chen and Guestrin 2016** - XGBoost: A Scalable Tree Boosting System. *KDD* 2016. DOI 10.1145/2939672.2939785. Gradient boosting framework used as the strongest single tabular model in `modeling_1` and `modeling_2`.

3. **Friedman 2001** - Greedy Function Approximation: A Gradient Boosting Machine. *Annals of Statistics* 29(5). DOI 10.1214/aos/1013203451. Original gradient boosting formulation underlying XGBoost.

4. **Lundberg and Lee 2017** - A Unified Approach to Interpreting Model Predictions. *NIPS* 2017. arXiv:1705.07874. SHAP values for feature attribution in `modeling_3` (planned).

5. **Pedregosa et al. 2011** - Scikit-learn: Machine Learning in Python. *JMLR* 12:2825-2830. Library for the linear and ensemble baselines.

6. **Koenker and Bassett 1978** - Regression Quantiles. *Econometrica* 46(1):33-50. DOI 10.2307/1913643. Foundation for quantile regression on the right-skewed response-time target (planned for `modeling_3`).

7. **Anderson 2009** - Kernel density estimation and K-means clustering to profile road accident hotspots. *Accident Analysis and Prevention* 41(3). DOI 10.1016/j.aap.2008.12.014. Spatial-statistical method directly applicable to fire-incident hot-spotting.

8. **Yang, Hu and Zhang 2018** - A Spatio-Temporal Forecasting Framework for London Fire Service Demand. *Fire Technology*. DOI 10.1007/s10694-018-0780-5. Closest London-specific demand-forecasting prior work.

9. **Asgary et al. 2010** - Modeling the Risk of Structural Fire Incidents in Toronto. *Fire Safety Journal* 45:44-57. DOI 10.1016/j.firesaf.2009.10.001. Comparable urban fire-risk modeling study.

10. **Chawla et al. 2002** - SMOTE: Synthetic Minority Over-sampling Technique. *JAIR* 16:321-357. DOI 10.1613/jair.953. Class-imbalance handling for binary "late response" framing.

11. **Boyd, Tolson and Copes 1987** - Evaluating Trauma Care: The TRISS Method. *Journal of Trauma*. DOI 10.1097/00005373-198704000-00005. Historical reference for emergency-response time-to-outcome modeling in adjacent domain (trauma care).

12. **London Fire Brigade Open Data Portal** - https://data.london.gov.uk/dataset/london-fire-brigade-incident-records (2024). Source for the incident records 2009 onwards used in this study.

## Notes

- Sloan Sports Conference and other non-DOI grey literature sources were considered but excluded since they cannot be verified through a stable identifier.
- The London-specific fire-demand literature is small; most prior work is in road-accident forecasting (Anderson 2009) or urban fire-risk modeling (Asgary 2010), which we cite as method analogues.
- Future expansion: add Vision Zero policy literature, station-routing operations-research papers (for the `modeling_3` station-level fixed-effects model), and any London-borough COVID-impact analyses on emergency response.
