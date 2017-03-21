# -*- coding: utf-8 -*-
"""
Created on Wed Mar 08 19:18:59 2017
@author: Chella Ram
"""

import pandas as pd 
#from matplotlib import pyplot as plt
#from scipy.cluster.hierarchy import dendrogram, linkage
#import numpy as np
from scipy.cluster.hierarchy import cophenet,linkage
from scipy.spatial.distance import pdist

scrip = 'ko'
data = pd.read_csv( scrip + '.csv',index_col = 0)

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




def recursor(ind,df_Z):
    
    members = []
    diff = len(df_Z)
    diff_1 = diff+1
    def helper(data):
        
        if int(data[0]) > diff and int(data[1]) > diff:
            helper(df_Z.loc[data[0]-diff_1])
            helper(df_Z.loc[data[1]-diff_1])
            
        elif int(data[0]) > diff and int(data[1]) < diff_1:
            helper(df_Z.loc[data[0]-diff_1])
            members.append(data[1])
            return
    
        elif int(data[0]) < diff_1 and int(data[1]) > diff:
            members.append(data[0])
            helper(df_Z.loc[data[1]-diff_1])
            return
            
        else:
            members.append(data[0])
            members.append(data[1])
            return
    
    helper(df_Z.loc[ind])
    return members
    
    
dfZ = pd.DataFrame(Z)
min_cluster_size = 29
max_cluster_size = 100


idx_list = dfZ[(dfZ[3]>min_cluster_size ) & (dfZ[3]<max_cluster_size)].index.values
clust_members_list = []


for idx in idx_list:
    clust_members_list.append(recursor(int(idx),dfZ))

    
clust_members_list = [[int(j) for j in i] for i in clust_members_list]

p = clust_members_list
kill = set()


for i,a in enumerate(p):
    for j,b in enumerate(p):
        if i!=j:
            if set(a).intersection(b):
                if len(a)<len(b):
                    kill.add(j)
                else:
                    kill.add(i)

                    
idx_range = set(range(0,len(idx_list)))
clust_indices = list(idx_range - kill)

clusters = [clust_members_list[i] for i in clust_indices]

for i,cluster in enumerate(clusters):
    trend_df = data.iloc[cluster,:].groupby('Trend').count().loc[[-1,0,1]]['Open']
    trend = float(trend_df.max())/float(trend_df.sum())
    which = trend_df.idxmax()
    print trend,which,len(cluster)

#No apparent pattern was discovered (only 1). Maybe more data can help. Get forex data.

