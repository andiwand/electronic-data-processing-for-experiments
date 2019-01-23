#!/usr/bin/env python3

import socket
import re
import numpy as np
import scipy.stats
import matplotlib.pyplot as plt

TCP_IP = '127.0.0.1'
TCP_PORT = 56700

def command(cmd):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send((cmd + '\n').encode('utf-8'))
    data = b''
    while True:
        r = s.recv(1024)
        if len(r) <= 0:
            break
        data += r
    s.close()
    return data.decode('utf-8')

def get_p2():
    response = command('help')
    m = re.search(r'p2:\[(.*)\]', response, re.I)
    return np.array([int(s) for s in m.group(1).split(',')])

def throw(p1, p2):
    response = command('throw %d %d' % (p1, p2))
    return np.array([int(c) for c in response.strip()])

def entropie(t):
    p = np.histogram(t, bins=range(1, 8), normed=True)[0]
    e = -np.sum(p*np.log2(p))
    return np.log2(6), e

def dist(t):
    h = plt.hist(t, bins=range(1, 8), range=(0, 6), normed=True)
    
    mean = 1/6
    std = np.std(h[0])
    plt.axhline(y=mean, color='r')
    plt.axhline(y=mean-std, color='r')
    plt.axhline(y=mean+std, color='r')
    
    plt.show()

def binomial(t, m):
    sums = []
    for i in range(len(t) // m):
        tt = t[m*i:m*(i+1)]
        sums.append(sum(tt))
    sums = np.array(sums)
    sums -= m
    
    n = 5*m
    
    mean = np.mean(sums)
    std = np.std(sums, ddof=1)
    
    plt.hist(sums, normed=True, color='b')
    plt.axvline(x=mean, color='b')
    plt.axvline(x=mean-std, color='b')
    plt.axvline(x=mean+std, color='b')
    
    mean, var = scipy.stats.binom.stats(n, 0.5, moments='mv')
    std = np.sqrt(var)
    
    x = np.arange(0, 5*m)
    plt.plot(x, scipy.stats.binom.pmf(x, n, 0.5), color='g')
    plt.axvline(x=mean, color='g')
    plt.axvline(x=mean-std, color='g')
    plt.axvline(x=mean+std, color='g')
    
    plt.show()

#p2 = [0, 1, 2, 3, 4, 5, 6, 71, 10, 11, 12, 13, 80, 20, 21, 22, 23, 100, 90, 70]
p2 = get_p2()

"""
gleichverteilt: 0
"""

for i in p2:
    print(i)
    t = throw(100000, i)
    e = entropie(t)
    print('entropy max = %f, measured = %f.' % e)
    dist(t)
    binomial(t, 1000)

