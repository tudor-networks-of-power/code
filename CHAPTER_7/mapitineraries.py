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

def tdist(d1,d2):
    if d1 != '00000000' and d2 != '00000000':
        t1 = time.mktime((int(d1[:4])+2000,int(d1[4:6]),int(d1[6:8]),0,0,0,0,0,0))
        t2 = time.mktime((int(d2[:4])+2000,int(d2[4:6]),int(d2[6:8]),0,0,0,0,0,0))
        return abs(t1-t2)/(24*3600.0)
    else:
        return 1E6

f = open('places_docs_final')
ff = open('fromto_all_place_mapped_sorted_wplm_itineraries_final_final')
fff = open('places.metadata')

name = {}
name['0'] = '-'
for line in f:
    l = line.strip().split('\t')
    name[l[0]] = l[1]

itin = defaultdict(list)
for line in ff:
    l = line.strip().split('\t')
    itin[int(l[0])].append(l)

coords = {}
for line in fff:
    l = line.strip().split('\t')
    coords[l[0]] = (l[1],l[2])
    
#ffff = open('itineraries','w')
ffff = open('itineraries_final_final','w')
c = 0
t = 0
itinc = defaultdict(list)
cind = {}
origtime = time.time()
all = len(itin)
for i in sorted(itin.keys()):
    t += 1
    print(t,i,len(itin[i]))
    if t%10 == 0:
        print(str((1.0/60)*(all-t)*(time.time()-origtime)/t)+' minutes remaining')
    cc = 0
    for j in itin[i]:
        print(j)
        if j[5] in coords:
            if j[5] not in name:
                name[j[5]] = 'new_place_look_up'
            reccoords = ('-','-')
            recname = '-'
            recplace = ('-',1E6)
            if int(j[1]) in itin:
                dtmin = 1E6
                for k in itin[int(j[1])]:
                    if dtmin > 0:
                        dt = min(tdist(j[2],k[2]),tdist(j[2],k[2]),tdist(j[3],k[2]),tdist(j[3],k[3]))
                        if dt < dtmin and k[5] != '0':
                            dtmin = dt
                            recplace = (k[5],dtmin)
                #print(recplace,c)
                if recplace[0] in coords:
                    reccoords = coords[recplace[0]]
                if recplace[0] in name:
                    recname = name[recplace[0]]
            ffff.write(str(c)+'\t'+str(coords[j[5]][0])+'\t'+str(coords[j[5]][1])+'\t'+str(name[j[5]])+'\t'+str(reccoords[0])+'\t'+str(reccoords[1])+'\t'+str(recname)+'\t'+str(recplace[0])+'\t'+str(recplace[1])+'\t'+'\t'.join(j)+'\t'+str(i)+'\n')
            if coords[j[5]] != ('-','-'):
                itinc[i].append(coords[j[5]])
                cind[i] = c
            cc = 1
        else:
            ffff.write('#\t-\t-\t-\t-\t-\t-\t'+'\t'.join(j)+'\t'+str(i)+'\n')
    c += cc
    ffff.write('\n\n')
ffff.close()

d = defaultdict(float)
for i in sorted(itinc.keys()):
    if len(itinc[i]) > 1:
        for j in range(1,len(itinc[i])):
            d[i] += vincenty(itinc[i][j-1],itinc[i][j]).miles
    
dl = {}
for i in coords.keys():
    if coords[i] != ('-','-'):
        dl[int(i)] = vincenty((51.515833, -0.092222),coords[i]).miles

#ffff = open('distances','w')
ffff = open('distances_final_final','w')
for i in sorted(d.items(),key=operator.itemgetter(1),reverse=True):
    ffff.write(str(i[0])+'\t'+str(i[1])+'\t'+str(cind[i[0]])+'\n')
ffff.close()

#ffff = open('distances_from_london','w')
ffff = open('distances_from_london_final_final','w')
for i in sorted(dl.items(),key=operator.itemgetter(1),reverse=True):
    if str(i[0]) not in name:
        name[str(i[0])] = 'new_name_look_up'
    ffff.write(str(i[0])+'\t'+str(i[1])+'\t'+str(name[str(i[0])])+'\n')
ffff.close()

