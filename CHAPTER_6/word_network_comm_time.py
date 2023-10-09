#!/usr/bin/env python                                                           
import sys
import os
import random
import networkx
import community
import operator
#import matplotlib
#import pylab
import math
#import cPickle
import time
from collections import defaultdict

f = open('time_communities_list')
empty = f.readline()
fff = open('word_network_comm_time.out','w')
for line in f:
    l = line.strip()
    print(l)
    ff = open('PEAK_WORD_NETWORKS/'+str(l))
    n = networkx.Graph()
    for line2 in ff:
        if '"' in line2:
            ll = line2.strip().split('"')
            n.add_edge(ll[1],ll[3])
    if len(n.edges()) > 0:
        fff.write(str(l)+'\t'+str(len(n.nodes()))+'\t'+str(len(n.edges()))+'\t'+str(community.modularity(community.best_partition(n),n))+'\n')
fff.close()
