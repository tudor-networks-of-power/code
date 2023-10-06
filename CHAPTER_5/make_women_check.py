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

f = open('women_people_docs_2016')
ffull = open('people_docs')
ff = open('linked_data_consolidated_amend_all_final_edited')
ffff = open('added_people')
lm = set([])
ld = {}
mapped = defaultdict(list)
for line in f:
    l = line.strip().split('\t')
    mapset = set(l[2].replace(';',' ').replace(',',' ').split())
    for k in mapset:
        if k != '0':
            lm.add(int(k))
            if int(l[0]) != int(k):
                mapped[int(k)].append(int(l[0]))


for line in ffull:
    l = line.strip().split('\t')
    ld[int(l[0])] = l[1].replace('++ ','').replace('+ ','')

for line in ffff:
    l = line.strip().split('\t')
    ld[int(l[0])] = l[1]
    
link = {}
for line in ff:
    l = line.strip().split('\t')
    link[int(l[0])] = l[2]

fff = open('make_women_check.html','w')
fff.write('<html><body><table>')
c = 0
for i in sorted(lm):
    linkstr = ''
    if i in link:
        linkstr = '<a target="_blank" href="'+str(link[i])+'">Bio</a>'
    col = ''
    if c%2 == 1:
        col = ' style="background-color:rgb(200,200,200)"'
    c += 1
    fff.write('<tr'+str(col)+'><td>'+str(i)+'</td><td>'+str(linkstr)+'</td><td>'+str(ld[i])+'</td><td>')
    for j in mapped[i]:
        fff.write(str(ld[j])+'<br>')
    fff.write('</td></tr>\n')
fff.write('</table></body></html>')
fff.close()

fff = open('women_list_to_be_checked','w')
for i in sorted(lm):
    fff.write(str(i)+'\n')
fff.close()
