# -*- coding: utf-8 -*-
"""
Created on Sat Dec 31 11:44:08 2016

@author: MING
"""
import pandas as pd
stock_data = pd.read_csv('D://Log/test.csv', parse_dates=[0])
stock_data.sort_values(by='Date', inplace=False)
ma_list = [20]
for ma in ma_list:
    stock_data['MA' + str(ma)] = pd.rolling_mean(stock_data['Price'], ma)
stock_data.sort_values('Date', ascending=False, inplace=True)
stock_data.to_csv('D://Log/test_ma.csv', index=False)
stock_data2 = pd.read_csv('D://Log/test_ma.csv', parse_dates=[0])
for i in range(31):
    if(stock_data2.Price[i] > stock_data2.MA20[i]):
        print(stock_data2.Date[i])