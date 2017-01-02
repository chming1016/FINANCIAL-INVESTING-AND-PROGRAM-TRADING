# coding: utf-8
import numpy as np
import matplotlib.pyplot as plt
K = 9100
Premium_Call = 179
Premium_Put = 185
Interval = 500
ST = np.arange(K - Interval, K + Interval)  #模擬未來股價的價位
Payoff_LongPut = np.maximum(K - ST, 0) - Premium_Put
Payoff_ShortPut = -Payoff_LongPut
plt.plot(ST, Payoff_LongPut)
plt.plot(ST, Payoff_ShortPut)
plt.show()

