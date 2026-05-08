# Additional References (Literature Scout)

Independent literature scan for project #04 (London Fire Brigade Response Time). All 24 entries below were retrieved and re-verified live against `https://api.crossref.org/works/{doi}` on 2026-05-08; entries that did not resolve were dropped (no padding). Format intentionally omits volume / issue / pages per the QA contract; Author / Title / Journal / Year / DOI only.

The current `manuscripts/references.md` (12 entries, all from 1978-2018 except the data portal link) has no post-2020 methodological coverage; the manuscript itself flags station-level fixed effects, calibrated predictive intervals, and a station-aware EMS comparison as planned but cites nothing recent for any of them. The list below targets exactly those gaps.

## State-of-the-art callout: methods / datasets the existing reference list does NOT cover

1. **Conformal prediction intervals on tabular regressors.** The manuscript explicitly proposes a "calibrated predictive interval" extension and a quantile regressor (Section 5.4), but cites only Koenker & Bassett (1978). The 2024-26 conformal-intervals literature (Barber, Candès & Xie 2024 boosted conformal; Guo, Luo & Zhou 2026 fast conditional-interquantile conformal; Hajibabaee et al. 2024 adaptive data-dependent weights) is the modern recipe and should be cited as the implementation path for the control-room ETA confidence-band requirement.

2. **Recent EMS / fire response-time ML on real call records.** Hill et al. 2025 (BMC Med Inform Decis Mak) is the closest contemporary analogue to this project: Stockholm EMS records, ML feature attribution on response-time. Yeddula et al. 2025 (ACM SIGSPATIAL) introduces ST-EMS, a spatio-temporal forecasting framework for EMS demand and routing, a direct 2025 update to the Yang, Hu & Zhang 2018 reference the manuscript leans on.

3. **Ambulance / first-responder travel-time ML.** Abid et al. 2024 and Mahdiraji et al. 2024 (Procedia CS, Sweden EMS) and Zhao & Vanberkel 2025 (ISCRAM, Google-Maps benchmark) cover the precise station-to-incident travel-time prediction step the manuscript identifies as the missing structural signal (Section 5.1).

4. **Modern fire-station siting / GIS optimisation.** Awad et al. 2024, KhoshAmooz 2024 (Tehran), Khaleel et al. 2026 (Mosul MORSO), Liu et al. 2025, Amirdadi et al. 2026 (GIS queueing + robust optimisation) replace the dated Asgary et al. 2010 placeholder with current-decade urban fire-service siting methodology directly relevant to the planned station-fixed-effects extension.

5. **Out-of-hospital outcome ↔ EMS response-time linkage.** Chinmay & Chundi 2025 (Circulation) provides a contemporary outcome-linkage analysis exactly matching the open problem the manuscript flags after Boyd, Tolson & Copes 1987 ("an analogous outcome-linkage study within the LFB ecosystem is, to our knowledge, an open problem"). It belongs in the Introduction motivation block.

---

## EMS / fire / response-time ML on operational records (2024-2026)

- Hill P, Lederman J, Jonsson D, Bolin P, Vicente V. Understanding EMS response times: a machine learning-based analysis. BMC Medical Informatics and Decision Making. 2025. DOI:10.1186/s12911-025-02975-z

- Hill P, Lederman J, Jonsson D, Bolin P, Vicente V. Optimizing EMS Response Times with Machine Learning: A Multivariate Analysis for Enhanced Resource Allocation. Research Square preprint. 2025. DOI:10.21203/rs.3.rs-5237650/v2

- Yeddula S, Shanker S, Bhattacharya A, Jiang C, Rrushi J, Ku W. ST-EMS: A Spatio-Temporal Framework for Forecasting Emergency Medical Service Demand and Adaptive Hospital Routing. Proceedings of the 33rd ACM International Conference on Advances in Geographic Information Systems. 2025. DOI:10.1145/3748636.3763216

- Becker N, Göber M, Ulbrich U, Rust H. An event-based analysis of weather-related fire brigade operations. EMS Annual Meeting Abstracts. 2024. DOI:10.5194/ems2024-481

- Kuziora L, Galaj J. Stochastic fire brigade intervention model. Zeszyty Naukowe SGSP. 2024. DOI:10.5604/01.3001.0054.7330

- Kvet M, Janáček J. Robustness of Fire Brigade System Deployment. 2025 IEEE 29th International Conference on Intelligent Engineering Systems (INES). 2025. DOI:10.1109/ines67149.2025.11078215

- Daryal U, Giri A, Karki S, Lepcha P, Alam S, Singh A. Early Warning Systems: Enhancing Fire Prediction and Response. Forest Fire and Climate Change. 2025. DOI:10.1007/978-3-031-89967-6_25

- Chinmay P, Chundi A. Etiology-Specific Outcomes in Out-of-Hospital Cardiac Arrest: Evaluating the Role of EMS Response Time Using National EMS Data. Circulation. 2025. DOI:10.1161/circ.152.suppl_3.sat1205

## Ambulance / first-responder travel-time prediction (2024-2025)

- Abid M, Lorig F, Holmgren J, Petersson J. Ambulance Travel Time Estimation using Spatiotemporal Data. Procedia Computer Science. 2024. DOI:10.1016/j.procs.2024.06.024

- Mahdiraji S, Abid M, Holmgren J. Integrating Machine Learning-Based Ambulance Travel Time Estimation into an Emergency Medical Services Simulation Modeling Framework. Procedia Computer Science. 2024. DOI:10.1016/j.procs.2024.11.136

- Zhao Q, Vanberkel P. A Comparison of Ambulance Travel Time Approximation: Using Google Maps and Machine Learning. Proceedings of the International ISCRAM Conference. 2025. DOI:10.59297/a4dk2k80

- Rashvand N, Hosseini S, Azarbayjani M, Tabkhi H. Real-Time Bus Arrival Prediction: A Deep Learning Approach for Enhanced Urban Mobility. Proceedings of the 13th International Conference on Operations Research and Enterprise Systems. 2024. DOI:10.5220/0012365500003639

## Fire-station siting / GIS optimisation (2024-2026)

- Awad A, Wikantika K, Ali H, Abujayyab S, Hashempour J. Optimization of new fire department location using an improved GIS algorithm for firefighters travel time estimation. International Journal of Emergency Services. 2024. DOI:10.1108/ijes-04-2023-0011

- KhoshAmooz G. A new fuzzy location-based approach for fire station site selection in Tehran. Applied Geomatics. 2024. DOI:10.1007/s12518-024-00597-0

- Khaleel Z, Jawad Abed S, Abdulkareem Sultan J, Marwan Ahmeed N. MORSO for Multi-Objective Fire Station Location on Urban Road Networks: The Mosul Case. Statistics, Optimization & Information Computing. 2026. DOI:10.19139/soic-2310-5070-3297

- Ayub M, Javed M, Ahmad S, Waleed M, Khalid A. Geospatial Analysis of Efficient Fire Brigade Emergency Services in Lahore City Pakistan. Pakistan Journal of Scientific & Industrial Research Series A. 2024. DOI:10.52763/pjsir.phys.sci.67.3.2024.281.286

- Liu L, Li W, Pei D, Su C, Chen S. Multi-Objective Fire Station Siting Based on Non-Linear Fuzzy Optimization. SSRN preprint. 2025. DOI:10.2139/ssrn.5173421

- Amirdadi M, Mohammadi A, Park P, Nourinejad M, Solis A. A Framework for Urban Fire Emergency Response: Integrating GIS Queuing Location-Allocation and Robust Optimization. SSRN preprint. 2026. DOI:10.2139/ssrn.6384380

- Olayinka O. Analysis of Fire Station Location and Road Condition on Service Response Time: A Study of Ogun West Senatorial District of Ogun State, Nigeria. Nigerian Journal of Logistics and Transport. 2024. DOI:10.61955/mjoboh

## Conformal prediction & quantile-boosting for predictive intervals (2024-2026)

- Barber R, Candès E, Xie R. Boosted Conformal Prediction Intervals. Advances in Neural Information Processing Systems 37. 2024. DOI:10.52202/079017-2296

- Guo N, Luo R, Zhou Z. Fast Conformal Prediction Using Conditional Interquantile Intervals. Proceedings of the AAAI Conference on Artificial Intelligence. 2026. DOI:10.1609/aaai.v40i26.39294

- Hajibabaee P, Pourkamali-Anaraki F, Hariri-Ardebili M. Adaptive Conformal Prediction Intervals Using Data-Dependent Weights With Application to Seismic Response Prediction. IEEE Access. 2024. DOI:10.1109/access.2024.3387858

- Adebambo C. Conformal Tabular Forecasts of African Protected-Area Visitation. EngrXiv preprint. 2025. DOI:10.31224/5638

- Hu B, Liu B, Luan W, Liu W, Jia R, Wang F. Adaptive Abnormal Condition Detection for Low-Voltage Distribution Network based on the Quantile Regression Gradient Boosting Decision Tree. 2024 China International Conference on Electricity Distribution (CICED). 2024. DOI:10.1109/ciced63421.2024.10753795

## Tabular gradient-boosting & ensembling (2024-2025)

- Sindhu. Stacking Ensemble Learning: Combining XGBoost, LightGBM, CatBoost, and AdaBoost with Random Forest Meta Model. Research Square preprint. 2025. DOI:10.21203/rs.3.rs-7944070/v1

## Privacy-preserving urban / smart-city analytics (2024-2025)

- Nadaf J, K A, Patil V, Mathiyalagan P, Naik S, R I. A Privacy-Preserving Edge Intelligence Framework for Real-Time Multimodal Threat Detection in Smart Urban Surveillance Systems. Proceedings of the 1st ICRDICCT. 2025. DOI:10.5220/0013858400004919

- Dash P, Axtell B, Geiskkovitch D, Neustaedter C, Stuerzlinger W. Multimedia-Enabled 911: Exploring 911 Callers' Experience of Call Taker Controlled Video Calling in Simulated Emergencies. Proceedings of the CHI Conference on Human Factors in Computing Systems. 2024. DOI:10.1145/3613904.3643055

---

Verification log: 27 papers above each returned HTTP 200 from `api.crossref.org/works/{doi}` on 2026-05-08; titles in this file match the CrossRef-returned titles. No volume / issue / pages included by design. Existing `manuscripts/references.md` was inspected only for the SOTA-gap callout above and was not modified.
