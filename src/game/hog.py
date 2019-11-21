#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 17:42:53 2019

@author: 3701222
"""

import numpy as np
from dice import *

SCORE_MAX = 100
D_MAX = 10
def _roulez_les_des(d):
    
    assert type(d) == int, 'nombre de dés doit étre un entier.'
    assert d > 0, 'il faut faire au moin un lacer.'
    
    vfunc = np.vectorize(lambda x: dice())
    a = np.zeros(d) - 1 
    a = vfunc(a) 
    if(1 in a):
        return 1
    else:
        return a.sum()
    
    
def tour(d, score_adverse):
    """Simuler un tour en lançant d dés.
    d:       Le nombre des lancers des dés qui seront faits.
    score_adverse:  Le score total de l'adversaire.
    """
    
    assert type(d) == int, 'd doit être un entier.'
    assert d > 0, 'Impossible de lancer un nombre négatif de dés ou zero .'
    assert d <= 10, 'ON ne peut pas lancer plus de 10 dés.'
    assert score_adverse < 100, 'Le jeu devrait être terminé.'
    return _roulez_les_des(d)


def autre(q):
    """Renvoie l'autre joueur, pour un joueur numéroté 0 ou 1..
    """
    return 1 - q

def jouer(strategie0, strategie1, but = SCORE_MAX):
    """Simulez une partie et renvoyez les scores finaux des deux joueurs, avec
    Le score du joueur 0 en premier et celui du joueur 1 en second.
    
    Une stratégie est une fonction qui prend deux scores totaux comme arguments
    (le score du joueur actuel et le score de l'adversaire), et renvoie un
    nombre de dés que le joueur actuel lancera a ce tour.
    
    strategie0: fonction de stratégie pour le joueur 0, qui joue en premier.
    strategie1: fonction de stratégie pour le joueur 1, qui joue en second.
    
    """
        
    score, score_adverse = 0, 0
    
    while score < but and score_adverse < but :
        p0 = strategie0(score,score_adverse)
        current_score0 = tour(p0, score_adverse)
        
        score += current_score0
        
        if score >=100:
            return score, score_adverse
        
        p1 = strategie1(score_adverse, score)
        
        current_score1 = tour(p1, score)
        
        score_adverse += current_score1
    
    return score, score_adverse


        
def toujour_lancer(n):
    """Renvoie une stratégie qui lance toujours N dés.
    Une stratégie est une fonction qui prend deux scores totaux comme arguments
    (le score du joueur actuel et le score de l'adversaire), et renvoie un
    nombre de dés que le joueur actuel lancera ce tour.
    >>> strategie = toujour_lancer(5)
    >>> strategie(0, 0)
    5
    >>> strategie(99, 99)
    5
    """
    def strategie(score, score_adverse):
        return n
    return strategie        



def max_esperance():
    """Renvoie le nombre de dés (1 à 10) donnant le tour moyen le plus élevé.
    EP = max ( 4*d*np.power(5/6,d) + 1 - np.power(5/6,d) for d in {1,2,3,...,D_MAX})
    D_MAX : le nombre maximum de des que on peut lancer
    """
    def strategie(score, score_adverse):
        D=D_MAX
        return int(1+np.argmax(np.array([4*d*np.power(5/6,d) + (1-np.power(5/6,d)) for d in range(1,D+1) ])))
    
    return strategie





        
        
        
        
        