#!/usr/bin/env python3

from multiprocessing import cpu_count, Pool
import numpy as np
import time

def pairwise(iterable):
    "s -> (s0, s1), (s2, s3), (s4, s5), ..."
    a = iter(iterable)
    return zip(a, a)

def dotnp(a, b):
    return a.dot(b)

def mydot2(a, b):
    if len(a) != len(b):
        return None
    result = 0
    for k in range(len(a)):
        result += a[k] * b[k]
    return result

def mydot(a, b):
    if a.shape[1] != b.shape[0]:
        return None
    result = np.zeros((a.shape[0], b.shape[1]))
    for i in range(a.shape[0]):
        for j in range(b.shape[1]):
            result[i, j] = mydot2(a[i,:], b[:,j])
    return result

def mydotmulti(a, b, pool):
    if a.shape[1] != b.shape[0]:
        return None
    async = [[None]*b.shape[1] for _ in range(a.shape[0])]
    for i in range(a.shape[0]):
        for j in range(b.shape[1]):
            async[i][j] = pool.apply_async(dot2, (a[i,:], b[:,j]))
    result = np.zeros((a.shape[0], b.shape[1]))
    for i in range(a.shape[0]):
        for j in range(b.shape[1]):
            result[i, j] = async[i][j].get()
    return result

def multidot(m, dot):
    a = m[0]
    for b in m[1:]:
        a = dot(a, b)
    return a

def multidotmulti(m, pool, dot):
    async = []
    for a, b in pairwise(m):
        f = pool.apply_async(dot, (a, b))
        async.append(f)
    results = [f.get() for f in async]
    if len(m) % 2 != 0:
        results.append(m[-1])
    if len(results) == 1:
        return results[0]
    return multidotmulti(results, pool, dot)

CPU_COUNT = cpu_count()
MATRIX_SIZE = 200
MATRIX_COUNT = 10

print('create thread pool %d' % CPU_COUNT)
pool = Pool(CPU_COUNT)

a = np.array([[1, 2], [3, 4], [5, 6]], dtype=float)
b = np.array([[4], [3]], dtype=float)
print(a)
print(b)
print(dotnp(a, b))
print(mydot(a, b))

m = [np.random.rand(MATRIX_SIZE, MATRIX_SIZE) for _ in range(MATRIX_COUNT)]
start = time.time()
a = multidot(m, dotnp)
print('numpy dot time: %f s' % (time.time() - start))
"""
start = time.time()
a = multidot(m, mydot)
print('my dot time: %f s' % (time.time() - start))
"""
"""
start = time.time()
a = multidot(m, mydotmulti)
print('my dot multi time: %f s' % (time.time() - start))
"""
start = time.time()
a = multidotmulti(m, pool, mydot)
print('multi dot time: %f s' % (time.time() - start))

