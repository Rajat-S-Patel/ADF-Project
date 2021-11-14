import json
from django.http.response import JsonResponse
from django.shortcuts import render,HttpResponse
from requests.models import to_native_string
import yfinance as yf
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from plotly import graph_objs as go
from datetime import date
import datetime

import json
import numpy as np

MAX_ITERATIONS=300
class NumpyEncoder(json.JSONEncoder):
    """ Special json encoder for numpy types """
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj,datetime.datetime):
            return obj.strftime("%Y-%m-%d").__str__()
        return json.JSONEncoder.default(self, obj)

START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")
CACHE={}
period = 4 * 365


data=None

def Jsonify(fig):
    return json.dumps(fig.to_plotly_json(), cls=NumpyEncoder)


def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    return data

def plot_raw_data(data):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=data['Date'], y=data['Close'],
            line={'color': 'rgb(35, 255, 163)', 'width': 2}, 
            fill='tonexty',
            fillcolor='rgba(35, 255, 163,0.2)',
            name="Close"))
    fig.update_xaxes(title='Date')
    fig.update_yaxes(title='Close')
    fig.layout.update(xaxis_rangeslider_visible=True)
    fig.layout.update(template='plotly_dark')
    fig.update_traces(showlegend=True)
    fig.update_xaxes(rangeselector={'buttons': [{'count': 7, 'label': '1w', 'step': 'day', 'stepmode': 'backward'},
                                            {'count': 1, 'label': '1m', 'step': 'month', 'stepmode': 'backward'},
                                            {'count': 6, 'label': '6m', 'step': 'month', 'stepmode': 'backward'},
                                            {'count': 1, 'label': '1y', 'step': 'year', 'stepmode': 'backward'},
                                            {'step': 'all'}],
                                'font': {'color': '#0e5297'}})
    return Jsonify(fig)

def forcast(data):
    
    model=Prophet()
    df_train = data[['Date','Close']]
    df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})
    model.fit(df_train,iter=MAX_ITERATIONS)
    future = model.make_future_dataframe(periods=period)
    forecast = model.predict(future)
    fig=plot_plotly(model, forecast)
    fig.layout.update(template='plotly_dark')
    fig.update_xaxes(rangeselector_font_color='#0e5297')
    fig.update_xaxes(title='Date')
    fig.update_yaxes(title='Close')
    fig.data[0].marker.color='rgb(35, 255, 163)'
    fig.update_traces(showlegend=True)
    fig.data[3].name='Prediction range'
    fig.layout.showlegend=True
    
    return Jsonify(fig)



def onload(ticker):
    global CACHE
    if(ticker in CACHE.keys()):
        return CACHE[ticker]
    else:
        data=load_data(ticker)
        forecast=forcast(data)
        chart=plot_raw_data(data)
        
        
        CACHE[ticker]={"chart":chart,"forecast":forecast}
        return CACHE[ticker]

