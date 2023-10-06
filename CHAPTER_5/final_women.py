#!/usr/bin/env python                                                           
import sys
import os
import random
import networkx
import operator
import matplotlib
import pylab
import math
from collections import defaultdict

f = open('women_list_to_be_checked')
ff = open('not_women_list')
fff = open('additional_women') # OVERRIDES not_women_list
ffff = open('additional_men') # OVERRIDES not_women_list

wl = set([])
for line in f:
    l = line.strip()
    wl.add(int(l))

nl = set([])
for line in ff:
    l = line.strip()
    nl.add(int(l))

for i in nl:
    if i not in wl:
        print(i)

fl = wl - nl

for line in fff:
    l = line.strip()
    fl.add(int(l))

for line in ffff:
    l = line.strip()
    if int(l) in fl:
        fl.remove(int(l))

fff = open('final_women.out','w')
for i in sorted(list(fl)):
    fff.write(str(i)+'\n')
fff.close()

ffff = open('fromto_all_place_mapped_sorted_women','w')
fa = open('fromto_all_place_mapped_sorted')
for line in fa:
    l = line.strip().split('\t')
    if int(l[0]) in fl and int(l[1]) in fl:
        ffff.write(line)
ffff.close()

ffff = open('fromto_all_place_mapped_sorted_at_least_one_woman','w')
fa = open('fromto_all_place_mapped_sorted')
for line in fa:
    l = line.strip().split('\t')
    if int(l[0]) in fl or int(l[1]) in fl:
        ffff.write(line)
ffff.close()

ffff = open('fromto_all_place_mapped_sorted_wtm','w')
fa = open('fromto_all_place_mapped_sorted')
for line in fa:
    l = line.strip().split('\t')
    if int(l[0]) in fl and int(l[1]) not in fl:
        ffff.write(line)
ffff.close()

ffff = open('fromto_all_place_mapped_sorted_mtw','w')
fa = open('fromto_all_place_mapped_sorted')
for line in fa:
    l = line.strip().split('\t')
    if int(l[0]) not in fl and int(l[1]) in fl:
        ffff.write(line)
ffff.close()

