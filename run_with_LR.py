from Reading_Price import read_data
from Feature_engineering import add_technical_indicators
from Data_Prepration import preprocess_data
from Linear_Regression import linear_regression


df = read_data(symbol='EURUSD=X',start="2010-01-01",interval='1d')
df = add_technical_indicators(df)
df = preprocess_data(df)

y_prec , mse , mspe = linear_regression(df,target='Close_next')
print(y_prec[-1])
print(mse)
print(mspe)

