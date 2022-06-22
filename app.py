import streamlit as st
import yfinance as yf
import pandas as pd

from utils import cumulative_return


st.title('SP500 Dashboard')
tickers = ['MSFT', 'AAPL', 'TSLA']

ticker_from_dropdown = st.multiselect('Pick a ticker', tickers)

start_date = st.date_input('Start', value=pd.to_datetime('2021-07-01'))
end_date = st.date_input('End', value=pd.to_datetime('today'))

if len(ticker_from_dropdown) > 0:
    yf_df = yf.download(ticker_from_dropdown, start_date, end_date)
    adj_close_srs = yf_df['Adj Close']
    cum_return = cumulative_return(adj_close_srs)
    st.header('Cumulative return of {}'.format(ticker_from_dropdown))
    st.line_chart(cum_return)