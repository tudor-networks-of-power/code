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

# ANNUAL
for year in range(1509,1604):
    curr = str(year)
    os.system('freq_hr - - '+curr+'0101 '+curr+'1231')

"""
# MONTHLY
for year in range(1509,1604):
    for month in range(1,13):
        curr = str(year)+'0'[0:int(month < 10)]+str(month)
        os.system('freq_hr - - '+curr+'00 '+curr+'99')
"""
