'''
Created on Dec 12, 2012

@author: pawelc
'''
import numpy as np
randn = np.random.randn
from pandas import *
from pandas.io.data import *
from pylab import *


#s = Series(randn(5), index=['a', 'b', 'c', 'd', 'e'])
#print s.median()
#print s.index

#x=np.random.standard_normal(250)
#index=DateRange('01/01/2012',periods=len(x))
#s=Series(x,index=index)

AAPL=DataReader('AAPL','yahoo',start="01/01/2006")
#AAPL['Ret']=log(AAPL['Close']/AAPL['Close'].shift(1))
#print AAPL[:10].to_string()
print AAPL['Close'][:10]
print AAPL['Close'].shift(1)[:10]
