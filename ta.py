import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import yfinance as yf
import datetime as dt

st.set_page_config(
    layout="wide"
)

@st.cache_data()
def get_data(ticket, period ,timeframe ):
    data = []
    current_time = dt.datetime.now().strftime("%d-%m-%Y %H:%M")
    temp = current_time
    # convert temp to datetime
    temp = dt.datetime.strptime(temp, "%d-%m-%Y %H:%M")
    
    converter = {
        '1h' : 1,
        '1d' : 24,
        '1w' : 168
    }
    
    for _ in range(30):
        try:
            df = yf.download(ticket, start=temp - dt.timedelta(hours=converter[period]), end= temp, interval= timeframe)
            if df.empty == False:
                data.append(df)
            temp = temp - dt.timedelta(hours=converter[period])
        except Exception as e:
            st.write('Error', e)
            break
    return data

st.cache_data()           
def POC(data):
    POCS = []
    for dt in data:
        temp = {}
        for close , volume in zip(dt['Close'], dt['Volume']):
            if close not in temp:
                temp[int(close)] = int(volume)
            else:
                temp[int(close)] += int(volume)
        POCS.append(temp)
    return POCS         
            
timeframe = st.selectbox("timeframe", ["1h", "1d", "1w"])

ticket = "BTC-USD"

if timeframe == "1h":
    interval = "1m"
    df = get_data(ticket, timeframe , interval)
    # st.write(df)
    POCS = POC(df)
    st.write(POCS)
elif timeframe == "1d":
    interval = "1h"
    df = get_data(ticket, timeframe , interval)
    # st.write(df)
    POCS = POC(df)
    st.write(POCS)
elif timeframe == "1w":
    interval = "1h"
    df = get_data(ticket, timeframe , interval)
    # st.write(df)
    POCS = POC(df)
    st.write(POCS)
    

    
