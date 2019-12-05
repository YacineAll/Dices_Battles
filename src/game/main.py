from outils import *
from hog import hog
import numpy as np


D = 10
N = 100
h = hog(D,N)


def moyenne(strategie1,strategie2,name1,name2,steps=1000):
    def f1():
        score1,score2 = h.jouer(strategie1,strategie2)
        return 0 if score1 > score2 else 1
    
    def f2():
        score1,score2 = h.jouer(strategie1,strategie2)
        return 0 if score1 > score2 else 1
    
    a = np.zeros((steps))-1
    vfunc = np.vectorize(lambda x: f1())
    s1 = 1 - vfunc(a).sum()/steps
    
    """
    a = np.zeros((steps))-1
    vfunc = np.vectorize(lambda x: f2())
    s2 = 1 - vfunc(a).sum()/steps
    """
    r = dict()
    t = dict()
    t[name2] = s1 
    r[name1] = t
    """
    t = dict()
    t[name1] = s2 
    r[name2] = t
    """
    return r

def function(stratiges,names):
    from itertools import  combinations_with_replacement
    l = list(combinations_with_replacement(stratiges,2))
    names = list(combinations_with_replacement(names,2))
    
    r=list()
    for i in range(len(l)):
        name1,name2 = names[i]
        s1,s2       = l[i]
        r.append(moyenne(s1,s2,name1,name2))
    return r 

if __name__ == "__main__":
    print("yacine")