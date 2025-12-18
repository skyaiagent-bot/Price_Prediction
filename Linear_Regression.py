import pandas as pd 
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error

def linear_regression(data_frame: pd.DataFrame, target: str):
    try:
        # تقسیم داده‌ها به ویژگی‌ها (X) و هدف (y)
        X = data_frame.drop(columns=target)
        y = data_frame[target]
        
        # تقسیم داده‌ها به مجموعه‌های آموزشی و آزمایشی
        train_dataset = int(len(X) * 0.8)
        X_train = X[:train_dataset]
        X_test = X[train_dataset:]
        y_train = y[:train_dataset]
        y_test = y[train_dataset:]
        
    except Exception as e:
        print(f"Error: {e}")
        return None, None, None
    
    # مقیاس‌بندی ویژگی‌ها با MinMaxScaler
    mms = MinMaxScaler()
    X_train_scaled = mms.fit_transform(X_train)
    X_test_scaled = mms.transform(X_test)  # استفاده از transform به جای fit_transform برای داده‌های تست

    # مدل رگرسیون خطی
    lr = LinearRegression()
    lr.fit(X_train_scaled, y_train)
    
    # پیش‌بینی و محاسبه خطاها
    y_prec = lr.predict(X_test_scaled)
    mae = mean_absolute_error(y_true=y_test, y_pred=y_prec)
    mape = mean_absolute_percentage_error(y_true=y_test, y_pred=y_prec)
    
    return y_prec, mae, mape

