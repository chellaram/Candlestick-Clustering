# -*- coding: utf-8 -*-
"""
Created on Wed Mar 08 19:18:59 2017

@author: Chella Ram
"""

import pandas as pd 
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
import numpy as np
from scipy.cluster.hierarchy import cophenet
from scipy.spatial.distance import pdist

data = pd.read_csv('C:\Users\chellar\Downloads\Candlestick-Clustering-master\infy.csv',index_col = 0)

# PRE-PROCESSING

### (Ht,Lt,Ct) = (H/O,L/O,C/O)
data['High'] = data['High']/data['Open']
data['Low'] = data['Low']/data['Open']
data['Close'] = data['Close']/data['Open']

### Midpoint Mt
data['Mid'] = (data['High'] - data['Low'])/2 + data['Low']
data = data.iloc[::-1]


data['Delta_1'] = (data['Mid'] - data['Mid'].shift(1))/data['Mid'].shift(1)
data['Delta_2'] = data['Delta_1'].shift(1)
#data['Delta_2'] = (data['Mid'] - data['Mid'].shift(2))/data['Mid'].shift(2)

data['High_2'] = data['High'].shift(2)
data['Low_2'] = data['Low'].shift(2)
data['Close_2'] = data['Close'].shift(2)

data['High_1'] = data['High'].shift(1)
data['Low_1'] = data['Low'].shift(1)
data['Close_1'] = data['Close'].shift(1)

data['MA_4'] = data['Close'].rolling(window=4).mean()
data['MA_3'] = data['Close'].rolling(window=3).mean()
data['MA_2'] = data['Close'].rolling(window=2).mean()
data.dropna(inplace = True)

data['Trend'] = 0
data.loc[((data['MA_4'] < data['MA_3']) & (data['MA_3'] < data['MA_2'])) , 'Trend'] = 1
data.loc[(data['MA_4'] > data['MA_3']) & (data['MA_3'] > data['MA_2']) , 'Trend'] = -1



e_T = data[['High_2','Low_2','Close_2','High_1','Low_1','Close_1','High','Low','Close','Delta_2','Delta_1']]
e_T.to_csv('C:\Users\Chella Rm\Documents\GitHub\Candlestick-Clustering\e_T.csv')


Z = linkage(e_T)
c, coph_dists = cophenet(Z, pdist(e_T))
print c





def recursor(idx,data):
    
    if int(data[0]) > 5303 and int(data[1]) > 5303:
        recursor(data[0]-5304,df_Z.loc[data[0]-5304])
        recursor(data[1]-5304,df_Z.loc[data[1]-5304])
        
    elif int(data[0]) > 5303 and int(data[1]) < 5304:
        recursor(data[0]-5304,df_Z.loc[data[0]-5304])
        print data[1]
        return

    elif int(data[0]) < 5304 and int(data[1]) > 5303:
        print data[0]
        recursor(data[1]-5304,df_Z.loc[data[1]-5304])
        return
        
    else:
        print data[0]
        print data[1]
        return

