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
import seaborn as sns

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

    stock_name = st.text_input('Enter the stock to fetch RT Data (ALL CAPS)', value='NIFTY')
    
    

    def loadOptionsData(symbol):
        import logging
        import http.client
        http.client.HTTPConnection.debuglevel = 1
        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True
        headers = {'authority': 'www.nseindia.com', 'sec-ch-ua': '"Google Chrome";v="89","Chromium";v="89", ";Not A Brand";v="99"', 'dnt': '1', 'sec-ch-ua-mobile': '?0','user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36', 
        'accept': '*/*','sec-fetch-site': 'same-origin', 'sec-fetch-mode': 'cors', 'sec-fetch-dest': 'empty',  'referer': 'https://www.nseindia.com/get-quotes/derivatives?symbol=TATASTEEL', 'accept-language': 'en-US,en;q=0.9', 'cookie': '_ga=GA1.2.1081862820.1614865340; _gid=GA1.2.1264843313.1614865340; bm_mi=9A4B9B11525D0E0771CB3018E77200AF~uBdVRpAS8H0oHTEVPVED5iZXRhbswRbqKr9FwRIsetfXmbIHY0sAbxdZo5tNT4NlJoD0v//v/5aLJS7opAIITW20uMU1K2+v9IYGmYPQC4JEy63vzpY1Eo9kQsXlR42FCR1jxWhvbJBDJj+rKQ9XczVCUiil+Z/LnEtpl9Jqb7q6hvLTMRGI5YyisNFgmtX2bZDkDJOSPtGGmSfINgJzgejwIpd73Eq46BDG0iUHDzl8sOowfiUO0VmJ6SKJK1YXpwwEeYAJ1eUc7cZ3wvnl+r9/lyJGgteYpDlWH0ICphM=; ak_bmsc=BACEC0601DD7BC089262BC414A09B25717CB3F26EE390000E98E42607E58EC21~plGmzJSDgUpUSGhsyhqglZod0mpHnIaGCKeJbCcijBnYLZ27mDAfI+zk7uYf1uka0FZGdh3UV0x0Ftvk1p4o+hlbwH0eTzCrzjU5dX5K53GdyzYqcFbkIk1Fhb3vK+I8Qo6+ire/GxtFwnrFsMPs4QFfI6p2kw1OWb1kkuO8jUOrvlSsQQRSOakdwPoI/huLPRFPyH5SzsT0CLtYxPkUDxoDp4EWiaqUjmToSqgBE1zvIsmGgS60P0zjg1no2vRldS; nsit=btA7vAkQKEl7v1W_C8IP_1YB; nseappid=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhcGkubnNlIiwiYXVkIjoiYXBpLm5zZSIsImlhdCI6MTYxNDk3ODQ3NSwiZXhwIjoxNjE0OTgyMDc1fQ.nOdnX3Zz4ecOXc9PPKS1adDtFe7uqSPzR0oje-xylqM; AKA_A2=A; _gat_UA-143761337-1=1; nseQuoteSymbols=[{"symbol":"ONGC","identifier":null,"type":"equity"},{"symbol":"TATASTEEL","identifier":null,"type":"equity"},{"symbol":"RELIANCE","identifier":null,"type":"equity"},{"symbol":"NIFTY","identifier":null,"type":"equity"},{"symbol":"ULTRACEMCO","identifier":null,"type":"equity"}]; RT="z=1&dm=nseindia.com&si=a0720b4b-d39f-448f-9660-f171042e20dc&ss=klwshj7q&sl=0&tt=0&bcn=%2F%2F684d0d3d.akstat.io%2F&ld=28vjz&nu=29229de80135c93cac9e000a3892125b&cl=1mn"; bm_sv=263F730BF03C98334C043DAEBC770704~9cA3hGpWATfOSB2FAj00RUrQkyz92xmEwCpJGDLFRRPgJ6yXndmO6Fb6JMBHSwg7MJJbmGmhQ7S7ZszJMA66POnRR1uXKfJp9HeONBk3VCVU9D0/l+SZrQO5jNEqacGg/EjVzBiLoZMWG6Zq/x55EDdbGmUtksz0kGEarJgYCFM='}

        try:
            if symbol == 'NIFTY':
                response = requests.get(
                'https://www.nseindia.com/api/option-chain-indices',
                params={'symbol': symbol}, headers=headers)
            else:
                response = requests.get(
                'https://www.nseindia.com/api/option-chain-equities',
                params={'symbol': symbol}, headers=headers)
        except Exception as e:
            print(f'this is the ex -> {e}')
        return response
    
    response = loadOptionsData(stock_name)

    if st.button('Click to Reload'):
        response = loadOptionsData(stock_name)

    
    s = json.dumps(response.json())
    j = json.loads(s)

    #creating DF
    df = pd.DataFrame(columns=[
        'OICALL', 
        'CHNG IN OI CALL',
        'VOLUME CALL',
        'IV CALL',
        'LTP CALL',
        'CHNG CALL',
        'BID QTY CALL',
        'BID PRICE CALL',
        'ASK PRICE CALL',
        'ASK QTY CALL',
        'STRIKE PRICE',
        'BID QTY PUT',
        'BID PRICE PUT',
        'ASK PRICE PUT',
        'ASK QTY PUT',
        'CHNG PUT',
        'LTP PUT',
        'IV PUT',
        'VOLUME PUT',
        'CHNG IN OI PUT',
        'OI PUT'
        ])

    #assigning values
    STRIKE_PRICE = []
    OICALL = []
    chgInOICALL = []
    volCALL = []
    IVCALL = []
    LTPCALL = []
    ChgCALL = []
    BIDQtyCALL = []
    BIDPriceCALL = []
    ASKPriceCALL = []
    ASKQtyCALL = []
    BIDQtyPUT = []
    BIDPricePUT = []
    ASKPricePUT = []
    ASKQtyPUT = []
    ChngPUT = []
    LTPPUT = []
    IVPUT = []
    volPUT = []
    chngInOIPUT = []
    OIPUT =[]

    for k in j['filtered']['data']:
        try:
            STRIKE_PRICE.append(k['strikePrice'])
            OICALL.append(k['CE']['openInterest'])
            chgInOICALL.append(k['CE']['changeinOpenInterest'])
            volCALL.append(k['CE']['totalTradedVolume'])
            IVCALL.append(k['CE']['impliedVolatility'])
            LTPCALL.append(k['CE']['lastPrice'])
            ChgCALL.append(k['CE']['change'])
            BIDQtyCALL.append(k['CE']['bidQty'])
            BIDPriceCALL.append(k['CE']['bidprice'])
            ASKPriceCALL.append(k['CE']['askPrice'])
            ASKQtyCALL.append(k['CE']['askQty'])
            BIDQtyPUT.append(k['PE']['bidQty'])
            BIDPricePUT.append(k['PE']['bidprice'])
            ASKPricePUT.append(k['PE']['askPrice'])
            ASKQtyPUT.append(k['PE']['askQty'])
            ChngPUT.append(k['PE']['change'])
            LTPPUT.append(k['PE']['lastPrice'])
            IVPUT.append(k['PE']['impliedVolatility'])
            volPUT.append(k['PE']['totalTradedVolume'])
            chngInOIPUT.append(k['PE']['changeinOpenInterest'])
            OIPUT.append(k['PE']['openInterest'])
        except:
            pass
            
    df['STRIKE PRICE'] = pd.Series(STRIKE_PRICE, )
    df['OICALL'] = pd.Series(OICALL)
    df['CHNG IN OI CALL'] = pd.Series(chgInOICALL)
    df['VOLUME CALL'] = pd.Series(volCALL)
    df['IV CALL'] = pd.Series(IVCALL)
    df['LTP CALL'] = pd.Series(LTPCALL)
    df['CHNG CALL'] = pd.Series(ChgCALL)
    df['BID QTY CALL'] = pd.Series(BIDQtyCALL)
    df['BID PRICE CALL'] = pd.Series(BIDPriceCALL)
    df['ASK PRICE CALL'] = pd.Series(ASKPriceCALL)
    df['ASK QTY CALL'] = pd.Series(ASKQtyCALL)
    df['BID QTY PUT'] = pd.Series(BIDQtyPUT)
    df['BID PRICE PUT'] = pd.Series(BIDPricePUT)
    df['ASK PRICE PUT'] = pd.Series(ASKPricePUT)
    df['ASK QTY PUT'] = pd.Series(ASKQtyPUT)
    df['CHNG PUT'] = pd.Series(ChngPUT)
    df['LTP PUT'] = pd.Series(LTPPUT)
    df['IV PUT'] = pd.Series(IVPUT)
    df['VOLUME PUT'] = pd.Series(volPUT)
    df['CHNG IN OI PUT'] = pd.Series(chngInOIPUT)
    df['OI PUT'] = pd.Series(OIPUT  ) 


    def df_style(val):
        return 'font-weight: bold'
    # def highlight_cols(x):
    #     #copy df to new - original data are not changed
    #     df = x.copy()
    #     cm = sns.light_palette("green", as_cmap=True)
    #     #select all values to default value - red color
    #     df.loc[:,:] = 'background-color: green'
    #     #overwrite values grey color
    #     df[['STRIKE PRICE']] = 'background-color: grey'
    #     #return color df
    #     return df    

    # s = df.style.apply(highlight_cols, axis=None)
    cm = sns.light_palette("green", as_cmap=True)
    s = df.style.background_gradient(cmap=cm, subset=pd.IndexSlice[:, ])
    s = df.style.background_gradient(cmap='viridis', subset=pd.IndexSlice[:, 'STRIKE PRICE'])
    s = df.style.applymap(df_style, subset=pd.IndexSlice[:, 'STRIKE PRICE'])
    st.write(s) 