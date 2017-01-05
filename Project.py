# -*- coding: utf-8 -*-
"""
Created on Sat Dec 31 11:44:08 2016
@author: MING
"""
import pandas as pd
import matplotlib.pyplot as plt
ma_list = [12, 26] # define ma days
stock_list = [2330, 2317, 2412, 1301, 1303, 1326, 2454, 2308, 2882, 2881] # define top10
stock_data = pd.read_csv('D://Log/raw_data.csv', parse_dates=[0]) # read data
money = []
for i in range(0,10): # initial money 
    money.append(10000)
def draw(input2): # draw function
    plt.plot(stock_data['Date'], stock_data[str(input2)],'r')
    plt.xlabel("Date") 
    plt.ylabel("Value") 
    plt.title(str(input2))
    plt.show()
def max_min(input2): # history max min function
    for i in range(len(input2)):
        max = -1
        min = 9999
        for j in range(len(stock_data.index)):
            if(stock_data[str(input2[i])][j] > max):
                max = stock_data[str(input2[i])][j]
            if(stock_data[str(stock_list[i])][j] < min):
                min = stock_data[str(input2[i])][j]
        #print(max, min)
def dif(ma12, ma26): # dif function
    return ma12 - ma26
def strategy(input2):
    stock_data = pd.read_csv('D://Log/output.csv', parse_dates=[0])
    text_file = open("D://Log/output.txt", "w")
    for i in range(len(input2)):
        buy = [] # buy list
        sell = [] # sell list
        lock = 0 # buy FIRST !!!
        AR = 0 # average return
        max = -1
        min = 9999
        count = 0 # win counter
        for j in range(len(stock_data.index)): # buy sell determine
            if(stock_data['signal_' + str(input2[i])][j]=='sell') and (lock == 1):
                stock_data = stock_data.set_value(j, 'real_' + str(stock_list[i]), 'sell')
                money[i] += stock_data[str(input2[i])][j]
                sell.append(stock_data[str(input2[i])][j])
            if(stock_data['signal_' + str(input2[i])][j]=='buy'):
                stock_data = stock_data.set_value(j, 'real_' + str(stock_list[i]), 'buy')
                money[i] -= stock_data[str(input2[i])][j]
                buy.append(stock_data[str(input2[i])][j])
                lock = 1
        if(len(sell) < len(buy)): # last day sell it
            sell.append(stock_data.at[len(stock_data.index)-1, str(input2[i])])
            stock_data = stock_data.set_value(len(stock_data.index)-1, 'real_' + str(input2[i]), 'sell')
        for j in range(len(sell)): # calculate each return
            AR += (sell[j]-buy[j])
            if(sell[j]-buy[j] > max):
                max = (sell[j]-buy[j])
            if(sell[j]-buy[j] < min):
                min = (sell[j]-buy[j])
            if(sell[j]-buy[j] > 0):
                count += 1
        text_file.write(str(input2[i])+'\tcount: '+str(len(buy))+'\tCR: '+str('{:.3f}'.format((money[i]-10000)/10000*100))+'\tAR: '+str('{:.2f}'.format(AR/len(buy)*100))+'%\tMaxR: '+str('{:.2f}'.format(max))+'%\tminR: '+str(min)+'%\twin: '+str('{:.2f}'.format(count/len(buy)*100)+'%\n'))
        #print(str(input2[i])+' count: '+str(len(buy))+' CR: '+str('{:.3f}'.format((money[i]-10000)/10000*100))+' AR: '+str('{:.2f}'.format(AR/len(buy)*100))+'% MaxR: '+str('{:.2f}'.format(max))+'% minR: '+str(min)+'% win: '+str('{:.2f}'.format(count/len(buy)*100)+'%'))
    text_file.close()
    stock_data.to_csv('D://Log/output3.csv', index=False)
stock_data.sort_values('Date', ascending=True, inplace=True)
for i in range(len(stock_list)):
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
                # sell signal
                stock_data = stock_data.set_value(j, 'signal_' + str(stock_list[i]), 'sell')
            if(stock_data['buff_' + str(stock_list[i])][j] < stock_data['buff_' + str(stock_list[i])][j+1]):
                # buy signal
                stock_data = stock_data.set_value(j, 'signal_' + str(stock_list[i]), 'buy')
#stock_data.sort_values('Date', ascending=True, inplace=True)
# output file
stock_data.to_csv('D://Log/output.csv', index=False)
#for i in range(len(stock_list)):
#    draw(stock_list[i], stock_list[i])
strategy(stock_list)
# history max min value
max_min(stock_list)
# draw picture
#for i in range(len(stock_list)):
#    draw(stock_list[i])