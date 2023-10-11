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

# CALCULATES NUMBER OF DAYS BETWEEN TWO DATES
def tdist(d1,d2):
    #print(d1,d2)
    if d1 != '00000000' and d2 != '00000000':
        t1 = time.mktime((int(d1[:4])+2000,int(d1[4:6]),int(d1[6:8]),0,0,0,0,0,0))
        t2 = time.mktime((int(d2[:4])+2000,int(d2[4:6]),int(d2[6:8]),0,0,0,0,0,0))
        return abs(t1-t2)/(24*3600.0)
    else:
        return 1E6

def lfac(s):
    return math.lgamma(s+1)

# CALCULATES PROBABILITY OF NO OVERLAP FOR TWO TIME PERIODS IN TOTAL TIME PERIOD (SEE EVERNOTE)
def calcp(s1,s2):
    T = tdist('15090101','16031231')
    #return 1.0-(1.0*(T-s1-s2)*(T-s1-s2))/((T-s1)*(T-s2))
    if T-s1-s2 >= 0:
        return math.exp(lfac(T-s1)+lfac(T-s2)-lfac(T)-lfac(T-s1-s2))
    else:
        return 0.0

# LOAD ITINERARIES INTO DICTIONARY KEYED BY PERSON ID
d = defaultdict(list)
f = open('itineraries_final_final')
for line in f:
    l = line.strip().split('\t')
    #print(l, len(l))
    if line[0] != '#' and len(l) > 1 and l[11] != '00000000':
        d[l[9]].append(l)
        
# CREATE PLACE SET
pl = defaultdict(set)
for i in d:
    for j in d[i]:
        pl[i].add(j[3])
 
# CREATE SEGMENT DICTIONARIES KEYED BY PERSON ID AND PLACE OF INTERVAL LISTS (seg) AND TOTAL INTERVAL DURATIONS (segd)
seg = {}
segd = {}
old = ''       
for i in d:
    seg[i] = defaultdict(list)
    segd[i] = defaultdict(float)
    start = -1
    for j in range(len(d[i])):
        if j == 0:
            start = d[i][j][11]
            stop = d[i][j][11]
            old = d[i][j][14]
        if j > 0 and d[i][j][14] == old:
            stop = d[i][j][11]
        if j > 0 and d[i][j][14] != old:
            seg[i][old].append((int(start),int(stop)))
            segd[i][old] += tdist(start,stop)+1
            start = d[i][j][11]
            stop = d[i][j][11]
            old = d[i][j][14]
    if i == '27756':
        print(d[i],i,start,stop,old)
    if start != -1:
        seg[i][old].append((int(start),int(stop)))
        segd[i][old] += tdist(start,stop)+1

# WRITE SEGMENT INFORMATION TO OUTPUT FILE
f = open('placeoverlap.seg_final_final','w')
for i in seg:
    for j in seg[i]:
        for k in seg[i][j]:
            f.write(str(i)+'\t'+str(j)+'\t'+str(k[0])+'\t'+str(k[1])+'\n')            
f.close()

# CREATE sigdist DICTIONARY OF SEGMENTS KEYED BY PLACE AND THEN INDIVIDUAL
sigdist = {}
for i in segd:
    for j in segd[i]:
        if j not in sigdist:
            sigdist[j] = {}
        if i not in sigdist[j]:
            sigdist[j][i] = segd[i][j]

# FOR EACH PLACE LOOK AT ALL PAIRS OF PEOPLE AND GENERATE PAIRWISE NULL MODEL PROBABILITIES pairp FOR THAT PLACE AND THOSE INDIVIDUALS
# THE AIM IS THEN TO CALCULATE A P-VALUE OF OVERLAP BY CHANCE FOR EACH PLACE AND EACH PAIR OF INDIVIDUALS, GIVEN THE DISTRIBUTION OF DURATIONS PEOPLE SPEND IN THIS PLACE.
dist = defaultdict(list)
pairp = {}
pv = {}
for i in sigdist:
    si = list(sigdist[i].items())
    if len(si) > 1:
        pairp[i] = {}
        for j in range(len(si)):
            for k in range(j+1,len(si)):
                p = 1-calcp(si[j][1],si[k][1]) # NULL MODEL PROBABILITY OF OVERLAP BY CHANCE GIVEN TWO TIME DURATIONS
                dist[i].append(p) # BUILDING CUMULATIVE DISTRIBUTION FOR p-value CALCULATION
                pairp[i][(si[j][0],si[k][0])] = p # BUILDING DICTIONARY OF PAIRWISE PROBABILITIES
                pairp[i][(si[k][0],si[j][0])] = p # DITTO

        dist[i].sort() # SORTING PROBABILITIES FOR P-VALUE CALCULATION
        psum = 0 # FOR BUILDING CUMULATIVE DISTRIBUTION
        pv[i] = {}
        for j in dist[i]:
            psum += j # BUILDING CUMULATIVE DISTRIBUTION
            pv[i][j] = psum # P-VALUE OF OVERLAP BY CHANCE FOR THIS PLACE, GIVEN THE DISTRIBUTION OF DURATIONS PEOPLE SPEND IN THIS PLACE. 

        #EXPLANATION OF ABOVE p-value: THE NULL MODEL PROBABILITY OF OBSERVING ANY PARTICULAR OVERLAP IS p*2.0/(N(N-1)) WHERE p IS THE SPECIFIC PROBABILITY GIVEN THE TIME WINDOWS OF TWO INDIVIDUALS. THE p-value IS THEN THE SUM OF ALL PROBABILITIES SMALLER OR EQUAL TO p, MULTIPLIED BY 2.0/(N(N-1)). TO BONFERRONI-CORRECT FOR A GIVEN LOCATION OVER ALL POSSIBLE HYPOTHESES (PAIRS OF PEOPLE) WE MULTIPLY BY N(N-1)/2 SO THE p-value IS JUST THE SUM OF ORDERED PROBABILITIES UP TO p.

# NOW WE IDENTIFY THE ACTUAL OVERLAPS
overlap = defaultdict(list)
sk = sorted(seg.keys())
for i in range(len(sk)): # LOOK AT ALL PEOPLE...
    print(i,len(sk))
    for j in range(i+1,len(sk)): # ...PAIRS AND CONSIDER ALL...
        for k in set(seg[sk[i]].keys()).intersection(set(seg[sk[j]].keys())): # ...PLACES THEY HAVE IN COMMON. THEN CONSIDER...
            for kk in seg[sk[i]][k]: # ...ALL SEGMENTS OF INDIVIDUAL A IN THAT PLACE, AND...
                for kkk in seg[sk[j]][k]: # ...ALL SEGMENTS OF INDIVIDUAL B IN THE SAME PLACE, AND...
                    ov = (max(kk[0],kkk[0]),min(kk[1],kkk[1])) # ...COMPARE START AND FINISH TIMES OF THE TWO SEGMENTS.
                    if ov[0] <= ov[1]: # IF THE LATER START TIME OF THE TWO IS EARLIER THAN THE EARLIER FINISH TIME OF THE TWO, WE HAVE AN OVERLAP.
                        overlap[(sk[i],sk[j])].append((k,ov,kk,kkk)) # RECORD THE OVERLAP       
                        overlap[(sk[j],sk[i])].append((k,ov,kkk,kk)) # DITTO

# BUILD DICTIONARY OF DATE OF FIRST COMMUNICATION BETWEEN TWO INDIVIDUALS
f = open('../fromto_all_place_mapped_sorted')
first = {}
for line in f:
    l = line.strip().split('\t')
    if (l[0],l[1]) not in first:
        first[(l[0],l[1])] = int(l[2])
        first[(l[1],l[0])] = int(l[2])

# WRITE ALL RESULTS OUT TO FILE
ff = open('placeoverlap.out_final_final','w')
for i in overlap:
    for j in overlap[i]:
        written = -1
        wrdate = '-'
        if (i[0],i[1]) in first:
            written = int(first[(i[0],i[1])] > j[1][0]) + int(first[(i[0],i[1])] > j[1][1])
            wrdate = str(first[(i[0],i[1])])
        ff.write(str(i[0])+'\t'+str(i[1])+'\t'+str(j[0])+'\t'+str(j[1][0])+'\t'+str(j[1][1])+'\t'+str(j[2][0])+'\t'+str(j[2][1])+'\t'+str(j[3][0])+'\t'+str(j[3][1])+'\t'+str(written)+'\t'+str(wrdate)+'\t'+str(pv[j[0]][pairp[j[0]][(i[0],i[1])]])+'\n')
ff.close()
