#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 14:26:06 2019

@author: ghiles
"""

import numpy as np



def Q(d,k):
    a = np.zeros((d+1,k+1))

    for _d in range(d+1):
        for _k in range(k+1):
            if (_k > 6*_d) or (_k < 2*_d):
                a[_d][_k] = 0.0
                continue
            if(_d == 1):
                a[_d][_k] = 1/5
                continue
            s = 0
            for i in range(2,7):
                if(_k>i):
                    s += a[_d-1][_k-i]

            a[_d][_k] = (1/5) * s

    return a[d][k]

def P(d,k):
    if k == 1:
        return 1.0 - (5.0/6.0)**d
    if (k > 6*d) or (k > 1 and k < 2*d):
        return 0.0
    return Q(d,k)*(5.0/6.0)**d


def generate_P_matrix(D):
	P_matrix = np.zeros((D+1,6*D+1))
	for i in range(1,D+1):
		for j in range(6*D+1):
			P_matrix[i][j] = P(i,j)
	return P_matrix




def EP(D=10):
    return 1+np.argmax(np.array([4*d*np.power(5/6,d) + (1-np.power(5/6,d)) for d in range(1,D+1) ]))

"""
def G():
    def f(j,k):
        return (k > 0 and j>0)

    t = N + 6*D
    t = N
    a = np.zeros( ( t, t , 2 ))
    for i in range(1,t):
        for  j in range(1,t):
            l = [ probabilite[d][1]*(1 - a[j][i-1][0] ) + sum([ probabilite[d][k] * ( 1-a[j][i-k][0] * f(j,i-k) )
            for k in range (2*d,6*d + 1) ])  for d in range(1,D+1)]
            a[i][j][0] = max(l)
            a[i][j][1] = 1+np.argmax(l)

    return a
"""


def esperance_gain(N,D,probabilite):
    a = np.full((N+6*D,N+6*D),0)

    a[N: , :N] = 1
    a[:N , N: ] = -1

    optimal = np.zeros((N, N), dtype = int)

    for x in range(N - 1, -1, -1):
        for y in range(x, -1, -1):
            for i,j in {(x,y),(y,x)}:
                tmp = - probabilite[ :, 1: ].dot(a[j, (i + 1):(i + 6 * D + 1)])

                optimal[i, j] = tmp[1: ].argmax() + 1

                a[i, j] =  tmp[optimal[i, j]]

    return a,optimal

def eg_simul(D,probabilite):
    def f(d1,d2):
        s_1 = s_2 = 0
        n = max(d1,d2)*6

        for i in range(1,6*d1+1):
            for j in range(1,6*d2+1):    

                if(j<i):
                    s_1 += probabilite[d1][i]

                if(i<j):
                    s_2 += probabilite[d2][j]
        p = (s_1 - s_2)/n
        return  np.round(p, 7)

    a = np.zeros((D+1,D+1))
    for d1 in range(1,D+1):
        for d2 in range(1,D+1):        
            a[d1][d2] = f(d1,d2)
    return a[1:,1:]



#probabilite = generate_P_matrix(D)
#probabilites_matrix = G()
#eg,opt = _esperanceGain()












