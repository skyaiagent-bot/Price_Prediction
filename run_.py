from Reading_Price import read_data
from Feature_engineering import add_technical_indicators
from Data_Prepration import preprocess_data
from candle_modifier import trend_finder,identify_trend
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from keras.datasets import mnist


df_daily = read_data(symbol='EURUSD=X',start="2015-01-01",interval="1d")
df_daily = add_technical_indicators(df_daily)


df_4h = read_data(symbol='EURUSD=X',start="2025-01-01",interval="4h")
df_4h = add_technical_indicators(df_4h)


df_1h = read_data(symbol='EURUSD=X',start="2025-01-01",interval="1h")
df_1h = add_technical_indicators(df_1h)


print(df_4h.head(2))
print('---------'*10)
print(df_daily.head(2))
print('---------'*10)
print(df_1h.head(2))