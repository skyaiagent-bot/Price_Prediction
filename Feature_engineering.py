import pandas as pd
import numpy as np
import talib as ta

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
    data['ATR'] = ta.ATR(high=data['High'].values.reshape(-1),low=data['Low'].values.reshape(-1),close=data['Close'].values.reshape(-1),timeperiod=14) 
 
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
    data = data.dropna(axis=0)
    return data
