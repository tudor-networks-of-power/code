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
    if d1 != '00000000' and d2 != '00000000':
        t1 = time.mktime((int(d1[:4])+2000,int(d1[4:6]),int(d1[6:8]),0,0,0,0,0,0))
        t2 = time.mktime((int(d2[:4])+2000,int(d2[4:6]),int(d2[6:8]),0,0,0,0,0,0))
        return abs(t1-t2)/(24*3600.0)
    else:
        return 1E6

d = defaultdict(list)
f = open('itineraries_final_final')
for line in f:
    l = line.strip().split('\t')
    #print(l, len(l))
    if line[0] != '#' and len(l) > 1:
        d[l[0]].append(l)

v = {}
detail = {}
for i in d:
    #print(i,d[i])
    for j in range(len(d[i])-1):
        #print(j,i)
        if d[i][j][11] == d[i][j][12] and d[i][j+1][11] == d[i][j+1][12]:
            dt = 1+tdist(d[i][j+1][11],d[i][j][11])
            if d[i][j][1] != '-' and d[i][j+1][1] != '-':
                ds = vincenty((float(d[i][j+1][1]),float(d[i][j+1][2])),(float(d[i][j][1]),float(d[i][j][2]))).miles
                v[str(i)+'_'+str(j)] = 1.0*ds/dt
                detail[str(i)+'_'+str(j)] = (v[str(i)+'_'+str(j)],ds,dt,d[i][j],d[i][j+1])

ff = open('velocities','w')
for i in sorted(v.items(),key=operator.itemgetter(1),reverse=True):
    #ff.write(str(i[0].split('_')[0])+'\t'+str(i[0].split('_')[1])+'\t'+str(i[1])+'\n')
    dd = detail[i[0]]
    ff.write(str(dd[-2][9])+' writing to '+str(dd[-2][10])+' from '+str(dd[-2][3])+' on '+str(dd[-2][11])+', and to '+str(dd[-1][10])+' from '+str(dd[-1][3])+' ('+str(int(dd[1]))+'km away) on '+str(dd[-1][11])+' ('+str(int(dd[2])-1)+' days later).\n')
ff.close()