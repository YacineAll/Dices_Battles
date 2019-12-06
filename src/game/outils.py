#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 14:26:06 2019

@author: ghiles
"""

import numpy as np
import pandas as pd 
from pulp import *





def Q(d,k):
    """
    int*int -> float
    Renvoie P(d,k|k!=1) c'est à dire la probabilite d'avoir k point avec d Dés sachant que aucun Dé tombe sur 1
    """
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
    """
    int*int -> float
    
    Renvoie P(d,k): La probabilite d'avoir k point avec d Dés.
    
    """
    if k == 1:
        return 1.0 - (5.0/6.0)**d
    if (k > 6*d) or (k > 1 and k < 2*d):
        return 0.0
    return Q(d,k)*(5.0/6.0)**d


def generate_P_matrix(D):
    """
    int -> 2ndarray
    Renvoie une matrice P tel que P[d,k] c'est la probabilté d'avoir k point avec d Dés.
    """    
    P_matrix = np.zeros((D+1,6*D+1))
    for i in range(1,D+1):
    	for j in range(6*D+1):
            P_matrix[i][j] = P(i,j)
    return P_matrix

def EP(D=10):
    """
    int -> int 
    Rend le nombre de Dés qui maximise l'espirance de gain entre 1...D
    """
    return 1+np.argmax(np.array([4*d*np.power(5/6,d) + (1-np.power(5/6,d)) for d in range(1,D+1) ]))


def probability_to_win(probabilite,D,N):
    """
    2ndarray * int * int -> 2ndarray
    
    Renvoie une matrice G de dimension 2 tel que G[i,j] est la probabilte que le joueur 1 gagne
    Sachant que i est le nombre de points que J1 besoin de pour atteindre N points, j est le nombre de points que J2 besoin de pour atteindre N points
    """
    def f(j,k):
        return (k > 0 and j>0)

    t = N + 6*D
    t = N
    a = np.zeros( ( t, t ))
    for i in range(1,t):
        for  j in range(1,t):
            l = [ probabilite[d][1]*(1 - a[j][i-1] ) + sum([ probabilite[d][k] * ( 1-a[j][i-k] * f(j,i-k) )
            for k in range (2*d,6*d + 1) ])  for d in range(1,D+1)]
            a[i][j] = max(l)

    return a


def esperance_gain(N,D,probas):
    """
    N: nombre de points maximum 
    D: nombre maximum de Dés
    probas : matrice des probabilités
    
    la fonction renvoie deux matrice: La matrice d'espirance de gain et la fonction des ooptimaux tel que:
    e[s1,s2]: l'espérance de gain du joueur1 dans l'état ou le joueur 1 a comme score :s1, et joueur 2 :s2
    o[score1,score2] : le nombre de Dé le plus optimale que le joueur 1 devra jouer dans l'état ou le joueur 1 a comme score s1 et joueur 2 s2
    """
    #on Cree un tableau de 
    e = np.full((N + 6 * D, N + 6 * D), np.nan)
    
    o = np.zeros((N, N), dtype = int)
    
    e[N: , :N] = 1
    e[:N, N: ] = -1
        
    for x in range(N - 1, -1, -1):
        for y in range(x, -1, -1):
            for i, j in {(x, y), (y, x)}:
                temp = - probas[ :, 1: ].dot(e[j, (i + 1):(i + 6 * D + 1)])
                o[i, j] = temp[1: ].argmax() + 1
                e[i, j] =  temp[o[i, j]]
    return e, o



def eg_simul(probabiltes,D):
    """
    2ndarray*int -> list(pulpVars)
    Prend en parametre la matrice des probabilités et le nombre de Dés maximum et resolue le probleme lineare et renvoie une liste de variable qui sont optimiser
    
    """
    def f(d1, d2):
        j1=0
        for i in range(1,len(probabiltes[d1])):
            j2 = 0
            for j in range(1,len(probabiltes[d2])):
                if(i>j):
                    j2 += probabiltes[d2][j]
                
                if(i<j):
                    j2 -= probabiltes[d2][j]
            j1 += probabiltes[d1][i]*j2
        return np.round(j1,15)
    a = np.zeros((D+1,D+1))
    for d1 in range(D+1):
        for d2 in range(D+1):
            a[d1,d2] = f(d1,d2)
    return a[1:,1:]


def lp_resolution(probabilite,D,j=1):
    """
    2ndarray * int  * int -> list of pulp object 
    Prend en parametre  probabilites, nombre maximum de dés D et j represente le joueur qui va jouer 
    Rend la liste des variables pulp 
    """
    
    if(j==1):
        g = eg_simul(probabilite,D)
    else:
        g = eg_simul(probabilite,D).T
        
    nb_variables = D+1

    prob = LpProblem("Dices Battles J"+str(j),LpMaximize)

    var_s = ['p'+str(chr(96+i)) for i in range(1,nb_variables) ]
    

    var_s +='z'

    variables = LpVariable.dicts("",var_s,lowBound=0,cat='Continuous')
    
    coefs_obj = g.T

    l = []
    for i in range(len(coefs_obj)):
        t = []
        for j in range(len(coefs_obj[0])):
            t.append(coefs_obj[i][j]*variables[var_s[j]])
        l.append(t)
    prob += 1*variables[var_s[nb_variables-1]]


    for i in range(len(l)):
        prob += lpSum(l[i]) -1*variables[var_s[nb_variables-1]] >= 0

    prob += lpSum([ v for n,v in variables.items() if n !='z']) == 1

    prob.solve()
        
    print("Status:", LpStatus[prob.status])
    
    for v in prob.variables():
        print(v.name, "=", v.varValue)
    print("Total Cost of Ingredients per can = ", value(prob.objective))
    
    return prob.variables()
    

