#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 16:38:44 2019

@author: ghiles
"""

import numpy as np

def Q(d, k):
	if (k > 6*d) or (k < 2*d):
		return 0.0
	if d == 1:
		return 0.2
	prob = 0.0
	for i in range(2,7):
		prob += 0.2*Q(d-1, k-i)
	return prob

def P(d, k):
	if k == 1:
		return 1.0 - (5.0/6.0)**d
	if (k > 6*d) or (k > 1 and k < 2*d):
		return 0.0
	return Q(d,k)*(5.0/6.0)**d

def generate_P_matrix(D):
	P_matrix = np.zeros((D,6*D))
	for i in range(D):
		for j in range(6*D):
			P_matrix[i][j] = P(i+1,j+1)
	return P_matrix

