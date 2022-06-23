import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from utils import cumulative_return, calc_performance_metrics


@st.cache
def get_sp_data():
    df = pd.read_csv('data/sp_clean_joined.csv')
    return df


sp_info_df = get_sp_data()

tickers = sp_info_df['Symbol'].values

#%% Page Selector
page = st.sidebar.radio('Pick type of components',
                        ('Overview', 'Single Stock', 'Stock Comparison'))


if page == 'Stock Comparison':
    st.title('Stock comparison')

    ticker_from_dropdown = st.multiselect('Pick a ticker', tickers)

    start_date = st.date_input('Start', value=pd.to_datetime('2021-07-01'))
    end_date = st.date_input('End', value=pd.to_datetime('today'))

    if len(ticker_from_dropdown) > 0:
        yf_df = yf.download(ticker_from_dropdown, start_date, end_date)
        adj_close_srs = yf_df['Adj Close']
        daily_return = adj_close_srs.pct_change().fillna(0)
        cum_return = cumulative_return(adj_close_srs)
        st.header('Cumulative return of {}'.format(ticker_from_dropdown))
        st.line_chart(cum_return)

        if len(ticker_from_dropdown) >= 2:
            performance_results = calc_performance_metrics(daily_return.values)
            performance_results_df = pd.DataFrame(
                performance_results,
                columns=cum_return.columns,
                index=['Annual Return',
                       'Annual Volatility',
                       'Sharpe Ratio',
                       'Downside Risk',
                       'Sortino Ratio',
                       'Calmar Ratio',
                       'Max Drawdown',
                       ]
            )
            st.dataframe(performance_results_df)

elif page == 'Overview':
    st.title('Overview')


    fig = px.box(sp_info_df, x='GICS Sector', y='Beta', points="all")
    fig.update_layout(width=1000, height=600)
    st.plotly_chart(fig)

    sp_info_market_cap_filtered_df = sp_info_df[sp_info_df['Market Cap (intraday) clean'] < 0.5e12]
    fig = px.box(sp_info_market_cap_filtered_df, x='GICS Sector', y='Market Cap (intraday) clean', points="all")
    fig.update_layout(width=1000, height=600)
    st.plotly_chart(fig)

    sp_info_ev_filtered_df = sp_info_df[sp_info_df['Enterprise Value clean'] < 0.5e12]
    fig = px.box(sp_info_ev_filtered_df, x='GICS Sector', y='Enterprise Value clean', points="all")
    fig.update_layout(width=1000, height=600)
    st.plotly_chart(fig)

    sp_info_ev_rev_filtered_df = sp_info_df[sp_info_df['Enterprise Value/Revenue'] < 30]
    fig = px.box(sp_info_ev_rev_filtered_df, x='GICS Sector', y='Enterprise Value/Revenue', points="all")
    fig.update_layout(width=1000, height=600)
    st.plotly_chart(fig)

    fig = px.sunburst(
        sp_info_df[["Enterprise Value clean", "GICS Sector", "GICS Sub-Industry", "Symbol"]],
        path=["GICS Sector", "GICS Sub-Industry", "Symbol"])
    fig.update_layout(width=1000, height=1000)
    st.plotly_chart(fig)



else:
    st.title('Single stock data')

    ticker_from_dropdown = st.selectbox('Pick a ticker', tickers)
    start_date = st.date_input('Start', value=pd.to_datetime('2021-07-01'))
    end_date = st.date_input('End', value=pd.to_datetime('today'))

    if len(ticker_from_dropdown) > 0:
        yf_df = yf.download(ticker_from_dropdown, start_date, end_date)
        stock_ticker = yf.Ticker(ticker_from_dropdown)
        stock_ticker_info = stock_ticker.info
        selected_keys = [
            'longName',
            'beta',
            'forwardPE',
            'trailingPE',
            'enterpriseValue',
            'marketCap',
            'fiftyTwoWeekHigh',
            'fiftyTwoWeekLow'
        ]
        concise_info = {selected_key: stock_ticker_info[selected_key] for selected_key in selected_keys}
        st.metric(label='Name', value=concise_info['longName'])
        col1, col2, col3 = st.columns(3)
        col1.metric(label='Beta', value=concise_info['beta'])
        col2.metric(label='Forward PE', value=concise_info['forwardPE'])
        col3.metric(label='Trailing PE', value=concise_info['trailingPE'])

        col4, col5  = st.columns(2)
        col4.metric(label='EV', value=concise_info['enterpriseValue'])
        col5.metric(label='Market Cap', value=concise_info['marketCap'])

        col6, col7 = st.columns(2)
        col4.metric(label='52W High', value=concise_info['fiftyTwoWeekHigh'])
        col5.metric(label='52W Low', value=concise_info['fiftyTwoWeekLow'])


        fig = go.Figure(data=[go.Candlestick(x=yf_df.index,
                                             open=yf_df['Open'],
                                             high=yf_df['High'],
                                             low=yf_df['Low'],
                                             close=yf_df['Close'])])
        fig.update_layout(
            width=1000, height=600,
            title="{}".format(ticker_from_dropdown),
            xaxis_rangeslider_visible=False
        )
        st.plotly_chart(fig, use_container_width=True)

