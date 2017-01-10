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
money = [] # initial money 1000000 for each stocks
for i in range(len(stock_list)):
    money.append(100000)
def draw(): # draw function
    plt.plot(stock_data['Date'], stock_data['total'])
    plt.grid(True)
    plt.xlabel('Years') 
    plt.ylabel('Money') 
    plt.title('Total')
    plt.savefig('total.png')
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
crawler() #crawl data first
stock_data = pd.read_csv('./raw.csv', parse_dates = [0]) # read data
stock_data.sort_values('Date', ascending = True, inplace = True) # sort by date asc
text_file = open('./result.txt', 'w')
# strategy
for i in range(len(stock_list)):
    buy = [] # buy list
    sell = [] # sell list
    lock = 0 # buy FIRST !!!
    R = [] # return list initial
    AR = 0 # average return initial
    max = -1 # initial max value
    min = 9999 # initial min value
    count = 0 # win counter
    nCR = 0 # n R of cumulative return
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
        # money remain
        stock_data.set_value(j, 'money_' + str(stock_list[i]), money[i])
        if(j+1 < len(stock_data.index)): # exclude last data
            if(stock_data['buff_' + str(stock_list[i])][j] > stock_data['buff_' + str(stock_list[i])][j+1]) and (lock == 1):
                # sell signal
                stock_data = stock_data.set_value(j+1, 'signal_' + str(stock_list[i]), 'sell')
                money[i] += ((stock_data[str(stock_list[i])][j+1])*1000) # total money remain
                sell.append((stock_data[str(stock_list[i])][j+1])*1000) # each sell value
            if(stock_data['buff_' + str(stock_list[i])][j] < stock_data['buff_' + str(stock_list[i])][j+1]):
                # buy signal
                stock_data = stock_data.set_value(j+1, 'signal_' + str(stock_list[i]), 'buy')
                money[i] -= ((stock_data[str(stock_list[i])][j+1])*1000) # total money remain
                buy.append((stock_data[str(stock_list[i])][j+1])*1000) # each buy value
                lock = 1 # buy first then you can sell
            # account each R value
            nR = (money[i]-100000)/100000
            if(len(sell) == len(buy)) and (len(sell)!=0):
                stock_data = stock_data.set_value(j+1, 'nR_' + str(stock_list[i]), nR)
            # account each stock value at that day
            stock_data = stock_data.set_value(j+1, 'value' + str(stock_list[i]), stock_data[str(stock_list[i])][j+1]*1000)
    # account each CR at each sell
    for j in range(len(stock_data.index)):
        if(stock_data['signal_' + str(stock_list[i])][j]=='sell'):
            nCR += stock_data['nR_' + str(stock_list[i])][j]
            stock_data = stock_data.set_value(j, 'nCR_' + str(stock_list[i]), nCR)
    if(len(sell) < len(buy)): # last day sell it
        sell.append(stock_data.at[len(stock_data.index)-1, str(stock_list[i])])
        stock_data = stock_data.set_value(len(stock_data.index)-1, 'signal_' + str(stock_list[i]), 'sell')
    for j in range(len(sell)): # calculate each return
        R.append((sell[j] - buy[j]) / buy[j]) # account R
        AR += R[j] # acount AR
        if(R[j] > max): # account max R
            max = R[j]
        if(R[j] < min): # account min R
            min = R[j]
        if(R[j] > 0): # account win time
            count += 1         
    #print(str(stock_list[i])+'\tcount: '+str(len(sell))+'\tCR: '+str('{:.3f}'.format(((money[i]-1000000)/1000000)*100))+'%\tAR: '+str('{:.4f}'.format(((AR/len(sell))*100)))+'%\tMaxR: '+str('{:.2f}'.format((max)*100))+'%\tminR: '+str('{:.2f}'.format((min)*100))+'%\twin: '+str('{:.2f}'.format(count/len(sell)*100)+'%\n'))
    text_file.write(str(stock_list[i])+'\tcount: '+str(len(sell))+'\tCR: '+str('{:.3f}'.format(((money[i]-100000)/100000)*100))+'%\tAR: '+str('{:.4f}'.format(((AR/len(sell))*100)))+'%\tMaxR: '+str('{:.2f}'.format((max)*100))+'%\tminR: '+str('{:.2f}'.format((min)*100))+'%\twin: '+str('{:.2f}'.format(count/len(sell)*100)+'%\n'))
# account total value for each day
for j in range(len(stock_data.index)):
    total = 0
    for k in range(len(stock_list)):
        total += stock_data.get_value(j, 'money_' + str(stock_list[k]))
    stock_data = stock_data.set_value(j, 'total' , total)
# output file
stock_data.to_csv('./output.csv', index=False)
text_file.close()
draw()