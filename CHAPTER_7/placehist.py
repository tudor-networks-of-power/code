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

hist = defaultdict(int)
f = open('fromto_all_place_mapped_sorted_wplm_itineraries_final_final')
for line in f:
    l = line.strip().split('\t')
    for i in l[5].split(','):
        if i != '0':
            hist[i] += 1

ff = open('placehist_rank.out','w')
for i in sorted(hist.items(),key=operator.itemgetter(1),reverse=True):
    ff.write(str(i[0])+'\t'+str(i[1])+'\n')
ff.close()

ff = open('placehist_dist.out','w')
for i in sorted(list(set(hist.values()))):
    ff.write(str(i)+'\t'+str(hist.values().count(i))+'\n')
ff.close()

