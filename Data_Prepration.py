import numpy as np
import pandas as pd

def preprocess_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    i want to predict close price for the next candle based on previous candles
    so we are going to shift close price by -1 to create the target variable
    """
    data = data.copy()
    data['Close_next'] = data['Close'].shift(-1)
    data = data.dropna().reset_index(drop=True)
    return data

