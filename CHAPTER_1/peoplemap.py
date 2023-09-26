#!/usr/bin/env python                                                           
import sys
import os
import random
import networkx
import operator
import matplotlib
import pylab
import math
import time
from collections import defaultdict

def tdist(d1,d2):
    #print(d1,d2)
    t1 = time.mktime((int(d1[:4])+2000,int(d1[4:6]),int(d1[6:8]),0,0,0,0,0,0))
    t2 = time.mktime((int(d2[:4])+2000,int(d2[4:6]),int(d2[6:8]),0,0,0,0,0,0))
    return abs(t1-t2)/(24*3600.0)

def printcontent(xml):
    fx = open('/Users/sebastianahnert/Desktop/DisambiguationEngine/'+xml)
    read = 0
    s = ''
    for line2 in fx:
        if '<ctxt>' in line2:
            read = 1
        if read == 1:
            s += line2
        if '</ctxt>' in line2:
            read = 0
    fx.close()    
    return s

def printxml(xml):
    fx = open('/Users/sebastianahnert/Desktop/DisambiguationEngine/'+xml)
    s = ''
    for line2 in fx:
        s += line2
    fx.close()    
    return s

def getimg(xml):
    fx = open('/Users/sebastianahnert/Desktop/DisambiguationEngine/'+xml)
    s = []
    cnt = 1
    for line2 in fx:
        if '<linkseq' in line2:
            s.append('<a href="'+line2.strip().replace('<','@').replace('>','@').split('@')[2].split('\\')[-1]+'">Image '+str(cnt)+'</a>')
            cnt += 1

    fx.close()    
    return s

def getimgcopy(xml):
    fx = open('/Users/sebastianahnert/Desktop/DisambiguationEngine/'+xml)
    s = []
    for line2 in fx:
        if '<linkseq' in line2:
            if 'spo2 corpus' in line2:
                link = line2.strip().split('>')[1][12:-9].replace('\\','/')
                corpus = 2
            if 'spo2 corpus' not in line2:
                link = line2.strip().split('>')[1][:-9].replace('\\','/')
                corpus = 1

            s.append('cp /Volumes/LaCie/SPO'+str(corpus)+'/Images/'+str(link)+' .')

    fx.close()    
    return s

f = open('people_docs_auto')
fc = open('checkforchains_straight_revised_190328_combined_edited')
fc2 = open('checkforchains_ambiguities_resolved')
ff = open('fromto_all_place')
fcdoc = open('cdoc_all')
ffrp = open('specific_replace')
ffrm = open('specific_remove')
ffad = open('specific_add')
fff = open('fromto_all_place_mapped','w')
fdis = open('peoplemap_discrepancies','w')
fpdis = open('peoplemap_people_discrepancies','w')
fdrop = open('peoplemap_dropped','w')
fcol = open('peoplemap_collapsed','w')
fcop = open('peoplemap_copies','w')
fcopcheck = open('peoplemap_copies_check','w')
fshmay = open('peoplemap_sheriff_mayor_vicech_master','w')
fshmayh = open('peoplemap_sheriff_mayor_vicech_master.html','w')
fshmayc = open('peoplemap_sheriff_mayor_vicech_master.copy','w')
fffff = open('fromto_all_place_likely_copies','w')
#fffff = open('fromto_all_place_likely_bundles','w')
fnew = open('added_people')
labelid = {}
mappedid = {}
mapms = {}
name = {}
msd1 = {}
msd2 = {}
xmld = {}
img = {}
imgcp = {}
ndis = 0
npdis = 0
nself = 0
ncop = 0
ncopcheck = 0
record = defaultdict(list)
for line in f:
    l = line.strip().split('\t')
    if l[1][:3] == '++ ': # GET RID OF PLUSSES
        l[1] = l[1][3:]
    if l[1][:2] == '+ ':
        l[1] = l[1][2:]
    #print(l)

    labelid[l[1]] = l[0]
    mappedid[l[1]] = l[2]
    mapms[l[1]] = l[3].split()
    name[l[0]] = l[1]

    if ';' in mappedid[l[1]] and len(mappedid[l[1]].split(';')) != len(mapms[l[1]]):
        #print(line)
        fdis.write(str(l[0])+'\t'+str(l[1])+'\n')
        ndis += 1

    if ('.' in mappedid[l[1]] or ',' in mappedid[l[1]]) and ';' not in mappedid[l[1]] and ('' in mappedid[l[1]].split(',') or '.' in mappedid[l[1]]):
        #print(line)
        fpdis.write(str(l[0])+'\t'+str(l[1])+'\n')
        npdis += 1
        
print(str(ndis)+' discrepancies between mapped ID and MS numbers.')
print(str(npdis)+' incomplete people-mapped IDs.')

for line in fc:
    l = line.strip().split('\t')
    if len(l) == 3:
        mappedid[l[1]] = l[2]

for line in fc2:
    l = line.strip().split('\t')
    if '#' not in line and len(l) > 1 and '...' not in l[2]:
        mappedid[l[1]] = l[2]

for line in fnew:
    a,b = line.strip().split('\t')
    labelid[b] = a
    name[a] = b

origms = {}
for line in fcdoc:
    l = line.strip()[31:]
    ll = l.split(':')
    origms[ll[0]] = ll[1][6:-7]

auth = defaultdict(set)
recp = defaultdict(set)

verbose = 0
ndrop = 0
nrem = 0
nmis = 0
already = set([])
ncol = 0
copyset = set([])

rpms = ''
repdic = {}
for line in ffrp:
    if '@' in line:
        rpms = line.strip()[1:]
        repdic[rpms] = []
    else:
        l = line.strip().split()
        for i in range(len(l)):
            l[i] = l[i].strip()
        repdic[rpms].append(l)

rpms = ''
adddic = defaultdict(list)
for line in ffrp:
    if '@' in line:
        rpms = line.strip()[1:]
    else:
        l = line.strip().split('\t')
        adddic[rpms].append(l)

rmlist = []
for line in ffrm:
    l = line.strip()
    rmlist.append(l)

for line in ff:
    l = line.strip().split('\t')
    frr = l[0]

    # DEAL WITH POSSIBILITY OF MULTIPLE AUTHORS AND ADDRESSEES IN fromto FILE
    if '; ' not in frr: 
        frrl = [frr]
    if '; ' in frr:
        #print(frr)
        frrl = []
        for i in frr.split('; '):
            frrl.append(i.strip())

    too = l[1]
    if '; ' not in too:
        tool = [too]
    if '; ' in too:
        tool = []
        for i in too.split('; '):
            tool.append(i.strip())

    """
    # USING 'Letters' IN DESCRIPTION TO DETECT BUNDLES OF UNRELATED LETTERS
    # THIS DOES NOT WORK WELL, AND SUCH BUNDLES ARE PROBABLY RELATIVELY RARE
    bundle = 0
    if len(tool) > 1 or len(frrl) > 1:
        ffff = open('/Users/sebastianahnert/Desktop/DisambiguationEngine/'+l[6])
        read = 0
        for line2 in ffff:
            if '<ctxt>' in line2:
                read = 1
            if read == 1 and ('Letters' in line2 or 'letters' in line2):
                bundle = 1
                bundlestr = line2.strip()
                break
            if '</ctxt>' in line2:
                read = 0
        ffff.close()    

    if bundle == 1:
        fffff.write(line)
        fffff.write(bundlestr+'\n')
    """

    copy = 0
    ffff = open('/Users/sebastianahnert/Desktop/DisambiguationEngine/'+l[6])
    read = 0
    for line2 in ffff:
        if '<ctxt>' in line2:
            read = 1
        if read == 1 and ('Copy' in line2 or 'copy' in line2):
            copy = 1
            copystr = line2.strip()
            copyset.add(l[6])
            break
        if '</ctxt>' in line2:
            read = 0
    ffff.close()    

    if copy == 1:
        fffff.write(line)
        fffff.write(copystr+'\n')

    # STORE REST OF DATA
    d1 = l[2]
    d2 = l[3]
    ms = l[4]
    pl = l[5]
    xml = l[6]

    # MAP DATES TO MS ID
    msd1[ms] = l[2]
    msd2[ms] = l[3]

    # MAP XML TO MS ID
    xmld[ms] = xml

    img[ms] = getimg(xml)
    imgcp[ms] = getimgcopy(xml)

    # OPTIONAL WARNING REGARDING POSSIBLE DISCREPANCIES IN specific_replace
    """
    if ms in repdic and len(frrl)*len(tool) != len(repdic[ms]):
        print('WARNING: FOR '+str(ms)+' WE HAVE '+str(len(repdic[ms]))+' ENTRIES IN specific_replace BUT '+str(len(frrl)*len(tool))+' EDGES RESULTING FROM '+str(len(frrl))+' SENDERS AND '+str(len(tool))+' RECIPIENTS.')
    """
    
    # LOOP ACROSS fromto AUTHORS (ONLY REALLY A LOOP IF WE HAVE MULTIPLE)
    for fr in frrl:
        for to in tool:
    
            if fr in mappedid: # IF NOT, WE'LL THROW AN ERROR MESSAGE BELOW.
                
                # IF MAPPED PERSON ID IS NOT SPLIT
                if ';' not in mappedid[fr] and ',' not in mappedid[fr]:
                    frl = [mappedid[fr]]
                    
                # IF MAPPED PERSON ID IS SPLIT IN TERMS OF MS
                if ';' in mappedid[fr] and ',' not in mappedid[fr]:
                    if len(mappedid[fr].split(';')) == len(mapms[fr]):                        
                        frl = []
                        c = 0
                        for i in mappedid[fr].split(';'):
                            if ms == mapms[fr][c]:
                                frl.append(i.strip())
                            c += 1
                    else:
                        if verbose == 1:
                            print('Error: '+str(labelid[fr])+'\t'+str(fr)+'\t'+str(len(mappedid[fr].split(';')))+'\t'+str(len(mapms[fr])))

                # IF MAPPED PERSON ID IS SPLIT IN TERMS OF PERSON
                if ';' not in mappedid[fr] and ',' in mappedid[fr]:
                    frl = []
                    for i in mappedid[fr].split(','):
                        frl.append(i.strip())
            
                # IF MAPPED PERSON ID IS SPLIT IN TERMS OF MS AND PERSON
                if ';' in mappedid[fr] and ',' in mappedid[fr]:
                    if len(mappedid[fr].split(';')) == len(mapms[fr]):                        
                        frl = []
                        c = 0
                        for i in mappedid[fr].split(';'):
                            if ms == mapms[fr][c]:
                                for j in i.split(','):
                                    frl.append(j.strip())
                            c += 1
                    else: 
                        if verbose == 1:
                            print('Error: '+str(labelid[fr])+'\t'+str(fr)+'\t'+str(len(mappedid[fr].split(';')))+'\t'+str(len(mapms[fr])))
                            
            if to in mappedid:

                # IF MAPPED PERSON ID IS NOT SPLIT
                if ';' not in mappedid[to] and ',' not in mappedid[to]:
                    tol = [mappedid[to]]
                    
                # IF MAPPED PERSON ID IS SPLIT IN TERMS OF MS
                if ';' in mappedid[to] and ',' not in mappedid[to]:
                    if len(mappedid[to].split(';')) == len(mapms[to]):                        
                        tol = []
                        c = 0
                        for i in mappedid[to].split(';'):
                            if ms == mapms[to][c]:
                                tol.append(i.strip())
                            c += 1
                    else: 
                        if verbose == 1:
                            print('Error: '+str(labelid[to])+'\t'+str(to)+'\t'+str(len(mappedid[to].split(';')))+'\t'+str(len(mapms[to])))
            
                # IF MAPPED PERSON ID IS SPLIT IN TERMS OF PERSON
                if ';' not in mappedid[to] and ',' in mappedid[to]:
                    tol = []
                    for i in mappedid[to].split(','):
                        tol.append(i.strip())
            
                # IF MAPPED PERSON ID IS SPLIT IN TERMS OF MS AND PERSON
                if ';' in mappedid[to] and ',' in mappedid[to]:
                    if len(mappedid[to].split(';')) == len(mapms[to]):                        
                        tol = []
                        c = 0
                        for i in mappedid[to].split(';'):
                            if ms == mapms[to][c]:
                                for j in i.split(','):
                                    tol.append(j.strip())
                            c += 1
                    else: 
                        if verbose == 1:
                            print('Error: '+str(labelid[to])+'\t'+str(to)+'\t'+str(len(mappedid[to].split(';')))+'\t'+str(len(mapms[to])))
                
            # IF ALL IS WELL
            if fr in mappedid and to in mappedid:
            
                # OUTPUT ALL LINKS THAT RESULT FROM THIS LETTER (WITHIN OUTER LOOPS)
                for i in frl:
                    for j in tol:
                        # CHECK FOR ERRORS
                        if (i == '-1' or i.strip().isdigit()) and (j == '-1' or j.strip().isdigit()):
                            # CHECK FOR UNKNOWN OR REMOVED
                            if int(i.strip()) > 0 and int(j.strip()) > 0:
                                # CHECK FOR DUPLICATES
                                if (str(i.strip()),str(j.strip()),str(d1),str(d2),str(origms[xml])) not in already or ((str(i.strip()),str(j.strip()),str(d1),str(d2),str(origms[xml])) in already and origms[xml][:3] == 'spo'): # LATTER CLAUSE IS USED IF WE ONLY HAVE AUTO-GENERATED MS ID

                                    #fff.write(str(i.strip())+'\t'+str(j.strip())+'\t'+str(d1)+'\t'+str(d2)+'\t'+str(ms)+'\t'+str(pl)+'\t'+str(xml)+'\t'+str(origms[xml])+'\n')
                                    
                                    record[(str(i.strip()),str(j.strip()),str(d1),str(d2))].append((str(i.strip()),str(j.strip()),str(d1),str(d2),str(ms),str(pl),str(xml),str(origms[xml])))
                                    
                                    # KEEP TRACK OF MULTIPLE COAUTHORS/CORECIPIENTS OF THIS MS
                                    auth[ms].add(i.strip())
                                    recp[ms].add(j.strip())
                                    
                                    already.add((str(i.strip()),str(j.strip()),str(d1),str(d2),str(origms[xml])))
                                else:
                                    fcol.write(str(i.strip())+'\t'+str(j.strip())+'\t'+str(d1)+'\t'+str(d2)+'\t'+str(ms)+'\t'+str(pl)+'\t'+str(xml)+'\t'+str(origms[xml])+'\n')
                                    ncol += 1
                            else:
                                fdrop.write(str(i.strip())+'\t'+str(j.strip())+'\t'+str(d1)+'\t'+str(d2)+'\t'+str(ms)+'\t'+str(pl)+'\t'+str(xml)+'\n')                          
                                if int(i.strip()) == 0 or int(j.strip()) == 0:
                                    nrem += 1
                                else:
                                    nmis += 1
                                ndrop += 1
                        else:
                            if verbose == 1:
                                print('Error: '+str(fr)+'\t'+str(to)+'\t"'+str(mappedid[fr])+'"\t"'+str(mappedid[to]+'"'))
                                
            else: 
                if verbose == 1:
                    print('Error: '+str(l))
 
# CHECK FOR DUPLICATES OF SENDER, RECIPIENT, MS ID, AND ONLY KEEP ONE WITH SMALLEST DATE WINDOW.
duprem = open('duplicate_ms_removals','w')
dupremn = 0
dupdic = defaultdict(list)
for i in record:
    for j in record[i]:
        if j[-1] != '':
            dupdic[(j[0],j[1],j[-1])].append((i,j,tdist(j[2],j[3]),j[2],j[3]))
for k in dupdic:
    if len(dupdic[k]) > 1:
        ss = sorted(dupdic[k],key=operator.itemgetter(2))
        for kk in ss[1:]: # MAKE SURE WE ONLY REMOVE LETTERS WITH EQUAL TIME WINDOW OR LESS PRECISE TIME WINDOW THAT CONTAINS THE MORE PRECISE ONE 
            if int(kk[3]) <= int(ss[0][3]) and int(kk[4]) >= int(ss[0][4]):
                record[kk[0]].remove(kk[1])
                duprem.write(str(ss[0])+'\t'+str(kk[1])+'\n')
                dupremn += 1
            #else:
                #print(str(ss[0])+'\t'+str(kk[1])+'\n')
duprem.close()

rmlist = set()
for i in record:
    if record[i] == []:
        rmlist.add(i)
for i in rmlist:
    record.pop(i)

# CHECK FOR COPIES (THAT MENTION 'copy' IN DESCRIPTION)
replaced = set([])
for i in record:
    copypresent = 0
    noncopypresent = 0
    copies = set([])
    allrec = set([])
    for j in record[i]:
        if j[6] in copyset:
            copypresent = 1
            copies.add(j)
        else:
            noncopypresent += 1
        allrec.add(j)
    if copypresent == 1 and noncopypresent > 1 and j[2] == j[3]:
        for k in allrec:
            if k not in copies:
                fcopcheck.write('Original:\n'+str(k)+'\n')
            if k in copies:
                fcopcheck.write('Copy:\n'+str(k)+'\n')
            fcopcheck.write(printcontent(k[6]))
            fcopcheck.write('\n')
        ncopcheck += 1
    if copypresent == 1 and noncopypresent > 0 and j[2] == j[3]:
        rmcopy = []
        for k in copies:
            for kk in k:
                fcop.write(str(kk)+'\t')
            fcop.write('\n')
            ncop += 1
        
            for kk in allrec:
                if kk not in copies and int(k[6].replace('m','').replace('v','').replace('p','').replace('x','').split('-')[-2]) == int(kk[6].replace('m','').replace('v','').replace('p','').replace('x','').split('-')[-2])+1:
                    rmcopy.append(k)
        fcop.write('\n')
        for k in rmcopy:
            allrec.remove(k)
            fcop.write('REMOVED: '+str(k)+'\n')

    for j in allrec:
        if j[0] == j[1]:
            nself += 1
        else:
            if j[4] not in repdic and j[4] not in rmlist:
                for k in j:
                    fff.write(str(k)+'\t')
                fff.write('\n')
            if j[4] in repdic and j[4] not in replaced: # REPLACEMENTS FROM specific_replace
                replaced.add(j[4])
                for kk in repdic[j[4]]:
                    for k in kk:
                        fff.write(str(k)+'\t')
                    for k in j[len(kk):]: 
                        fff.write(str(k)+'\t')
                    fff.write('\n')
            if j[4] in adddic:
                for kk in adddic[j[4]]:
                    for k in kk:
                        fff.write(str(k)+'\t')
                    for k in j[len(kk):]:
                        fff.write(str(k)+'\t')
                    fff.write('\n')

fff.close()
fcop.close()

print(str(ndrop)+' edges dropped due to removed individuals ('+str(nrem)+') or missing rule-based disambiguation information ('+str(nmis)+').')
print(str(ncol)+' collapsed edges.')
print(str(ncop)+' copies, of which '+str(ncopcheck)+' should be checked.')            
print(str(dupremn)+' duplicates with same sender, recipient, and MS ID removed.')
print(str(nself)+' self-edges (probably due to letter bundles) removed.')

# GENERATE COAUTHOR NETWORK
coauth = []
for i in auth:
    if len(auth[i]) > 1:
        al = list(auth[i])
        for j in range(len(auth[i])):
            for k in range(j+1,len(auth[i])):
                coauth.append((al[j],al[k],i,msd1[i],msd2[i]))
    
# GENERATE CORECIPIENT NETWORK
corecp = []
for i in recp:
    if len(recp[i]) > 1:
        rl = list(recp[i])
        for j in range(len(recp[i])):
            for k in range(j+1,len(recp[i])):
                corecp.append((rl[j],rl[k],i,msd1[i],msd2[i]))
    
# OUTPUT COAUTHOR NETWORK
fff = open('coauthnet','w')
for i in coauth:
    for j in i:
        fff.write(str(j)+'\t')
    fff.write('\n')
fff.close()

# OUTPUT CORECIPIENT NETWORK
fff = open('corecpnet','w')
for i in corecp:
    for j in i:
        fff.write(str(j)+'\t')
    fff.write('\n')
fff.close()
#fffff.close()
fdis.close()

# SPECIAL FILTER TO DOUBLE-CHECK MAYORS AND SHERIFFS.
for i in labelid:
    # CHECK ANY UNNAMED MAYOR OR SHERIFF OF A PARTICULAR PLACE THAT HAS BEEN MAPPED 
    if i in mappedid and i in mapms and mappedid[i] != '0' and (i[:9] == 'Mayor of ' or i[:11] == 'Sheriff of ' or i[:16] == 'Vice-Chancellor ' or i[:10] == 'Master of ') and mappedid[i] != labelid[i]:
        c = 0
        for j in mapms[i]:
            # CHECK ANY DATE IN FIRST THREE MONTHS OF YEAR:
            if msd1[j][4:] < '0401' or msd2[j][4:] < '0401':
                jj = mappedid[i]
                if ';' in mappedid[i]:
                    jj = mappedid[i].split(';')[c]
                if ',' in jj:
                    s = ''
                    for k in jj.split(','):
                        s += name[k.strip()]+' ('+str(k.strip())+')  AND '
                    s = s[:-5]
                else:
                    s = name[jj.strip()]+' ('+str(jj)+')'
                fshmay.write(str(i)+' ('+str(labelid[i])+') mapped to '+str(s)+'\n')
                fshmay.write('MANUSCRIPT HANDLE: '+str(j)+'\n')
                fshmay.write('FROM DATE: '+str(msd1[j])+'\n')
                fshmay.write('TO DATE: '+str(msd2[j])+'\n')
                fshmay.write('XML\n'+str(printxml(xmld[j]))+'\n\n')
                fshmayh.write(str(i)+' ('+str(labelid[i])+') mapped to '+str(s)+'\n')
                fshmayh.write('<br>MANUSCRIPT HANDLE: '+str(j)+'\n')
                fshmayh.write('<br>FROM DATE: '+str(msd1[j])+'\n')
                fshmayh.write('<br>TO DATE: '+str(msd2[j])+'\n')
                fshmayh.write('<br>IMAGES: ')
                for k in img[j]:
                    fshmayh.write(str(k)+' ')                
                fshmayh.write('<p>XML\n'+str(printxml(xmld[j]).replace('<','&lt;').replace('>','&gt'))+'<p><p>')
                for k in imgcp[j]:
                    fshmayc.write(str(k)+'\n')                
                
            c += 1
