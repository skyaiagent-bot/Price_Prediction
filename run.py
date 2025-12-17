from Reading_Price import read_data
from Feature_engineering import add_technical_indicators
from Data_Prepration import preprocess_data
from Linear_Regression import linear_regression

df = read_data(symbol='EURUSD=X',start="2010-01-01",interval='1d')
df = add_technical_indicators(df)
df = preprocess_data(df)
# print(df.columns)
# ['Close','High','Low','Open','SMA_20','SMA_50','EMA_20','EMA_50','RSI_14']
x,y,z = linear_regression(df,'Close','High','Low','Open','SMA_20','SMA_50','EMA_20','EMA_50','RSI_14',
    target='Close_next')

print(x)