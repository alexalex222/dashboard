# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# %%
val_metric_df = pd.read_csv('data/sp500_Cos_ValMetrics.csv')
cos_data_df = pd.read_csv('data/sp500_CosData.csv')
sector_data_df = pd.read_csv('data/sp500_SectorData.csv')

cos_data_df = cos_data_df.rename(columns={"symbol": "Symbol"}, errors="raise")


# %%
num_conv_table = {'K': 3, 'M': 6, 'B': 9, 'T': 12}
temp_num_array = np.zeros((len(val_metric_df), 2))
for i in range(len(val_metric_df)):
    temp_str_1 = val_metric_df['Market Cap (intraday)'][i]
    temp_str_2 = val_metric_df['Enterprise Value'][i]
    temp_num_array[i, 0] = float(temp_str_1[:-1]) * 10 ** num_conv_table[temp_str_1[-1]]
    temp_num_array[i, 1] = float(temp_str_2[:-1]) * 10 ** num_conv_table[temp_str_2[-1]]

num_to_df = pd.DataFrame(temp_num_array, columns=['Market Cap (intraday) clean', 'Enterprise Value clean'])
val_metric_df = pd.concat((val_metric_df, num_to_df), axis=1)


# %%
# join all tables together
joined_df = pd.merge(val_metric_df, cos_data_df, on='Symbol')
joined_df = pd.merge(joined_df, sector_data_df, on='Symbol')
joined_df.to_csv('data/sp_clean_joined.csv', index=False)


# %%
import plotly.express as px
import plotly.io as pio
pio.renderers.default = "browser"
joined_df = pd.read_csv('data/sp_clean_joined.csv')
fig = px.sunburst(
    joined_df[["Enterprise Value clean", "GICS Sector", "GICS Sub-Industry", "Symbol"]],
    path=["GICS Sector", "GICS Sub-Industry", "Symbol"])
fig.show()


# %%
import yfinance as yf

stock = yf.Ticker('AMZN')
stock_info = stock.info
selected_keys = ['longName', 'beta', 'forwardPE', 'trailingPE',  'enterpriseValue', 'marketCap', 'fiftyTwoWeekHigh', 'fiftyTwoWeekLow']
concise_info = {selected_key: stock_info[selected_key] for selected_key in selected_keys}


