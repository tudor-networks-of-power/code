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

f = open('places_docs_final')
ff = open('place_disambiguation_spreadsheet_new_final.txt')
fff = open('fromto_all_place_mapped_sorted')

print('Reading place metadata...')

plm = {}
url = {}
coord = {}
for line in ff:
    l = line.strip().split('\t')
    #print(line)
    plm[l[0]] = l[1:]
    url[l[0]] = '-'
    coord[l[0]] = '-'

print('Reading places_docs...')

name = {}
number = {}
ms = {}
map = {}
mapnet = networkx.DiGraph()
for line in f:
    l = line.strip().split('\t')
    name[l[0]] = l[1]
    number[l[1]] = l[0]
    ms[l[0]] = l[3]
    map[l[0]] = l[2].replace(' ','')
    if ';' not in map[l[0]]:
        mapnet.add_edge(l[0],map[l[0]])
    if ';' in map[l[0]]:
        for i in map[l[0]].split(';'):
            mapnet.add_edge(l[0],i.strip())
    if ',' in map[l[0]]:
        for i in map[l[0]].split(','):
            mapnet.add_edge(l[0],i.strip())

print('Reading fromto...')

ft = []
for line in fff:
    l = line.strip().split('\t')
    ft.append(l)

print('Mapping...')
c = 0
ffff = open('fromto_all_place_mapped_sorted_wplm','w')
erralready = set([])
for i in ft:
    ftm = i[:]
    ftm[5] = 0
    if i[5] in number and i[4] in ms[number[i[5]]].split():
        if ';' not in map[number[i[5]]]:
            ftm[5] = map[number[i[5]]]
        elif ';' in map[number[i[5]]]:
            if len(ms[number[i[5]]].split()) == len(map[number[i[5]]].split(';')):
                ftm[5] = map[number[i[5]]].split(';')[ms[number[i[5]]].split().index(i[4])]
            else:
                if number[i[5]] not in erralready:
                    print('\ndocument mismatch for '+str(number[i[5]])+':')#+str(len(ms[number[i[5]]].split()))+' versus '+str(len(map[number[i[5]]].split(';'))))
                    #print(i)
                    print(i[5],ms[number[i[5]]],map[number[i[5]]])
                    erralready.add(number[i[5]])

    if i[5] in number and i[4] not in ms[number[i[5]]].split(): # WHICH MAY HAPPEN BECAUSE OF specific_replace
        if ';' not in map[number[i[5]]]:
            ftm[5] = map[number[i[5]]]
            print(i)
                
        # NOTE THAT MULTIPLE COMMA-SEPARATED PLACES ARE JUST REPLACED BY COMMA-SEPARATED IDS IN FROMTO FILE. LINES BELOW HANDLE EXCEPTIONS WHEN NUMBERS OF PLACES DON'T MATCH UP BETWEEN NAME FIELD AND MAPPED ID FIELD
        if ',' in map[number[i[5]]] and not (len(i[5].split(';')) == len(map[number[i[5]]].split(',')) or len(i[5].split(',')) == len(map[number[i[5]]].split(','))): 
            if number[i[5]] not in erralready:
                print('\nmultiple place mismatch for '+str(number[i[5]])+':')# '+str(len(ms[number[i[5]]].split()))+' versus '+str(len(map[number[i[5]]].split(','))))
                #print(i)
                print(i[5],ms[number[i[5]]],map[number[i[5]]])
                erralready.add(number[i[5]])

    c += 1
    
    for j in ftm:
        ffff.write(str(j)+'\t')
    ffff.write('\n')

ffff.close()

