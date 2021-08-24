import pandas as pd
import streamlit as st
import datetime


st.set_page_config(
   page_title="Predict stocks",
   page_icon="🧊",
   layout="wide",
   initial_sidebar_state="expanded",
)

st.title('Nifty')
dataCEN = pd.read_csv(f'niftyCE{str(datetime.date.today())}.csv',)
dataCEN.drop('Unnamed: 0', axis=1, inplace = True)
dataPEN = pd.read_csv(f'niftyPE{str(datetime.date.today())}.csv')
dataPEN.drop('Unnamed: 0', axis=1, inplace = True)

st.table(dataPEN[75:])