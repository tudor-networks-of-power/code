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

d = defaultdict(list)
for i in range(1509,1604):
    f = open('FREQ_HR_OUT/freq_hr_-_-_'+str(i)+'0101_'+str(i)+'1231.out')
    for line in f:
        l = line.split()
        d[l[1]].append((i,int(l[0][:-1])))

diff = {}
for i in d:
    l = []
    for j in d[i]:
        l.append(j[1])
    if i[:2] not in ['x0','x2']:
        diff[i] = math.log(max(l))-math.log(min(l))

ds = sorted(diff.items(),key=operator.itemgetter(1))

for i in ds:
    if not i[0].isdigit():
        print(i)
    #print(d[i[0]])

ff = open('extractchanges.out','w')
ds = sorted(diff.items(),key=operator.itemgetter(1),reverse=True)
for i in ds:
    if not i[0].isdigit():
        ff.write(str(i[0])+'\t'+str(i[1])+'\n')
ff.close()
