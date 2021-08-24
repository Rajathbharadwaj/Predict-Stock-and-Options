import streamlit as st
import datetime
from dummy import variable

import pandas as pd

def colorChanger(val):
    if isinstance(val, str):
        if val == 'sell' or val == "Don't buy":
            color = 'red'
        elif val == 'buy':
            color = 'green'
        else:
            color = 'yellow'
        return 'color: %s' % color
    else:
        pass


st.set_page_config(
   page_title="Predict stocks",
   page_icon="🧊",
   layout="wide",
   initial_sidebar_state="expanded", )

st.title('Stock Status')

df = pd.read_csv('stockStatus.csv')
df.drop('Unnamed: 0', axis=1, inplace = True)
styled = df.style.applymap(colorChanger)
# df.set_index('name', inplace=True)
st.table(styled,)
