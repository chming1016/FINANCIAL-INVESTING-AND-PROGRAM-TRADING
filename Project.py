# -*- coding: utf-8 -*-
"""
Created on Sat Dec 31 11:44:08 2016

@author: MING
"""
import pandas as pd
import matplotlib.pyplot as plt
def draw(input,input2):
    plt.plot(stock_data['Date'], stock_data[str(input2)],'b')
    plt.plot(stock_data['Date'], stock_data[str(input)],'r')
    plt.xlabel("Date") 
    plt.ylabel("Value") 
    plt.title(str(input)+str(input2))
    plt.show()
def dif(ma12, ma26): # dif function
    return ma12 - ma26
ma_list = [12, 26] # define ma days
stock_list = [2330, 2317, 2412, 1301, 1303, 1326, 2454, 2308, 2882, 2881] # define top10
stock_data = pd.read_csv('D://Log/raw_data.csv', parse_dates=[0]) # read data
stock_data = pd.DataFrame(stock_data, columns = ['Date','2330','2317','2412','1301','1303','1326','2454','2308','2882','2881'])
for i in range(len(stock_list)):
    # calculate ma
    for ma in ma_list:
        stock_data['MA' + str(ma) + '_' + str(stock_list[i])] = pd.rolling_mean(stock_data[str(stock_list[i])], ma)
    # calculate DIF
    res = dif(stock_data['MA' + str(ma_list[0]) + '_' +str(stock_list[i])], stock_data['MA' + str(ma_list[1]) + '_' +str(stock_list[i])])
    for j in range(len(stock_data.index)):
        stock_data = stock_data.set_value(j, 'DIF_' + str(stock_list[i]), str(res[j]))
    # calculate MACD
    stock_data['MACD_' + str(stock_list[i])] = pd.rolling_mean(stock_data['DIF_' + str(stock_list[i])], 9)
    # determine when to buy or sell
    for j in range(len(stock_data.index)):
        if(res[j] > stock_data['MACD_' + str(stock_list[i])][j]):
            stock_data = stock_data.set_value(j, 'new_' + str(stock_list[i]), 1)
        else:
            stock_data = stock_data.set_value(j, 'new_' + str(stock_list[i]), 0)
    for j in range(len(stock_data.index)):
        if(j+1 < len(stock_data.index)): # exclude last data
            if(stock_data['new_' + str(stock_list[i])][j] > stock_data['new_' + str(stock_list[i])][j+1]):
                # sell
                stock_data = stock_data.set_value(j, 'decision_' + str(stock_list[i]), 'sell')
            if(stock_data['new_' + str(stock_list[i])][j] < stock_data['new_' + str(stock_list[i])][j+1]):
                # buy
                stock_data = stock_data.set_value(j, 'decision_' + str(stock_list[i]), 'buy')
stock_data.sort_values('Date', ascending=True, inplace=True)
# output file
stock_data.to_csv('D://Log/output.csv', index=False)
#for i in range(len(stock_list)):
#    draw(stock_list[i])