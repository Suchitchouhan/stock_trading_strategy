
# coding: utf-8

# In[ ]:


import pandas as pd
import datetime
import pandas_datareader.data as web
from pandas import Series, DataFrame
print("welcome to stock analysis")
try:
    while True:
          sk=input("Enter the stock name >> ")    
          print("Enter starting and ending date of stocks .Inorder to analysis \n ")
          a=int(input('Starting year > '))
          b=int(input('starting month > '))
          c=int(input('starting day > '))
          a2=int(input('ending year > '))
          b2=int(input('ending month > '))
          c2=int(input('ending day > '))
          break
except:
    print("something worng with your input \n")
try:     
     start = datetime.datetime(a,b,c)
     end = datetime.datetime(a2,b2,c2)
     df = web.DataReader(sk, 'yahoo', start, end)
except:
    print("we are not able to fatch data")
df['Date_stock']=df.index


# In[13]:


delta=df['Adj Close'].diff(1)
delta=delta.dropna()
up=delta.copy()
down=delta.copy()
up[up<0]=0
down[down>0]=0
#get the time peroid
period=14
#calculate gains and loss
avg_gain=up.rolling(window=period).mean()
avg_loss=abs(down.rolling(window=period).mean())
#calculate the RSI
#Calcute the Relative strength(RS)
RS=avg_gain/avg_loss
RSI=100.0-(100.0/(1.0+RS))
new_df=pd.DataFrame()
new_df['Adj Close']=df['Adj Close']
new_df['RSI']=RSI
plt.style.use('fivethirtyeight')
plt.figure(figsize=(12.5,4.5))
plt.plot(df['Date_stock'],new_df['Adj Close'],color='blue',label=stock)
plt.title("adj .close")
plt.xlabel(str(start)+"-"+str(end))
plt.ylabel('adj .close price')
plt.legend()
plt.show()
plt.figure(figsize=(12.5,4.5))
plt.title('RSI')
plt.plot(new_df.index,new_df['RSI'],color='blue',label='RSI')
plt.xlabel(str(start)+"-"+str(end))
plt.ylabel("RSI")
plt.axhline(0,linestyle='--',alpha=0.5,color='grey')
plt.axhline(10,linestyle='--',alpha=0.5,color='orange')
plt.axhline(20,linestyle='--',alpha=0.5,color='green')
plt.axhline(30,linestyle='--',alpha=0.5,color='red')
plt.axhline(70,linestyle='--',alpha=0.5,color='red')
plt.axhline(80,linestyle='--',alpha=0.5,color='green')
plt.axhline(90,linestyle='--',alpha=0.5,color='orange')
plt.axhline(100,linestyle='--',alpha=0.5,color='grey')
plt.show()


# In[7]:


#simple moving average of 30 days windows
sma30=pd.DataFrame()
sma30['Adj close price']=df['Adj Close'].rolling(window=30).mean()
#simple moving average of 100 days window
sma100=pd.DataFrame()
sma100['Adj close price']=df['Adj Close'].rolling(window=100).mean()
data=pd.DataFrame()
data[stock]=df['Adj Close']
data['sma30']=sma30['Adj close price']
data['sma100']=sma100['Adj close price']
import numpy as np
def buy_sell(data):
    signbuy=[]
    signsell=[]
    flag=-1
    for i in range(len(data)):
        if data['sma30'][i]>data['sma100'][i]:
            if flag!=1:
                signbuy.append(data[stock][i])
                signsell.append(np.nan)
                flag=1
            else:
                signbuy.append(np.nan)
                signsell.append(np.nan)
        elif data['sma30'][i]<data['sma100'][i]:
            if flag!=0:
                signbuy.append(np.nan)
                signsell.append(data[stock][i])
                flag=0
            else:
                signbuy.append(np.nan)
                signsell.append(np.nan)    
        else:
            signbuy.append(np.nan)
            signsell.append(np.nan)
    return (signbuy,signsell)        
buy_sell=buy_sell(data)
data['buy signal']=buy_sell[0]
data['sell signal']=buy_sell[1]
plt.style.use('fivethirtyeight')
plt.figure(figsize=(12.5,4.5))
plt.plot(data[stock],label=stock,alpha=0.35)
plt.plot(data['sma30'],label="sma30",alpha=0.35)
plt.plot(data['sma100'],label='sma100',alpha=0.35)
plt.scatter(data.index,data['buy signal'],label='buy',marker='^',color='green')
plt.scatter(data.index,data['sell signal'],label='sell',marker='v',color='red')
plt.title("adj close price buy and sell signal")
plt.xlabel(str(start)+"-"+str(end))
plt.ylabel("Adj Close price USD")
plt.legend()
plt.show()


# In[8]:


#this program uses the moving Average convergence/Divergence (MACD) crossover to determine when to buy and sell stock
#calculate the MACF and signal line indicators
#calculate the short term exponential moving average(EMA)


# In[9]:


#macf
shortema=df.Close.ewm(span=12,adjust=False).mean()
longema=df.Close.ewm(span=26,adjust=False).mean()
#calculate the MACD line
macd=shortema-longema
#calculate signal line
signal=macd.ewm(span=9,adjust=False).mean()
plt.figure(figsize=(12.2,4.5))
plt.plot(df.index,macd,label=stock+" MACD",color='red',alpha=0.75)
plt.plot(df.index,signal,label='signal line',color='blue',alpha=0.75)
plt.xlabel('Date')
plt.xticks(rotation=45)
plt.legend()
plt.show()


# In[10]:


df['macd']=macd
df['signal line']=signal
def ema_buy_sell(signal):
    buy=[]
    sell=[]
    flag=-1
    for i in range(0,len(signal)):
        if signal['macd'][i]>signal['signal line'][i]:
            sell.append(np.nan)
            if flag!=1:
                buy.append(signal['Close'][i])
                flag=1
            else:
                buy.append(np.nan)
        elif signal['macd'][i]<signal['signal line'][i]:
            buy.append(np.nan)
            if flag!=0:
                sell.append(signal['Close'][i])
                flag=0
            else:
                sell.append(np.nan)        
        else:  
            buy.append(np.nan) 
            sell.append(np.nan)
    return  (buy,sell)      
ab=ema_buy_sell(df)
df['buy_signal_price']=ab[0]
df['sell_signal_price']=ab[1]
plt.figure(figsize=(12.5,4.5))
plt.scatter(df.index,df['buy_signal_price'],color='green',label='buy',marker='^')
plt.scatter(df.index,df['sell_signal_price'],color='red',label='buy',marker='v')
plt.plot(df['Close'],label='Close price',alpha=0.35)
plt.title('close price buy and sell signal ')
plt.xlabel('Date')
plt.xticks(rotation=45)
plt.ylabel('close price')
plt.legend()
plt.show()

