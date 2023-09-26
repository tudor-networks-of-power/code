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

include_recipients = 0

increcstr = '_wo_rec' # NOTE: THIS IS TO PRESERVE ORIGINAL lettertimegaps OUTPUT FILES, WHICH WOULD HAVE '' HERE.
if include_recipients == 1:
    increcstr = '_w_rec'

def tdist(d1,d2):
    #print(d1,d2)
    t1 = time.mktime((int(d1[:4])+2000,int(d1[4:6]),int(d1[6:8]),0,0,0,0,0,0))
    t2 = time.mktime((int(d2[:4])+2000,int(d2[4:6]),int(d2[6:8]),0,0,0,0,0,0))
    return abs(t1-t2)/(24*3600.0)
    
gap = {}
gapcluster = defaultdict(list)
corr = defaultdict(list)
f = open('fromto_all_place_mapped_sorted')
for line in f:
    l = line.strip().split('\t')
    if l[2] != '00000000' and l[3] != '00000000':
        corr[l[0]].append((l[2],l[3],l[1]))
        if include_recipients == 1:
            corr[l[1]].append((l[2],l[3],l[0]))
        if (l[2],l[3]) not in gap:
            gap[(l[2],l[3])] = tdist(l[2],l[3])
        gapcluster[(l[2],l[3])].append(tuple(l))

dt = defaultdict(list)
for i in corr:
    for j in range(1,len(corr[i])):
        dt[i].append(tdist(corr[i][j-1][0],corr[i][j][0]))
        
ddt = {}
ddtl = {}
for i in dt:
    ddt[i] = max(dt[i])
    ddtl[i] = (corr[i][dt[i].index(ddt[i])],corr[i][dt[i].index(ddt[i])+1])

fff = open('lettertimegaps_subs'+increcstr,'w')
for i in sorted(ddt.items(),key=operator.itemgetter(1),reverse=True):
    fff.write(str(i)+'\t'+str(ddtl[i[0]])+'\n')
fff.close()

ffff = open('lettertimegaps_gaps'+increcstr,'w')
for i in sorted(gap.items(),key=operator.itemgetter(1),reverse=True):
    ffff.write(str(i[0])+'\t'+str(len(gapcluster[i[0]]))+'\t'+str(1.0*i[1]/365.241)+'\t'+str(gapcluster[i[0]][0])+'\n')
ffff.close()
