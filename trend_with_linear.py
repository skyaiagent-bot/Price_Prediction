import numpy as np
import pandas as pd


def rolling_slope(series,window=20):
    x= np.arange(window)
    slopes = np.full(len(series),np.nan)

    for i in range(window,len(series)):
        y = series[i-window:i]
        m,_ = np.polyfit(x,y,1)
        slopes[i] = m
    return slopes


