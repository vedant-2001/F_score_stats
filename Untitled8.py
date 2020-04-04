#!/usr/bin/env python
# coding: utf-8

# In[300]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[301]:


import datetime


# In[302]:


import pandas_datareader as web


# In[303]:


start = datetime.datetime(2017,1,1)
end = datetime.datetime(2019,12,18)


# In[304]:


aapl = web.DataReader('AAPL','yahoo',start,end)


# In[305]:


aapl.head()


# In[306]:


aapl['Adj Open'] = aapl['Open'] * aapl['Adj Close']/aapl['Close']
aapl['Adj High'] = aapl['High'] * aapl['Adj Close']/aapl['Close']
aapl['Adj Low'] = aapl['Low'] * aapl['Adj Close']/aapl['Close']


# In[307]:


aapl['positive_dm']=0
aapl['negative_dm']=0 
aapl['true_range'] =0
aapl['positive_direction']=0 
aapl['negative_direction']=0
aapl['DX']=0
aapl['ADX']=0
aapl['trend']=0
aapl['']


# In[ ]:


def get_true_range(aapl):
    for row in range(2,len(aapl)):

        aapl['value_1'].iloc[row]  = aapl[' High'].iloc[row] - aapl['Low'].iloc[row]
        aapl['value_2'].iloc[row] = aapl[' Low'].iloc[row] - aapl['Low'].iloc[row-1]
        aapl['value_3'].iloc[row] = aapl['High'].iloc[row] - aapl['Low'].iloc[row]
        aapl['true_range'].iloc[row] =max(aapl['value_1'].iloc[row],aapl['value_2'].iloc[row],aapl['value_3'].iloc[row])
    


# In[ ]:


aapl.tail()


# In[ ]:


def positive_signal_generation(aapl):
    for row in range(2,len(aapl)):
        if aapl['High'].iloc[row] - aapl['High'].iloc[row - 1] > aapl['Low'].iloc[row - 1] - aapl['Low'].iloc[row]:
            aapl['positive_dm'].iloc[row] = aapl['High'].iloc[row] - aapl['High'].iloc[row - 1]
        
        else :
            aapl['positive_dm'].iloc[row] = 0
            
                
         
            


# In[ ]:



aapl.head()


# In[ ]:


def negative_signal_generation(aapl):
    for row in (2,len(aapl)):
        if aapl['Low'].iloc[row -1] - aapl['Low'].iloc[row] > aapl['High'].iloc[row] - aapl['High'].iloc[row -1]:
            aapl['negative_dm'].iloc[row] = aapl['Low'].iloc[row-1] - aapl['Low'].iloc[row]
        else :
            aapl['negative_dm'].iloc[row] = 0


# In[ ]:


def positive_index(aapl):
    for rows in range(2,len(aapl)):
        aapl['positive_direction'].iloc[row] = (aapl['positive_dm'].iloc[row] / aapl['true_range'].iloc[row])*100
        


# In[ ]:


aapl['positive_direction']


# In[ ]:


def negative_index(aapl):
    for rows in range(2,len(aapl)):
        aapl['negative_direction'].iloc[row] = (aapl['negative_dm'].iloc[row]) *100 / aapl['true_range'].iloc[row]


# In[ ]:


aapl['negative_direction']


# In[ ]:


def create_dx(aapl):
    for rows in range(2,len(aapl)):
        aapl['DX'].iloc[row] = (aapl['positive_dm'].iloc[row] - aapl['negative_dm'].iloc[row])*100 / aapl['positive_dm'].iloc[row] + aapl['negative_dm'].iloc[row]
        


# In[ ]:


aapl['AMX'] = aapl['DX'].rolling(len(aapl)).mean()


# In[ ]:


aapl.head()


# In[ ]:


aapl['trend'] = np.where(aapl['AMX']>25,1,0)
    


# In[ ]:


aapl['trend'].plot(figsize = (6,2),label ='TRADING STRATEGY')


# In[309]:


#now we will calculate the return we'll get on this strategy
aapl['Direction'] = np.where(aapl['positive_direction'] >aapl['negative_direction'],1,-1) * aapl['trend']


# In[311]:


aapl['daily_returns'] = aapl['Adj Close'].pct_change(1)


# In[318]:


aapl['Strategy Returns'] = aapl['Direction']* aapl['daily_returns']


# In[321]:


(aapl['Strategy Returns'] +1).cumprod().plot()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


aapl['daily_returns'] = aapl['Adj Close'].pct_change()


# In[ ]:





# In[ ]:




