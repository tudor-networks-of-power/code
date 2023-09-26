#!/usr/bin/env python                                                           
import sys
import os
import random
import networkx
import operator
import matplotlib
import pylab
import math
from collections import defaultdict
import geopy
from geopy.distance import vincenty
import time

def tdist(d1,d2):
    #print(d1,d2)
    t1 = time.mktime((int(d1[:4])+2000,int(d1[4:6]),int(d1[6:8]),0,0,0,0,0,0))
    t2 = time.mktime((int(d2[:4])+2000,int(d2[4:6]),int(d2[6:8]),0,0,0,0,0,0))
    return abs(t1-t2)/(24*3600.0)
    
hist = defaultdict(int)
total = 0
f = open('fromto_all_place')
for line in f:
    l = line.strip().split('\t')
    if l[2] != '00000000' and l[3] != '00000000':
        hist[round(tdist(l[2],l[3]))] += 1
    total += 1

fff = open('lettertime_stats.out','w')
fff.write('# date uncertainty (days) \t number of letters (before mapping)\n')
for i in sorted(hist.items(),key=operator.itemgetter(0)):
    fff.write(str(i[0])+'\t'+str(i[1])+'\n')
fff.close()

print('\n=========================\nTotal letters: '+str(total))
print('Total letters with dates: '+str(sum(list(hist.values()))))
print('Letters with exact dates: '+str(hist[0]))
print('Letters with ten-day window: '+str(hist[10]))
print('Letters with a month-long window: '+str(hist[27]+hist[28]+hist[29]+hist[30]))
print('Letters with a year-long window: '+str(hist[364]+hist[365]))
print('Number of different time windows: '+str(len(hist.keys())))
print('\nFor a full histogram see lettertime_stats.out\nNote: All of these are measured on the raw letter data, i.e. before mapping IDs and splitting multiple individuals.\n=========================\n')
