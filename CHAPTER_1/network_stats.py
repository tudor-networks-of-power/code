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

f = open('fromto_all_place_mapped_sorted')
ff = open('coauthnet')
fff = open('corecpnet')

let = networkx.Graph()
aut = networkx.Graph()
rec = networkx.Graph()

nl = 0
na = 0
nr = 0

letaut = 0
letrec = 0
autrec = 0
letautrec = 0

for line in f:
    l = line.strip().split('\t')
    let.add_edge(l[0],l[1])
    nl += 1

for line in ff:
    l = line.strip().split('\t')
    aut.add_edge(l[0],l[1])
    na += 1

for line in fff:
    l = line.strip().split('\t')
    rec.add_edge(l[0],l[1])
    nr += 1

for i in let.edges():
    a = int(aut.has_edge(*i))
    r = int(rec.has_edge(*i))
    letaut += a
    letrec += r
    letautrec += a*r

for i in aut.edges():
    r = int(rec.has_edge(*i))
    autrec += r

letautrecdic = defaultdict(int)

for i in let.edges():
    letautrecdic[(1,int(aut.has_edge(*i)),int(rec.has_edge(*i)))] += 1.0/(1+int(aut.has_edge(*i))+int(rec.has_edge(*i)))

for i in aut.edges():
    letautrecdic[(int(let.has_edge(*i)),1,int(rec.has_edge(*i)))] += 1.0/(int(let.has_edge(*i))+1+int(rec.has_edge(*i)))

for i in rec.edges():
    letautrecdic[(int(let.has_edge(*i)),int(aut.has_edge(*i)),1)] += 1.0/(int(let.has_edge(*i))+int(aut.has_edge(*i))+1)

print('')
print('Number of records:')
print(' Letters (after separating out multiple senders and recipients): '+str(nl))
print(' Co-author instances: '+str(na))
print(' Co-recipient instances: '+str(nr))
print('')
print('Number of nodes: '+str(len(let.nodes()))+'\n')
print('Number of edges:')
print(' Letter network: '+str(len(let.edges())))
print(' Co-author network: '+str(len(aut.edges())))
print(' Co-recipient network: '+str(len(rec.edges())))
print('')
print('Edge overlaps:')
print(' Letters & co-authors: '+str(letaut))
print(' Letters & co-recipients: '+str(letrec))
print(' Co-authors & co-recipients: '+str(autrec))
print(' Letters, co-authors & co-recipients: '+str(letautrec))
print('')

print('let aut rec')
for i in sorted(list(letautrecdic.keys())):
    print(str(i)+'\t'+str(letautrecdic[i]))
