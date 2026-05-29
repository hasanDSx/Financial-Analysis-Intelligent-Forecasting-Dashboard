import warnings
warnings.filterwarnings('ignore')

import pandas as pd

import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_absolute_percentage_error

# 1. READ & CLEAN DATA
excel_path = "/mnt/37B082B36FAB9CEA/Power BI & ML/01. Financial Analysis/Data/Financial Data.xlsx"
sales_df = pd.read_excel(excel_path)
sales_df['Date'] = pd.to_datetime(sales_df['Date'])
sales_column = ' Sales' if ' Sales' in sales_df.columns else 'Net Sales'

for col in [sales_column, 'Units Sold', 'Profit', 'Discounts']:
    sales_df[col] = pd.to_numeric(sales_df[col].replace('[$,]', '', regex=True), errors='coerce')

# 2. AGGREGATE MONTHLY
total_monthly = sales_df.groupby('Date')[[sales_column, 'Units Sold', 'Profit', 'Discounts']].sum().sort_index()

print(f"Date range: {total_monthly.index.min().date()} to {total_monthly.index.max().date()}")
print(f"Total months: {len(total_monthly)}\n")

# 3. FORECASTING FUNCTION
def get_best_ets_forecast(series, test_size=4, horizon=6):
    configs = [('add', None, None), ('add', 'add', 12), ('mul', None, None), 
               ('mul', 'add', 12), (None, None, None), (None, 'add', 12)]
    best_mape = float('inf')
    best_cfg = None
    
    for tr, se, sp in configs:
        try:
            m = ExponentialSmoothing(series.iloc[:-test_size], trend=tr, seasonal=se, seasonal_periods=sp).fit()
            mape = mean_absolute_percentage_error(series.iloc[-test_size:], m.forecast(test_size))
            if mape < best_mape:
                best_mape, best_cfg = mape, (tr, se, sp)
        except: continue
    tr, se, sp = best_cfg
    final_m = ExponentialSmoothing(series, trend=tr, seasonal=se, seasonal_periods=sp).fit()
    return final_m.forecast(horizon), (1 - best_mape) * 100

# 4. EXECUTION
targets = {'Sales': sales_column, 'Units': 'Units Sold', 'Profit': 'Profit', 'Discounts': 'Discounts'}
forecasts = {}

print("MODEL EVALUATION SUMMARY:")
print("-" * 40)
for label, col in targets.items():
    fc, acc = get_best_ets_forecast(total_monthly[col])
    forecasts[label] = fc
    print(f"{label:<15} | Accuracy: {acc:>6.2f}%")
print("-" * 40 + "\n")

# 5. TOP-DOWN DISTRIBUTION
numeric_cols = [sales_column, 'Units Sold', 'Profit', 'Discounts']
weights = sales_df.groupby(['Segment', 'Country', 'Product'])[numeric_cols].sum() / sales_df[numeric_cols].sum()
future_dates = pd.date_range(start=total_monthly.index.max() + pd.DateOffset(months=1), periods=6, freq='MS')

records = []
for i, fdate in enumerate(future_dates):
    for idx, row in weights.iterrows():
        records.append({
            'Date': fdate, 'Segment': idx[0], 'Country': idx[1], 'Product': idx[2],
            'Predicted_Units_Sold': round(forecasts['Units'].values[i] * row['Units Sold'], 2),
            'Predicted_Net_Sales': round(forecasts['Sales'].values[i] * row[sales_column], 2),
            'Predicted_Discounts': round(forecasts['Discounts'].values[i] * row['Discounts'], 2),
            'Predicted_Profit': round(forecasts['Profit'].values[i] * row['Profit'], 2)
        })

# 6. OUTPUT
final_df = pd.DataFrame(records)
output_path = "/home/hasan/Downloads/Final_Predictions.csv"
final_df.to_csv(output_path, index=False)

print(f"File saved to: {output_path}")
#print(f"Total rows generated: {len(final_df):,}\n")
print("\nData sample:\n")
print(final_df.head(3).to_string(index=False))
