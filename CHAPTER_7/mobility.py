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

name = {}
f = open('people_docs_auto')
for line in f:
    l = line.strip().split('\t')
    name[l[0]] = l[1]

f = open('added_people')
for line in f:
    l = line.strip().split('\t')
    name[l[0]] = l[1]

f = open('renamed_people')
for line in f:
    l = line.strip().split('\t')
    name[l[0]] = l[1]

d = defaultdict(list)
#f = open('itineraries')
f = open('itineraries_final_final')
for line in f:
    l = line.strip().split('\t')
    #print(l, len(l))
    if line[0] != '#' and len(l) > 1:
        d[l[0]].append(l)
        
pl = defaultdict(set)
for i in d:
    for j in d[i]:
        pl[i].add(j[3])

jour = defaultdict(int)
for i in d:
    for j in range(len(d[i])-1):
        jour[i] += int(d[i][j][3] != d[i][j+1][3])
        
dist = {}
id = {}
#ff = open('distances')
ff = open('distances_final_final')
for line in ff:
    l = line.strip().split('\t')
    dist[l[2]] = float(l[1])
    id[l[2]] = l[0]

smob = {}
mob = {}
for i in d:
    if i in id:
        if jour[i] > 0:
            mob[id[i]] = [str(i),str(dist[i]),str(len(pl[i])),str(len(d[i])),str(1.0*dist[i]/len(d[i])),str(1.0*len(pl[i])/len(d[i])),str(jour[i]),str(1.0*dist[i]/jour[i]),str(1.0*len(pl[i])/jour[i])]
        if jour[i] == 0:
            mob[id[i]] = [str(i),str(dist[i]),str(len(pl[i])),str(len(d[i])),str(1.0*dist[i]/len(d[i])),str(1.0*len(pl[i])/len(d[i])),'0','0','0']
        smob[id[i]] = len(pl[i])

#fff = open('mobilities','w')
fff = open('mobilities_final_final','w')
for i in sorted(smob.items(),key=operator.itemgetter(1),reverse=True):
    fff.write('\t'.join(mob[i[0]])+'\t'+str(i[0])+'\t'+str(name[i[0]])+'\n')
fff.close()
