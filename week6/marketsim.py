'''
Created on Dec 12, 2012

@author: pawelc
'''
from pandas import *
from qstkutil import DataAccess as da
import numpy as np
import math
import copy
import qstkutil.qsdateutil as du
import datetime as dt
import qstkutil.DataAccess as da
import qstkutil.tsutil as tsu
import qstkstudy.EventProfiler as ep
from Carbon.Fonts import times
from pandas.io.data import DataReader

initial_cash=1000000
orders_file="orders.csv"
values_file="values.csv"

orders = read_csv('orders.csv',parse_dates=[[0,1,2]],header=None,index_col=[0])
orders.columns=["Stock","Operation","Shares","X"]
orders=orders.shift(16, freq='H')
orders=orders.drop("X",axis=1).sort()
#

#get market data
dateRange=DatetimeIndex(start=orders.index.min(),end=orders.index.max(),freq="D")
dataobj = da.DataAccess('Yahoo')
stockNames=orders["Stock"].unique()
portfolio = dataobj.get_data(list(dateRange), stockNames, 'close').dropna()
portfolio['Cash']=initial_cash
portfolio['Year']=None
portfolio['Month']=None
portfolio['Day']=None

orders=portfolio.join(orders)

for s in stockNames:
    portfolio["%s_Shares"%s]=0
portfolio["Value"]=initial_cash

for row in orders.iterrows():
    stock=row[1]['Stock']
    if isinstance(stock,str):
        op=row[1]['Operation']
        shares=row[1]['Shares']
        columnsShares="%s_Shares"%stock
        currentShares=portfolio.get_value(row[0],columnsShares)
        price=portfolio.get_value(row[0],stock)
        opValue=price*shares
        currentCash=portfolio.get_value(row[0],'Cash')
        if op=='Buy': 
            portfolio.ix[portfolio.index>=row[0],columnsShares]=shares+currentShares
            portfolio.ix[portfolio.index>=row[0],'Cash']=currentCash-opValue
        elif stock and op=="Sell":
            portfolio.ix[portfolio.index>=row[0],columnsShares]=currentShares-shares
            portfolio.ix[portfolio.index>=row[0],'Cash']=currentCash+opValue
    #update value
    value=0
    for s in stockNames:
        value+=portfolio.get_value(row[0],"%s_Shares"%s)*portfolio.get_value(row[0],"%s"%s)
    value+=portfolio.get_value(row[0],'Cash')
    portfolio.ix[portfolio.index>=row[0],'Value']=value
    portfolio.ix[portfolio.index==row[0],'Year']=row[0].year
    portfolio.ix[portfolio.index==row[0],'Month']=row[0].month
    portfolio.ix[portfolio.index==row[0],'Day']=row[0].day

portfolio.to_csv('values.csv',cols=['Year','Month','Day','Value'],header=False,index=False)    
#print portfolio.to_string()