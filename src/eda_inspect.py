"""Quick inspection: row counts, schema, target stats (sampled)."""
import pandas as pd
import os, json

DATA = 'data/'
OUT = {}

csv_path = f'{DATA}/lfb_incidents_2009_2017.csv'
n_csv = sum(1 for _ in open(csv_path, 'r', encoding='latin-1', errors='replace')) - 1
OUT['csv_rows'] = n_csv
df1 = pd.read_csv(csv_path, nrows=200000, low_memory=False, encoding='latin-1')
OUT['csv_cols'] = list(df1.columns)
print('CSV rows total:', n_csv)
print('CSV cols n:', len(df1.columns))

x2_path = f'{DATA}/lfb_incidents_2018_2023.xlsx'
df2 = pd.read_excel(x2_path, nrows=50000)
OUT['xlsx2_cols'] = list(df2.columns)
print('XLSX 2018-2023 sample:', df2.shape)

x3_path = f'{DATA}/lfb_incidents_2024_on.xlsx'
df3 = pd.read_excel(x3_path, nrows=50000)
OUT['xlsx3_cols'] = list(df3.columns)
print('XLSX 2024+ sample:', df3.shape)

import openpyxl
def xlsx_rows(p):
    wb = openpyxl.load_workbook(p, read_only=True)
    ws = wb.active
    n = ws.max_row
    wb.close()
    return n
OUT['xlsx2_rows'] = xlsx_rows(x2_path) - 1
OUT['xlsx3_rows'] = xlsx_rows(x3_path) - 1
print('xlsx2 rows:', OUT['xlsx2_rows'])
print('xlsx3 rows:', OUT['xlsx3_rows'])

tgt = 'FirstPumpArriving_AttendanceTime'
for nm, df in [('csv200k', df1), ('xlsx2_50k', df2), ('xlsx3_50k', df3)]:
    if tgt in df.columns:
        s = pd.to_numeric(df[tgt], errors='coerce').dropna()
        OUT[f'{nm}_target'] = {
            'n': int(len(s)),
            'mean': float(s.mean()),
            'median': float(s.median()),
            'p95': float(s.quantile(0.95)),
            'min': float(s.min()),
            'max': float(s.max()),
            'missing_pct': float(df[tgt].isna().mean() * 100),
        }
        print(nm, OUT[f'{nm}_target'])

for nm, df in [('csv', df1), ('xlsx2', df2), ('xlsx3', df3)]:
    bcol = 'ProperCase' if 'ProperCase' in df.columns else ('IncGeo_BoroughName' if 'IncGeo_BoroughName' in df.columns else None)
    if bcol:
        OUT[f'{nm}_borough_top10'] = df[bcol].value_counts().head(10).to_dict()
    if 'IncidentGroup' in df.columns:
        OUT[f'{nm}_incidentgroup'] = df['IncidentGroup'].value_counts().head(10).to_dict()
    if 'CalYear' in df.columns:
        OUT[f'{nm}_calyear_min_max'] = (int(df['CalYear'].min()), int(df['CalYear'].max()))

for nm, df in [('csv', df1), ('xlsx2', df2), ('xlsx3', df3)]:
    miss = (df.isna().mean()*100).sort_values(ascending=False).head(15)
    OUT[f'{nm}_missing_top15'] = miss.round(2).to_dict()

with open('./src/eda_summary.json', 'w') as f:
    json.dump(OUT, f, indent=2, default=str)
print('SAVED summary')
