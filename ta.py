import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import yfinance as yf
import datetime as dt
import plotly.subplots as sp

st.set_page_config(
    layout="wide"
)

@st.cache_data()
def get_data(ticket, period ,timeframe ):
    data = []
    current_time = dt.datetime.now()
    temp = current_time
    
    converter = {
        '1h' : 1,
        '1d' : 24,
        '1w' : 168
    }
    
    high_low_open_close = []
    
    while len(data) < 20:
        try:
            start = str(temp - dt.timedelta(hours=converter[period])).split(':')[0]+":00"
            start = pd.to_datetime(start)
            end = str(temp).split(':')[0]+":00"
            end = pd.to_datetime(end)
            # st.write(start , end)
            df = yf.download(ticket, start=start, end=end, interval= timeframe)
            if df.empty == False:
                data.append(df)
                # st.write(df)
                high_low_open_close.append([df['Open'][0] , df['Close'][-1] , max(df['High']) , min(df['Low'])])
            temp = temp - dt.timedelta(hours=converter[period])
        except Exception as e:
            pass
    return data , high_low_open_close

st.cache_data()           
def POC(data):
    POCS = []
    for dt in data:
        temp = {}
        for close , volume in zip(dt['Close'], dt['Volume']):
            if int(close) not in temp:
                temp[int(close)] = int(volume)
            else:
                temp[int(close)] += int(volume)
        POCS.append(temp)
    return POCS

@st.cache_data()
def TPO(data):
    TPOS = []
    for dt in data:
        temp = {}
        for close in dt['Close']:
            if int(close) not in temp:
                temp[int(close)] = 1
            else:
                temp[int(close)] += 1
        TPOS.append(temp)
    return TPOS


@st.cache_data()
def create_bar_chart(data, name , time):
    
    fig = sp.make_subplots(rows=2, cols=len(data), subplot_titles=[f'' for i in range(len(data))])

    for index, dt in enumerate(data):
        dt = pd.DataFrame.from_dict(dt, orient='index').reset_index()
        
        if name == 'POC':
            dt = dt.rename(columns={'index': 'Price', 0: 'POC'})
        else:
            dt = dt.rename(columns={'index': 'Price', 0: 'TPO'})
        
        # Add horizontal bar chart trace
        if time == '1h':
            time = 'hour'
        elif time == '1d':
            time = 'day'
        elif time == '1w':
            time = 'week'
        
        bar_trace = go.Histogram(x=dt[name], y=dt['Price'], orientation='h', name=f"{(19 - index)} {time} ago", marker=dict(color=px.colors.qualitative.Plotly[6]))
        fig.add_trace(bar_trace, row=1, col=index+1)

    # Update layout for subplot grid
    fig.update_layout(title_text=f'{name} Chart' , showlegend=False)
            
    return fig

def crete_candle_cart(timeframe , max_POCs , max_TPOs , data):
    ticket = "BTC-USD"
    right_now = dt.datetime.now()
    
    data = pd.DataFrame(data).rename(columns={0: 'Open', 1: 'Close', 2: 'High', 3: 'Low'})
    
    fig = sp.make_subplots(rows=1, cols=1)    
    fig.add_trace(go.Candlestick(x=data.index,
                    open=data['Open'],
                    high=data['High'],
                    low=data['Low'],
                    close=data['Close'], name='market data'), row=1, col=1)
    
    
    for i in range(len(max_POCs)-len(data.index)):
        max_POCs.pop()
    
    POCs = pd.DataFrame(max_POCs)
    POCs = POCs.rename(columns={0: 'POC'})
    POCs['time'] = data.index
    
    for i in range(len(max_TPOs)-len(data.index)):
        max_TPOs.pop()
    
    TPOs = pd.DataFrame(max_TPOs)
    TPOs = TPOs.rename(columns={0: 'TPO'})
    TPOs['time'] = data.index
    
    fig.add_trace(go.Scatter(x=POCs['time'], y=POCs['POC'], mode='markers', name='POC'), row=1, col=1)
    fig.add_trace(go.Scatter(x=TPOs['time'], y=TPOs['TPO'], mode='markers', name='TPO'), row=1, col=1)
    
    fig.update_layout(title=f"{ticket} {timeframe} chart", yaxis_title='Price (USD)')
    
    return fig

            
timeframe = st.selectbox("timeframe", ["1h", "1d", "1w"])

ticket = "BTC-USD"

if timeframe == "1h":
    interval = "1m"
    df , high_low_close_open= get_data(ticket, timeframe , interval)
    POCS = POC(df)
    max_POCs = []
    max_TPOs = []
    for poc in POCS:
        # get max value
        max_value = max(poc.values())
        # get key corresponding to max value
        max_keys = [k for k, v in poc.items() if v == max_value]
        max_POCs.append(max_keys)
    TP0S = TPO(df)
    for tpo in TP0S:
        # get max value
        max_value = max(tpo.values())
        # get key corresponding to max value
        max_keys = [k for k, v in tpo.items() if v == max_value]
        max_TPOs.append(max_keys)
    

elif timeframe == "1d":
    interval = "5m"
    df , high_low_close_open= get_data(ticket, timeframe , interval)
    POCS = POC(df)
    max_POCs = []
    max_TPOs = []
    for poc in POCS:
        # get max value
        max_value = max(poc.values())
        # get key corresponding to max value
        max_keys = [k for k, v in poc.items() if v == max_value]
        max_POCs.append(max_keys)
    TP0S = TPO(df)
    for tpo in TP0S:
        # get max value
        max_value = max(tpo.values())
        # get key corresponding to max value
        max_keys = [k for k, v in tpo.items() if v == max_value]
        max_TPOs.append(max_keys)

elif timeframe == "1w":
    interval = "1h"
    df , high_low_close_open= get_data(ticket, timeframe , interval)
    POCS = POC(df)
    max_POCs = []
    max_TPOs = []
    for poc in POCS:
        # get max value
        max_value = max(poc.values())
        # get key corresponding to max value
        max_keys = [k for k, v in poc.items() if v == max_value]
        max_POCs.append(max_keys)
    TP0S = TPO(df)
    for tpo in TP0S:
        # get max value
        max_value = max(tpo.values())
        # get key corresponding to max value
        max_keys = [k for k, v in tpo.items() if v == max_value]
        max_TPOs.append(max_keys)
    
st.plotly_chart(crete_candle_cart(timeframe , max_POCs , max_TPOs , high_low_close_open), use_container_width=True)
st.plotly_chart(create_bar_chart(POCS, 'POC' , timeframe), use_container_width=True)
st.write('---')
st.plotly_chart(create_bar_chart(TP0S, 'TPO' , timeframe), use_container_width=True)
