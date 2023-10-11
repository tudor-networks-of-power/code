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

xmlparse = {}
xmlparse['docid'] = 'Document ID'
xmlparse['cdoc'] = 'Document Ref.'
xmlparse['cauth'] = 'Author'
xmlparse['crep'] = 'Recipient'
xmlparse['cd'] = 'Day'
xmlparse['cyr'] = 'Year'
xmlparse['cpl'] = 'Place'
xmlparse['ctit'] = 'Title'

def printxmlhtml(xml):
    s = ''
    f = open('<INSERT PATH TO SPO XML METADATA IF AVAILABLE>'+xml)
    out = 0
    count = 0
    linklist = []
    linklast = 0 
    for lineraw in f:
        line = lineraw.strip().replace('<title/>','') # RARE TAG THAT MESSES UP HTML 
        for j in xmlparse:
            if '<'+j+'>' in line:
                s += '<b>'+xmlparse[j]+':</b> '+line.strip()[len(j)+2:-(len(j)+3)]+'<br>'
        if '<linkseq ' in line:
            count += 1
            if 'spo2 corpus' in line:
                link = line.strip().split('>')[1][12:-9].replace('\\','/')
                corpus = 2
            if 'spo2 corpus' not in line:
                link = line.strip().split('>')[1][:-9].replace('\\','/')
                corpus = 1

            linklist.append(link)
            linklast = 1

        if linklast == 1 and  '<linkseq ' not in line:
            s += '<a href="/image=1">Images ('+str(len(linklist))+')</a><br>'
            linklast = 0

        if '<ctxt>' in line:
            out = 1
        if out == 1:
            s += line.strip().replace('<ctxt>','').replace('</ctxt>','')
        if '</ctxt>' in line:
            out = 0

        if '<cun>' in line:
            out = 1
        if out == 1:
            s += line.strip().replace('<cun>','').replace('</cun>','')
        if '</cun>' in line:
            out = 0


    return s

def printxmlhtmlplain(xml):
    s = ''
    f = open('<INSERT PATH TO SPO XML METADATA IF AVAILABLE>'+xml)
    out = 0
    count = 0
    linklist = []
    linklast = 0 
    for lineraw in f:
        line = lineraw.strip().replace('<title/>','') # RARE TAG THAT MESSES UP HTML 
        s += line
        
    return s

mentionedby = defaultdict(set)
mentionedto = defaultdict(set)
mentionedbydocs = {}
mentionedtodocs = {}
f = open('mentions')
for line in f:
    l = line.strip().split('\t')
    mentionedby[int(l[0])].add(int(l[2]))
    mentionedto[int(l[1])].add(int(l[2]))
    if int(l[0]) not in mentionedbydocs:
        mentionedbydocs[int(l[0])] = defaultdict(list)
    mentionedbydocs[int(l[0])][int(l[2])].append(l[3])
    if int(l[1]) not in mentionedtodocs:
        mentionedtodocs[int(l[1])] = defaultdict(list)
    mentionedtodocs[int(l[1])][int(l[2])].append(l[3])

os.system('mkdir OVERLAP7')
    
f = open('places_docs_final')
pname = {}
pname['0'] = '-'
for line in f:
    l = line.strip().split('\t')
    pname[l[0]] = l[1]

name = {}
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

f = open('fromto_all_place_mapped_sorted')
first = {}
for line in f:
    l = line.strip().split('\t')
    if l[0] not in first:
        first[l[0]] = {}
    if l[1] not in first[l[0]]:
        if l[1] not in first or (l[1] in first and l[0] not in first[l[1]]):
            first[l[0]][l[1]] = int(l[2])

coauthnet = defaultdict(list)
f = open('coauthnet')
for line in f:
    l = line.strip().split()
    coauthnet[(l[0],l[1])].append(l[3])
    coauthnet[(l[1],l[0])].append(l[3])

f = open('placeoverlap.out_final_final') 
overlaps = {}
for line in f:
    l = line.strip().split()
    # NOTE: placeoverlap.out CONTAINS ALL ENTRIES FOR BOTH ORDERINGS OF NAME IDS
    if ((l[0],l[1]) not in coauthnet or ((l[0],l[1]) in coauthnet and l[3] not in coauthnet[(l[0],l[1])])) and l[2] != '4466': # FILTERING OUT LONDON
        if int(l[0]) not in overlaps:
            overlaps[int(l[0])] = {}
        #if l[1] not in overlaps:
            #overlaps[l[1]] = {}
        if int(l[1]) not in overlaps[int(l[0])]:
            overlaps[int(l[0])][int(l[1])] = defaultdict(list)
        #if l[0] not in overlaps[l[1]]:
            #overlaps[l[1]][l[0]] = defaultdict(list)
        overlaps[int(l[0])][int(l[1])][l[2]].append((l[3],l[4],l[5],l[6],l[7],l[8],l[-3],l[-2],l[-1]))
        #overlaps[int(l[0])][int(l[1])][l[2]].append((l[3],l[4],l[-3],l[-2],l[-1]))
        #overlaps[int(l[0])][int(l[1])][l[2]].append((l[3],l[4],l[-2],l[-1]))
        #overlaps[l[1]][l[0]][l[2]].append((l[3],l[4],l[-2],l[-1]))
    
npeople = {}
npeoplewcomm = defaultdict(int)
nplacesset = defaultdict(set)
nplacessetwcomm = defaultdict(set)
sigset = defaultdict(set)

mtotal = defaultdict(int)
total = defaultdict(int)

for i in overlaps:
    ff = open('OVERLAP7/'+str(i)+'.html','w')
    ff.write('<html>')
    ff.write('<b>'+name[str(i)]+' ('+str(i)+')</b><p><p>')
    ff.write('<i>Overlaps with communication:</i> (jump to <a href="#wooverlaps">overlaps without communication)</a><p>')
    npeople[i] = len(overlaps[i])
    for j in overlaps[i]:
        if (str(i) in first and str(j) in first[str(i)]) or (str(j) in first and str(i) in first[str(j)]):
            npeoplewcomm[i] += 1
            ff.write('<a href="'+str(j)+'.html">'+name[str(j)]+' ('+str(j)+')</a><br>')
            for k in overlaps[i][j]:
                nplacessetwcomm[i].add(k)
                nplacesset[i].add(k)
                if k not in pname:
                    pname[k] = '?'
                ff.write(pname[k]+' ('+str(k)+'):<br>')
                for kk in overlaps[i][j][k]:
                    ff.write(str(name[str(i)])+': from '+str(kk[2])+' to '+str(kk[3])+'; ')
                    ff.write(str(name[str(j)])+': from '+str(kk[4])+' to '+str(kk[5])+'; ')
                    ff.write('overlap: '+str(kk[0])+' to '+str(kk[1])+' ')
                    #ff.write(str(kk[0])+' to '+str(kk[1]))
                    if kk[-3] != '-1':
                        if kk[-3] == '0':
                            ab = 'after'
                        if kk[-3] == '2':
                            ab = 'before'
                        if i in first and j in first[i]:
                            sr = 'sending'
                        else:
                            sr = 'receiving'
                        ff.write(' '+ab+' '+sr+' first communication on '+str(kk[-2]))
                    ff.write('<br>')
                ff.write('<p>')
            ff.write('<p>')
    ff.write('<a name="wooverlaps"></a><i>Overlaps without communication:</i><p>')
    for j in overlaps[i]:
        if (str(i) not in first or (str(i) in first and str(j) not in first[str(i)])) and (str(j) not in first or (str(j) in first and str(i) not in first[str(j)])):
            ff.write('<a href="'+str(j)+'.html">'+name[str(j)]+' ('+str(j)+')</a><br>')
            mention = 0
            if i in mentionedby[j]:
                ff.write('<b>'+name[str(j)]+' ('+str(j)+') mentions '+name[str(i)]+' ('+str(i)+'):</b><br>')
                mention = 1
                for kk in mentionedbydocs[j][i]:
                    ff.write('<textarea>'+printxmlhtmlplain(kk)+'</textarea><br>')
            if i in mentionedto[j]:
                ff.write('<b>'+name[str(i)]+' ('+str(i)+') is mentioned to '+name[str(j)]+' ('+str(j)+'):</b><br>')
                mention = 1
                for kk in mentionedtodocs[j][i]:
                    ff.write('<textarea>'+printxmlhtmlplain(kk)+'</textarea><br>')
            if j in mentionedby[i]:
                ff.write('<b>'+name[str(i)]+' ('+str(i)+') mentions '+name[str(j)]+' ('+str(j)+'):</b><br>')
                mention = 1
                for kk in mentionedbydocs[i][j]:
                    ff.write('<textarea>'+printxmlhtmlplain(kk)+'</textarea><br>')
            if j in mentionedto[i]:
                ff.write('<b>'+name[str(j)]+' ('+str(j)+') is mentioned to '+name[str(i)]+' ('+str(i)+'):</b><br>')
                mention = 1
                for kk in mentionedtodocs[i][j]:
                    ff.write('<textarea>'+printxmlhtmlplain(kk)+'</textarea><br>')
            mtotal[i] += mention
            total[i] += 1
            for k in overlaps[i][j]:
                nplacesset[i].add(k)
                if k not in pname:
                    pname[k] = '?'
                ff.write(pname[k]+' ('+str(k)+'):<br>')
                for kk in overlaps[i][j][k]:
                    ff.write(str(name[str(i)])+': from '+str(kk[2])+' to '+str(kk[3])+'; ')
                    ff.write(str(name[str(j)])+': from '+str(kk[4])+' to '+str(kk[5])+'; ')
                    ff.write('overlap: '+str(kk[0])+' to '+str(kk[1])+' ')
                    #ff.write(str(kk[0])+' to '+str(kk[1]))
                    if kk[-3] != '-1':
                        if kk[-3] == '0':
                            ab = 'after'
                        if kk[-3] == '2':
                            ab = 'before'
                        if i in first and j in first[i]:
                            sr = 'sending'
                        else:
                            sr = 'receiving'
                        ff.write(' '+ab+' '+sr+' first communication on '+str(kk[-2]))
                    ff.write(' [significance: '+str(kk[-1])+']<br>')
                    sigset[i].add(float(kk[-1]))
                ff.write('<p>')
            ff.write('<p>')
    ff.write('</html>')
    ff.close()
    
nplaces = {}
for i in nplacesset:
    nplaces[i] = len(nplacesset[i])

nplaceswcomm = {}
for i in nplacesset:
    nplaceswcomm[i] = len(nplacessetwcomm[i])

ftotal = {}
for i in mtotal:
    ftotal[i] = 1.0*mtotal[i]/total[i]

sigsetmin = {}
for i in sigset:
    sigsetmin[i] = min(sigset[i])

ff = open('OVERLAP7/index.html','w')
ff.write('<html>')
ff.write('<a href="index.html">By person ID</a> ')
ff.write('<a href="ppindex.html">By number of people</a> ')
ff.write('<a href="ppwcindex.html">By number of people (w. comm.)</a> ')
ff.write('<a href="pindex.html">By number of places</a> ')
ff.write('<a href="pwcindex.html">By number of places (w. comm.)</a><p> ')
ff.write('<a href="mindex.html">By number of people without communications and with mentions</a> ')
ff.write('<a href="mfindex.html">By fraction of people without communications and with mentions</a><p> ')
ff.write('<a href="sigindex.html">By most significant overlap score of an individial</a><p> ')
c = 1
for i in sorted(overlaps.keys()):
    ff.write(str(c)+'. <a href="'+str(i)+'.html">'+name[str(i)]+' ('+str(i)+')</a><br>')
    c += 1
ff.write('</html>')
ff.close()

ff = open('OVERLAP7/ppwcindex.html','w')
ff.write('<html>')
ff.write('<a href="index.html">By person ID</a> ')
ff.write('<a href="ppindex.html">By number of people</a> ')
ff.write('<a href="ppwcindex.html">By number of people (w. comm.)</a> ')
ff.write('<a href="pindex.html">By number of places</a> ')
ff.write('<a href="pwcindex.html">By number of places (w. comm.)</a><p> ')
ff.write('<a href="mindex.html">By number of people without communications and with mentions</a> ')
ff.write('<a href="mfindex.html">By fraction of people without communications and with mentions</a><p> ')
ff.write('<a href="sigindex.html">By most significant overlap score of an individial</a><p> ')
c = 1
for i in sorted(npeoplewcomm.items(),key=operator.itemgetter(1),reverse=True):
    ff.write(str(c)+'. <a href="'+str(i[0])+'.html">'+name[str(i[0])]+' ('+str(i[0])+')</a> - '+str(i[1])+'<br>')
    c += 1
ff.write('</html>')
ff.close()

ff = open('OVERLAP7/ppindex.html','w')
ff.write('<html>')
ff.write('<a href="index.html">By person ID</a> ')
ff.write('<a href="ppindex.html">By number of people</a> ')
ff.write('<a href="ppwcindex.html">By number of people (w. comm.)</a> ')
ff.write('<a href="pindex.html">By number of places</a> ')
ff.write('<a href="pwcindex.html">By number of places (w. comm.)</a><p> ')
ff.write('<a href="mindex.html">By number of people without communications and with mentions</a> ')
ff.write('<a href="mfindex.html">By fraction of people without communications and with mentions</a><p> ')
ff.write('<a href="sigindex.html">By most significant overlap score of an individial</a><p> ')
c = 1
for i in sorted(npeople.items(),key=operator.itemgetter(1),reverse=True):
    ff.write(str(c)+'. <a href="'+str(i[0])+'.html">'+name[str(i[0])]+' ('+str(i[0])+')</a> - '+str(i[1])+'<br>')
    c += 1
ff.write('</html>')
ff.close()

ff = open('OVERLAP7/pindex.html','w')
ff.write('<html>')
ff.write('<a href="index.html">By person ID</a> ')
ff.write('<a href="ppindex.html">By number of people</a> ')
ff.write('<a href="ppwcindex.html">By number of people (w. comm.)</a> ')
ff.write('<a href="pindex.html">By number of places</a> ')
ff.write('<a href="pwcindex.html">By number of places (w. comm.)</a><p> ')
ff.write('<a href="mindex.html">By number of people without communications and with mentions</a> ')
ff.write('<a href="mfindex.html">By fraction of people without communications and with mentions</a><p> ')
ff.write('<a href="sigindex.html">By most significant overlap score of an individial</a><p> ')
c = 1
for i in sorted(nplaces.items(),key=operator.itemgetter(1),reverse=True):
    ff.write(str(c)+'. <a href="'+str(i[0])+'.html">'+name[str(i[0])]+' ('+str(i[0])+')</a> - '+str(i[1])+'<br>')
    c += 1
ff.write('</html>')
ff.close()

ff = open('OVERLAP7/pwcindex.html','w')
ff.write('<html>')
ff.write('<a href="index.html">By person ID</a> ')
ff.write('<a href="ppindex.html">By number of people</a> ')
ff.write('<a href="ppwcindex.html">By number of people (w. comm.)</a> ')
ff.write('<a href="pindex.html">By number of places</a> ')
ff.write('<a href="pwcindex.html">By number of places (w. comm.)</a><p> ')
ff.write('<a href="mindex.html">By number of people without communications and with mentions</a> ')
ff.write('<a href="mfindex.html">By fraction of people without communications and with mentions</a><p> ')
ff.write('<a href="sigindex.html">By most significant overlap score of an individial</a><p> ')
c = 1
for i in sorted(nplaceswcomm.items(),key=operator.itemgetter(1),reverse=True):
    ff.write(str(c)+'. <a href="'+str(i[0])+'.html">'+name[str(i[0])]+' ('+str(i[0])+')</a> - '+str(i[1])+'<br>')
    c += 1
ff.write('</html>')
ff.close()

ff = open('OVERLAP7/mindex.html','w')
ff.write('<html>')
ff.write('<a href="index.html">By person ID</a> ')
ff.write('<a href="ppindex.html">By number of people</a> ')
ff.write('<a href="ppwcindex.html">By number of people (w. comm.)</a> ')
ff.write('<a href="pindex.html">By number of places</a> ')
ff.write('<a href="pwcindex.html">By number of places (w. comm.)</a><p> ')
ff.write('<a href="mindex.html">By number of people without communications and with mentions</a> ')
ff.write('<a href="mfindex.html">By fraction of people without communications and with mentions</a><p> ')
ff.write('<a href="sigindex.html">By most significant overlap score of an individial</a><p> ')
c = 1
for i in sorted(mtotal.items(),key=operator.itemgetter(1),reverse=True):
    ff.write(str(c)+'. <a href="'+str(i[0])+'.html">'+name[str(i[0])]+' ('+str(i[0])+')</a> - '+str(i[1])+' ('+str(100.0*ftotal[i[0]])+'%)<br>')
    c += 1
ff.write('</html>')
ff.close()

ff = open('OVERLAP7/mfindex.html','w')
ff.write('<html>')
ff.write('<a href="index.html">By person ID</a> ')
ff.write('<a href="ppindex.html">By number of people</a> ')
ff.write('<a href="ppwcindex.html">By number of people (w. comm.)</a> ')
ff.write('<a href="pindex.html">By number of places</a> ')
ff.write('<a href="pwcindex.html">By number of places (w. comm.)</a><p> ')
ff.write('<a href="mindex.html">By number of people without communications and with mentions</a> ')
ff.write('<a href="mfindex.html">By fraction of people without communications and with mentions</a><p> ')
ff.write('<a href="sigindex.html">By most significant overlap score of an individial</a><p> ')
c = 1
for i in sorted(ftotal.items(),key=operator.itemgetter(1),reverse=True):
    ff.write(str(c)+'. <a href="'+str(i[0])+'.html">'+name[str(i[0])]+' ('+str(i[0])+')</a> - '+str(100.0*i[1])+'% ('+str(mtotal[i[0]])+')<br>')
    c += 1
ff.write('</html>')
ff.close()

ff = open('OVERLAP7/sigindex.html','w')
ff.write('<html>')
ff.write('<a href="index.html">By person ID</a> ')
ff.write('<a href="ppindex.html">By number of people</a> ')
ff.write('<a href="ppwcindex.html">By number of people (w. comm.)</a> ')
ff.write('<a href="pindex.html">By number of places</a> ')
ff.write('<a href="pwcindex.html">By number of places (w. comm.)</a><p> ')
ff.write('<a href="mindex.html">By number of people without communications and with mentions</a> ')
ff.write('<a href="mfindex.html">By fraction of people without communications and with mentions</a><p> ')
ff.write('<a href="sigindex.html">By most significant overlap score of an individial</a><p> ')
c = 1
for i in sorted(sigsetmin.items(),key=operator.itemgetter(1)):
    ff.write(str(c)+'. <a href="'+str(i[0])+'.html">'+name[str(i[0])]+' ('+str(i[0])+')</a> - '+str(i[1])+'<br>')
    c += 1
ff.write('</html>')
ff.close()

ff = open('overlapstats_final_final.out','w')
for i in overlaps:
    ff.write(str(i)+'\t'+str(name[str(i)].replace(' ','_'))+'\t'+str(npeople[i])+'\t'+str(npeoplewcomm[i])+'\t'+str(nplaces[i])+'\t'+str(nplaceswcomm[i])+'\n')
ff.close()
