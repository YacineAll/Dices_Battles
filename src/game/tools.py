from outils import *
from hog import hog
import numpy as np


D = 20
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
    
    r = dict()
    t = dict()
    t[name2] = s1 
    r[name1] = t
    
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
        if(name1 != name2):
            r.append(moyenne(s2,s1,name2,name1))
    return r 

def get_pandas_data():
    a = [h.strategie_aveugle(),h.strategie_optimale(),h.strategie_aleatoire()]
    names=["aveugle","optimale","aleatoire"]
    a = function(a,names)
    d=dict({ n : dict() for n in names })
    for k in a:
        _k = list(k.keys())[0]
        _v = list(k.values())[0]
        default_data = dict()
        for x in k.values():
            d[_k].update(x)
    import pandas as pd
    df = pd.DataFrame(d).T
    df.to_csv("./data.csv")
    return  df