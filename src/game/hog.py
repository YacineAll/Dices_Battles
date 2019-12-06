#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 17:42:53 2019

@author: 3701222
"""

import numpy as np
from dice import *
from outils import *






class hog:
    """
    La Classe hog represente toutes la logique de Jeu
    """
    
    def __init__(self,D=10,N=100):
        """
        D = nombre maximum de Dés qu'on peut lancer.
        N = nombre maximum de points qu'on peut atteindre.
        """    
        self.SCORE_MAX = N
        self.D_MAX = D
        
        # On crée la table des probabilités. 
        self.probabiltes = generate_P_matrix(self.D_MAX)
        # On crée les tables: l'esperance de gain et la table des optimal.
        self.eg,self.opt = esperance_gain(self.SCORE_MAX,self.D_MAX,self.probabiltes)
        
    def _roulez_les_des(self,d):
        """
        d : nombre de Dés que on lance.
        """
        assert type(d) == int, 'nombre de dés doit étre un entier.'
        assert d > 0, 'il faut faire au moin un lacer.'

        #dice(): renvoie un entier entre 1 et 6 
        vfunc = np.vectorize(lambda x: dice())
        a = np.zeros(d) - 1
        
        #on crée un tableau a d valeurs qui representes les lancer de chaque Dé.
        a = vfunc(a)
        
        # si on au moin un 1 on renvoie 1 si non la somme des lancer
        if(1 in a):
            return 1
        else:
            return a.sum()


    def _tour(self,d, score_adverse):
        """Simuler un tour en lançant d dés.
        d:Le nombre des lancers des dés qui seront faits.
        score_adverse:  Le score total de l'adversaire.
        """

        assert type(d) == int, 'd doit être un entier.'
        assert d > 0, 'Impossible de lancer un nombre négatif de dés ou zero .'
        assert d <= self.D_MAX, 'ON ne peut pas lancer plus de 10 dés.'
        assert score_adverse < self.SCORE_MAX, 'Le jeu devrait être terminé.'
        return self._roulez_les_des(d)



    def jouer(self , strategie0, strategie1):
        """Simulez une partie et renvoyez les scores finaux des deux joueurs, avec
        Le score du joueur 0 en premier et celui du joueur 1 en second.

        Une stratégie est une fonction qui prend deux scores totaux comme arguments
        (le score du joueur actuel et le score de l'adversaire), et renvoie un
        nombre de dés que le joueur actuel lancera a ce tour.

        strategie0: fonction de stratégie pour le joueur 0, qui joue en premier.
        strategie1: fonction de stratégie pour le joueur 1, qui joue en second.

        """
        but = self.SCORE_MAX
        
        score, score_adverse = 0, 0

        #Tant que on est pas arriver à score max on joue.
        while score < but and score_adverse < but :
            p0 = strategie0(score,score_adverse)
            current_score0 = self._tour(p0, score_adverse)

            score += current_score0

            if score >=100:
                return score, score_adverse

            p1 = strategie1(score_adverse, score)

            current_score1 = self._tour(p1, score)

            score_adverse += current_score1

        return score, score_adverse



    def strategie_toujour_lancer(self,n):
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
        def strategy(score, opponent_score):
            return n
        return strategy
    
    def strategie_aleatoire(self):
        """Renvoie le nombre de dés (1 à 10) donnant le tour moyen le plus élevé.
        EP = max ( 4*d*np.power(5/6,d) + 1 - np.power(5/6,d) for d in {1,2,3,...,D_MAX})
        D_MAX : le nombre maximum de des que on peut lancer
        """
        def strategie(score, score_adverse):
            return np.random.randint(self.D_MAX) + 1
        return strategie


    def strategie_aveugle(self):
        """Renvoie le nombre de dés (1 à 10) donnant le tour moyen le plus élevé.
        EP = max ( 4*d*np.power(5/6,d) + 1 - np.power(5/6,d) for d in {1,2,3,...,D_MAX})
        D_MAX : le nombre maximum de des que on peut lancer
        """
        def strategie(score, score_adverse):
            D=self.D_MAX
            return int(1+np.argmax(np.array([4*d*np.power(5/6,d) + (1-np.power(5/6,d)) for d in range(1,D+1) ])))
        return strategie

    
    def strategie_optimale(self):
        """Renvoie le nombre de dés (1 à 10) 
        On utilise la matrice des optimaux calculé à l'initialisation
        """
        def strategie(score, score_adverse):
            return int(self.opt[score][score_adverse])
        return strategie




