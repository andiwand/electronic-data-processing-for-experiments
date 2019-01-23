#!/usr/bin/env python3

import time
import numpy as np
import matplotlib.pyplot as plt

class Random:
    def __init__(self, a, c, m, seed=0):
        self._a = a
        self._c = c
        self._m = m
        self._x = seed
    def seed(self, seed):
        self._x = seed
    def rand(self):
        x = int((self._a*self._x+self._c) % self._m)
        self._x = x
        return x
    def uni01(self):
        return self.rand() / (self._m-1)
    def uni(self, imax):
        return self.rand() % (imax+1)
    def uni01vec(self, n):
        return np.array([self.uni01() for _ in range(n)])

def spektral(random, n, path):
    with open(path, 'w') as f:
        for _ in range(n):
            f.write(' '.join([str(random.uni01()) for _ in range(3)]))
            f.write('\n')

def mc_integral(f, a, b, r, n):
    rx = a+(b-a)*r.uni01vec(n)
    y = np.vectorize(f)(rx)
    y_min, y_max = np.min(y), np.max(y)
    ry = np.array([y_min+(y_max-y_min)*r.uni01() for _ in range(n)])
    return ((b-a)*(y_max-y_min)/n)*(np.sum((ry>0) & (ry<y)) - np.sum((ry<0) & (ry>y)))

def mc_converge(f, a, b, r, nn):
    result = []
    for n in nn:
        i = mc_integral(lambda x: np.exp(-x**2/2)/np.sqrt(2*np.pi), -4, 4, ansic, n)
        result.append((n, i))
    return np.array(result)

def mc_kugel(rand, n, dd):
    result = []
    for d in dd:
        r = []
        for _ in range(n):
            x = -0.5+rand.uni01vec(d)
            r.append(np.sqrt(np.sum(x*x)))
        r = np.array(r)
        v = (1/n) * np.sum(r<=0.5)
        result.append((d, v))
    return np.array(result)

# aufgabe 1
n = 10000
seed = 7
randu = Random(65539, 0, 2**31, seed)
ansic = Random(1103515245, 12345, 2**31, seed)

spektral(randu, n, 'randu.csv')
spektral(ansic, n, 'ansic.csv')

# aufgabe 2a
f = lambda x: np.exp(-x**2/2)/np.sqrt(2*np.pi)
ansic.seed(time.time())
con = mc_converge(f, -4, 4, ansic, [10**i for i in range(1, 7)])
plt.plot(con[:,0], con[:,1])
plt.axhline(y=1)
plt.gca().set_xscale('log')
plt.show()

# aufgabe 2b
n = 10000
ansic.seed(time.time())
kugel = mc_kugel(ansic, n, list(range(1, 13)))
plt.plot(kugel[:,0], kugel[:,1])
plt.show()

