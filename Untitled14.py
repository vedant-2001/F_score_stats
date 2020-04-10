#!/usr/bin/env python
# coding: utf-8

# In[72]:


import pandas as pd
import numpy as np
from pandas_datareader import data
import requests
from math import sqrt
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')
get_ipython().run_line_magic('matplotlib', 'inline')


# In[73]:


portfolio = 1e5 #Portfolio total worth of 1 lakh
tscost = 0.005 #Per trade transaction cost of 0.5%, so if two stocks of 30 each are bought, (1+0.005)*2*30 is charged in total
nstocks = 0

stock_list = ['BHEL.NS','ITC.NS','LUPIN.NS','RELIANCE.NS','IBVENTURES.NS'] #Stock list, to add a stock simply
                                                                           #add the ticker according to Yahoo! Finance
for stock in stock_list:
    nstocks+=1          #Calculates number of stocks according to input stock list


# In[74]:


def readData(ticker, n):
    stocks.append(data.DataReader(ticker, 'yahoo',start='1/1/2015')) #Taking backtesting period as roughly 5 years


# In[75]:


def BBands(df1):
    window = 25
    no_of_std = 2
    rolling_mean1 = df1['Adj Close'].rolling(window).mean()
    rolling_std1 = df1['Adj Close'].rolling(window).std()
    
    df1['Bollinger High'] = rolling_mean1 + (rolling_std1 * no_of_std)
    df1['Bollinger Mid'] = rolling_mean1
    df1['Bollinger Low'] = rolling_mean1 - (rolling_std1 * no_of_std)
    df1['Position'] = 0


# In[76]:


def RSI(df1):
    
    temp=df1['Adj Close'].diff()
    diff_values=temp[~np.isnan(temp)]
    o=df1['Open'].tolist()
    c=np.zeros(len(df1))
    df1['Position'] = 0
    
    
    a=diff_values.index.tolist()
    b=diff_values.tolist()
    c=np.zeros(len(df1))
   
    RSI=pd.DataFrame()

    count=0
    for count in range(0,len(df1)-13):
        
        Total_loss=0
        Total_gain=0
        for i in range(count,count+13):
            if(b[i]>0):
                Total_gain+=b[i]
                #print('Gain ',Total_gain)
            
            elif(b[i]<0):
                Total_loss-=b[i]
                
            if(Total_loss!=0):
                RS=Total_gain/Total_loss
                
                
            
        RSI_Val=100-(100/(1+RS))
        
        c[count+13]=RSI_Val
        
    
    df1['RSI']=c


# In[77]:


def Strategy(df1):
    for row in range(len(df1)):
        if df1['Position'].iloc[row -1] == 1 :
            if df1['Low'].iloc[row] <= df1['Bollinger Low'].iloc[row] and df1['RSI'].iloc[row] > 30 :
                df1['Position'].iloc[row] = 1
            else :
                df1['Position'].iloc[row] = 0
                
                
                
            if df1['High'].iloc[row] >= df1['Bollinger High'].iloc[row] and df1['RSI'].iloc[row > 70] :
                df1['Position'].iloc[row] = -1
            else :
                df1['Position'].iloc[row] = 0
                
                
        elif df1['Position'].iloc[row-1] == 0:
            
            if df1['Low'].iloc[row] <= df1['Bollinger Low'].iloc[row] and df1['RSI'].iloc[row] < 30 :
                df1['Position'].iloc[row] = 1
            else :
                 df1['Position'].iloc[row] = 0
                
                
            if df1['High'].iloc[row] >= df1['Bollinger High'].iloc[row] and df1['RSI'].iloc[row] < 70 :
                df1['Position'].iloc[row] = -1
            else :
                 df1['Position'].iloc[row] = 0
                


# In[78]:



#Iterating over all the tickers to read data, generate Bollinger Bands and formulate portfolio positions based on strategy
i = 0
stocks = []
for ticker in stock_list:
    readData(ticker,i)
    RSI(stocks[i])
    BBands(stocks[i])
    Strategy(stocks[i])
    i+=1


# In[79]:


s = (len(stocks[0]),nstocks) #setting the dimensions of the weights vector depending on the available data points
weights = np.zeros(s) 
sumwts = 0

for row in range(len(stocks[0])):
    i = 0
    for i in range(nstocks):
        sumwts+=np.abs(stocks[i]['Position'].iloc[row]) #checking how many positions were taken on that day
    for i in range(nstocks):
        if sumwts>0:
            #weights assigned as:
            #weights = (portfolio*position)/(no.of positions * adj close on that day * (1+transac cost))
            weights[row][i]=(portfolio*stocks[i]['Position'].iloc[row])/((sumwts*stocks[i]['Adj Close'].iloc[row])*(1+tscost))
        else:
            weights[row][i]=0
i = 0


for i in range(nstocks):
    stocks[i]['Market Return'] = (stocks[i]['Adj Close'] - stocks[i]['Adj Close'].shift(1)) #Absolute market return

    
#Calculating portfolio return
stocks[0]['Strategy Return']=0
i = 0
for i in range(nstocks):
    stocks[0]['Strategy Return']+=stocks[i]['Market Return'] * weights[:,i] #multiplying market return of each
                                                                            #ticker with its weight
stocks[0]['Strategy Return'][64:].cumsum().plot() #Plotting strategy return

