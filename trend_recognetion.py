import numpy as np
import pandas as pd

def trend_finder(df:pd.DataFrame,windows=3,candel_type_category=[0,1,2]):
    df["Candle_type"] = np.select(
        [df['Close']>df['Open'],df['Close']<df["Open"]],
        [1,-1],
        default=0
    )
    # candle body size
    df['Candle_body'] = abs(df['Close'] - df['Open'])
    df['Candle_size'] = df['Candle_body']/df['Candle_body'].max()
    
    
    trend = []

    for i in range(len(df)):
        if i < windows -1 :
            trend.append(0)
            continue

        windows_type = df['Candle_type'].iloc[i-windows+1:i+1]

        windows_size = df['Candle_size'].iloc[i-windows+1:i+1]

        if ( windows_type == 1 ).all() and ( windows_size > threshold ).all():
            trend.append(1)
        elif ( windows_type == -1 ).all() and ( windows_size > threshold ).all():
            trend.append(-1)
        
        else :
            trend.append(0)
        
    df['Trend'] = trend
    return df
    
    

def Candel_type_cat(df:pd.DataFrame):

    candle_type_category = []
    for i in range(len(df)):
    
        if df['Candle_body'].iloc[i] < df['ATR'].iloc[i] * 0.3:
            candle_type_category.append(-1)
        elif df['ATR'].iloc[i] * 0.3 <= df['Candle_body'].iloc[i] < df['ATR'].iloc[i] * 0.7 :
            candle_type_category.append(0)
        elif df['ATR'].iloc[i] * 1.0 > df['Candle_body'].iloc[i] >= df['ATR'].iloc[i] * 0.7 :
            candle_type_category.append(1)
        elif df['Candle_body'].iloc[i] >= df['ATR'].iloc[i] * 1.0 :
            candle_type_category.append(2)
    
    df['Candle_type_category'] = candle_type_category

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
                    df.loc[df.index[i], 'Entry_signal'] = -1
                    df.loc[df.index[i], 'Entry_type'] = 'short'

    
    return df


def identify_exit_point(df:pd.DataFrame,trend_confrimation=1,exit_after_confrimation = 0):
    for i in range(len(df)):
        pass

    pass
    