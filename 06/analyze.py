#!/usr/bin/env python3

import sys
from getopt import *
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    opt=getopt(sys.argv[1:], "i:")
    
    rate = 44100#22050
    in_filename='record16.dat'
    
    for o in opt[0]:
       if o[0]=='-i': in_filename=o[1]

    fidat = open(in_filename, "r")
    amps = np.array([int(line) for line in fidat.readlines()])
    amps_x = np.arange(0, len(amps)/rate, 1./rate)
    plt.plot(amps_x, amps)
    plt.show()

    x = np.fft.rfftfreq(len(amps), d=1/rate)
    fqs = np.abs(np.fft.rfft(amps))
    plt.plot(x, fqs)
    plt.show()

