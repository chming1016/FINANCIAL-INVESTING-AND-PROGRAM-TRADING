# -*- coding: utf-8 -*-
"""
Created on Sat Dec 31 11:44:08 2016
@author: MING
"""
import pandas as pd
ma_list = [12, 26] # define ma days
stock_list = [2330, 2317, 2412, 1301, 1303, 1326, 2454, 2308, 2882, 2881] # define top10
money = []
for i in range(0,10): # initial money 
    money.append(10000)
def dif(ma12, ma26): # dif function
    return ma12 - ma26
stock_data = pd.read_csv('D://Log/raw_data.csv', parse_dates=[0]) # read data
stock_data.sort_values('Date', ascending=True, inplace=True)
text_file = open("D://Log/test_output.txt", "w")
for i in range(len(stock_list)):
    buy = [] # buy list
    sell = [] # sell list
    lock = 0 # buy FIRST !!!
    AR = 0 # average return
    max = -1
    min = 9999
    count = 0 # win counter
    # calculate ma
    for ma in ma_list:
        stock_data['MA' + str(ma) + '_' + str(stock_list[i])] = pd.rolling_mean(stock_data[str(stock_list[i])], ma)
    # calculate DIF
    res = dif(stock_data['MA' + str(ma_list[0]) + '_' +str(stock_list[i])], stock_data['MA' + str(ma_list[1]) + '_' +str(stock_list[i])])
    for j in range(len(stock_data.index)):
        stock_data = stock_data.set_value(j, 'DIF_' + str(stock_list[i]), str(res[j]))
    # calculate MACD
    for j in range(len(stock_data.index)):
        stock_data['MACD_' + str(stock_list[i])] = pd.rolling_mean(stock_data['DIF_' + str(stock_list[i])], 9)
    # determine when to buy or sell
    for j in range(len(stock_data.index)):
        if(res[j] > stock_data['MACD_' + str(stock_list[i])][j]):
            stock_data = stock_data.set_value(j, 'buff_' + str(stock_list[i]), 1)
        else:
            stock_data = stock_data.set_value(j, 'buff_' + str(stock_list[i]), 0)
    for j in range(len(stock_data.index)):
        if(j+1 < len(stock_data.index)): # exclude last data
            if(stock_data['buff_' + str(stock_list[i])][j] > stock_data['buff_' + str(stock_list[i])][j+1]):
                # buy signal
                stock_data = stock_data.set_value(j, 'signal_' + str(stock_list[i]), 'buy')
                money[i] -= stock_data[str(stock_list[i])][j]
                buy.append(stock_data[str(stock_list[i])][j])
            if(stock_data['buff_' + str(stock_list[i])][j] < stock_data['buff_' + str(stock_list[i])][j+1]):
                # sell signal
                stock_data = stock_data.set_value(j, 'signal_' + str(stock_list[i]), 'sell')
                money[i] += stock_data[str(stock_list[i])][j]
                sell.append(stock_data[str(stock_list[i])][j])
    if(len(sell) < len(buy)): # last day sell it
        sell.append(stock_data.at[len(stock_data.index)-1, str(stock_list[i])])
    for j in range(len(sell)): # calculate each return
        AR += (sell[j]-buy[j])
        if(sell[j]-buy[j] > max):
            max = (sell[j]-buy[j])
        if(sell[j]-buy[j] < min):
            min = (sell[j]-buy[j])
        if(sell[j]-buy[j] > 0):
            count += 1
    text_file.write(str(stock_list[i])+'\tcount: '+str(len(buy))+'\tCR: '+str('{:.3f}'.format((money[i]-10000)/10000*100))+'\tAR: '+str('{:.2f}'.format(AR/len(buy)*100))+'%\tMaxR: '+str('{:.2f}'.format(max))+'%\tminR: '+str(min)+'%\twin: '+str('{:.2f}'.format(count/len(buy)*100)+'%\n'))
# output file
stock_data.to_csv('D://Log/test_output.csv', index=False)
text_file.close()