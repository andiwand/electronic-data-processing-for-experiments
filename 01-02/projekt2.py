#!/usr/bin/env python3

import time
import numpy as np

CPU_MODES = [ 'user', 'nice', 'system', 'idle', 'iowait', 'irq', 'softirq' ]

def readcpu():
    f = open('/proc/stat', 'r')
    cpu = f.readline()
    f.close()
    cpu = [int(i) for i in cpu.split()[1:]]
    cpu = np.array(cpu)
    return cpu

def estimatecpu(c1, c2):
    d = c2 - c1
    return d / np.sum(d)

def printcpu(cpu):
    cpu = cpu * 100
    print(" ".join("%s: %f%%" % (m, u) for m, u in zip(CPU_MODES, cpu)))

c1 = readcpu()
while True:
    time.sleep(2)
    c2 = readcpu()
    d = estimatecpu(c1, c2)
    printcpu(d)
    c1 = c2

