#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 17:34:39 2019

@author: 3701222

MOGPL Project
"""

from random import randint
faces = 6

def dice():
    """
    Un fonction qui renvoie un nombre entre 1 et 6 inclu aleatoirement.
    """
    return randint(1,faces)
