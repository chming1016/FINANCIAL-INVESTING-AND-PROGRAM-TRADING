# -*- coding: utf-8 -*-
"""
Created on Sat Dec 31 11:44:08 2016

@author: MING
"""
import pandas as pd
stock_list = [2330, 2317, 2412, 1301, 1303, 1326, 2454, 2308, 2882, 2881]
stock_data = pd.read_csv('D://Log/raw_data.csv', parse_dates=[0])
stock_data = pd.DataFrame(stock_data, columns = ['Date','2330','2317','2412','1301','1303','1326','2454','2308','2882','2881'])
stock_data.sort_values(by='Date', inplace=False)
for i in range(len(stock_list)):
    stock_data['MA20_' + str(stock_list[i])] = pd.rolling_mean(stock_data[str(stock_list[i])], 20)
stock_data.sort_values('Date', ascending=True, inplace=True)
stock_data.to_csv('D://Log/ma_data.csv', index=False)
ma_data = pd.read_csv('D://Log/ma_data.csv', parse_dates=[0])
for i in range(len(stock_list)):
    for j in range(len(ma_data.index)):
        if(ma_data[str(stock_list[i])][j] > ma_data['MA20_'+str(stock_list[i])][j]):
            ma_data = ma_data.set_value(j, 'new_'+str(stock_list[i]), 'V')
ma_data.to_csv('D://Log/ma_data.csv', index=False)