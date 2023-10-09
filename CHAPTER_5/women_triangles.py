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

n = networkx.DiGraph()
edgetimes = defaultdict(list)
edgems = defaultdict(list)
mstimes = {}
f = open('fromto_all_place_mapped_sorted')
for line in f:
    l = line.strip().split('\t')
    n.add_edge(l[0],l[1])
    edgetimes[(l[0],l[1])].append(int(l[2]))
    edgems[(l[0],l[1])].append(l[6])
    mstimes[l[6]] = int(l[2])

mf = {}
mf[0] = 'm'
mf[1] = 'f'
gender = {}
for i in n.nodes():
    gender[i] = mf[int(i in women)]

nn = n.to_undirected()
triangles = set([])
for i in set(women).intersection(set(nn.nodes())) - set(['24679','24658','19699']):
    nl = nn.neighbors(i)
    for j in range(len(nl)):
        for k in range(j+1,len(nl)):
            if nn.has_edge(nl[j],nl[k]):
                s = tuple(sorted([i,nl[j],nl[k]]))
                if s not in triangles:
                    triangles.add(s)

print(len(triangles)) 

networkx.set_node_attributes(n,'gender',gender)
nm = networkx.algorithms.isomorphism.categorical_node_match('gender','-')

library = []
librarydic = defaultdict(list)
for i in triangles:
    tmp = n.subgraph(list(i))
    dontadd = 0
    for j in range(len(library)):
        dontadd += int(networkx.is_isomorphic(tmp,library[j],node_match=nm))
        if dontadd == 1:
            break
    if dontadd == 0:
        library.append(tmp)
        librarydic[j].append(i)
    if dontadd == 1:
        librarydic[j].append(i)

os.system('mkdir WOMEN_TRIANGLES')
fout = open('WOMEN_TRIANGLES/women_triangles.out','w')
for i in range(len(library)):
    fout.write(str(len(librarydic[i]))+'\t')
    for j in library[i].edges():
        fout.write(str(sorted(library[i].nodes()).index(j[0]))+str(gender[j[0]])+'->'+str(sorted(library[i].nodes()).index(j[1]))+str(gender[j[1]])+' ')
    fout.write('\n')
    for j in sorted(librarydic[i]):
        fout.write(str(name[j[0]])+' ['+str(j[0])+']\t'+str(name[j[1]])+' ['+str(j[1])+']\t'+str(name[j[2]])+' ['+str(j[2])+']\n')
    fout.write('\n')
fout.close()

col = {}
col['m'] = '#AACCFF'
col['f'] = '#FFCCAA'

for i in range(len(library)):
    fout = open('WOMEN_TRIANGLES/women_triangles_'+str(i)+'.dot','w')
    fout.write('digraph t\n{\n')
    for j in library[i].nodes():
        fout.write('"'+str(sorted(library[i].nodes()).index(j))+str(gender[j])+'" [label="'+str(gender[j].upper())+'",shape="circle",style="filled",color="'+col[gender[j]]+'"];\n')
    for j in library[i].edges():
        fout.write('"'+str(sorted(library[i].nodes()).index(j[0]))+str(gender[j[0]])+'" -> "'+str(sorted(library[i].nodes()).index(j[1]))+str(gender[j[1]])+'";\n')
    fout.write('\n}\n')
    fout.close()
    os.system('neato WOMEN_TRIANGLES/women_triangles_'+str(i)+'.dot -Goverlap=scale -Tjpg > WOMEN_TRIANGLES/women_triangles_'+str(i)+'.jpg')

fout = open('WOMEN_TRIANGLES/women_triangles.html','w')
fout.write('<html>\n')
fout.write('<a name="top"></a>')
for i in range(len(library)):
    fout.write('<a href="#'+str(i)+'"><img src="women_triangles_'+str(i)+'.jpg"></a>')
#fout.write('<p><hr><p>')
for i in range(len(library)):
    #for j in library[i].edges():
    #    fout.write(str(sorted(library[i].nodes()).index(j[0]))+str(gender[j[0]])+'->'+str(sorted(library[i].nodes()).index(j[1]))+str(gender[j[1]])+' ')
    #fout.write('\n')
    fout.write('<a name="'+str(i)+'"></a>')
    fout.write('<p><hr><p><img src="women_triangles_'+str(i)+'.jpg"><p>')
    fout.write('<br><a href="#top">return to top</a><p>')
    fout.write(str(len(librarydic[i]))+'<p><table>')
    for j in sorted(librarydic[i]):
        fout.write('<tr><td>'+str(name[j[0]])+' ['+str(j[0])+']</td><td>'+str(name[j[1]])+' ['+str(j[1])+']</td><td>'+str(name[j[2]])+' ['+str(j[2])+']</td></tr>')
    fout.write('</table><p>')
fout.write('</html>')
fout.close()

for ii in list(triangles):
    for j in [[0,1,2],[0,2,1],[1,2,0],[1,0,2],[2,0,1],[2,1,0]]:
        i = [0,1,2]
        i[0] = ii[j[0]]
        i[1] = ii[j[1]]
        i[2] = ii[j[2]]
        if (i[0],i[1]) in edgetimes and (i[1],i[2]) in edgetimes:
            if (i[0],i[2]) in edgetimes or (i[2],i[0]) in edgetimes:
                if ((i[0],i[2]) not in edgetimes or (i[0],i[2]) in edgetimes and edgetimes[(i[0],i[1])][0] <= edgetimes[(i[0],i[2])][0]) and ((i[2],i[0]) not in edgetimes or (i[2],i[0]) in edgetimes and edgetimes[(i[0],i[1])][0] <= edgetimes[(i[2],i[0])][0]):
                    f = open('wt_tmp','w')
                    for j in edgems[(i[1],i[2])]:
                        f.write(str(j)+'\n')
                    f.close()
                    #os.system('python /Users/sebastianahnert/Dropbox/DropboxDisambiguation/whindexsearch_restricted.py "'+str(name[i[0]].split(',')[0])+'" /Users/sebastianahnert/Dropbox/Workspace/TCM/C/TUDORNETWORKS/wt_tmp > wt_tmp2')
                    # LESS STRICT VERSION: (ONLY USES LAST NAME OF FIRST COMMA SECTION)
                    os.system('python /Users/sebastianahnert/Dropbox/DropboxDisambiguation/whindexsearch_restricted.py "'+str(name[i[0]].split(',')[0].split()[-1])+'" /Users/sebastianahnert/Dropbox/Workspace/TCM/C/TUDORNETWORKS/wt_tmp > wt_tmp2')
                    f = open('wt_tmp2')
                    s1 = f.readline().strip()
                    s2 = f.readline().strip()
                    nm = f.readline().strip()
                    if s2 != '0':
                        ff = open(nm)
                        filteredms = []
                        for line in ff:
                            mstmp = line.strip()
                            if ((i[0],i[2]) not in edgetimes or edgetimes[(i[0],i[2])][0] >= mstimes[mstmp]) and ((i[2],i[0]) not in edgetimes or edgetimes[(i[2],i[0])][0] >= mstimes[mstmp]) and mstimes[mstmp] >= edgetimes[(i[0],i[1])][0]:
                                filteredms.append(line.strip())
                        if filteredms != []:
                            print(str(name[ii[0]])+'\t'+str(name[ii[1]])+'\t'+str(name[ii[2]])+'\t'+' '.join(ii)+'\t'+str(' '.join(filteredms)))

                            

