# -*- coding: utf-8 -*-
"""
Created on Sat Dec 31 11:44:08 2016
@author: MING
"""
import pandas as pd
import pandas.io.data as web
import matplotlib.pyplot as plt
import datetime
ma_list = [12, 26] # define ma days
stock_list = [2330, 2317, 2412, 1301, 1303, 1326, 2454, 2308, 2882, 2881] # define top10
def draw(input2): # draw function
    for i in range(len(input2)):
        plt.plot(stock_data['Date'], stock_data[str(input2[i])])
    plt.xlabel('Date') 
    plt.ylabel('Value') 
    plt.title(str(input2))
    plt.show()
def crawler(): # crawl yahoo source
    start = datetime.datetime(2011,11,16) # start time
    end = datetime.datetime(2017,1,1) # end time
    df1 = pd.DataFrame() # new dataframe
    for i in range(len(stock_list)):
        sid = str(stock_list[i]) + '.tw'
        df = web.DataReader(sid,'yahoo', start, end)
        df1[str(stock_list[i])] = df['Close']
    df1.to_csv('./raw.csv', cols = ['Date'])
def dif(ma12, ma26): # dif function
    return ma12 - ma26
#crawler()
stock_data = pd.read_csv('./raw.csv', parse_dates = [0]) # read data
stock_data.sort_values('Date', ascending = True, inplace = True) # sort by date asc
text_file = open('./output.txt', 'w')
for i in range(len(stock_list)):
    buy = [] # buy list
    sell = [] # sell list
    lock = 0 # buy FIRST !!!
    R = [] # return list initial
    CR = 1 # cumulative return initial
    max = -1 # initial max value
    min = 9999 # initial min value
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
            if(stock_data['buff_' + str(stock_list[i])][j] > stock_data['buff_' + str(stock_list[i])][j+1]) and (lock == 1):
                # sell signal
                stock_data = stock_data.set_value(j+1, 'signal_' + str(stock_list[i]), 'sell')
                sell.append(stock_data[str(stock_list[i])][j+1])
            if(stock_data['buff_' + str(stock_list[i])][j] < stock_data['buff_' + str(stock_list[i])][j+1]):
                # buy signal
                stock_data = stock_data.set_value(j+1, 'signal_' + str(stock_list[i]), 'buy')
                buy.append(stock_data[str(stock_list[i])][j+1])
                lock = 1
    if(len(sell) < len(buy)): # last day sell it
        sell.append(stock_data.at[len(stock_data.index)-1, str(stock_list[i])])
        stock_data = stock_data.set_value(len(stock_data.index)-1, 'signal_' + str(stock_list[i]), 'sell')
    for j in range(len(sell)): # calculate each return
        R.append((sell[j] - buy[j]) / buy[j])
        CR *= (1 + R[j])
        if(R[j] > max):
            max = R[j]
        if(R[j] < min):
            min = R[j]
        if(R[j] > 0):
            count += 1
    print(str(stock_list[i])+'\tcount: '+str(len(sell))+'\tCR: '+str('{:.3f}'.format((CR-1)*100))+'%\tAR: '+str('{:.4f}'.format(((CR**(1/len(sell)))-1)*100))+'%\tMaxR: '+str('{:.2f}'.format((max)*100))+'%\tminR: '+str('{:.2f}'.format((min)*100))+'%\twin: '+str('{:.2f}'.format(count/len(sell)*100)+'%\n'))
    text_file.write(str(stock_list[i]) + '\tcount: '+str(len(sell)) + '\tCR: '+str('{:.3f}'.format((CR-1)*100)) + '%\tAR: '+str('{:.4f}'.format(((CR**(1/len(sell)))-1)*100)) + '%\tMaxR: ' + str('{:.2f}'.format((max)*100)) + '%\tminR: ' + str('{:.2f}'.format((min)*100)) + '%\twin: ' + str('{:.2f}'.format(count/len(sell)*100) + '%\n'))
# output file
stock_data.to_csv('./output.csv', index=False)
text_file.close()
draw(stock_list)