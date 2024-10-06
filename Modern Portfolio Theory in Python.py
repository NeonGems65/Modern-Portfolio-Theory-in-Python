#!/usr/bin/env python
# coding: utf-8

# # Importing Libraries

# In[1]:


import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# # Downloading Financial Data

# In[2]:


stocks = [
  "XLY", "VCR", "CMG", "CZR", "SONY", "TM", "TSLA",
  "XLF", "VFH", "BLK", "GS", "ICE", "LAZ", "MS", "OPY", "PYPL", "UBS",
  "VHT", "XLV", "HBIO", "ILMN", "IQV", "MCK", "REGN",
  "AIQ", "SMH", "VGT", "AMD", "ASML", "CRM", "INTU", "MSFT", "NOW", "NVDA", "PLTR", "SNOW", "ARM",
  "QQQ", "SCHD", "VYM", "VIG"]

# stocks = ["HDFCBANK.NS", "ICICIBANK.NS", "AXISBANK.NS", "SBIN.NS"]

#Any random number of stocks can be added or dropped(Make sure to also edit portfoliostd function accordingly)

stocks = yf.download(stocks, start = "2009-01-01", end = "2024-10-02")
#Start and End time can be configured


# # Creating Log Return Data Frame

# In[3]:


#Creating a data frame with the log returns
stocks_lr = np.log(1+stocks["Adj Close"].pct_change())
stocks_lr.dropna()


# # Creating Function to Calculate Portfolio Return
# 
# ## Portfolio Return is given by: 
# ### (Asset 1 Weight x Expected Return) + (Asset 2 Weight x Expected Return)..
# 

# In[4]:


#Function to calculate portfolio return
def portfolioreturn(weights):
    return np.dot(stocks_lr.mean(),weights)*252


# # Function to Calculate Portfolio Standard Deviation (Risk)
# ## Portfolio Risk is given by(example for 3 asset portfolio):
# ![Portfolio-Standard-Deviation-Formula-1.png](attachment:Portfolio-Standard-Deviation-Formula-1.png)

# In[5]:


def portfoliostd(weights):
    return (np.dot(np.dot(stocks_lr.cov(),weights),weights))**(1/2)*np.sqrt(252)


# # Function to Generate Random Weights

# In[6]:


def weightscreator(stocks_lr):
    rand = np.random.random(len(stocks_lr.columns))
    rand /= rand.sum()
    return rand 


# # Function to Find Returns and Standard Deviation for "i" Random Portfolio Weight Arrays

# In[7]:


returns = []
stds = []
w = []

for i in range(1000): #Use the number of iterations you seem fit
    print(i)
    weights = weightscreator(stocks_lr)
    returns.append(portfolioreturn(weights))
    stds.append(portfoliostd(weights))
    w.append(weights)


# # Using MatPlotLib To Plot the Efficient Frontier
# 
# ## Where Efficient Frontier is the graph between Portfolio Risk and Return

# In[8]:

# ## Finding Max Returns and Associated Risk

# In[9]:


print("Max return =", max(returns))
print("Corresponding Standard Deviation =", stds[returns.index(max(returns))])

i = 0
while True: #Use the number of iterations you seem fit
    i += 1
    weights = weightscreator(stocks_lr)
    print(i)
    if (portfolioreturn(weights) >= max(returns)):
        weight_new = weights
        print("Your Efficient Portfolio is:",weight_new) #Returns portfolio weights for above condition being satisfied
        break
    
print(sum(weight_new))

print("Returns corresponding to weights found :",portfolioreturn(weight_new)) #Prints return of found weights
print("Risk associated with weights found :",portfoliostd(weight_new)) #Prints Risk of found weights
         

plt.scatter(stds,returns,c="red",s=0.2,alpha=0.75) #Customise size according to number of iterations being plotter
plt.scatter(stds[returns.index(max(returns))], max(returns),c = "green", s=3) #Customise size for this too
plt.text(stds[returns.index(max(returns))],max(returns),"Maximum Return", fontsize=7) #Customise font size for this too
plt.scatter(min(stds),returns[stds.index(min(stds))] ,c = "blue", s=3) #Customise size for this too
plt.text(min(stds),returns[stds.index(min(stds))],"Minimum Variance", fontsize=7) #Customise font size for this too
plt.title("Efficient Frontier", fontsize = 20)
plt.xlabel("Portfoliostd(Risk)", fontsize = 15)
plt.ylabel("Portfolioreturn(Return)", fontsize = 15)
plt.figure(figsize=(30,20))
plt.show()






