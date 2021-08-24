import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

import pandas as pd
import pandas_ta
from datetime import datetime
import streamlit as st


fig = make_subplots(specs=[[{"secondary_y": True}]])

# bn = pd.read_csv('bankniftyCE2021-05-05.csv')
# bn.drop('Unnamed: 0', axis=1, inplace=True)
# bnsn = bn.ta.supertrend(period=7, multiplier=0.3)
# total = pd.concat([bn, bnsn], axis=1)

def visualize(total):
    total['date'] = pd.to_datetime(total['date'])
    fig.add_trace(go.Candlestick(x=total['date'],
                    open=total['open'],
                    high=total['high'],
                    low=total['low'],
                    close=total['close']),
                secondary_y=True)

    fig.add_trace(
        go.Bar(x=total['date'],
                y = total['volume'])
    )


    fig.layout.yaxis2.showgrid=False
    return fig

df = pd.read_csv('32500CE.csv')
viz = visualize(df)
st.plotly_chart(viz)



