#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

def laplace(p0, p1, mask, omega=1):
    p2 = p1.copy()
    for i in range(1, mask.shape[0] - 1):
        for j in range(1, mask.shape[1] - 1):
            if mask[i, j]:
                continue
            p2[i, j] = 0.25 * (p1[i, j-1] + p1[i-1, j] + p1[i, j+1] + p1[i+1, j])
    res = p2 - p0
    p2 = p0 + omega * res
    return p2, res

def vectors(p):
    result = np.zeros((p.shape[0], p.shape[1], 2))
    for i in range(1, p.shape[0] - 1):
        for j in range(1, p.shape[1] - 1):
            result[i, j, 0] = p[i, j] - p[i, j - 1]
            result[i, j, 1] = p[i, j] - p[i - 1, j]
    return result

if __name__ == '__main__':
    path = 'data/pl_ko60x60.dat'#'data/zyl-100x100-20-49-0.dat'
    limit = 1E-4
    max_iterations = 10000
    omega = 1.835
    
    mask = []
    potential = []
    for line in open(path, 'r').readlines():
        split = line.split()
        mask.append([e.startswith('*') for e in split])
        potential.append([float(e.replace('*', '')) for e in split])
    mask = np.array(mask)
    potential = np.array(potential)
    
    plt.imshow(potential, interpolation='nearest')
    plt.show()
    
    p0, p1 = potential, potential
    for i in range(max_iterations):
        p2, res = laplace(p0, p1, mask, omega)
        a = np.mean(np.abs(res))
        print(i, a)
        #plt.imshow(p2, interpolation='nearest')
        #plt.show()
        if a < limit:
            break
        p0 = p1
        p1 = p2
    
    plt.imshow(p2, interpolation='nearest')
    plt.contour(p2, linewidths=3)
    plt.show()
    
    e = vectors(p2)
    plt.quiver(e[:,:,0], e[:,:,1])
    plt.contour(p2, linewidths=3)
    plt.show()

