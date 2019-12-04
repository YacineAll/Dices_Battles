from outils import *
from hog import hog
import numpy as np


D = 10
N = 100
h = hog(D,N)


def moyenne(strategie1,strategie2,steps=1000):
    def f():
        score1,score2 = h.jouer(strategie1,strategie2)
        return 0 if score1 > score2 else 1
    
    a = np.zeros((steps))-1
    vfunc = np.vectorize(lambda x: f())
    
    return 1 - vfunc(a).sum()/steps


if __name__ == "__main__":
    a = np.asarray([moyenne(h.strategie_aveugle(),h.strategie_aveugle()) for i in range(0,100)])
    np.savetxt('data.csv', a, delimiter=',')
