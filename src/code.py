#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 14:26:06 2019

@author: ghiles
"""



import numpy as np




N = 100
D = 10
K = 6*D



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



def _esperanceGain():
        """
        """
        n = N
        d = D
        eg = np.full((n + 6 * d, n + 6 * d), np.nan)
        #eg = np.zeros((n + 6 * d, n + 6 * d))
        opt = np.zeros((n, n), dtype = int)

        #remplissage des cas de base de l'esperance
        eg[n: , :n] = 1
        eg[:n, n: ] = -1

        for x in range(n - 1, -1, -1):
            for y in range(x, -1, -1):
                for i, j in {(x, y), (y, x)}:
                    #tableau des esperances pour chaque quantité de dés possible :
                    ed = - probabilite[ :, 1: ].dot(eg[j, (i + 1):(i + 6 * d + 1)])
                    opt[i, j] = ed[1: ].argmax() + 1
                    eg[i, j] =  ed[opt[i, j]]
        return eg, opt

def esp(d1,d2):
    a = probabilite[d1][np.arange(1,6*d1+1)].dot(np.arange(1,6*d1+1))
    b = probabilite[d2][np.arange(1,6*d2+1)].dot(np.arange(1,6*d2+1))
    return a,b
probabilite = generate_P_matrix(D)
#probabilites_matrix = G()
eg,opt = _esperanceGain()












