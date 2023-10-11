#!/usr/bin/env python                                                           
import sys
import os
import random
import networkx
import operator
import matplotlib
#import pylab
import math
from collections import defaultdict
import geopy
from geopy.distance import vincenty
import time

nl = {}
f = open('placehist_rank.out')
for line in f:
    l = line.strip().split('\t')
    nl[l[0]] = int(l[1])

radius = 10.0
gl = 0
ff = open('distances_from_london_final_final')
for line in ff:
    l = line.strip().split('\t')
    if float(l[1]) <= radius and l[0] in nl:
        gl += nl[l[0]]

print(str(gl)+' letters from within a '+str(radius)+' mile radius of the City of London.')
