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
# from visualizer import visualize

st.set_page_config(
   page_title="Predict stocks",
   page_icon="🧊",
   layout="wide",
   initial_sidebar_state="expanded", )

st.title('Bank Nifty')




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
    

# indices = pd.read_csv(f'indicesCE{str(datetime.date.today())}.csv')
# indices.drop('Unnamed: 0', axis=1, inplace = True)
# st.write('Indices')
# st.write(indices)
# dataCE = pd.read_csv(f'bankniftyCE{str(datetime.date.today())}.csv')
# dataCE.drop('Unnamed: 0', axis=1, inplace = True)
# # figbnCE = visualize(dataCE)
# # st.plotly_chart(figbnCE)
# dataPE = pd.read_csv(f'bankniftyPE{str(datetime.date.today())}.csv')
# dataPE.drop('Unnamed: 0', axis=1, inplace = True)

# st.write('Call Option data')

# ce = st.write(dataCE[len(dataCE)-15:])
# st.write('Put Option data')
# pe = st.write(dataPE[len(dataPE)-15:] )

# --------- nifty -------


st.title('Nifty')
dataCEN = pd.read_csv(f'niftyCE{str(datetime.date.today())}.csv',)
dataCEN.drop('Unnamed: 0', axis=1, inplace = True)
dataPEN = pd.read_csv(f'niftyPE{str(datetime.date.today())}.csv')
dataPEN.drop('Unnamed: 0', axis=1, inplace = True)
st.write('Call Option data')
ceN = st.write(dataCEN[len(dataCEN)-15:])
st.write('Put Option data')
peN = st.write(dataPEN[len(dataPEN)-15:])

# ------------



st.write('Banknifty')
dfRt = pd.read_csv('banknifty_status.csv',)
dfRt.drop('Unnamed: 0', axis=1, inplace = True)
s = dfRt.style.applymap(colorChanger)
st.table(s)
st.write('Nifty')
dfRtN = pd.read_csv('nifty_status.csv')
dfRtN.drop('Unnamed: 0', axis=1, inplace = True)
sN = dfRtN.style.applymap(colorChanger)
st.table(sN)

# st.write('Tatasteel')
# dfts = pd.read_csv('tatasteel_status.csv')
# dfts.drop('Unnamed: 0', axis=1, inplace=True)
# ts = dfts.style.applymap(colorChanger)
# st.table(ts)
# ------- tatasteel

# --------- nifty -------





#-----------------TATASTEEL----------------
# st.title('Tatasteel')
# st.write('TS CE Data')
# dataCEts = pd.read_csv(f'tatasteelCE{str(datetime.date.today())}.csv',)
# dataCEts.drop('Unnamed: 0', axis=1, inplace = True)
# ind = len(dataCEts)-1 - 75
# st.write(dataCEts[ind:])

# st.write('TS PE Data')
# dataOptCEts = pd.read_csv(f'tatasteelPE{str(datetime.date.today())}.csv',)
# dataOptCEts.drop('Unnamed: 0', axis=1, inplace = True)
# st.write(dataOptCEts[75:])





# nifty_opt = get_history(symbol="NIFTYBANK",
#                         start=date(2021,4,6),
#                         end=date(2021,4,6),
#                         index=True,
#                         option_type='PE',
#                         strike_price=33900,
#                         expiry_date=date(2021,4,8))
# st.write(nifty_opt)