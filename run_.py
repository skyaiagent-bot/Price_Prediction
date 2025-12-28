from Reading_Price import read_data
from Feature_engineering import add_technical_indicators
from Data_Prepration import preprocess_data
from trend_recognetion import trend_finder,identify_entry_points
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns



df = read_data(symbol='EURUSD=X',start="2010-01-01",interval="1d")
df = add_technical_indicators(df)
df = preprocess_data(df)
df = trend_finder(df)
df = identify_entry_points(df)



plt.figure(figsize=(10, 8))  # تنظیم اندازه تصویر
sns.heatmap(df.drop(columns='Entry_type').corr(), annot=True, cmap="coolwarm")  # رسم نقشه حرارتی برای ماتریس همبستگی داده‌ها
plt.show()
