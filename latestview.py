import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
from fbprophet import Prophet
from datetime import date
import datetime
import time
from fbprophet.plot import plot_plotly, plot_components_plotly
from get_all_tickers import get_tickers as gt
import asyncio 
import requests
import json
import seaborn as sns
import schedule
from dummy import *
from nsetools import Nse
import requests




def colorChanger(val):
    if isinstance(val, str):
        pass
    else:
        color = 'red' if val < 0 else 'green'
        return 'color: %s' % color
    

def colorChangerRev(val):
    if isinstance(val, str):
        pass
    else:
        color = 'red' if val == 0 else 'green'
        return 'color: %s' % color 
    
    
st.set_page_config(
   page_title="Predict stocks",
   page_icon="🧊",
   layout="wide",
   initial_sidebar_state="expanded", )

st.title('Bank Nifty')

dataCE = pd.read_csv(f'bankniftyCE{str(datetime.date.today())}.csv')
dataCE.drop('Unnamed: 0', axis=1, inplace = True)
st.write(dataCE[150:])
dataOptCE = pd.read_csv(f'bankniftyOptCE{str(datetime.date.today())}.csv')
dataOptCE.drop('Unnamed: 0', axis=1, inplace = True)
st.write(dataOptCE[150:])
dataOptPE = pd.read_csv(f'bankniftyOptPE{str(datetime.date.today())}.csv')
dataOptPE.drop('Unnamed: 0', axis=1, inplace = True)
st.write(dataOptPE[150:])

dfRt = pd.read_csv('banknifty_status.csv',)
dfRt.drop('Unnamed: 0', axis=1, inplace = True)
s = dfRt.style.applymap(colorChanger)
st.table(s)

# --------- nifty -------
st.write('Nifty')
dfRtN = pd.read_csv('nifty_status.csv')
dfRtN.drop('Unnamed: 0', axis=1, inplace = True)
sN = dfRtN.style.applymap(colorChanger)
st.table(sN)
st.title('Nifty')
dataCEN = pd.read_csv(f'niftyCE{str(datetime.date.today())}.csv',)
dataCEN.drop('Unnamed: 0', axis=1, inplace = True)
st.write(dataCEN[150:])
st.title('Nifty CE Data')
dataOptCEN = pd.read_csv(f'niftyOptCE{str(datetime.date.today())}.csv',)
dataOptCEN.drop('Unnamed: 0', axis=1, inplace = True)
st.write(dataOptCEN[150:])
st.title('Nifty PE Data')
dataOptPEN = pd.read_csv(f'niftyOptPE{str(datetime.date.today())}.csv',)
dataOptPEN.drop('Unnamed: 0', axis=1, inplace = True)
st.write(dataOptPEN[150:])
#-----------------TATASTEEL----------------
# st.write('TATASTEEL')
# dfRtts = pd.read_csv('tatasteel_status.csv')
# dfRtts.drop('Unnamed: 0', axis=1, inplace = True)
# sts = dfRtts.style.applymap(colorChanger)
# st.table(sts)
# st.title('tatasteel')
# dataCEts = pd.read_csv(f'tatasteelCE{str(datetime.date.today())}.csv',)
# dataCEts.drop('Unnamed: 0', axis=1, inplace = True)
# st.write(dataCEts[150:])
# st.title('TS CE Data')
# dataOptCEts = pd.read_csv(f'tatasteelOptCE{str(datetime.date.today())}.csv',)
# dataOptCEts.drop('Unnamed: 0', axis=1, inplace = True)
# st.write(dataOptCEts[145:])
# st.title('TS PE Data')
# dataOptPEts = pd.read_csv(f'tatasteelOptPE{str(datetime.date.today())}.csv',)
# dataOptPEts.drop('Unnamed: 0', axis=1, inplace = True)
# st.write(dataOptPEts[83:])







# nifty_opt = get_history(symbol="NIFTYBANK",
#                         start=date(2021,4,6),
#                         end=date(2021,4,6),
#                         index=True,
#                         option_type='PE',
#                         strike_price=33900,
#                         expiry_date=date(2021,4,8))
# st.write(nifty_opt)