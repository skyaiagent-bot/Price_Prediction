import pandas as pd 
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error ,mean_absolute_percentage_error
"""
we traing to predict price with Linear Regression
"""
def linear_regression(data_frame:pd.DataFrame,*features:str,target:str ):
    X = data_frame[features]
    y = data_frame[target]
    train_dataset = int(len(X)*0.8)
    X_train = X[:train_dataset]
    X_test = X[train_dataset:]
    y_train = y[:train_dataset]
    y_test = y[train_dataset:]
    mms = MinMaxScaler()
    X_train_scaled = mms.fit_transform(X_train)
    X_test_scaled = mms.fit_transform(X_test)
    lr = LinearRegression()
    lr.fit(X_train_scaled,y_train)
    y_prec = lr.predict(y_test)
    mae = mean_absolute_error(y_pred=y_prec,y_true=y_test)
    mape=mean_absolute_percentage_error(y_true=y_test,y_pred=y_prec)
    return y_prec,mae,mape


