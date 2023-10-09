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

peakthresh = 1000 # MAXIMUM RANK TO BE COUNTED AS PART OF A PEAK

p = {}
f = open('extractchanges_profiles.script.sh')
empty = f.readline()
for line in f:
    l = line.strip().split(' ')
    p[l[1]] = {}
    ff = open('CHANGE_PROFILES/'+str(l[1])+'.profile')
    for line2 in ff:
        ll = line2.strip().split()
        if float(ll[1]) < peakthresh:
            p[l[1]][int(ll[0])] = float(ll[1])

maxgap = 3 # MAX GAP IN YEARS BEFORE WE SPLIT PEAKS
peaks = defaultdict(list)
for i in p:
    if len(p[i]) > 1:
        #print()
        tmppeak = []
        pik = sorted(p[i].keys())
        for j in range(len(pik)-1):
            tmppeak.append(pik[j])
            gap = int(pik[j+1])-int(pik[j])
            if gap > maxgap*10000:
                peaks[i].append(tmppeak)
                tmppeak = []
        peaks[i].append(tmppeak)

for i in peaks.keys():
    #print(p[i])
    #print(sorted(p[i].keys()))
    #print(peaks[i])
    for j in peaks[i]:
        if len(j) > 0:
            os.system('python extractwordnetwork_for_peaks.py '+str(i)+' 0 '+str(j[0])[:4]+'0000 '+str(j[-1])[:4]+'9999')
            print('python extractwordnetwork_for_peaks.py '+str(i)+' 0 '+str(j[0])[:4]+'0000 '+str(j[-1])[:4]+'9999')
