# London Fire Brigade Response Time - Exploration Report 1

## 1. Project context

The London Fire Brigade (LFB) is the busiest fire and rescue service in the UK and one of the largest in the world. The objective of this Portfolio project is to analyse and estimate response and mobilisation times. The headline target variable is `FirstPumpArriving_AttendanceTime`, the time in seconds between the 999 call and the arrival of the first pump on scene.

## 2. Data sources

Open data published on data.london.gov.uk:

- Incident records: https://data.london.gov.uk/dataset/london-fire-brigade-incident-records
- Mobilisation records: https://data.london.gov.uk/dataset/london-fire-brigade-mobilisation-records

Only the incident records are loaded for this first exploration. The mobilisation file will be joined in the modelling phase.

## 3. Files supplied

| File | Size | Format | Total rows (excl. header) |
|---|---|---|---|
| `lfb_incidents_2009_2017.csv`  | 314 MB | CSV   | 988,279 |
| `lfb_incidents_2018_2023.xlsx` | 147 MB | XLSX  | 670,635 |
| `lfb_incidents_2024_on.xlsx`   | 66 MB  | XLSX  | 305,442 |
| `lfb_metadata.xlsx`            | 13 KB  | XLSX  | 39 column descriptors |

Combined raw size 526 MB, total roughly 1.96 million incident records.

Note: although the first file is named `2009_2017`, the CalYear column in the 200k row sample only covers 2009-2010. The xlsx samples confirm the second file starts in 2018 and the third in 2024. The full year span will be re-checked once the whole file is parsed during pre-processing, but headline coverage is January 2009 through 2024+, in line with the brief.

## 4. Schema

The metadata workbook describes 39 columns. Key groups:

- Time: `DateOfCall`, `CalYear`, `TimeOfCall`, `HourOfCall`
- Incident classification: `IncidentGroup`, `StopCodeDescription`, `SpecialServiceType`
- Property: `PropertyCategory`, `PropertyType`, `AddressQualifier`
- Location: `Postcode_full`, `Postcode_district`, `IncGeo_BoroughCode`, `IncGeo_BoroughName`, `ProperCase`, `IncGeo_WardCode`, `IncGeo_WardName`, `IncGeo_WardNameNew`, `Easting_m`, `Northing_m`, `Easting_rounded`, `Northing_rounded`, `Latitude`, `Longitude`, `FRS`, `IncidentStationGround`
- Response (target and helpers): `FirstPumpArriving_AttendanceTime`, `FirstPumpArriving_DeployedFromStation`, `SecondPumpArriving_AttendanceTime`, `SecondPumpArriving_DeployedFromStation`, `NumStationsWithPumpsAttending`, `NumPumpsAttending`, `PumpCount`, `PumpMinutesRounded`, `Notional Cost (£)`, `NumCalls`

Identifiers: `IncidentNumber`, `UPRN`, `USRN`. UPRN, postcode, exact eastings/northings and lat/lon are redacted for residential dwellings, which is the dominant source of missingness in those columns.

## 5. Sampling strategy

The raw files are too large to load fully in a single session. The notebook therefore:

- Streams the CSV with `open()` to count rows without parsing, then reads `nrows=200000` for distributional stats.
- Counts xlsx rows via `openpyxl.load_workbook(read_only=True).active.max_row`, then reads `nrows=50000` from each xlsx for distributional stats.

Sample sizes used for the stats below: 200,000 rows from CSV, 50,000 rows from each xlsx.

## 6. Target distribution: `FirstPumpArriving_AttendanceTime` (seconds)

| Period sample | n | missing % | mean (s) | median (s) | p95 (s) | min (s) | max (s) |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2009-2017 (n=200k) | 179,268 | 10.37 | 322.3 | 296.0 | 588.0 | 1 | 1200 |
| 2018-2023 (n=50k)  |  46,910 |  6.18 | 311.5 | 293.0 | 546.5 | 1 | 1198 |
| 2024+    (n=50k)   |  47,773 |  4.45 | 319.2 | 302.0 | 554.0 | 1 | 1200 |

Observations:

- Distribution is right-skewed across all three eras. Median sits at roughly 5 minutes, p95 at roughly 9-10 minutes, hard cap around 1,200 seconds (20 minutes).
- Missingness on the target has dropped over time (10.4 percent in the 2009-2017 sample down to 4.4 percent in 2024+), which is good news for modelling on more recent data.
- The 1,200 second ceiling looks like an operational truncation and should be flagged as a possible data quality artefact during pre-processing.

See `reports/target_distribution.png` for histograms with the median marked.

## 7. Incident type breakdown

From the 2009-2017 sample of 200k rows:

| IncidentGroup | count | share |
|---|---:|---:|
| False Alarm     | 94,306 | 47% |
| Special Service | 61,059 | 31% |
| Fire            | 44,635 | 22% |

The 2018-2023 and 2024+ samples show the same ordering (False Alarm dominant, Fire smallest). False Alarm is the single largest category in every era, which has direct implications for response time modelling because false alarms tend to have different operational priority handling.

## 8. Borough breakdown

Top 6 boroughs by incident count in the 2009-2017 sample:

| Borough | count |
|---|---:|
| Westminster   | 14,916 |
| Camden        | 11,155 |
| Tower Hamlets | 10,519 |
| Southwark     | 10,153 |
| Lambeth       |  8,471 |
| Hackney       |  8,173 |

Central and inner London boroughs dominate counts. Median response time by borough varies materially - the notebook prints the 10 fastest and 10 slowest boroughs by sample median, useful as a quick sanity check before building any model.

See `reports/borough_top15.png` and `reports/incident_group.png`.

## 9. Missing values

Top missing columns are consistent across all three files:

- `SecondPumpArriving_AttendanceTime` and `SecondPumpArriving_DeployedFromStation`: 63 to 67 percent missing. By design - many incidents only need one pump.
- `SpecialServiceType`: 60 to 69 percent missing. By design - only filled for Special Service incidents.
- `Postcode_full`, `UPRN`, `Easting_m`, `Northing_m`, `Latitude`, `Longitude`: 43 to 60 percent missing. Redacted for residential addresses (privacy).

The redacted-for-dwellings group is the most consequential for modelling. Coarse location is still available via `Easting_rounded`, `Northing_rounded`, `IncGeo_BoroughName`, `Postcode_district` and `IncidentStationGround`, so we can drop the redacted columns without losing geographic signal.

## 10. Key observations and next steps

1. The 2024+ file appears to be a partial year. Data quality on the target is the best of the three eras (4.45 percent missing).
2. The target is right-skewed with a fixed upper bound near 1,200 seconds. Either log-transform it for regression, or model the censoring explicitly.
3. False Alarm is the dominant incident type and likely behaves differently from Fire and Special Service. Stratify by `IncidentGroup` when splitting train/test.
4. Drop redacted columns (`Postcode_full`, exact `Easting_m` / `Northing_m`, `Latitude`, `Longitude`, `UPRN`) and rely on rounded grid plus borough/ward/station ground for spatial features.
5. Engineer time features from `DateOfCall` plus `HourOfCall` (weekday, month, hour bin, holiday flag).
6. For the modelling notebook, build a single pre-processed parquet covering all three files (sampled if needed), keyed on `IncidentNumber`, ready to join with the mobilisation file.

## 11. Artefacts

- Notebook: `notebooks/01_eda.ipynb` (executed end-to-end)
- Figures: `reports/target_distribution.png`, `reports/incident_group.png`, `reports/borough_top15.png`
- Inspection JSON: `src/eda_summary.json`
- Helper scripts: `src/eda_inspect.py`, `src/count_csv.py`
