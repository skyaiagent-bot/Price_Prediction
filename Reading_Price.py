import yfinance as yf 
import pandas as pd 
import numpy as np 

def read_data(symbol:str ,start:str,interval:str):
    data = yf.download(symbol,start=start,interval=interval)
    return data