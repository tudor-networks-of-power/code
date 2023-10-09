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

ff = open('freq_hr.tmp','w')

f = open('fromto_all_place_mapped_sorted')
for line in f:
    l = line.strip().split('\t')
    if (',' not in sys.argv[1] and sys.argv[1] in ['-',l[0]]) or (',' in sys.argv[1] and l[0] in sys.argv[1].split(',')):
        #print(line,sys.argv[2])
        if (',' not in sys.argv[2] and sys.argv[2] in ['-',l[1]]) or (',' in sys.argv[2] and l[1] in sys.argv[2].split(',')):
            #print(line)
            if sys.argv[3] == '-' or int(l[2]) >= int(sys.argv[3]):
                if sys.argv[4] == '-' or int(l[3]) <= int(sys.argv[4]):
                    ff.write(str(l[6])+'\n')
ff.close()

os.system('python whindexfreq.py freq_hr.tmp 5000')
os.system('mv freq_hr.tmp.whfreq FREQ_HR_OUT/freq_hr_'+str('_'.join(sys.argv[1:]))+'.out')
