#!/usr/bin/env python                                                           
import sys
import os
import random
import networkx
import operator
#import matplotlib
#import pylab
import math
#import cPickle
import time
from collections import defaultdict

fnlist = [('hen.deg.hist','Henry VIII'),('edw.deg.hist','Edward VI'),('mar.deg.hist','Mary I'),('eli.deg.hist','Elizabeth I'),('all.deg.hist','Tudor period')]

for fn in fnlist:
    print('\n'+fn[1]+':')
    f = open(fn[0])
    l = []
    total = 0
    for line in f:
        a,b = line.strip().split('\t')
        l.append((float(a),float(b)))
        total += float(b)
    
    perc = 0
    for i in l:
        perc += 100.0*i[1]/total
        print(str(fn[1])+': '+str(perc*total/100)+' people ('+str(perc)+'%) have degree less than or equal to '+str(i[0]))

    l.reverse()

    print(' ')
    
    perc = 0
    for i in l:
        perc += 100.0*i[1]/total
        print(str(fn[1])+': '+str(perc*total/100)+' people ('+str(perc)+'%) have degree greater or equal to '+str(i[0]))
    
