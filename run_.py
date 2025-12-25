from Reading_Price import read_data
from Feature_engineering import add_technical_indicators
from Data_Prepration import preprocess_data
from trend_recognetion import trend_finder



df = read_data(symbol='EURUSD=X',start="2010-01-01",interval="1d")
df = add_technical_indicators(df)
df = preprocess_data(df)
df = trend_finder(df)


print(df[['Candle_type','Candle_type_category','Trend']].head(50))






