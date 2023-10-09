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

def exhex(n):
    z = '0'
    return z[:int(n < 16)]+hex(n)[-1-int(n > 16):]
           
ff = open('fromto_all_place_mapped_sorted')
fff = open('people_docs_auto')
fff2 = open('renamed_people')
fff3 = open('added_people')

os.system('tudor_seb whindexsearch.py '+str(sys.argv[1]))

f = open('out')
letters = set([])
for line in f:
    a = line.strip()
    letters.add(a)

# WHETHER TO REMOVE NODES THAT HAVE THE SEARCH ARGUMENT IN THEIR NAME
removename = int(sys.argv[2])

fdate = 0
tdate = 20000000
if len(sys.argv) > 3:
    fdate = int(sys.argv[3])
    tdate = int(sys.argv[4])

edges = []
net = networkx.DiGraph()
edgetime = {}
edgetimeall = defaultdict(list)
edgetimecount = {}
count = 1
for line in ff:
    l = line.strip().split('\t')
    if (l[6] in letters) and int(l[2]) >= fdate and int(l[3]) <= tdate: 
        edges.append((l[0],l[1]))
        net.add_edge(l[0],l[1])
        if (l[0],l[1]) not in edgetime:
            edgetime[(l[0],l[1])] = int(l[2])
            edgetimecount[(l[0],l[1])] = count
            count += 1
        if l[2] != l[3]:
            edgetimeall[(l[0],l[1])].append((l[2],l[3]))
        else:
            edgetimeall[(l[0],l[1])].append(l[2])
        
name = {}
for line in fff:
    l = line.strip().split('\t')
    name[l[0]] = l[1]+'\\n['+l[0]+']'

for line in fff2:
    l = line.strip().split('\t')
    name[l[0]] = l[1]+'\\n['+l[0]+']'

for line in fff3:
    l = line.strip().split('\t')
    name[l[0]] = l[1]+'\\n['+l[0]+']'

if len(sys.argv) == 3:
    sss = sys.argv[1]+'_'+sys.argv[2]
if len(sys.argv) == 5:
    sss = sys.argv[1]+'_'+sys.argv[2]+'_'+sys.argv[3]+'_'+sys.argv[4]

os.system('mkdir PEAK_WORD_NETWORKS')
ffff = open('PEAK_WORD_NETWORKS/'+str(sss)+'.dot','w')
ffff.write('digraph '+str(sss)+'{')
already = set([])
ealready = set([])
minedgetime = 1E12
maxedgetime = -1
for i in edges:
    if i not in ealready and (removename == 0 or (sys.argv[1].lower() not in name[i[0]].lower() and sys.argv[1].lower() not in name[i[1]].lower())):
        if edgetime[i] < minedgetime:
            minedgetime = edgetime[i]
        print(edgetime[i],minedgetime)
        if edgetime[i] > maxedgetime:
            maxedgetime = edgetime[i]

if minedgetime < 15090101:
    minedgetime = 15090101

if maxedgetime > 16041231:
    maxedgetime = 16041231

for i in edges:
    if i not in ealready and (removename == 0 or (sys.argv[1].lower() not in name[i[0]].lower() and sys.argv[1].lower() not in name[i[1]].lower())):
        c = int(255.0*(edgetime[i]-minedgetime)/(maxedgetime-minedgetime)) 
        cc = 255-int(255.0*(edgetime[i]-minedgetime)/(maxedgetime-minedgetime)) 
        #print(edgetime[i],maxedgetime,minedgetime,c)
        if edgetimeall[i][0] != edgetimeall[i][-1]:
            ffff.write('"'+str(name[i[0]])+'" -> "'+str(name[i[1]])+'" [color="#'+exhex(c)+'00'+exhex(cc)+'",label="order: '+str(edgetimecount[i])+'\\nfrom: '+str(edgetimeall[i][0])+'\\nletters: '+str(len(edgetimeall[i]))+'\\nuntil: '+str(edgetimeall[i][-1])+'"];\n')
        if len(edgetimeall[i]) == 1:
            ffff.write('"'+str(name[i[0]])+'" -> "'+str(name[i[1]])+'" [color="#'+exhex(c)+'00'+exhex(cc)+'",label="order: '+str(edgetimecount[i])+'\\n on:'+str(edgetimeall[i][0])+'"];\n')
        ealready.add(i)

ffff.write('\n}\n')
ffff.close()

