#!/usr/bin/env python3

import math
import numpy as np
import matplotlib.path as mpath
import matplotlib.pyplot as plt

# geocoordinates as (lat, lon)

RADIUS = 6370000 # m
NUMBERS = 10**4

def readdata(path):
    data = np.genfromtxt(path, delimiter=',')
    #data[:,0:2] = np.radians(data[:,0:2])
    data = data[:, :-1]
    return data

def orthodrome(start, end):
    # distance in radians between start and end
    return np.arccos(np.sin(start[0]) * np.sin(end[0]) + np.cos(start[0]) * np.cos(end[0]) * np.cos(end[1] - start[1]))

def umfang(data):
    data = np.radians(data)
    result = 0
    for i in range(-1, len(data) - 1):
        result += orthodrome(data[i], data[i + 1])
    return result * RADIUS

def umfang2(data):
    data = np.radians(data)
    return np.sum(orthodrome(data.T, np.roll(data, -1, axis=0).T)) * RADIUS

def viereck(min, max):
    return (max[1] - min[1]) * (np.cos(min[0]) - np.cos(max[0])) * RADIUS ** 2

def flaeche_schwerpunkt(data, n):
    data = np.radians(data)
    data[:,0] = np.pi * 0.5 - data[:,0]
    min, max = np.min(data, axis=0), np.max(data, axis=0)
    bounds = viereck(min, max)
    
    points = np.column_stack((np.random.uniform(min[0], max[0], n), np.random.uniform(min[1], max[1], n)))
    inside = mpath.Path(data).contains_points(points)
    
    p = np.sum(inside) / n
    mean = p * bounds
    var = p * (1 - p) / n * bounds
    
    pointsin = points[inside]
    schwerpunkt = np.average(pointsin, axis=0, weights=np.sin(pointsin[:,0]))
    schwerpunkt[0] = np.pi * 0.5 - schwerpunkt[0]
    schwerpunkt = np.degrees(schwerpunkt)
    
    #plt.plot(data[:,0], data[:,1])
    #plt.scatter(pointsin[:,0], pointsin[:,1])
    #plt.show()
    
    return mean, var, schwerpunkt

data = readdata('gps.csv')
u = umfang(data[:,0:2])
print('umfang: %f km' % (u * 1E-3))
# 2706 km
f = flaeche_schwerpunkt(data[:,0:2], NUMBERS)
# 83,879 km^2
print('flaeche %f +/- %f km^2' % (f[0] * 1E-9, f[1] * 1E-9))
# 47.61°, 13.782778°
print('schwerpunkt %s' % f[2])

