import pandas as pd
import numpy as np
import talib as ta
from trend_with_linear import rolling_slope

def add_technical_indicators(data:pd.DataFrame)->pd.DataFrame:
    """
    Adds technical indicators to the given DataFrame.

    Parameters:
    data (pd.DataFrame): DataFrame containing stock price data with 'Open', 'High', 'Low', 'Close', and 'Volume' columns.

    Returns:
    pd.DataFrame: DataFrame with added technical indicators.
    """
    data = pd.DataFrame(data)
    # Moving Averages
    data['SMA_20'] = ta.SMA(data['Close'].values.reshape(-1), timeperiod=20)
    data['SMA_50'] = ta.SMA(data['Close'].values.reshape(-1), timeperiod=50)
    data['EMA_20'] = ta.EMA(data['Close'].values.reshape(-1), timeperiod=20)
    data['EMA_50'] = ta.EMA(data['Close'].values.reshape(-1), timeperiod=50)
    data['MA_slope'] = data['SMA_50'] - data['SMA_50'].shift(5)
    data['ATR'] = ta.ATR(high=data['High'].values.reshape(-1),low=data['Low'].values.reshape(-1),close=data['Close'].values.reshape(-1),timeperiod=14) 
    
    data['ADX'] = ta.ADX(data['High'].values.reshape(-1), data['Low'].values.reshape(-1), data['Close'].values.reshape(-1), timeperiod=14)
    data['PLUS_DI'] = ta.PLUS_DI(data['High'].values.reshape(-1), data['Low'].values.reshape(-1), data['Close'].values.reshape(-1), timeperiod=14)
    data['MINUS_DI'] = ta.MINUS_DI(data['High'].values.reshape(-1), data['Low'].values.reshape(-1), data['Close'].values.reshape(-1), timeperiod=14)
    # Relative Strength Index (RSI)
    data['RSI_14'] = ta.RSI(data['Close'].values.reshape(-1), timeperiod=14)

    # Bollinger Bands
    upperband, middleband, lowerband = ta.BBANDS(data['Close'].values.reshape(-1), timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    data['BB_upper'] = upperband
    data['BB_middle'] = middleband
    data['BB_lower'] = lowerband

    # MACD
    macd, macdsignal, macdhist = ta.MACD(data['Close'].values.reshape(-1), fastperiod=12, slowperiod=26, signalperiod=9)
    data['MACD'] = macd
    data['MACD_signal'] = macdsignal
    data['MACD_hist'] = macdhist
    # conditions = [
    #     (data['ADX'] > 18) &
    #     (data['PLUS_DI'] > data['MINUS_DI']) &
    #     (data['MA_slope'] > 0),

    #     (data['ADX'] > 18) &
    #     (data['MINUS_DI'] > data['PLUS_DI']) &
    #     (data['MA_slope'] < 0),

    #     (data['ADX'] <= 18)
    # ]
    # choices = ['Downtrend', 'Uptrend', 'Range']
    # data['Market_Regime'] = np.select(conditions, choices, default='Range')
    
    # window = 10
    # data['LR_slope'] = rolling_slope(data['Close'].values.reshape(-1) , window=window)
    # data['Slope_norm'] = data["LR_slope"] / data['ATR']

    # threshold = data['Slope_norm'].rolling(100).std() * 0.5
    # condition = [
    #     data['Slope_norm'] > threshold,
    #     data['Slope_norm'] < -threshold
    # ]

    # choices_  = [ 'UpTrend',"DownTrend"]
    # data['Market_Regime_LR'] = np.select(condition, choices_, default='Range') 

    long_window = 70 
    short_window = 18
    data['LR_long'] = rolling_slope(data['Close'].values.reshape(-1),window=long_window)
    data['LR_short'] = rolling_slope(data['Close'].values.reshape(-1),window=short_window)

    data['LR_long_norm'] = data['LR_long']/data['ATR']
    data['LR_short_norm'] = data['LR_short']/data['ATR']


    long_threshold = 0.04
    short_threshold = 0.015
    
    conditions=[
    (data['LR_long_norm'] > long_threshold) & (data['LR_short_norm'] > short_threshold),
    (data['LR_long_norm'] < -long_threshold) & (data['LR_short_norm'] < -short_threshold),
    (data['LR_long_norm'] > long_threshold) & (data['LR_short_norm'] < -short_threshold),
    (data['LR_long_norm'] < -long_threshold) & (data['LR_short_norm'] > short_threshold)     
    ]

    choices = [
    'Uptrend',
    'Downtrend',
    'Pullback_in_Uptrend',
    'Rally_in_Downtrend'
    ]


    data['Market_Regime_LR'] = np.select(conditions, choices, default='Range')


    data = data.dropna(axis=0)
    return data
# Uptrend