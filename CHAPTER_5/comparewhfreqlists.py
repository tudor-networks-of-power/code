#!/usr/bin/env python                                                           
import sys
import os
import random
import networkx
import operator
#import matplotlib
#import pylab
import math
from collections import defaultdict

f = open(sys.argv[1])
ff = open(sys.argv[2])

rank1 = {}
for line in f:
    l = line.strip().split()
    rank1[l[1]] = int(l[0][:-1])

rank2 = {}
for line in ff:
    l = line.strip().split()
    rank2[l[1]] = int(l[0][:-1])

normrd = {}
for i in sorted(list(set(rank1.keys()).intersection(rank2.keys()))):
    normrd[i] = math.log(rank1[i])-math.log(rank2[i])

fff = open('comparewhfreqlists.out','w')
fff.write('log rank 1 - log rank 2\trank in '+sys.argv[1]+'\trank in '+sys.argv[2]+'\n')
for i in sorted(normrd.items(),key=operator.itemgetter(1),reverse=True):
    fff.write(str(i[0])+'\t'+str(i[1])+'\t'+str(rank1[i[0]])+'\t'+str(rank2[i[0]])+'\n')
fff.close()
    
