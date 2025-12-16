from Reading_Price import read_data
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
    # Moving Averages
    data['SMA_20'] = ta.SMA(data['Close'], timeperiod=20)
    data['SMA_50'] = ta.SMA(data['Close'], timeperiod=50)
    data['EMA_20'] = ta.EMA(data['Close'], timeperiod=20)
    data['EMA_50'] = ta.EMA(data['Close'], timeperiod=50)

    # Relative Strength Index (RSI)
    data['RSI_14'] = ta.RSI(data['Close'], timeperiod=14)

    # Bollinger Bands
    upperband, middleband, lowerband = ta.BBANDS(data['Close'], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    data['BB_upper'] = upperband
    data['BB_middle'] = middleband
    data['BB_lower'] = lowerband

    # MACD
    macd, macdsignal, macdhist = ta.MACD(data['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
    data['MACD'] = macd
    data['MACD_signal'] = macdsignal
    data['MACD_hist'] = macdhist

    return data