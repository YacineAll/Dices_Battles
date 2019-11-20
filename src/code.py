#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 14:26:06 2019

@author: ghiles
"""

import numpy as np
import matplotlib.pyplot as plt



def Q(d,k):
    D=d
    K = k
    a = np.zeros((D+1,K+1))
    
    for _d in range(1,D+1):
        for _k in range(2,K+1):
            if(_d == 1): 
                a[_d][_k] = 1/5
            else :
                a[_d][_k] = (sum([ a[_d-1][_k-i] for  i in range(2,7) if (_k-i>=0) and (_d-1>=0)  ]) /5)
                
    return a[d][k]
            
def P(D,K):
    a = np.zeros((D+1,K+1))
    
    for d in range(1,D+1):
        for k in range(1,K+1):
            if k == 1 : 
                a[d][k] = 1 - np.power(5/6,d)
            if ((k >= 2) and (k <= 2*d-1) ) or (k > 6*d) : 
                a[d][k] = 0        
            
            if (k >= 2*d) and ( k <= 6*d ):
                if (d == 1):
                    a[d][k]=1/6
                else:
                    a[d][k] = np.power(5/6,d) * Q(d,k)
    return a

D = 10
K = 6*D

probabilite = P(D,K)


def EP(D=10):
    return 1+np.argmax(np.array([4*d*np.power(5/6,d) + (1-np.power(5/6,d)) for d in range(1,D+1) ]))



def EG(d,p):
    return sum([p[d][i]*i for i in range (p.shape[0] + 1 ) ])

plt.plot([i for i in range(1,D+1)],np.array([4*d*np.power(5/6,d) + (1-np.power(5/6,d)) for d in range(1,D+1) ]))
plt.plot([i for i in range(1,D+1)],[ EG(d,probabilite) for d in range(1,D+1)])









