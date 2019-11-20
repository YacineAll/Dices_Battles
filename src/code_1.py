#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 14:26:06 2019

@author: ghiles
"""

import numpy as np
import matplotlib.pyplot as plt




def Q(d,k,liste):
    
    if(liste[d,k] != -1):
        return liste[d,k]
    
    if ((k >= 2) and (k <= (2*d)-1)) or ( k > 6*d):
        liste[d,k] = 0 
        return 0
            
    return sum([ Q(d-1,k-i)/5 for i in range(2,7) ])
    
    
def P(d,k):
    
    
    if(d<1):
        return 0
    
    
    if (k == 1) :
        return 1-np.power(5/6,d)
    
    if(d==1 and k<=6):
        return (1/5) * (1-np.power(5/6,d))
    
    
    if ((k >= 2) and (k <= (2*d)-1)) or ( k > 6*d):
        return 0

    
    return np.power(5/6,d) * Q(d,k)





"""
D = 100
K = 6*D

probabilite = P(D,K)
def EP(D):
    return np.array([4*d*np.power(5/6,d) + (1-np.power(5/6,d)) for d in range(1,D+1) ])



def EG(d,p):
    return sum([p[d][i]*i for i in range (p.shape[0]) ])

plt.plot([i for i in range(1,D+1)],np.array([4*d*np.power(5/6,d) + (1-np.power(5/6,d)) for d in range(1,D+1) ]))
plt.plot([i for i in range(1,D+1)],[ EG(d,probabilite) for d in range(1,D+1)])

#EG(6,P(6,6)[1])

"""