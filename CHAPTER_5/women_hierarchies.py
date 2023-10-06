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

whichgender = 'women'#'men'

women = set([])
fff = open('final_women.out')
for line in fff:
    women.add(line.strip())

fff = open('people_docs_auto')
fff2 = open('renamed_people')
fff3 = open('added_people')
    
name = {}
for line in fff:
    l = line.strip().split('\t')
    name[l[0]] = l[1]

for line in fff2:
    l = line.strip().split('\t')
    name[l[0]] = l[1]

for line in fff3:
    l = line.strip().split('\t')
    name[l[0]] = l[1]

ran = 0
if len(sys.argv) > 1:
    ran = int(sys.argv[1])

rstr = ''
if ran > 0:
    rstr = '_ran'+str(ran)

n = networkx.DiGraph()
edgetimes = defaultdict(list)
edgems = defaultdict(list)
mstimes = {}
f = open('fromto_all_place_mapped_sorted')
for line in f:
    l = line.strip().split('\t')
    #if ran == 1:
    #    if random.random() > 0.5:
    #        sw = l[0][:]
    #        l[0] = l[1][:]
    #        l[1] = sw[:]
    n.add_edge(l[0],l[1])
    #edgetimes[(l[0],l[1])].append(int(l[2]))
    #edgems[(l[0],l[1])].append(l[6])
    #mstimes[l[6]] = int(l[2])

if ran == 1:
    nnew = networkx.DiGraph()
    for i in n.edges():
        if not n.has_edge(i[1],i[0]) and random.random() > 0.5:
            nnew.add_edge(i[1],i[0])
        else:
            nnew.add_edge(i[0],i[1])
    n = nnew.copy()

"""
# EDGE SWAP VERY SLOW, AND ALSO FOR QUESTIONS ABOUT HIERARCHY IT'S BEST TO JUST RANDOMIZE EDGE DIRECTION (ran = 1) AND NOT TOPOLOGY
if ran == 2:
    le = len(n.edges())
    for it in range(le*10):
        if it%100 == 0:
            print(it)
        r = random.sample(n.edges(),2)
        if not n.has_edge(r[0][0],r[1][1]) and not n.has_edge(r[0][1],r[1][0]):
            n.add_edge(r[0][0],r[1][1])
            n.add_edge(r[0][1],r[1][0])
            n.remove_edge(r[0][0],r[0][1])
            n.remove_edge(r[1][0],r[1][1])
"""

mf = {}
mf[0] = 'm'
mf[1] = 'f'
gender = {}
for i in n.nodes():
    gender[i] = mf[int(i in women)]

excl_monarchs = 1 # EXCLUDES TRIADS IN WHICH ELIZABETH I, MARY I, OR MARY QUEEN OF SCOTS IS THE ONLY WOMAN

exclmstr = ''
if excl_monarchs == 1:
    exclmstr = '_excl_mon'

nn = n.to_undirected()
triangles = set([])
if whichgender == 'men':
    tset = set(nn.nodes())-set(women)
else:
    if excl_monarchs == 0:
        tset = set(women).intersection(set(nn.nodes())) # - set(['24679','24658','19699'])
    if excl_monarchs == 1:
        tset = set(women).intersection(set(nn.nodes())) - set(['24679','24658','19699'])
for i in tset:
    nl = nn.neighbors(i)
    for j in range(len(nl)):
        for k in range(j+1,len(nl)):
            if nn.has_edge(nl[j],nl[k]):
                s = tuple(sorted([i,nl[j],nl[k]]))
                if s not in triangles:
                    triangles.add(s)

if excl_monarchs == 0:
    print('Number of triads with at least one woman: '+str(len(triangles)))

if excl_monarchs == 1:
    print('Number of triads with at least one non-monarch (EI, MI, MQS) woman: '+str(len(triangles)))

pos1 = defaultdict(int)
pos2 = defaultdict(int)
pos3 = defaultdict(int)
total = defaultdict(int)

pos1dic = defaultdict(list)
pos2dic = defaultdict(list)
pos3dic = defaultdict(list)

for i in triangles:
    for j in i:
        if (gender[j] == 'f' and whichgender == 'women') or (gender[j] == 'm' and whichgender == 'men'):
            others = list(set(i)-set([j]))
            #pos1[j] += int(n.has_edge(j,others[0]))*int(n.has_edge(j,others[1]))
            #pos2[j] += int((int(n.has_edge(j,others[0]))*int(n.has_edge(others[1],j))*int(n.has_edge(others[1],others[0])) + int(n.has_edge(j,others[1]))*int(n.has_edge(others[0],j))*int(n.has_edge(others[0],others[1]))) > 0)
            #pos3[j] += int(n.has_edge(others[0],j))*int(n.has_edge(others[1],j))
            pos1[j] += int(n.has_edge(j,others[0]))*int(n.has_edge(j,others[1]))*(int(n.has_edge(others[0],others[1]))+int(n.has_edge(others[1],others[0])))
            pos2[j] += int(n.has_edge(j,others[0]))*int(n.has_edge(others[1],j))*int(n.has_edge(others[1],others[0])) + int(n.has_edge(j,others[1]))*int(n.has_edge(others[0],j))*int(n.has_edge(others[0],others[1]))
            pos3[j] += int(n.has_edge(others[0],j))*int(n.has_edge(others[1],j))*(int(n.has_edge(others[0],others[1]))+int(n.has_edge(others[1],others[0])))
            if int(n.has_edge(j,others[0]))*int(n.has_edge(j,others[1]))*(int(n.has_edge(others[0],others[1]))+int(n.has_edge(others[1],others[0]))) > 0:
                if n.has_edge(others[0],others[1]):
                    pos1dic[j].append((j,others[0],others[1]))

                if n.has_edge(others[1],others[0]):
                    pos1dic[j].append((j,others[1],others[0]))

            if int(n.has_edge(j,others[0]))*int(n.has_edge(others[1],j))*int(n.has_edge(others[1],others[0])) == 1:
                pos2dic[j].append((others[1],j,others[0]))

            if int(n.has_edge(j,others[1]))*int(n.has_edge(others[0],j))*int(n.has_edge(others[0],others[1])) == 1:
                pos2dic[j].append((others[0],j,others[1]))

            if int(n.has_edge(others[0],j))*int(n.has_edge(others[1],j))*(int(n.has_edge(others[0],others[1]))+int(n.has_edge(others[1],others[0]))) > 0:
                if n.has_edge(others[0],others[1]):
                    pos3dic[j].append((others[0],others[1],j))

                if n.has_edge(others[1],others[0]):
                    pos3dic[j].append((others[1],others[0],j))

            total[j] += 1

"""
for i in total:
    pos1[i] *= 1.0/total[i]
    pos2[i] *= 1.0/total[i]
    pos3[i] *= 1.0/total[i]
"""

pav = {}
for i in total:
    p = [pos1[i],pos2[i],pos3[i]]
    ps = sum(p)+int(sum(p) == 0)
    pav[i] = 1.0*pos1[i]/ps+2.0*pos2[i]/ps+3.0*pos3[i]/ps

if excl_monarchs == 0:
    print('Number of women that are part of triads: '+str(len(total)))

if excl_monarchs == 1:
    print('Number of women that are part of triads with at least one non-monarch (EI, MI, MQS) woman: '+str(len(total)))

cpos1 = 0
cpos2 = 0
cpos3 = 0
c = 0
ff = open(whichgender+'_hierarchies'+rstr+exclmstr+'.out','w')
fff = open(whichgender+'_hierarchies'+rstr+exclmstr+'.detail.out','w')
for ii in sorted(total.items(),key=operator.itemgetter(1),reverse=True):
    i = ii[0]
    p = [pos1[i],pos2[i],pos3[i]]
    pr = p.index(max(p))+1
    c += 1
    cpos1 += 1.0*pos1[i]/total[i]
    cpos2 += 1.0*pos2[i]/total[i]
    cpos3 += 1.0*pos3[i]/total[i]
    # NOTE: FACTOR OF 2 BEFORE c TAKES INTO ACCOUNT THAT THERE ARE TWO POSSIBLE DIRECTED TRIANGLES FOR EACH CASE
    ff.write(str(i)+'\t'+str(pos1[i])+'\t'+str(pos2[i])+'\t'+str(pos3[i])+'\t'+str(total[i])+'\t'+str(pr)+'\t'+str(pav[i])+'\t'+str(1.0*cpos1/(2*c))+'\t'+str(1.0*cpos2/(2*c))+'\t'+str(1.0*cpos3/(2*c))+'\t'+str(name[i])+'\n')

    fff.write(str(i)+'\t'+str(pos1[i])+'\t'+str(pos2[i])+'\t'+str(pos3[i])+'\t'+str(total[i])+'\t'+str(pr)+'\t'+str(pav[i])+'\t'+str(1.0*cpos1/(2*c))+'\t'+str(1.0*cpos2/(2*c))+'\t'+str(1.0*cpos3/(2*c))+'\t'+str(name[i])+'\nPosition 1:\n')
    for j in pos1dic[i]:
        for k in j:
            fff.write(name[k]+' ['+str(k)+']\t')
        fff.write('\n')
    fff.write('--------------------\nPosition 2:\n')
    for j in pos2dic[i]:
        for k in j:
            fff.write(name[k]+' ['+str(k)+']\t')
        fff.write('\n')
    fff.write('--------------------\nPosition 3:\n')
    for j in pos3dic[i]:
        for k in j:
            fff.write(name[k]+' ['+str(k)+']\t')
        fff.write('\n')
    fff.write('====================\n')

fff.close()
ff.close()



avpos1 = defaultdict(float)
avpos2 = defaultdict(float)
avpos3 = defaultdict(float)
avpr = defaultdict(float)
avpav = defaultdict(float)
avcpos1 = defaultdict(float)
avcpos2 = defaultdict(float)
avcpos3 = defaultdict(float)
stdcpos1 = defaultdict(float)
stdcpos2 = defaultdict(float)
stdcpos3 = defaultdict(float)

itmax = 10

# COMPREHENSIVE RANDOMIZATION
for it in range(itmax):
    print(it)
    nnew = networkx.DiGraph()
    for i in n.edges():
        if not n.has_edge(i[1],i[0]) and random.random() > 0.5: # THIS FLIPS EDGES WITH 50% PROBABILITY IF THERE IS NO RECIPROCAL EDGE
            nnew.add_edge(i[1],i[0])
        else:
            nnew.add_edge(i[0],i[1]) # IF THE EDGE IS RECIPROCAL THEN BOTH ARE ADDED THROUGH THIS (AS BOTH APPEAR IN THE FOR LOOP AND FAIL THE ABOVE CONDITION).
    n = nnew.copy()

    pos1 = defaultdict(int)
    pos2 = defaultdict(int)
    pos3 = defaultdict(int)
    total = defaultdict(int)

    for i in triangles:
        for j in i:
            if (gender[j] == 'f' and whichgender == 'women') or (gender[j] == 'm' and whichgender == 'men'):
                others = list(set(i)-set([j]))
                pos1[j] += int(n.has_edge(j,others[0]))*int(n.has_edge(j,others[1]))*(int(n.has_edge(others[0],others[1]))+int(n.has_edge(others[1],others[0])))
                pos2[j] += int(n.has_edge(j,others[0]))*int(n.has_edge(others[1],j))*int(n.has_edge(others[1],others[0])) + int(n.has_edge(j,others[1]))*int(n.has_edge(others[0],j))*int(n.has_edge(others[0],others[1]))
                pos3[j] += int(n.has_edge(others[0],j))*int(n.has_edge(others[1],j))*(int(n.has_edge(others[0],others[1]))+int(n.has_edge(others[1],others[0])))
                total[j] += 1

    pav = {}
    for i in total:
        p = [pos1[i],pos2[i],pos3[i]]
        ps = sum(p)+int(sum(p) == 0)
        pav[i] = 1.0*pos1[i]/ps+2.0*pos2[i]/ps+3.0*pos3[i]/ps

    cpos1 = 0
    cpos2 = 0
    cpos3 = 0
    c = 0
    for ii in sorted(total.items(),key=operator.itemgetter(1),reverse=True):
        i = ii[0]
        p = [pos1[i],pos2[i],pos3[i]]
        pr = p.index(max(p))+1
        c += 1
        # NOTE: FACTOR OF 2 TAKES INTO ACCOUNT THAT THERE ARE TWO POSSIBLE DIRECTED TRIANGLES FOR EACH CASE
        cpos1 += 1.0*pos1[i]/(2*total[i])
        cpos2 += 1.0*pos2[i]/(2*total[i])
        cpos3 += 1.0*pos3[i]/(2*total[i])

        avpos1[i] += 1.0*pos1[i]/itmax
        avpos2[i] += 1.0*pos2[i]/itmax
        avpos3[i] += 1.0*pos3[i]/itmax
        avpr[i] += 1.0*pr/itmax
        avpav[i] += 1.0*pav[i]/itmax
        avcpos1[i] += 1.0*cpos1/itmax
        avcpos2[i] += 1.0*cpos2/itmax
        avcpos3[i] += 1.0*cpos3/itmax
        stdcpos1[i] += 1.0*cpos1*cpos1/itmax
        stdcpos2[i] += 1.0*cpos2*cpos2/itmax
        stdcpos3[i] += 1.0*cpos3*cpos3/itmax
        

for i in total:
    stdcpos1[i] -= avcpos1[i]*avcpos1[i]
    stdcpos1[i] = math.sqrt(stdcpos1[i])
    stdcpos2[i] -= avcpos2[i]*avcpos2[i]
    stdcpos2[i] = math.sqrt(stdcpos2[i])
    stdcpos3[i] -= avcpos3[i]*avcpos3[i]
    stdcpos3[i] = math.sqrt(stdcpos3[i])

ff = open(whichgender+'_hierarchies_ran1_av'+exclmstr+'.out','w')
c = 1
for ii in sorted(total.items(),key=operator.itemgetter(1),reverse=True):
    i = ii[0]
    ff.write(str(i)+'\t'+str(avpos1[i])+'\t'+str(avpos2[i])+'\t'+str(avpos3[i])+'\t'+str(total[i])+'\t'+str(avpr[i])+'\t'+str(avpav[i])+'\t'+str(1.0*avcpos1[i]/c)+'\t'+str(1.0*avcpos2[i]/c)+'\t'+str(1.0*avcpos3[i]/c)+'\t'+str(1.0*stdcpos1[i]/c)+'\t'+str(1.0*stdcpos2[i]/c)+'\t'+str(1.0*stdcpos3[i]/c)+'\t'+str(name[i])+'\n')
    c += 1
ff.close()

