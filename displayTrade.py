import streamlit as st
import datetime
from dummy import variable

import pandas as pd

st.set_page_config(
   page_title="Predict stocks",
   page_icon="🧊",
   layout="wide",
   initial_sidebar_state="expanded", )
# {str(datetime.date.today())}.txt


def colorChanger(val):
    if isinstance(val, float):
        color = 'red' if val < 0 else 'green'
        return 'color: %s' % color
    else:
        pass

try:
    
    st.title('Banknifty')
    banknifty = open(f'/home/rajath/Automated-Trading/ubuntu/banknifty{str(datetime.date.today())}.txt')
    linesbn = banknifty.read()
    lst = []
    for d in eval(linesbn):
        lst.append(d)
    
    df = pd.DataFrame.from_dict(lst).set_index('PurchaseTime')
    
    # df.astype({
    #     'boughtPrice': 'float64',
    #     'ltpCE': 'float64',
    #     'ltpPE': 'float64',
    #     'PnL':'float64',
    #     'PnlMul': 'float64',
    #     'exitPrice': 'float64'
    # })
    styled = df.style.applymap(colorChanger)
    st.dataframe(styled)
    st.info(f"The total Profit is {df['PnLMul'].sum()} total number of trades till now are {len(df)}")
except Exception as e:
    st.warning(e) 


try:       
    st.title('Nifty')
    nifty = open(f'/home/rajath/Automated-Trading/ubuntu/nifty{str(datetime.date.today())}.txt')
    linesn = nifty.read()
    lst = []
    for d in eval(linesn):
        lst.append(d)
    
    df = pd.DataFrame.from_dict(lst).set_index('PurchaseTime')
    
    styled = df.style.applymap(colorChanger)
    
    st.dataframe(styled)
    st.info(f"The total Profit is {df['PnLMul'].sum()} and total number of trades till now are {len(df)}")
except Exception as e:
    st.warning(e)