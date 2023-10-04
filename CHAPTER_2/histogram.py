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

f = open(sys.argv[1])

bin = 1.0

if len(sys.argv) > 2:
    bin = float(sys.argv[2])

l = []
for line in f:
    a = line.strip()
    l.append(a)
    
d = defaultdict(int)
for i in l:
    if len(sys.argv) > 3: 
        if sys.argv[3] == '0':
            d[bin*int(1.0*((float(i)))/bin)] += 1
        if sys.argv[3] == '1' and float(i) > 0:
            d[bin*int(1.0*(math.log(float(i),10))/bin)] += 1
    else:
        d[bin*int(1.0*((float(i)))/bin)] += 1

#for i in sorted(d.items(),key=operator.itemgetter(1)):
#    print(str(i[0])+'\t'+str(i[1]))

for i in sorted(d.items(),key=operator.itemgetter(0)):
    print(str(i[0])+'\t'+str(i[1]))

    
