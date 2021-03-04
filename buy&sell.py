import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from fbprophet import Prophet
from datetime import date
import time
from fbprophet.plot import plot_plotly, plot_components_plotly
from get_all_tickers import get_tickers as gt
import asyncio 
import requests
import json

st.set_page_config(
   page_title="Predict stocks",
   page_icon="🧊",
   layout="wide",
   initial_sidebar_state="expanded", )

add_selectbox = st.sidebar.selectbox(
    "Want to predict stocks or options?",
    ('Stocks', 'Options'))



if add_selectbox == 'Stocks':
    stocks = ("AAPL", "GOOGL", "MSFT", )
    # nifty  = yf.Ticker('^NSEI')
    # st.write(nifty.info,)
    # st.write(nifty.recommendations)
    symbols = open('stock.txt', 'r')
    sym = []
    for sy in symbols.readlines():
        sym.append(sy)

    available_stocks = st.sidebar.selectbox("Available stocks symbol", sym)
    placeholder = st.empty()

    placeholder.title("Predict stocks and Options")

    selected_stock = st.text_input('Enter the stock name to predict', value=available_stocks)
    st.warning("Note only yahoo symbols work as of now",)
    START = "2015-01-01"
    TODAY = date.today().strftime("%Y-%m-%d")

    # st.title("Select Stock to Predict")
    # selected_stock = st.selectbox("Stocks", stocks)

    @st.cache
    def loadStockData(ticker):
        data = yf.download(ticker, start=START, end=TODAY)
        data.reset_index(inplace=True)
        return data

    data = loadStockData(selected_stock)
    if st.checkbox('Show raw data'):
        st.text("Select the last n days to fetch")
        val = st.slider('days', min_value=5, max_value=30)
        st.write(data.tail(int(val)))
    
    

    
    # sts = st.success(f"Loaded last {val} days")
    # sts.empty()
    
    openORclose = st.radio("Predict closing or opening price?", ('Close', 'Open'),)
    @st.cache
    def prediction(dataset, period_to_predict, closeOrOpen):
        if closeOrOpen == 'Close':
            m = Prophet()
            m.fit(dataset.rename(columns={'Date':'ds', 'Close':'y'},))
            future = m.make_future_dataframe(periods=int(period_to_predict))
            forecast = m.predict(future)
            return m, forecast
        
        else:    
            m = Prophet()
            m.fit(dataset.rename(columns={'Date':'ds', 'Open':'y'},))
            future = m.make_future_dataframe(periods=int(period_to_predict))
            forecast = m.predict(future)
            return m, forecast
        
    period_to_predict = st.slider('Prediction for how many days? max 365', min_value= 10, max_value=365)
    data_load_state = st.text('Loading data...')
    m, forecast = prediction(data, period_to_predict, openORclose)        
    st.write(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(int(period_to_predict)))
    fig1 = m.plot(forecast)
    st.plotly_chart(plot_plotly(m, forecast))
    data_load_state.text('Loading data...done!')
    
   

else:
    st.title('Options')

    
    def loadOptionsData(symbol):
        import logging
        import http.client
        http.client.HTTPConnection.debuglevel = 1
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True
        headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0"}
        response = requests.get(
            'https://www.nseindia.com/api/option-chain-indices',
            params={'symbol': symbol}, headers=headers)
        return response
        # else:
        #     loadOptionsData(val)
    
    r = loadOptionsData('NIFTY')

    st.dataframe(pd.read_json(json.dumps(r.json())))