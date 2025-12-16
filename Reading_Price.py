import yfinance as yf 
import pandas as pd 
import numpy as np 

def read_data(symbol:str ,timeframe:str,interval:str):
    data = yf.download(symbol=symbol,timeframe=timeframe,interval=interval)
    return data