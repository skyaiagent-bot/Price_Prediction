import numpy as np
import pandas as pd

def trend_finder(df:pd.DataFrame,windows=3,threshold=0.02):
    df["Candle_type"] = np.select(
        [df['Close']>df['Open'],df['Close']<df["Open"]],
        [1,-1],
        default=0
    )
    # candle body size
    df['Candle_body'] = abs(df['Close'] - df['Open'])
    df['Candle_size'] = df['Candle_body']/df['Candle_body'].median()
    trend = []

    for i in range(len(df)):
        if i < windows -1 :
            trend.append(0)
            continue

        windows_type = df['Candle_type'].iloc[i-windows+1:i+1]
        windows_size = df['Candle_size'].iloc[i-windows+1:i+1]

        if (windows_type == 1).all() and (windows_size > threshold).all():
            trend.append(1)
        elif (windows_type == -1).all() and (windows_size > threshold ).all():
            trend.append(-1)
        
        else :
            trend.append(0)
    
    
    df['Trend'] = trend
    
    
    return df

def identify_entry_points(df:pd.DataFrame,trend_confirmation=1,entry_after_confirmation=0):

    df['Entry_signal'] = 0
    df['Entry_type'] = None

    for i in range(len(df)):
        if df['Trend'].iloc[i] == 1:
            if i >= trend_confirmation + entry_after_confirmation:
                if(df['Trend'].iloc[i-trend_confirmation+1:i+1]==1).all():
                    df.loc[df.index[i],'Entry_signal'] = 1
                    df.loc[df.index[i],'Entry_type'] = 'long'
        
        elif df['Trend'].iloc[i] == -1:  # روند نزولی
            if i >= trend_confirmation + entry_after_confirmation:
                if (df['Trend'].iloc[i-trend_confirmation+1:i+1] == -1).all():
                    df.loc[df.index[i], 'Entry_signal'] = 1
                    df.loc[df.index[i], 'Entry_type'] = 'short'

    
    return df