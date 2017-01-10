#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  8 18:53:48 2017

@author: ming
"""
import pandas as pd
import matplotlib.pyplot as plt
stock_data = pd.read_csv('./Y9999.csv', parse_dates = [0]) # read data
stock_data.sort_values('Date', ascending = True, inplace = True) # sort by date asc
stock_data.index.name = 'Date'
stock_data['Close'] = stock_data['Close'].str.replace(',', '')
stock_data['Close'] = stock_data['Close'].astype(float)
plt.plot(stock_data['Date'], stock_data['Close'])
stock_data2 = pd.read_csv('./output.csv', parse_dates = [0]) # read data
stock_data2.sort_values('Date', ascending = True, inplace = True) # sort by date asc
plt.plot(stock_data2['Date'], stock_data2['total']/1000)
plt.grid(True)
plt.xlabel('Years') 
plt.ylabel('Money') 
plt.title('Total')
plt.show()