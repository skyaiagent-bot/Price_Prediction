import numpy as np
import pandas as pd

def trend_finder(df:pd.DataFrame,windows=3,candel_type_category=0):
    df["Candle_type"] = np.select(
        [ df['Close'] > df['Open'] , df['Close'] < df["Open"]],
        [1,-1],
        default=0
    )
    # candle body size
    df['Candle_body'] = abs(df['Close'] - df['Open'])


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
    


    
    
    trend = []

    for i in range(len(df)):
        if i < windows -1 :
            trend.append(0)
            continue

        windows_type = df['Candle_type'].iloc[i-windows+1:i+1]

        windows_size = df['Candle_type_category'].iloc[i-windows+1:i+1]

        if ( windows_type == 1 ).all() and ( windows_size > candel_type_category ).all():
            trend.append(1)
        
        elif ( windows_type == -1 ).all() and ( windows_size > candel_type_category ).all():
            trend.append(-1)
        
        else :
            trend.append(0)
        
    df['Trend'] = trend
    
    return df
    
    


def identify_entry_points(df: pd.DataFrame):
    df['Entry_signal'] = None
    df["Exit_signal"] = None
    df['Entry_type'] = None

    for i in range(len(df)-1):  # تا ایندکس آخر منهای یک
        if df['Candle_type'].iloc[i] == 1 and df['Candle_type_category'].iloc[i] >= 0:
            df.loc[i, 'Entry_signal'] = 1
            df.loc[i+1, "Exit_signal"] = 1
            df.loc[i, 'Entry_type'] = 'Long'

        elif df['Candle_type'].iloc[i] == -1 and df['Candle_type_category'].iloc[i] >= 0:
            df.loc[i, 'Entry_signal'] = -1
            df.loc[i+1, "Exit_signal"] = -1
            df.loc[i, 'Entry_type'] = 'Short'
        else:
            df.loc[i, 'Entry_signal'] = 0
            df.loc[i+1, "Exit_signal"] = 0
            df.loc[i, 'Entry_type'] = 'Range'

    return df
#
    