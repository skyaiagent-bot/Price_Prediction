import numpy as np
import pandas as pd

def trend_finder(df:pd.DataFrame,windows=3,candel_type_category=0):
    df["Candle_type"] = np.select(
        [ df['Close'] > df['Open'] , df['Close'] < df["Open"]],
        [1,-1],
        default=0
    )
    # candle body size
    df['Candle_size'] = abs(df['High'] - df['Low'])


    candle_type_category = []
    for i in range(len(df)):
    
        if df['Candle_size'].iloc[i] < df['ATR'].iloc[i] * 0.2:
            candle_type_category.append(0)
        elif df['ATR'].iloc[i] * 0.2 <= df['Candle_size'].iloc[i] < df['ATR'].iloc[i] * 0.4 :
            candle_type_category.append(1)
        elif df['ATR'].iloc[i] * 0.7 > df['Candle_size'].iloc[i] > df['ATR'].iloc[i] * 0.4 :
            candle_type_category.append(2)
        elif 0.9 > df['Candle_size'].iloc[i] >= df['ATR'].iloc[i] * 0.7 :
            candle_type_category.append(3)        
        elif  df['Candle_size'].iloc[i] >= df['ATR'].iloc[i] * 0.9 :
            candle_type_category.append(4)
    
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
    
    


# def identify_entry_points(df: pd.DataFrame): OLD VERSION
#     df['Entry_signal'] = None
#     df["Exit_signal"] = None
#     df['Entry_type'] = None
# 
#     for i in range(len(df)-1):  # تا ایندکس آخر منهای یک
#         if df['Candle_type'].iloc[i] == 1 and df['Candle_type_category'].iloc[i] >= 0:
#             df.loc[i, 'Entry_signal'] = 1
#             df.loc[i+1, "Exit_signal"] = 1
#             df.loc[i, 'Entry_type'] = 'Long'

#         elif df['Candle_type'].iloc[i] == -1 and df['Candle_type_category'].iloc[i] >= 0:
#             df.loc[i, 'Entry_signal'] = -1
#             df.loc[i+1, "Exit_signal"] = -1
#             df.loc[i, 'Entry_type'] = 'Short'
#         else:
#             df.loc[i, 'Entry_signal'] = 0
#             df.loc[i+1, "Exit_signal"] = 0
#             df.loc[i, 'Entry_type'] = 'Range'

#     return df
#


def identify_trend(df:pd.DataFrame):
    df['Candle_weight'] = df['Candle_type'] * df['Candle_type_category']
    df['Trend_Strength'] = None
    df['Movement_Trend'] = None
    df
    """
    short = -1
    range = 0
    Long = 1
    """
    for i in range(len(df)-3):
        x  = df['Candle_weight'].iloc[i:i+3].sum()

        df.loc[i,'Trend_Strength'] = x

        if df['Candle_weight'].iloc[i:i+3].sum() >= 2 :
         
            df.loc[i:i+3,'Movement_Trend' ] = 1

        elif df['Candle_weight'].iloc[i:i+3].sum() <= -2 :
        
            df.loc[i:i+3,'Movement_Trend' ] = -1
        
        else:
            
            df.loc[i:i+3,'Movement_Trend' ] = 0
           
    return df