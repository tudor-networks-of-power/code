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

os.system('mkdir FREQ_HR_OUT')

# ANNUAL                                                                                                                                             
for year in range(1509,1604):
    curr = str(year)
    os.system('freq_hr - - '+curr+'0101 '+curr+'1231')
