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

# ONE ARGUMENT: PERSON ID, ALL TIME ASSUMED
# TWO ARGUMENTS: ALL PEOPLE, TIME WINDOW
# THREE ARGUMENTS: PERSON ID, TIME WINDOW (CAN INTERPRET PERSON ID AS FIRST OR LAST ARGUMENT)

if len(sys.argv) == 2:
    person = sys.argv[1]
    fdate = 0
    tdate = int(2*1E7)

elif len(sys.argv) == 3:
    person = '-1'
    fdate = int(sys.argv[1])
    tdate = int(sys.argv[2])

elif len(sys.argv) == 4: 
    if int(sys.argv[1]) < 1E6: # FIRST ARGUMENT IS PERSON ID
        person = sys.argv[1]
        fdate = int(sys.argv[2])
        tdate = int(sys.argv[3])
    else: # LAST ARGUMENT IS PERSON ID
        person = sys.argv[3]
        fdate = int(sys.argv[1])
        tdate = int(sys.argv[2])

else:
    print('NEED ONE TO THREE ARGUMENTS:\n ONE ARGUMENT: PERSON ID, ALL TIME ASSUMED\n TWO ARGUMENTS: ALL PEOPLE, TIME WINDOW\n THREE ARGUMENTS: PERSON ID, TIME WINDOW (CAN INTERPRET PERSON ID AS FIRST OR LAST ARGUMENT)')
    sys.exit()

name = {}
name['40000'] = '-'

f = open('people_docs_auto')
for line in f:
    l = line.strip().split('\t')
    name[l[0]] = l[1]

f = open('added_people')
for line in f:
    l = line.strip().split('\t')
    name[l[0]] = l[1]

f = open('renamed_people')
for line in f:
    l = line.strip().split('\t')
    name[l[0]] = l[1]


def writeranking(d,s):
    global name
    ff = open('ins_'+s+'_'+sys.argv[1]+'_'+sys.argv[2],'w')
    for i in sorted(dict(d).items(),key=operator.itemgetter(1),reverse=True):
        ff.write(i[0]+'\t'+str(i[1])+'\t'+name[i[0]]+'\n')
    ff.close()

n = networkx.DiGraph()
f = open('fromto_all_place_mapped_sorted')
for line in f:
    l = line.strip().split('\t')
    if fdate <= int(l[2]) <= tdate:
        if n.has_edge(l[0],l[1]):
            w = n.get_edge_data(l[0],l[1])['weight']
            n.add_edge(l[0],l[1],weight=w+1)
        else:
            n.add_edge(l[0],l[1],weight=1)

d = n.degree()
od = n.out_degree()
id = n.in_degree()
wd = n.degree(weight='weight')
wod = n.out_degree(weight='weight')
wid = n.in_degree(weight='weight')

if person != '-1':
    if person in n.nodes():
        drnk = (sorted(dict(d).values(),reverse=True).index(d[person])+1)
        odrnk = (sorted(dict(od).values(),reverse=True).index(od[person])+1)
        idrnk = (sorted(dict(id).values(),reverse=True).index(id[person])+1)
        wdrnk = (sorted(dict(wd).values(),reverse=True).index(wd[person])+1)
        wodrnk = (sorted(dict(wod).values(),reverse=True).index(wod[person])+1)
        widrnk = (sorted(dict(wid).values(),reverse=True).index(wid[person])+1)
        print('ID\tfdate\ttdate\tdegree\tout-degree\tin-degree\tweighted degree\tweighted out-degree\tweighted in-degree\tname')
        print(str(person)+'\t'+str(fdate)+'\t'+str(tdate)+'\t'+str(d[person])+' ('+str(drnk)+', '+'{:.2f}'.format(100.0*drnk/len(d))+'%)\t'+str(od[person])+' ('+str(odrnk)+', '+'{:.2f}'.format(100.0*odrnk/len(od))+'%)\t'+str(id[person])+' ('+str(idrnk)+', '+'{:.2f}'.format(100.0*idrnk/len(id))+'%)\t'+str(wd[person])+' ('+str(wdrnk)+', '+'{:.2f}'.format(100.0*wdrnk/len(wd))+'%)\t'+str(wod[person])+' ('+str(wodrnk)+', '+'{:.2f}'.format(100.0*wodrnk/len(wod))+'%)\t'+str(wid[person])+' ('+str(widrnk)+', '+'{:.2f}'.format(100.0*widrnk/len(wid))+'%)\t'+str(name[person]))
        print('(Numbers in brackets give rank and percentage rank.)')
    else:
        print('Person ID '+str(person)+' is not in the network.')

if person == '-1':
    writeranking(d,'deg')
    writeranking(id,'ideg')
    writeranking(od,'odeg')
    writeranking(wd,'wdeg')
    writeranking(wid,'wideg')
    writeranking(wod,'wodeg')
