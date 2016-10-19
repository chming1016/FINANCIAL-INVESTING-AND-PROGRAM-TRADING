# coding: utf-8
import numpy as np
import matplotlib.pyplot as plt
K = 9100
Premium_Call = 179
Premium_Put = 185
Interval = 500
ST = np.arange(K - Interval, K + Interval)  #模擬未來股價的價位
Payoff_LongCall = np.maximum(ST - K, 0) - Premium_Call
Payoff_ShortCall = -Payoff_LongCall
plt.plot(ST, Payoff_LongCall)
plt.plot(ST, Payoff_ShortCall)
plt.show()

