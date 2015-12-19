'''
Created on Dec 14, 2012

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
from pylab import *

inFile='values.csv'
indexToCompare='$SPX'

values = read_csv('values.csv',parse_dates=[[0,1,2]],header=None,index_col=[0])
values.columns=["Values"]
values=values.shift(16, freq='H')
values=values.sort()

#get market data
dateRange=DatetimeIndex(start=values.index.min(),end=values.index.max(),freq="D")
dataobj = da.DataAccess('Yahoo')
indexToCompareClose = dataobj.get_data(list(dateRange), [indexToCompare], 'close').dropna()

values=values.join(indexToCompareClose)

values['Values_Ret']=(values['Values']-values['Values'].shift(1))/values['Values'].shift(1)
values['$SPX_Ret']=(values['$SPX']-values['$SPX'].shift(1))/values['$SPX'].shift(1)

subplot(211)
values['Values'].plot()
ylabel('Portfolio value')

subplot(212)
values['$SPX'].plot()
ylabel('$SPX value')

figure()

subplot(211)
values['Values_Ret'].plot()
ylabel('Values_Ret')

subplot(212)
values['$SPX_Ret'].plot()
ylabel('$SPX_Ret')

#show()
portMean=values['Values_Ret'].mean()
indexMean=values['$SPX_Ret'].mean()
portStd=values['Values_Ret'].std()
indexStd=values['$SPX_Ret'].std()

print "Average daily return of portfolio is %f %%"%(portMean*100)
print "Average daily return of %s is %f %%\n"%(indexToCompare,indexMean*100)
print "Stddev of daily return of portfolio is %f %%"%(portStd*100)
print "Stddev of daily return of %s is %f %%\n"%(indexToCompare,indexStd*100)
print 'Sharpe ratio of portfolio is ',sqrt(250)*portMean/portStd
print 'Sharpe ratio of index is %f',sqrt(250)*indexMean/indexStd
#print values[-10:]