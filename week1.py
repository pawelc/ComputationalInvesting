#import numpy as np
#np.test('full')
import math

def sharpRatio(periods,rMu,rSigma):
    return math.sqrt(periods)*rMu/rSigma
     
print sharpRatio(12, .01, .04)