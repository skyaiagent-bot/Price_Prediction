from Reading_Price import read_data
from Feature_engineering import add_technical_indicators ,bullish_bearish
from Data_Prepration import preprocess_data
from candle_modifier import trend_finder,identify_trend
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from keras.datasets import mnist
import time



df_daily = read_data(symbol='EURUSD=X',start="2025-01-01",interval="1d")
df_daily = add_technical_indicators(df_daily)
df_daily = bullish_bearish(df_daily)

df_4h = read_data(symbol='EURUSD=X',start="2025-01-01",interval="4h")
df_4h = add_technical_indicators(df_4h)


df_1h = read_data(symbol='EURUSD=X',start="2025-01-01",interval="1h")
df_1h = add_technical_indicators(df_1h)

df_daily.index = df_daily.index.tz_localize(None)
df_4h.index = df_4h.index.tz_localize(None)
df_1h.index = df_1h.index.tz_localize(None)


df_daily.index = pd.to_datetime(df_daily.index)
df_4h.index = pd.to_datetime(df_4h.index)

# print(df_daily.columns)


df_4h['Daily_Bias'] = df_daily['Daily_Bias'].reindex(df_4h.index.floor('D'),method='ffill').values





long_pullback = (
    (df_4h['Daily_Bias'] == 'Bullish') &
    (df_4h['Close'].values.reshape(-1) < df_4h['EMA_20'].values.reshape(-1))
)

short_pullback = (
    (df_4h['Daily_Bias'] == 'Bearish') &
    (df_4h['Close'].values.reshape(-1) > df_4h['EMA_20'].values.reshape(-1))
)

df_4h['H4_Pullback'] = np.where(
    long_pullback, 'Long_Pullback',
    np.where(short_pullback, 'Short_Pullback', 'None')
)

df_4h['H4_Pullback'] = np.where(
    long_pullback, 'Long_Pullback',
    np.where(short_pullback, 'Short_Pullback', 'None')
)


df_1h['H4_Pullback'] = df_4h['H4_Pullback'].reindex(
    df_1h.index.floor('4h'),
    method='ffill'
).values

df_1h['Daily_Bias'] = df_daily['Daily_Bias'].reindex(
    df_1h.index.floor('D'),
    method='ffill'
).values







long_entry = (
    (df_1h['Daily_Bias'] == 'Bullish') &
    (df_1h['H4_Pullback'] == 'Long_Pullback') &
    (df_1h['Close'] > df_1h['High'].shift(1)) &
    (df_1h['EMA20_slope'] > 0)  &
    (df_1h['Body'] > df_1h['Body_avg'])
)


print(type(df_1h['Close']))

df_1h['Entry_Signal'] = np.where(long_entry, 'Long', 'None')

# print(len(df_4h))
# print(len(df_1h))
# print(df_1h[['Daily_Bias','H4_Pullback']].tail())

long_entry = (
    (df_1h['Daily_Bias'] == 'Bullish') &
    (df_1h['H4_Pullback'] == 'Long_Pullback') &
    (df_1h['Close'] > df_1h['High'].shift(1)) &
    (df_1h['EMA20_slope'] > 0) &
    (df_1h['Body'] > df_1h['Body_avg'])
)

df_1h['Entry_Signal'] = np.where(long_entry, 'Long', 'None')

# print(df_1h['Entry_Signal'].value_counts())

trades = df_1h[df_1h['Entry_Signal'] != 'None'].copy()



results = []
for idx in trades.index:
    direction = df_1h.loc[idx,'Entry_Signal']
    entry = df_1h.loc[idx,'Entry_Price']
    sl = df_1h.loc[idx,'SL']
    tp = df_1h.loc[idx,'TP']

    future_data = df_1h.loc[idx:].iloc[1:]
    outcome = None
    for i , row in future_data.iterrows():
        if direction == 'Long':
            if row['Low'] <= sl:
                outcome = -1
                break
            
            if row['High'] >= tp:
                outcome = 2 
                break
        
        if direction == 'Short':

            if row['High'] >= sl:
                outcome = -1
                break

            if row['Low'] <= tp:
                outcome = 2 
                break
    if outcome == None:
        outcome = 0
    
    results.append(outcome)


trades['Outcome_R'] = results