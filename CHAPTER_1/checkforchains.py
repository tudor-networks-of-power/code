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

def cumulpredecessors(i):
    global n
    old = -1
    s = set(n.predecessors(i))
    while old < len(s):
        old = len(s)
        ss = s.copy()
        for j in s:
            ss.update(n.predecessors(j))
        s = ss.copy()
    return list(s)

def cumulsuccessors(i):
    global n
    old = -1
    s = set(n.successors(i))
    while old < len(s):
        old = len(s)
        ss = s.copy()
        for j in s:
            ss.update(n.successors(j))
        s = ss.copy()
    return list(s)

def findroot(node):
    global n
    nodelist = []
    ns = len(n.successors(node))
    while ns == 1 and len(nodelist) == len(set(nodelist)):
        node = n.successors(node)[0]
        ns = len(n.successors(node))
        nodelist.append(node)
    if ns == 0 or node in n.successors(node):
        return (node,nodelist)
    if ns > 0 and node not in n.successors(node):
        return ('-',nodelist)

lsaved = {}
f = open('people_docs_auto')
n = networkx.DiGraph()
for line in f:
    l = line.strip().split('\t')
    lsaved[l[0]] = l
    if l[0] != l[2] and ',' not in l[2]:
        ll = l[2].replace(' ','').split(';')
        for i in ll:
            if i != '0':
                n.add_edge(l[0],i)
    
fn = open('added_people')
added = {}
for line in fn:
    a,b = line.strip().split('\t')
    added[a] = b

ff = open('checkforchains_ambiguities','w')
fff = open('checkforchains_straight','w')
namb = 0
nstr = 0
already = set([])
for i in n.nodes():
    if len(n.predecessors(i))-int(i in n.predecessors(i)) > 0 and len(n.successors(i))-int(i in n.successors(i)) > 0 and i not in already:
        j = findroot(i)
        if j[0] == '-':
            alreadytmp = set([])
            #print(cumulpredecessors(i),i,cumulsuccessors(i))
            alreadytmp.update(set(cumulpredecessors(i)))
            alreadytmp.update(set(cumulsuccessors(i)))
            alreadytmp.add(i)

            for k in sorted(list(alreadytmp)):
                if k in lsaved:
                    if len(lsaved[k][2]) > 20:
                        lsaved[k][2] = lsaved[k][2][:20]+'...'
                    if len(lsaved[k][3]) > 20:
                        lsaved[k][3] = lsaved[k][3][:20]+'...'
                    ff.write('\t'.join(lsaved[k])+'\n')

            ff.write('\n')
            already.update(alreadytmp)
            namb += 1
        else:
            if i in lsaved and (';' not in lsaved[i][2] or j[0] not in lsaved[i][2].replace(' ','').split(';')) and (',' not in lsaved[i][2] or j[0] not in lsaved[i][2].replace(' ','').split(',')) and i not in already: # IGNORE CASES WHERE ROOT MAPS TO ITSELF IN SOME CASES BUT NOT ALL (SEE 36081 FOR EXAMPLE). THESE WOULD BE UNCHANGED BY THE TRANSFORMATION BELOW, BUT BE COUNTED IN THE STATS AND PRINTED IN THE OUTPUT FILE.
                nstr += 1
                if j[0] in lsaved:
                    fff.write('======================\nROOT NODE:\n'+'\t'.join(lsaved[j[0]][:3]))
                else:
                    if j[0] in added:
                        fff.write('======================\nROOT NODE:\n'+str(j[0])+'\t'+str(added[j[0]]))
                fff.write('\n\nTRANSFORM:\n')
                cpset = set(cumulpredecessors(j[0]))
                for k in cpset:
                    fff.write('\t'.join(lsaved[k][:3])+'\n')
                for k in cpset:
                    if ';' not in lsaved[k][2] and ',' not in lsaved[k][2]:
                        lsaved[k][2] = j[0]
                    if ';' in lsaved[k][2] and ',' not in lsaved[k][2]:
                        lstmp = []
                        for kk in lsaved[k][2].replace(' ','').split(';'):
                            if kk not in cpset or kk == k: # DON'T CHANGE SELF-LOOPS AS THEY MAY POINT TO MORE GENERIC LABELS INTENTIONALLY (SEE ID 17827 FOR EXAMPLE)
                                lstmp.append(kk)
                            else:
                                lstmp.append(j[0])
                        lsaved[k][2] = '; '.join(lstmp)
                    if ';' not in lsaved[k][2] and ',' in lsaved[k][2]:
                        lstmp = []
                        for kk in lsaved[k][2].replace(' ','').split(','):
                            if kk not in cpset or kk == k: # SEE ABOVE
                                lstmp.append(kk)
                            else:
                                lstmp.append(j[0])
                        lsaved[k][2] = ', '.join(lstmp)
                    if ';' in lsaved[k][2] and ',' in lsaved[k][2]:
                        lstmp = []
                        for kk in lsaved[k][2].replace(' ','').split(','):
                            llstmp = []
                            for kkk in kk.split(';'):
                                if kkk not in cpset or kkk == k: # SEE ABOVE
                                    llstmp.append(kkk)
                                else:
                                    llstmp.append(j[0])
                            lstmp.append('; '.join(llstmp))
                        lsaved[k][2] = ', '.join(lstmp)
                fff.write('\nTO:\n')
                for k in cpset:
                    fff.write('\t'.join(lsaved[k][:3])+'\n')
                fff.write('\n')
            
            already.update(cpset)

ff.close()
fff.close()

print(str(namb)+' ambiguous chains.')
print(str(nstr)+' straight chains.')

"""

un = n.to_undirected()
straightfwd = 0
total = 0
for i in networkx.connected_components(un):
    flag = 0
    if len(i) > 3:
        for j in i:
            if n.in_degree(j)-int(j in n.predecessors(j)) > 0 and n.out_degree(j)-int(j in n.successors(j)) > 0:
                flag = 1
                break
    if flag == 1:
        outdegzero = 0
        root = ('-','')
        for j in i:
            outdegzero += int(n.out_degree(j) == 0)
            if n.out_degree(j) == 0:
                root = j
        print(n.subgraph(i).edges(),outdegzero)
        #if outdegzero > 1:
        #    for k in n.subgraph(i).edges():
        #        ffff.write('"'+str(k[0])+'" -> "'+str(k[1])+'";\n')
        straightfwd += int(outdegzero == 1)
        total += 1

        if outdegzero == 1:
            for j in sorted(i):
                if j in lsaved:
                    fff.write(str(lsaved[j][0])+'\t'+str(lsaved[j][1])+'\t'+str(root[0])+'\t'+str(lsaved[j][3])+'\n')
                else:
                    fff.write(str(j)+'\t added\n')

        if outdegzero != 1:
            for j in sorted(i):
                root = findroot(j)
                if root[0] != '-' and j in lsaved and j != root[0]:
                        fff.write(str(lsaved[j][0])+'\t'+str(lsaved[j][1])+'\t'+str(root[0])+'\t'+str(lsaved[j][3])+'\n')
                if root[0] == '-':
                    fffff.write(str(flag)+'\t'+str(j)+'\t'+str(root[1])+'\t'+str(n.subgraph(n.successors(j)).edges())+'\n')

fff.close()
ffff.write('}\n')
ffff.close()
fffff.close()

print(total,straightfwd)
"""
