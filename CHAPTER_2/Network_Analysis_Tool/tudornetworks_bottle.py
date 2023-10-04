#!/usr/bin/env python                                                           
import sys
import os
import random
import networkx
import operator
#import matplotlib
#import pylab
import math
#import cPickle
import time
from collections import defaultdict
from bottle import route, run, template, request

current = '25959'
view = 'indiv'
period = 'all'
item = 2
xmlprint = ''
image = ''
x = ''
y = ''
searchterms = ''
checked1 = 'checked'
checked2 = ''

meas = {}
meas[0] = 'Total Degree'
meas[1] = 'Out-degree'
meas[2] = 'In-degree'
meas[3] = 'Total Strength'
meas[4] = 'Out-strength'
meas[5] = 'In-strength'
meas[6] = 'Eigenvector cent.'
meas[7] = 'Betweenness'
meas[8] = 'Eigenvector cent. rank'
meas[9] = 'Betweenness rank'

monfull = {}
monfull['hen'] = 'Henry VIII'
monfull['edw'] = 'Edward VI'
monfull['mar'] = 'Mary I'
monfull['eli'] = 'Elizabeth I'
monfull['all'] = 'All'
monfull['cus'] = 'Custom'

xmlparse = {}
xmlparse['docid'] = 'Document ID'
xmlparse['cdoc'] = 'Document Ref.'
xmlparse['cauth'] = 'Author'
xmlparse['crep'] = 'Recipient'
xmlparse['cd'] = 'Day'
xmlparse['cyr'] = 'Year'
xmlparse['cpl'] = 'Place'
xmlparse['ctit'] = 'Title'

def printxml(xml):
    fx = open('<INSERT PATH TO SPO XML FILES>'+xml)
    s = ''
    for line2 in fx:
        s += line2
    fx.close()    
    return s

def printxmlhtml(xml):
    s = ''
    f = open('<INSERT PATH TO SPO XML FILES>'+xml)
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

def display(current,frll,toll,name,msg,period,xmlprint,image):
    global link
    s = '<html><head><STYLE type = \"text/css\" media = \"screen\"\n<!--\n\-->\n</STYLE><LINK HREF=\"static/interfacestyle2.css\" rel=\"stylesheet\" type=\"text/css\" media=\"all\" title=\"Standard\"></head><div class="title"><b>Tudor Networks of Power</b></div>'
    #print(current,frl,tol)
    s += '<div class="current">'+'<br>'#+msg+'<p>'
    s += '<b>'+name[current]+' ['+current+'] </b>'
    if current in link:
        s += '(<a target="_blank" href="'+str(link[current])+'">Bio</a>)'
    s += '<p>'
    if current in net[period].nodes():
        s += '<b><a href="/item=2">Total degree: </a></b>'+str(net[period].degree(current))+' ('+str(degrank[period][current])+' / '+"%.4f"%(100.0*degrank[period][current]/len(degrank[period]))+'%)<br>'
        s += '<b><a href="/item=3">Out-degree: </a></b>'+str(net[period].out_degree(current))+' ('+str(odegrank[period][current])+' / '+"%.4f"%(100.0*odegrank[period][current]/len(odegrank[period]))+'%)<br>'
        s += '<b><a href="/item=4">In-degree: </a></b>'+str(net[period].in_degree(current))+' ('+str(idegrank[period][current])+' / '+"%.4f"%(100.0*idegrank[period][current]/len(idegrank[period]))+'%)<p>'
        s += '<b><a href="/item=5">Total strength: </a></b>'+str(net[period].degree(current,weight='w'))+' ('+str(wdegrank[period][current])+' / '+"%.4f"%(100.0*wdegrank[period][current]/len(wdegrank[period]))+'%)<br>'
        s += '<b><a href="/item=6">Out-strength: </a></b>'+str(net[period].out_degree(current,weight='w'))+' ('+str(wodegrank[period][current])+' / '+"%.4f"%(100.0*wodegrank[period][current]/len(wodegrank[period]))+'%)<br>'
        s += '<b><a href="/item=7">In-strength: </a></b>'+str(net[period].in_degree(current,weight='w'))+' ('+str(widegrank[period][current])+' / '+"%.4f"%(100.0*widegrank[period][current]/len(widegrank[period]))+'%)<p>'
        s += '<b><a href="/item=8">Eigenvector centrality: </a></b>'+str(eig[period][current])+' ('+str(eigrank[period][current])+' / '+"%.4f"%(100.0*eigrank[period][current]/len(eigrank[period]))+'%)<br>'
        s += '<b><a href="/item=9">Betweenness centrality: </a></b>'+str(betw[period][current])+' ('+str(betwrank[period][current])+' / '+"%.4f"%(100.0*betwrank[period][current]/len(betwrank[period]))+'%)<p>'
    else:
        s += '<br>does not appear in current period.<p>'
    s += '<a href="/item=1">List view by name</a><p>'
    s += '<a href="/edge">Edge list</a><p>'
    s += '<a href="/similar='+str(current)+'">Show individuals with similar network profile</a><p>'
    s += '<a href="/xmlprint='+str(current)+'$">View all this person\'s correspondence</a><p>'
    s += '<b>Current period:</b> '+str(monfull[period])
    if period != 'all':
        s += ' ('+str(mfdate[period])+'-'+str(mtdate[period])+')'
    s += '<br>'
    s += '<b>Select period: </b>'
    for i in monarchs:
        if current in net[i].nodes():
            s += '<a href="/period='+str(i)+'">'+str(monfull[i])+'</a>'
            if i not in ['hen','mar','eli','edw','all','cus']:
                s += ' <a href="/delete='+str(monfull[i])+'"><sup><small>x</small></sup></a>'
        else:
            s += str(monfull[i])
            if i not in ['hen','mar','eli','edw','all','cus']:
                s += ' <a href="/delete='+str(monfull[i])+'"><sup><small>x</small></sup></a>'
        s += ' - '

    s = s[:-3]
    s += '<p><b>Set custom period:</b><br> <form method="POST" action="/setperiod">from <input type="text" size="8" name="fdate" value="'+str(mfdate['cus'])+'"> to <input type="text" size="8" name="tdate" value="'+str(mtdate['cus'])+'"><input type="submit" name="submit" value="Set"></form><form method="POST" action="/save"><p><b>Name custom period: </b><input type="text" size="8" name="savename"><input type="submit" name="submit" value="Save"></form>'
    #s += '<a href="/period=all">All</a><p>' 
    s += '</div>'
    s += '<div class="alias">'
    if current in alias:
        already = set([]) # BECAUSE SAME ALIAS CAN APPEAR IN MULTIPLE CONTEXTS (e.g. A, B and A, C, and just A) WHICH LEADS TO MULTIPLE IDENTIAL alias ENTRIES
        for k in alias[current]:
            if k[0] in number and number[k[0]] != current and k[0] not in already:
                already.add(k[0])
                s += str(k[0])+' (<a href="/xmlprint='+str(current)+'_'+str(k[0])+'!">see letters</a>)'
                #for jj in k[1]:
                #    if jj in msr:
                #        # CHANGE THIS - WANT TO SEE ALL LETTERS FOR AN ALIAS IN ONE GO
                #        s += ' <a href="/xmlprint='+str(msr[jj])+'!">'+str(msr[jj])+'</a> '
                s += '<br>'
                #s += name[k[0]]+'<br>'# '+str(k[1])+'<br>'
    s += '</div>'
    if current in net[period].nodes():
        s += '<p><div class="fromlist">'
        frlc = defaultdict(int)
        for i in frll:
            frlc[i] += 1
        #s += str(net.out_degree(current))+' '
        #s += str(net.in_degree(current))+' '
        #s += str(net.degree(current))+' '
        #s += str(betw[current])+' '
        #s += str(eig[current])+' '
        s += 'sends '+str(len(frll))+' letters to '+str(len(frlc))+' people:<p>'
        for i in sorted(frlc.items(),key=operator.itemgetter(1),reverse=True):
            s += '<a href="/current='+str(i[0])+'">'+str(name[i[0]])+' ['+str(i[0])+']</a> (<a href="/xmlprint='+str(current)+'_'+str(i[0])+'">'+str(i[1])+'</a>) <br>'
        s += '</div><p><div class="tolist">'
        tolc = defaultdict(int)
        for i in toll:
            tolc[i] += 1
        s += 'receives '+str(len(toll))+' letters from '+str(len(tolc))+' people:<p>'
        for i in sorted(tolc.items(),key=operator.itemgetter(1),reverse=True):
            s += '<a href="/current='+str(i[0])+'">'+str(name[i[0]])+' ['+str(i[0])+']</a> (<a href="/xmlprint='+str(i[0])+'_'+str(current)+'">'+str(i[1])+'</a>) <br>'
        s += '</div>'
    #else:
    #    s = current+' not present in '+str(monfull[period])+'\'s period'
    #    s += '</div>'

    checked1 = 'checked'
    checked2 = ''

    if xmlprint != '':
        s += '<div class="xmlprint">'
        if '@' not in xmlprint and '!' not in xmlprint and '$' not in xmlprint:
            mslist = net[period].get_edge_data(xmlprint.split('_')[0],xmlprint.split('_')[1])['l']
            s += str(len(mslist))+' items of correspondence<p><b>From:</b> '+str(name[xmlprint.split('_')[0]])+' ['+str(xmlprint.split('_')[0])+']<br><b>To:</b> '+str(name[xmlprint.split('_')[1]])+' ['+str(xmlprint.split('_')[1])+']<p>'
            
        if '!' in xmlprint:
            mslist = []
            for jj in alias[xmlprint[:-1].split('_')[0]]:
                if jj[0] == xmlprint[:-1].split('_')[1]:
                    for k in jj[1]:
                        if k in msr: # MS MIGHT HAVE BEEN REMOVED AFTER people_docs_auto WAS GENERATED
                            mslist.append(msr[k])

        if '$' in xmlprint:
            mslist = allar[current]

        senhist = defaultdict(int)
        rechist = defaultdict(int)
        
        if '@' in xmlprint:
            mslist = []
            sf = open('out')
            #logic = sf.readline().strip()
            #if logic == 'AND':
            #    checked1 = 'checked'
            #    checked2 = ''
            #if logic == 'OR':
            #    checked1 = ''
            #    checked2 = 'checked'
            #logic = ' '+logic+' '
            for line in sf:
                if line.strip() != 'No_results':
                    mslist.append(line.strip()) 
            sf.close()
                
            if len(mslist) > 0:
                mslisttmp = []
                for i in mslist:
                    j = 0
                    if i in xmlr:
                        j = int(fdate[xmlr[i]])
                    mslisttmp.append((i,j))
                mslisttmp.sort(key=operator.itemgetter(1))
                mslistnew = []
                for i in mslisttmp:
                    mslistnew.append(i[0])
                
                mslist = mslistnew[:]
                for i in mslist:
                    if i in xmlr:
                        senhist[sen[xmlr[i]]] += 1
                        rechist[rec[xmlr[i]]] += 1
                                
        if mslist == []:
            searchtermlist = searchterms.split(' ')
            s += 'No results for '+str(searchterms)+'<p>'#\''+str(logic.join(searchtermlist))+'\'.<p>'

        searchtermlist = []
        if mslist != [] and '@' in xmlprint:
            searchtermlist = searchterms.split(' ')
            s += str(len(mslist))+' results for \''+str(searchterms)+'\':<p>'#+str(logic.join(searchtermlist))+'\'.<p>'

        if len(senhist) > 0:
            s += '<p><b>Senders:</b><p>'
            for i in sorted(senhist.items(),key=operator.itemgetter(1),reverse=True):
                s += str('<a href="/current='+str(i[0])+'">'+str(name[i[0]])+' ('+str(i[1])+')<br>')
            s += '<p>'

        if len(rechist) > 0:
            s += '<p><b>Recipients:</b><p>'
            for i in sorted(rechist.items(),key=operator.itemgetter(1),reverse=True):
                s += str('<a href="/current='+str(i[0])+'">'+str(name[i[0]])+' ('+str(i[1])+')<br>')
            s += '<p>'
            
        #mslist2 = []
        #if net[period].has_edge(xmlprint.split('_')[1],xmlprint.split('_')[0]):
        #    mslist2 = net[period].get_edge_data(xmlprint.split('_')[1],xmlprint.split('_')[0])['l']
        mcount = 0
        linklist = defaultdict(list)
        corpuslist = {}
        yearlist = []
        for i in mslist:
            ss = ''
            sstxt = ''
            ssim = ''
            if '@' not in xmlprint:
                f = open('<INSERT PATH TO SPO XML FILES>'+xml[i])
            if '@' in xmlprint:
                f = open('<INSERT PATH TO SPO XML FILES>'+str(i))
            out = 0
            count = 0
            #linklist = []
            linklast = 0 
            xmlparsetmp = {}
            for lineraw in f:
                line = lineraw.strip().replace('<title/>','') # RARE TAG THAT MESSES UP HTML 
                for j in xmlparse:
                    if '<'+j+'>' in line:
                        xmlparsetmp[j] = line.strip()[len(j)+2:-(len(j)+3)]

                if '<linkseq ' in line:
                    count += 1
                    if 'spo2 corpus' in line:
                        linktmp = line.strip().split('>')[1][12:-9].replace('\\','/')
                        corpus = 2
                    if 'spo2 corpus' not in line:
                        linktmp = line.strip().split('>')[1][:-9].replace('\\','/')
                        corpus = 1

                    linklist[mcount].append(linktmp)
                    corpuslist[mcount] = corpus
                    linklast = 1

                if linklast == 1 and  '<linkseq ' not in line:
                    ssim += '<a href="/image='+str(mcount)+'_1">Images ('+str(len(linklist[mcount]))+')</a><br>'
                    linklast = 0

                if '<ctxt>' in line or '<cun>' in line:
                    out = 1
                if out == 1:
                    sstmp = line.strip().replace('<ctxt>','').replace('</ctxt>','').replace('<cun>','').replace('</cun>','')
                    for k in searchtermlist:
                        if ' '+k+' ' in sstmp:
                            sstmp = sstmp.replace(' '+k+' ',' <span>'+str(k)+'</span> ')
                        if ' '+k+'.' in sstmp:
                            sstmp = sstmp.replace(' '+k+'.',' <span>'+str(k)+'</span>.')
                        if ' '+k+',' in sstmp:
                            sstmp = sstmp.replace(' '+k+',',' <span>'+str(k)+'</span>,')
                        if ' '+k[0].upper()+k[1:]+' ' in sstmp:
                            sstmp = sstmp.replace(' '+k[0].upper()+k[1:]+' ',' <span>'+str(k[0].upper()+k[1:])+'</span> ')
                        if ' '+k[0].upper()+k[1:]+'.' in sstmp:
                            sstmp = sstmp.replace(' '+k[0].upper()+k[1:]+'.',' <span>'+str(k[0].upper()+k[1:])+'</span>.')
                        if ' '+k[0].upper()+k[1:]+',' in sstmp:
                            sstmp = sstmp.replace(' '+k[0].upper()+k[1:]+',',' <span>'+str(k[0].upper()+k[1:])+'</span>,')
                    sstxt += sstmp
                if '</ctxt>' in line or '</cun>' in line:
                    out = 0

            ss += '<p><a name="'+str(mcount)+'"></a>'+ssim

            #if xmlparsetmp['cyr'].isdigit():
            #    yearlist.append(int(xmlparsetmp['cyr']))

            if '@' not in xmlprint:
                if int(fdate[i]) > 15000000:
                    yearlist.append(int(fdate[i][:4])+(1.0/12.0)*(int(fdate[i][4:6])-1)+(1.0/365.0)*(int(fdate[i][6:8])-1))
            if '@' in xmlprint:
                if i in xmlr and int(fdate[xmlr[i]]) > 15000000:
                    yearlist.append(int(fdate[xmlr[i]][:4])+(1.0/12.0)*(int(fdate[xmlr[i]][4:6])-1)+(1.0/365.0)*(int(fdate[xmlr[i]][6:8])-1))

            for j in xmlparsetmp:
                if j in ['crep','cauth']:
                    if ';' not in xmlparsetmp[j]:
                        personlink = ''
                        if xmlparsetmp[j].strip() in number:
                            i0set = set([])
                            for i in mapto[number[xmlparsetmp[j].strip()]]:
                                i0set.add(i[0])
                                for ii in i[1]:
                                    if xmlparsetmp['cdoc'] == ii.replace('_',' '):
                                        personlink = i[0]
                            if personlink == '' and len(i0set) == 1:
                                personlink = list(i0set)[0]
                        if personlink == '':
                            ss += '<b>'+str(xmlparse[j])+':</b> '+str(xmlparsetmp[j])+'<br>'
                        if personlink != '':
                            ss += '<b>'+str(xmlparse[j])+':</b> <a href="/current='+str(personlink)+'">'+str(xmlparsetmp[j])+'</a><br>'
                    if ';' in xmlparsetmp[j]:
                        sstmp = '<b>'+str(xmlparse[j])+':</b> '
                        for jj in xmlparsetmp[j].split(';'):
                            personlink = ''
                            if jj.strip() in number:
                                for i in mapto[number[jj.strip()]]:
                                    for ii in i[1]:
                                        if xmlparsetmp['cdoc'] == ii.replace('_',' '):
                                            personlink = i[0]
                            if personlink == '':
                                sstmp += str(jj)+'; '
                            if personlink != '':
                                sstmp += '<a href="/current='+str(personlink)+'">'+str(jj)+'</a>; '

                        sstmp = sstmp[:-2]
                        ss += sstmp+'<br>'

                    #ss += '<b><a href="/current=''">'+xmlparse[j]+':</a></b> '+line.strip()[len(j)+2:-(len(j)+3)]+'<br>'

            for j in xmlparsetmp:
                if j not in ['crep','cauth']:
                    ss += '<b>'+str(xmlparse[j])+':</b> '+str(xmlparsetmp[j])+'<br>'

            ss += sstxt

            mcount += 1
            s += ss
            
        s += '</div>'
        
        if yearlist != []:
            s += '<div class="yearrange">'
            yr = math.ceil(yearlist[-1])-math.floor(yearlist[0])
            yr += int(yr == 0)
            s += '<div class="leftyear">'+str(int(math.floor(yearlist[0])))+'</div>'
            s += '<div class="rightyear">'+str(int(math.ceil(yearlist[-1])))+'</div>'
            mc = 0
            for i in yearlist:
                s += '<a href="http://localhost:8081/#'+str(mc)+'"><div class="bar" style="left: '+str(77.0+18.0*(float(i)-math.floor(yearlist[0]))/yr)+'%"></div></a>'
                mc += 1
            s += '</div>'

    if image != '':
        imagetuple = image.split('_')
        os.system('rm -f <INSERT PATH TO STATIC DIRECTORY>/static/*.jpg')
        s += '<div class="dark"></div>'
        os.system('cp <INSERT PATH TO SPO IMAGES>'+str(corpuslist[int(imagetuple[0])])+'/Images/'+linklist[int(imagetuple[0])][int(imagetuple[1])-1]+' <INSERT PATH TO STATIC DIRECTORY>/static/')

        s += '<div class="image"><div class="actualimage"><a href="/static/'+linklist[int(imagetuple[0])][int(imagetuple[1])-1].split('/')[-1]+'" target="blank"><img  width=100% src="../static/'+linklist[int(imagetuple[0])][int(imagetuple[1])-1].split('/')[-1]+'"></a></div>'
        s += '<div class="x"><a href="/current='+str(current)+'">X</a></div>'
        if int(imagetuple[1]) > 1:
            s += '<div class="prev"><a href="/image='+str(int(imagetuple[0]))+'_'+str(int(imagetuple[1])-1)+'">prev</a></div>'
        if int(imagetuple[1]) < len(linklist[int(imagetuple[0])]):
            s += '<div class="next"><a href="/image='+str(int(imagetuple[0]))+'_'+str(int(imagetuple[1])+1)+'">next</a></div>'
        s += '</div>'

    """
    floc = open('local.dot','w')
    floc.write('digraph floc\n{\n')
    tmpnet = net[period].subgraph(list(set(net[period].successors(current)).union(set(net[period].predecessors(current)))))
    for i in tmpnet.nodes():
        if i != current:
            floc.write('node "'+str(i)+'" [label="",shape="circle",color="black",style="filled"];\n')
    for i in tmpnet.edges():
        if current not in [i[0],i[1]]:
            floc.write('"'+str(i[0])+'" -> "'+str(i[1])+'";\n')
    floc.write('}\n')
    floc.close()
    os.system('neato local.dot -Tjpg -Goverlap=scale > local.jpg')
    """
    s += '<div class="searchbox"><form action="/search" method=POST><input type="text" size="10" name="search"><input type="submit" name="submit" value="Search">'#<input type="radio" name="logic" value="AND" '+str(checked1)+'>AND<input type="radio" name="logic" value="OR" '+str(checked2)+'>OR</form></div>'
    s += '</form></div>'
    return s
    

def displaylist(item,name,period,xmlprint):
    s = '<html><head><STYLE type = \"text/css\" media = \"screen\"\n<!--\n\-->\n</STYLE><LINK HREF=\"static/interfacestyle2.css\" rel=\"stylesheet\" type=\"text/css\" media=\"all\" title=\"Standard\"></head><div class="title"><b>Tudor Networks of Power</b></div>'
    s += '<div class="biglist">'
    s += '<b>Current period: </b>'+str(monfull[period])
    if period != 'all':
        s += ' ('+str(mfdate[period])+'-'+str(mtdate[period])+')'
    s += '<p>'
    s += '<b>Select period: </b>'
    for i in monarchs:
        if i in ['hen','mar','eli','edw','all','cus']:
            s += '<a href="/period='+str(i)+'">'+str(monfull[i])+'</a> - '
        if i not in ['hen','mar','eli','edw','all','cus']:
            s += '<a href="/period='+str(i)+'">'+str(monfull[i])+'</a> <a href="/delete='+str(monfull[i])+'"><sup><small>x</small></sup></a> - '
    s = s[:-3]
    s += '<p><b>Set custom period:</b> <form method="POST" action="/setperiod">from <input type="text" size="8" name="fdate" value="'+str(mfdate['cus'])+'"> to <input type="text" size="8" name="tdate" value="'+str(mtdate['cus'])+'"><input type="submit" name="submit" value="Set"></form><form method="POST" action="/save"><br><b>Name custom period: </b><input type="text" size="8" name="savename"><input type="submit" name="submit" value="Save"></form><p><a href="/edge">Edge list</a><p>'
    if womenonly == 0:
        s += '<a href="/womenonly=1">women only</a><p>'
    if womenonly == 1:
        s += '<a href="/womenonly=0">men and women</a><p>'
    s += '<table>'
    s += '<tr>'
    s += '<td>Rank</td>'
    s += '<td>Signature</td>'
    s += '<td><a href="/item=1">Name</a></td>'
    s += '<td><a href="/item=2">Total degree</a></td>'
    s += '<td><a href="/item=3">Out-degree</a></td>'
    s += '<td><a href="/item=4">In-degree</a></td>'
    s += '<td><a href="/item=5">Total strength</a></td>'
    s += '<td><a href="/item=6">Out-strength</a></td>'
    s += '<td><a href="/item=7">In-strength</a></td>'
    s += '<td><a href="/item=8">Eigenvector cent.</a></td>'
    s += '<td><a href="/item=9">Betweenness cent.</a></td>'
    s += '</tr>'
    cnt = 1

    rvl1 = len(rankvec['hen'])
    rvl2 = len(rankvec['edw'])
    rvl3 = len(rankvec['mar'])
    rvl4 = len(rankvec['eli'])

    for i in sorted(bigrank[period],key=operator.itemgetter(item),reverse=bool(item != 1)):#[:1000]:
        if womenonly == 0 or i[0] in women:
            s += '<tr><td>'+str(cnt)+'.</td>'

            col1 = 0
            if i[0] in rankvec['hen']:
                col1 = int(50+170.0*(1.0-1.0*math.log(rankvec['hen'][i[0]][0])/math.log(rvl1)))

            col2 = 0
            if i[0] in rankvec['edw']:
                col2 = int(50+170.0*(1.0-1.0*math.log(rankvec['edw'][i[0]][0])/math.log(rvl2)))

            col3 = 0
            if i[0] in rankvec['mar']:
                col3 = int(50+170.0*(1.0-1.0*math.log(rankvec['mar'][i[0]][0])/math.log(rvl3)))

            col4 = 0
            if i[0] in rankvec['eli']:
                col4 = int(50+170.0*(1.0-1.0*math.log(rankvec['eli'][i[0]][0])/math.log(rvl4)))

            s += '<td><div class="squarebox"><div class="square1" style="background-color:rgb('+str(col1)+','+str(col1)+','+str(col1)+')"></div><div class="square2" style="background-color:rgb('+str(col2)+','+str(col2)+','+str(col2)+')"></div><div class="square3" style="background-color:rgb('+str(col3)+','+str(col3)+','+str(col3)+')"></div><div class="square4" style="background-color:rgb('+str(col4)+','+str(col4)+','+str(col4)+')"></div></div></td>'
            if item == 1:
                s += '<td><i><a href="/current='+str(i[0])+'">'+str(i[1])+' ['+str(i[0])+']</a> (<a href="/similar='+str(i[0])+'">find similar</a>)</i></td>'
            if item != 1:
                s += '<td><a href="/current='+str(i[0])+'">'+str(i[1])+' ['+str(i[0])+']</a> (<a href="/similar='+str(i[0])+'">find similar</a>)</td>'
            c = 2
            for j in i[2:-2]:
                colrgb = str(hex(int(170.0*(1.0-(1.0*math.log(rankvec[period][i[0]][c-2])/math.log(len(rankvec[period])))))))[-2:].upper()
                col = ' bgcolor="#'+str(colrgb)+str(colrgb)+str(colrgb)+'"'
                if c != item:
                    s += '<td'+str(col)+'>'+str(j)+' ('+str(rankvec[period][i[0]][c-2])+')</td>\n'
                if c == item:
                    s += '<td'+str(col)+'><i>'+str(j)+' ('+str(rankvec[period][i[0]][c-2])+')</i></td>\n'
                c += 1
            s += '</tr>'
        cnt += 1
    s += '</table>'
    s += '</div>'

    s += '<div class="plot">'

    sx = ['','','','','','','','','','']    
    sy = ['','','','','','','','','','']    

    if x != '' and y != '':
        os.system('grep \''+str(period)+'\' bigrank.out | awk -F\'\\t\' \'{print $'+str(int(x)+1)+'" "$'+str(int(y)+1)+'}\' > plot')
        fpll = open('labels','w')
        fpll.write('set terminal postscript enhanced "Helvetica" 2\nset output "static/plot2.ps"\n')
        fpll.write('set xlabel "'+str(meas[int(x)-2])+'" font "Helvetica, 12"\n')
        fpll.write('set ylabel "'+str(meas[int(y)-2])+'" font "Helvetica, 12"\n')
        fpll.write('set xtics font "Helvetica, 12"\n')
        fpll.write('set ytics font "Helvetica, 12"\n')
        count = defaultdict(int)
        for i in bigrank[period]:
            if float(i[int(x)]) > 0 and float(i[int(y)]) > 0:
                fpll.write('set label "'+str(i[1])+'" at '+str(i[int(x)])+','+str(i[int(y)])+' rotate by -'+str(30+5*count[(i[int(x)],i[int(y)])])+'\n')
                count[(i[int(x)],i[int(y)])] += 1
        fpll.close()
        os.system('gnuplot plot.plotscript')
        os.system('cat labels plot.plotscript2 > plot.plotscript.tmp')
        os.system('gnuplot plot.plotscript.tmp')
        s += '<a target="_blank" href="/static/plot2.ps"><img src="/static/plot.png"></a>'
        sx[int(x)-2] = 'selected'
        sy[int(y)-2] = 'selected'

    s += '<p><form action="/plot" method="POST">'
    s += 'X-Axis:<br><select name="x">'
    s += '<option value="2"'+str(sx[0])+'>Total degree</option>'
    s += '<option value="3"'+str(sx[1])+'>Out-degree</option>'
    s += '<option value="4"'+str(sx[2])+'>In-degree</option>'
    s += '<option value="5"'+str(sx[3])+'>Total strength</option>'
    s += '<option value="6"'+str(sx[4])+'>Out-strength</option>'
    s += '<option value="7"'+str(sx[5])+'>In-strength</option>'
    s += '<option value="10"'+str(sx[8])+'>Eigenvector centrality rank</option>'
    s += '<option value="11"'+str(sx[9])+'>Betweenness rank</option>'
    s += '</select>'
    s += '<p>Y-axis:<br><select name="y">'
    s += '<option value="2"'+str(sy[0])+'>Total degree</option>'
    s += '<option value="3"'+str(sy[1])+'>Out-degree</option>'
    s += '<option value="4"'+str(sy[2])+'>In-degree</option>'
    s += '<option value="5"'+str(sy[3])+'>Total strength</option>'
    s += '<option value="6"'+str(sy[4])+'>Out-strength</option>'
    s += '<option value="7"'+str(sy[5])+'>In-strength</option>'
    s += '<option value="10"'+str(sy[8])+'>Eigenvector centrality rank</option>'
    s += '<option value="11"'+str(sy[9])+'>Betweenness rank</option>'
    s += '</select>'
    s += '<p><input type="submit" name="submit" value="Plot">'
    s += '</form>'
    s += '</div>'

    return s


def dist(r1,r2,n):
    d = 0
    for i in range(len(r1)):
        d += ((1.0*math.log(r1[i])/math.log(n))-(1.0*math.log(r2[i])/math.log(n)))*((1.0*math.log(r1[i])/math.log(n))-(1.0*math.log(r2[i])/math.log(n)))
    return math.sqrt(d)


def reldist(r1,r2,n):
    avr1 = 0
    for i in range(len(r1)):
        avr1 += 1.0*math.log(r1[i])/(math.log(n)*len(r1))
    avr2 = 0
    for i in range(len(r2)):
        avr2 += 1.0*math.log(r2[i])/(math.log(n)*len(r2))
    d = 0
    for i in range(len(r1)):
        d += ((1.0*math.log(r1[i])/(math.log(n)*avr1))-(1.0*math.log(r2[i])/(math.log(n)*avr2)))*((1.0*math.log(r1[i])/(math.log(n)*avr1))-(1.0*math.log(r2[i])/(math.log(n)*avr2)))
    return math.sqrt(d)
    
def displaysimilar(item,name,period,xmlprint,current):
    s = '<html><head><STYLE type = \"text/css\" media = \"screen\"\n<!--\n\-->\n</STYLE><LINK HREF=\"static/interfacestyle2.css\" rel=\"stylesheet\" type=\"text/css\" media=\"all\" title=\"Standard\"></head><div class="title"><b>Tudor Networks of Power</b></div>'
    s += '<div class="biglist">'
    s += '<b>Current period: </b>'+str(monfull[period])
    if period != 'all':
        s += ' ('+str(mfdate[period])+'-'+str(mtdate[period])+')'
    s += '<p>'
    s += '<b>Select period: </b>'
    for i in monarchs:
        if i in ['hen','mar','eli','edw','all','cus']:
            if current in rankvec[i]:
                s += '<a href="/period='+str(i)+'">'+str(monfull[i])+'</a> - '
            if current not in rankvec[i]:
                s += str(monfull[i])+' - '
        if i not in ['hen','mar','eli','edw','all','cus']:
            if current in rankvec[i]:
                s += '<a href="/period='+str(i)+'">'+str(monfull[i])+'</a> <a href="/delete='+str(monfull[i])+'"><sup><small>x</small></sup></a> - '
            if current not in rankvec[i]:
                s += str(monfull[i])+' <a href="/delete='+str(monfull[i])+'"><sup><small>x</small></sup></a> - '
    s = s[:-3]
    s += '<p><b>Set custom period:</b> <form method="POST" action="/setperiod">from <input type="text" size="8" name="fdate" value="'+str(mfdate['cus'])+'"> to <input type="text" size="8" name="tdate" value="'+str(mtdate['cus'])+'"><input type="submit" name="submit" value="Set"></form><form method="POST" action="/save"><br><b>Name custom period: </b><input type="text" size="8" name="savename"><input type="submit" name="submit" value="Save"></form><p><a href="/edge">Edge list</a><p>'
    if disttype == 'abs':
        s += '<p>Distance type: absolute (<a href="/switchdist=rel">switch to relative</a>)<p>'
    if disttype == 'rel':
        s += '<p>Distance type: relative (<a href="/switchdist=abs">switch to absolute</a>)<p>'
    s += 'Displaying most similar rank profiles to '+str(name[current])+' ('+str(current)+'):<p>'
    s += '<table>'
    s += '<tr>'
    s += '<td>Rank</td>'
    s += '<td><a href="/item=1">Name</a></td>'
    s += '<td><a href="/item=2">Total degree</a></td>'
    s += '<td><a href="/item=3">Out-degree</a></td>'
    s += '<td><a href="/item=4">In-degree</a></td>'
    s += '<td><a href="/item=5">Total strength</a></td>'
    s += '<td><a href="/item=6">Out-strength</a></td>'
    s += '<td><a href="/item=7">In-strength</a></td>'
    s += '<td><a href="/item=8">Eigenvector cent.</a></td>'
    s += '<td><a href="/item=9">Betweenness cent.</a></td>'
    s += '</tr>'
    cnt = 1
    bigranktmp = []
    for i in bigrank[period]:
        if disttype == 'rel':
            bigranktmp.append(tuple(list(i)+[reldist(rankvec[period][i[0]],rankvec[period][current],len(rankvec[period]))]))
        if disttype == 'abs':
            bigranktmp.append(tuple(list(i)+[dist(rankvec[period][i[0]],rankvec[period][current],len(rankvec[period]))]))
    cc = len(bigranktmp[0])-1
    sbrt = sorted(bigranktmp,key=operator.itemgetter(cc),reverse=False)
    print(sbrt[:10])
    print(sbrt[-10:])
    for i in sbrt[:1000]:
        s += '<tr><td>'+str(cnt)+'.</td>'
        #if item == 1:
        #    s += '<td><i><a href="/current='+str(i[0])+'">'+str(i[1])+' ['+str(i[0])+']</a> (<a href="/similar='+str(i[0])+'">find similar</a>)</i></td>'
        #if item != 1:
        s += '<td><a href="/current='+str(i[0])+'">'+str(i[1])+' ['+str(i[0])+']</a> (<a href="/similar='+str(i[0])+'">find similar</a>)</td>'
        c = 2
        for j in i[2:-3]:
            colrgb = str(hex(int(170.0*(1.0-(1.0*math.log(rankvec[period][i[0]][c-2])/math.log(len(rankvec[period])))))))[-2:].upper()
            col = ' bgcolor="#'+str(colrgb)+str(colrgb)+str(colrgb)+'"'
            #if c != item:
            s += '<td'+str(col)+'>'+str(j)+' ('+str(rankvec[period][i[0]][c-2])+')</td>\n'
            #if c == item:
            #    s += '<td'+str(col)+'><i>'+str(j)+' ('+str(rankvec[period][i[0]][c-2])+')</i></td>\n'
            c += 1
        s += '</tr>'
        cnt += 1
    s += '</table>'
    s += '</div>'

    return s


def displayedgelist(item,name,period,xmlprint):
    s = '<html><head><STYLE type = \"text/css\" media = \"screen\"\n<!--\n\-->\n</STYLE><LINK HREF=\"static/interfacestyle.css\" rel=\"stylesheet\" type=\"text/css\" media=\"all\" title=\"Standard\"></head><div class="title"><b>Tudor Networks of Power</b></div>'
    s += '<div class="biglist">'
    s += '<b>Current period: </b>'+str(monfull[period])
    if period != 'all':
        s += ' ('+str(mfdate[period])+'-'+str(mtdate[period])+')'
    s += '<p>'
    s += '<b>Select period: </b>'
    for i in monarchs:
        if i in ['hen','mar','eli','edw','all','cus']:
            s += '<a href="/period='+str(i)+'">'+str(monfull[i])+'</a> - '
        if i not in ['hen','mar','eli','edw','all','cus']:
            s += '<a href="/period='+str(i)+'">'+str(monfull[i])+'</a> <a href="/delete='+str(monfull[i])+'"><sup><small>x</small></sup></a> - '
    s = s[:-3]
    s += '<p><b>Set custom period:</b> <form method="POST" action="/setperiod">from <input type="text" size="8" name="fdate" value="'+str(mfdate['cus'])+'"> to <input type="text" size="8" name="tdate" value="'+str(mtdate['cus'])+'"><input type="submit" name="submit" value="Set"></form><form method="POST" action="/save"><br><b>Name custom period: </b><input type="text" size="8" name="savename"><input type="submit" name="submit" value="Save"></form><p>'
    s += '<a href="/node">Node list</a><p>' 
    s += '<table>'
    s += '<tr>'
    s += '<td>Rank</td>'
    s += '<td>Name 1</td>'
    s += '<td>Name 2</td>'
    s += '<td><a href="/item=1">Weight</a></td>'
    s += '<td><a href="/item=2">Edge betweenness</a></td>'
    s += '</tr>'
    cnt = 1
    for i in sorted(bigedgerank[period],key=operator.itemgetter(item+3),reverse=True)[:1000]:
        s += '<tr><td>'+str(cnt)+'.</td>'
        s += '<td><a href="/current='+str(i[0])+'">'+str(i[1])+' ['+str(i[0])+']</a></td>'
        s += '<td><a href="/current='+str(i[2])+'">'+str(i[3])+' ['+str(i[2])+']</a></td>'
        c = 1
        for j in i[4:-1]:
            if c != item and j != i[4]:
                s += '<td>'+str(j)+'</td>'
            if c == item and j != i[4]:
                s += '<td><i>'+str(j)+'</i></td>'
            if c != item and j == i[4]:
                s += '<td><a href="/xmlprint='+str(i[0])+'_'+str(i[2])+'">'+str(j)+'</a></td>'
            if c == item and j == i[4]:
                s += '<td><i><a href="/xmlprint='+str(i[0])+'_'+str(i[2])+'">'+str(j)+'</a></i></td>'
            c += 1
        s += '</tr>'
        cnt += 1
    s += '</table>'
    s += '</div>'

    return s

def recalccus():
    fr['cus'] = defaultdict(list)
    to['cus'] = defaultdict(list)
    frl['cus'] = defaultdict(list)
    tol['cus'] = defaultdict(list)
    net['cus'] = networkx.DiGraph()

    c = 0
    for l in llink:
        if mfdate['cus'] <= l[2] <= l[3] <= mtdate['cus']:
            if net['cus'].has_edge(l[0],l[1]):
                ltmp = net['cus'].get_edge_data(l[0],l[1])['l']
                ltmp.append(c)
                net['cus'].add_edge(l[0],l[1])
                net['cus'][l[0]][l[1]].update({'l':ltmp,'w':len(ltmp)})
                #net['cus'].add_edge(l[0],l[1],{'l':ltmp,'w':len(ltmp)})
            if not net['cus'].has_edge(l[0],l[1]):
                net['cus'].add_edge(l[0],l[1])
                net['cus'][l[0]][l[1]].update({'l':[c],'w':1})
                #net['cus'].add_edge(l[0],l[1],{'l':[c],'w':1})
            fr['cus'][l[0]].append(c)
            to['cus'][l[1]].append(c)
            frl['cus'][l[0]].append(l[1])
            tol['cus'][l[1]].append(l[0])
        c += 1

    for l in net['cus'].edges():
        ltmp = net['cus'].get_edge_data(l[0],l[1])['l']
        dltmp = {}
        dltmp['l'] = ltmp
        dltmp['w'] = len(ltmp)
        net['cus'].add_edge(l[0],l[1])
        net['cus'][l[0]][l[1]].update(dltmp)


    degrank['cus'] = {}
    idegrank['cus'] = {}
    odegrank['cus'] = {}
    wdegrank['cus'] = {}
    widegrank['cus'] = {}
    wodegrank['cus'] = {}
    eigrank['cus'] = {}
    betwrank['cus'] = {}
    edgebetwrank['cus'] = {}
    wrank['cus'] = {}
    
    sd = sorted(dict(net['cus'].degree()).values(),reverse=True)
    for j in sorted(net['cus'].degree().items(),key=operator.itemgetter(1),reverse=True):
        degrank['cus'][j[0]] = sd.index(j[1])+1
        
    sid = sorted(dict(net['cus'].in_degree()).values(),reverse=True)
    for j in sorted(net['cus'].in_degree().items(),key=operator.itemgetter(1),reverse=True):
        idegrank['cus'][j[0]] = sid.index(j[1])+1
        
    sod = sorted(dict(net['cus'].out_degree()).values(),reverse=True)
    for j in sorted(net['cus'].out_degree().items(),key=operator.itemgetter(1),reverse=True):
        odegrank['cus'][j[0]] = sod.index(j[1])+1
        
    swd = sorted(dict(net['cus'].degree(weight='w')).values(),reverse=True)
    for j in sorted(net['cus'].degree(weight='w').items(),key=operator.itemgetter(1),reverse=True):
        wdegrank['cus'][j[0]] = swd.index(j[1])+1
        
    swid = sorted(dict(net['cus'].in_degree(weight='w')).values(),reverse=True)
    for j in sorted(net['cus'].in_degree(weight='w').items(),key=operator.itemgetter(1),reverse=True):
        widegrank['cus'][j[0]] = swid.index(j[1])+1
        
    swod = sorted(dict(net['cus'].out_degree(weight='w')).values(),reverse=True)
    for j in sorted(net['cus'].out_degree(weight='w').items(),key=operator.itemgetter(1),reverse=True):
        wodegrank['cus'][j[0]] = swod.index(j[1])+1
        
    print('Betweenness...')
    betw['cus'] = networkx.betweenness_centrality(net['cus'])
    
    print('Eigenvector centrality...')
    eig['cus'] = networkx.eigenvector_centrality(net['cus'])

    print('Edge betweenness...')
    edgebetw['cus'] = networkx.edge_betweenness_centrality(net['cus'])
    eigrank['cus'] = {}
    seig = sorted(eig['cus'].values(),reverse=True)
    for j in sorted(eig['cus'].items(),key=operator.itemgetter(1),reverse=True):
        eigrank['cus'][j[0]] = seig.index(j[1])+1
    
    betwrank['cus'] = {}
    sbetw = sorted(betw['cus'].values(),reverse=True)
    for j in sorted(betw['cus'].items(),key=operator.itemgetter(1),reverse=True):
        betwrank['cus'][j[0]] = sbetw.index(j[1])+1
        
    bigrank['cus'] = []
    rankvec['cus'] = {}
    for i in net['cus'].nodes():
        bigrank['cus'].append((i,name[i],net['cus'].degree(i),net['cus'].out_degree(i),net['cus'].in_degree(i),net['cus'].degree(i,weight='w'),net['cus'].out_degree(i,weight='w'),net['cus'].in_degree(i,weight='w'),eig['cus'][i],betw['cus'][i],eigrank['cus'][i],betwrank['cus'][i]))
        rankvec['cus'][i] = (degrank['cus'][i],odegrank['cus'][i],idegrank['cus'][i],wdegrank['cus'][i],wodegrank['cus'][i],widegrank['cus'][i],eigrank['cus'][i],betwrank['cus'][i])
        
    fbr = open('bigrank.out','w')
    for i in bigrank:
        for j in bigrank[i]:
            fbr.write(str(i)+'\t'+str(j[0])+'\t')
            for k in j[2:]:
                fbr.write(str(k)+'\t')
            fbr.write('\n')
            #fbr.write(str(eigrank[i][j[0]])+'\t'+str(betwrank[i][j[0]])+'\n')
    fbr.close()

    edgebetwrank['cus'] = {}
    sedgebetw = sorted(edgebetw['cus'].values(),reverse=True)
    for j in sorted(edgebetw['cus'].items(),key=operator.itemgetter(1),reverse=True):
        edgebetwrank['cus'][j[0]] = sedgebetw.index(j[1])+1
        
    bigedgerank['cus'] = []
    for i in net['cus'].edges():
        bigedgerank['cus'].append((i[0],name[i[0]],i[1],name[i[1]],net['cus'].get_edge_data(*i)['w'],edgebetw['cus'][(i[0],i[1])],edgebetwrank['cus'][(i[0],i[1])]))
    
    fbr = open('bigedgerank.out','w')
    for i in bigedgerank:
        for j in bigedgerank[i]:
            fbr.write(str(i)+'\t'+str(j[0])+'\t'+str(j[2])+'\t')
            for k in j[4:]:
                fbr.write(str(k)+'\t')
            fbr.write('\n')
    fbr.close()

    fp = open('period','w')
    for i in monarchs:
        if i not in ['eli','mar','edw','hen','all']:
            fp.write(str(i)+'\t'+str(mfdate[i])+' '+str(mtdate[i])+'\n')
    fp.close()

def copycus(new):
    fr[new] = fr['cus'].copy()
    to[new] = to['cus'].copy()
    frl[new] = frl['cus'].copy()
    tol[new] = tol['cus'].copy()
    net[new] = net['cus'].copy()

    degrank[new] = degrank['cus'].copy()
    idegrank[new] = idegrank['cus'].copy()
    odegrank[new] = odegrank['cus'].copy()
    wdegrank[new] = wdegrank['cus'].copy()
    widegrank[new] = widegrank['cus'].copy()
    wodegrank[new] = wodegrank['cus'].copy()
    eigrank[new] = eigrank['cus'].copy()
    betwrank[new] = betwrank['cus'].copy()
    edgebetwrank[new] = edgebetwrank['cus'].copy()

    betw[new] = betw['cus'].copy()
    edgebetw[new] = edgebetw['cus'].copy()
    eig[new] = eig['cus'].copy()
    
    bigrank[new] = bigrank['cus'][:]
    rankvec[new] = rankvec['cus'].copy()
    bigedgerank[new] = bigedgerank['cus'][:]

    fbr = open('bigrank.out','w')
    for i in bigrank:
        for j in bigrank[i]:
            fbr.write(str(i)+'\t'+str(j[0])+'\t')
            for k in j[2:]:
                fbr.write(str(k)+'\t')
            fbr.write('\n')
            #fbr.write(str(eigrank[i][j[0]])+'\t'+str(betwrank[i][j[0]])+'\n')
    fbr.close()

    fbr = open('bigedgerank.out','w')
    for i in bigedgerank:
        for j in bigedgerank[i]:
            fbr.write(str(i)+'\t'+str(j[0])+'\t'+str(j[2])+'\t')
            for k in j[4:]:
                fbr.write(str(k)+'\t')
            fbr.write('\n')
    fbr.close()

    fp = open('period','w')
    for i in monarchs:
        if i not in ['eli','mar','edw','hen','all']:
            fp.write(str(i)+'\t'+str(mfdate[i])+' '+str(mtdate[i])+'\n')
    fp.close()

def rmcus(new):
    fr.pop(new)
    to.pop(new)
    frl.pop(new)
    tol.pop(new)
    net.pop(new)

    degrank.pop(new)
    idegrank.pop(new)
    odegrank.pop(new)
    wdegrank.pop(new)
    widegrank.pop(new)
    wodegrank.pop(new)
    eigrank.pop(new)
    betwrank.pop(new)

    betw.pop(new)
    eig.pop(new)
    
    bigrank.pop(new)
    bigedgerank.pop(new)
    
    fbr = open('bigrank.out','w')
    for i in bigrank:
        for j in bigrank[i]:
            fbr.write(str(i)+'\t'+str(j[0])+'\t')
            for k in j[2:]:
                fbr.write(str(k)+'\t')
            fbr.write('\n')
            #fbr.write(str(eigrank[i][j[0]])+'\t'+str(betwrank[i][j[0]])+'\n')
    fbr.close()

    fbr = open('bigedgerank.out','w')
    for i in bigedgerank:
        for j in bigedgerank[i]:
            fbr.write(str(i)+'\t'+str(j[0])+'\t'+str(j[2])+'\t')
            for k in j[4:]:
                fbr.write(str(k)+'\t')
            fbr.write('\n')
    fbr.close()

    fp = open('period','w')
    for i in monarchs:
        if i not in ['eli','mar','edw','hen','all']:
            fp.write(str(i)+'\t'+str(mfdate[i])+' '+str(mtdate[i])+'\n')
    fp.close()


f = open('fromto_all_place_mapped_sorted')
ff = open('people_docs_auto')
fff = open('added_people')
ffff = open('renamed_people')
fffff = open('cleanlinkeddata.out')
wf = open('final_women.out')

print('Loading data...')

mfdate = {}
mtdate = {}
mfdate['hen'] = '15090421'
mtdate['hen'] = '15470128'
mfdate['edw'] = '15470128'
mtdate['edw'] = '15530706'
mfdate['mar'] = '15530706'
mtdate['mar'] = '15581117'
mfdate['eli'] = '15581117'
mtdate['eli'] = '16030324'
mfdate['all'] = '10000000'
mtdate['all'] = '20000000'
mfdate['cus'] = '10000000'
mtdate['cus'] = '10000000' #EMPTY TO START WITH

monarchs = ['hen','edw','mar','eli','all']
fp = open('period')
for line in fp:
    l = line.strip().split()
    mfdate[l[0]] = l[1]
    mtdate[l[0]] = l[2] 
    monarchs.append(l[0])
fp.close()

for i in monarchs:
    if i not in monfull:
        monfull[i] = i.replace('_',' ')

c = 0
llink = []
fdate = {}
tdate = {}
xml = {}
xmlr = {}
msr = {}
net = {}
fr = {}
to = {}
frl = {}
tol = {}
net = {}
eig = {}
betw = {}
edgebetw = {}
allar = defaultdict(list)
sen = {}
rec = {}
womenonly = 0
disttype = 'abs'
for i in monarchs:
    fr[i] = defaultdict(list)
    to[i] = defaultdict(list)
    frl[i] = defaultdict(list)
    tol[i] = defaultdict(list)
    net[i] = networkx.DiGraph()

for line in f:
    l = line.strip().split('\t')
    llink.append(l[:])
    fdate[c] = l[2]
    tdate[c] = l[3]
    xml[c] = l[6]
    xmlr[l[6]] = c
    msr[l[4]] = c
    allar[l[0]].append(c)
    allar[l[1]].append(c)
    sen[c] = l[0]
    rec[c] = l[1]

    for i in monarchs:
        if mfdate[i] <= l[2] <= l[3] <= mtdate[i]:
            if net[i].has_edge(l[0],l[1]):
                ltmp = net[i].get_edge_data(l[0],l[1])['l']
                ltmp.append(c)
                net[i].add_edge(l[0],l[1])
                net[i][l[0]][l[1]].update({'l':ltmp,'w':len(ltmp)})
                #net[i].add_edge(l[0],l[1],{'l':ltmp,'w':len(ltmp)})
            if not net[i].has_edge(l[0],l[1]):
                net[i].add_edge(l[0],l[1])
                net[i][l[0]][l[1]].update({'l':[c],'w':1})
                #net[i].add_edge(l[0],l[1],{'l':[c],'w':1})
            fr[i][l[0]].append(c)
            to[i][l[1]].append(c)
            frl[i][l[0]].append(l[1])
            tol[i][l[1]].append(l[0])
    
    #if c == 10000:
    #    break

    if c%100 == 0:
        print(c)
    c += 1

"""
print('Creating weights...')

for i in monarchs:
    for l in net[i].edges():
        ltmp = net[i].get_edge_data(l[0],l[1])['l']
        dltmp = {}
        dltmp['l'] = ltmp
        dltmp['w'] = len(ltmp)
        net[i].add_edge(l[0],l[1],dltmp)
"""

degrank = {}
idegrank = {}
odegrank = {}
wdegrank = {}
widegrank = {}
wodegrank = {}
eigrank = {}
betwrank = {}
edgebetwrank = {}
wrank = {}
bigrank = {}
rankvec = {}
bigedgerank = {}

recalculate = 0

if recalculate == 1:
    for i in monarchs:
        degrank[i] = {}
        idegrank[i] = {}
        odegrank[i] = {}
        wdegrank[i] = {}
        widegrank[i] = {}
        wodegrank[i] = {}
        wrank[i] = {}
        eigrank[i] = {}
        betwrank[i] = {}
        edgebetwrank[i] = {}
        
        print('Ranking '+str(i))
    
        sd = sorted(dict(net[i].degree()).values(),reverse=True)
        for j in sorted(net[i].degree().items(),key=operator.itemgetter(1),reverse=True):
            degrank[i][j[0]] = sd.index(j[1])+1
        
        sid = sorted(dict(net[i].in_degree()).values(),reverse=True)
        for j in sorted(net[i].in_degree().items(),key=operator.itemgetter(1),reverse=True):
            idegrank[i][j[0]] = sid.index(j[1])+1
        
        sod = sorted(dict(net[i].out_degree()).values(),reverse=True)
        for j in sorted(net[i].out_degree().items(),key=operator.itemgetter(1),reverse=True):
            odegrank[i][j[0]] = sod.index(j[1])+1
        
        swd = sorted(dict(net[i].degree(weight='w')).values(),reverse=True)
        for j in sorted(net[i].degree(weight='w').items(),key=operator.itemgetter(1),reverse=True):
            wdegrank[i][j[0]] = swd.index(j[1])+1
        
        swid = sorted(dict(net[i].in_degree(weight='w')).values(),reverse=True)
        for j in sorted(net[i].in_degree(weight='w').items(),key=operator.itemgetter(1),reverse=True):
            widegrank[i][j[0]] = swid.index(j[1])+1
        
        swod = sorted(dict(net[i].out_degree(weight='w')).values(),reverse=True)
        for j in sorted(net[i].out_degree(weight='w').items(),key=operator.itemgetter(1),reverse=True):
            wodegrank[i][j[0]] = swod.index(j[1])+1

        weights = {}
        for j in net[i].edges():
            weights[(j[0],j[1])] = net[i].get_edge_data(*j)['w']
        sw = sorted(weights.values(),reverse=True)
        for j in sorted(weights.items(),key=operator.itemgetter(1),reverse=True):
            wrank[i][j[0]] = sw.index(j[1])+1
        
        print('Betweenness...')
        betw[i] = networkx.betweenness_centrality(net[i])
    
        print('Eigenvector centrality...')
        eig[i] = networkx.eigenvector_centrality(net[i])

        print('Edge betweenness...')
        edgebetw[i] = networkx.edge_betweenness_centrality(net[i])
        
        eigrank[i] = {}
        seig = sorted(eig[i].values(),reverse=True)
        for j in sorted(eig[i].items(),key=operator.itemgetter(1),reverse=True):
            eigrank[i][j[0]] = seig.index(j[1])+1
    
        betwrank[i] = {}
        sbetw = sorted(betw[i].values(),reverse=True)
        for j in sorted(betw[i].items(),key=operator.itemgetter(1),reverse=True):
            betwrank[i][j[0]] = sbetw.index(j[1])+1
        
        edgebetwrank[i] = {}
        sedgebetw = sorted(edgebetw[i].values(),reverse=True)
        for j in sorted(edgebetw[i].items(),key=operator.itemgetter(1),reverse=True):
            edgebetwrank[i][j[0]] = sedgebetw.index(j[1])+1

calcyears = 0
if calcyears == 1:
    cusfsaf = mfdate['cus'][:]
    custsaf = mtdate['cus'][:]

    for yr in range(1510,1603):
        mfdate['cus'] = str(yr)+'0101'
        mtdate['cus'] = str(yr)+'1231'
        recalccus()
        copycus(str(yr))
        if str(yr) not in monarchs:
            monarchs.append(str(yr))
        mfdate[str(yr)] = str(yr)+'0101'
        mtdate[str(yr)] = str(yr)+'1231'
        monfull[str(yr)] = str(yr)
    
    mfdate['cus'] = cusfsaf
    mtdate['cus'] = custsaf
            
name = {}
# TEMPORARY ERROR FIX
name['37204'] = 'ERROR'
name['40000'] = 'ERROR'

alias = defaultdict(list)

for line in ff:
    l = line.strip().split('\t')
    name[l[0]] = l[1]
    l[2] = l[2].replace(' ','')
    if ';' not in l[2] and ',' not in l[2]:
        alias[l[2]].append((l[1],l[3].split()))
    if ';' not in l[2] and ',' in l[2]:
        l1split = l[1].replace(', and ',' and ').replace(' and ',', ').replace(', ',',').split(',')
        if len(l1split) == len(l[2].split(',')):
            for k in range(len(l1split)):
                alias[l[2].split(',')[k]].append((l1split[k],l[3].split()))
        else:
            for k in l[2].split(','):
                alias[k].append((l[1],l[3].split()))
    if ';' in l[2] and ',' not in l[2]:
        ls = l[2].split(';')
        for k in set(ls):
            lss = []
            for kk in range(len(ls)):
                if k == ls[kk]:
                    lss.append(l[3].split()[kk])
            alias[ls[kk]].append((l[1],lss))

    if ';' in l[2] and ',' in l[2]:
        ls = l[2].split(';')
        for k in set(ls):
            lss = []
            for kk in range(len(ls)):
                if k == ls[kk]:
                    lss.append(l[3].split()[kk])
                l1split = l[1].replace(', and ',' and ').replace(' and ',', ').replace(', ',',').split(',')
                if len(l1split) == len(ls[kk].split(',')):
                    for kkk in range(len(l1split)):
                        alias[ls[kk].split(',')[kkk]].append((l1split[kkk],lss))
                else:
                    for kkk in ls[kk].split(','):
                        alias[kkk].append((l[1],lss))
            
for line in fff:
    l = line.strip().split('\t')
    name[l[0]] = l[1]

for line in ffff:
    l = line.strip().split('\t')
    name[l[0]] = l[1]

women = set([])
for line in wf:
    l = line.strip()
    women.add(l)

number = {}
for i in name:
    number[name[i]] = i

mapto = defaultdict(list)
for i in alias:
    for j in alias[i]:
        if j[0] in number:
            mapto[number[j[0]]].append((i,j[1]))

link = {}
for line in fffff:
    l = line.strip().split('\t')
    #print(l)
    link[l[0]] = l[2]

for k in monarchs:
    for i in set(fr[k].keys()).union(set(to[k].keys())):
        if i not in name:
            if i in fr[k]:
                print('ERROR: No name for ID '+str(i)+':')
                #for j in fr[i]:
                #    print(link[j])
                #    print(printxml(xml[j]))
            if i in to[k]:
                print('ERROR: No name for ID '+str(i)+':')
                #for j in to[i]:
                #    print(link[j])
                #    print(printxml(xml[j]))


print('Calculating rankings...')

recalcset = set(monarchs)

if recalculate == 0:
    sds = {}
    sids = {}
    sods = {}
    swds = {}
    swids = {}
    swods = {}
    sw = {}
    for i in monarchs:
        degrank[i] = {}
        idegrank[i] = {}
        odegrank[i] = {}
        wdegrank[i] = {}
        widegrank[i] = {}
        wodegrank[i] = {}
        wrank[i] = {}
        eigrank[i] = {}
        betwrank[i] = {}
        edgebetwrank[i] = {}
        eig[i] = {}
        betw[i] = {}
        edgebetw[i] = {}
        bigrank[i] = []
        rankvec[i] = {}
        bigedgerank[i] = []

        sds[i] = sorted(dict(net[i].degree()).values(),reverse=True)
        sids[i] = sorted(dict(net[i].in_degree()).values(),reverse=True)
        sods[i] = sorted(dict(net[i].out_degree()).values(),reverse=True)
        swds[i] = sorted(dict(net[i].degree(weight='w')).values(),reverse=True)
        swids[i] = sorted(dict(net[i].in_degree(weight='w')).values(),reverse=True)
        swods[i] = sorted(dict(net[i].out_degree(weight='w')).values(),reverse=True)

        weights = {}
        for j in net[i].edges():
            weights[(j[0],j[1])] = net[i].get_edge_data(*j)['w']
        sw[i] = sorted(weights.values(),reverse=True)
        for j in sorted(weights.items(),key=operator.itemgetter(1),reverse=True):
            wrank[i][j[0]] = sw[i].index(j[1])+1


    fbr = open('bigrank.out')
    for line in fbr:
        l = line.strip().split('\t')
        degrank[l[0]][l[1]] = sds[l[0]].index(int(l[2]))+1
        odegrank[l[0]][l[1]] = sods[l[0]].index(int(l[3]))+1
        idegrank[l[0]][l[1]] = sids[l[0]].index(int(l[4]))+1
        wdegrank[l[0]][l[1]] = swds[l[0]].index(int(l[5]))+1
        wodegrank[l[0]][l[1]] = swods[l[0]].index(int(l[6]))+1
        widegrank[l[0]][l[1]] = swids[l[0]].index(int(l[7]))+1

        """
        degrank[l[0]][l[1]] = int(l[2])
        odegrank[l[0]][l[1]] = int(l[3])
        idegrank[l[0]][l[1]] = int(l[4])
        wdegrank[l[0]][l[1]] = int(l[5])
        wodegrank[l[0]][l[1]] = int(l[6])
        widegrank[l[0]][l[1]] = int(l[7])
        """
        eig[l[0]][l[1]] = float(l[8])
        betw[l[0]][l[1]] = float(l[9])
        eigrank[l[0]][l[1]] = int(float(l[10]))
        betwrank[l[0]][l[1]] = int(float(l[11]))
        bigrank[l[0]].append((l[1],name[l[1]],int(l[2]),int(l[3]),int(l[4]),int(l[5]),int(l[6]),int(l[7]),float(l[8]),float(l[9]),float(l[10]),float(l[11])))
        rankvec[l[0]][l[1]] = (degrank[l[0]][l[1]],odegrank[l[0]][l[1]],idegrank[l[0]][l[1]],wdegrank[l[0]][l[1]],wodegrank[l[0]][l[1]],widegrank[l[0]][l[1]],eigrank[l[0]][l[1]],betwrank[l[0]][l[1]])
    fbr.close()

    fbr = open('bigedgerank.out')
    for line in fbr:
        l = line.strip().split('\t')
        if l[0] in recalcset:
            recalcset.remove(l[0])
        wrank[l[0]][(l[1],l[2])] = sw[l[0]].index(int(l[3]))+1
        edgebetw[l[0]][(l[1],l[2])] = float(l[4])
        edgebetwrank[l[0]][(l[1],l[2])] = int(float(l[5]))
        bigedgerank[l[0]].append((l[1],name[l[1]],l[2],name[l[2]],int(l[3]),float(l[4]),int(l[5])))
    fbr.close()

if recalculate == 0 and len(recalcset) > 0:
    for i in recalcset:
        degrank[i] = {}
        idegrank[i] = {}
        odegrank[i] = {}
        wdegrank[i] = {}
        widegrank[i] = {}
        wodegrank[i] = {}
        wrank[i] = {}
        eigrank[i] = {}
        betwrank[i] = {}
        edgebetwrank[i] = {}
        
        print('Ranking '+str(i))
    
        sd = sorted(dict(net[i].degree()).values(),reverse=True)
        for j in sorted(net[i].degree().items(),key=operator.itemgetter(1),reverse=True):
            degrank[i][j[0]] = sd.index(j[1])+1
        
        sid = sorted(dict(net[i].in_degree()).values(),reverse=True)
        for j in sorted(net[i].in_degree().items(),key=operator.itemgetter(1),reverse=True):
            idegrank[i][j[0]] = sid.index(j[1])+1
        
        sod = sorted(dict(net[i].out_degree()).values(),reverse=True)
        for j in sorted(net[i].out_degree().items(),key=operator.itemgetter(1),reverse=True):
            odegrank[i][j[0]] = sod.index(j[1])+1
        
        swd = sorted(dict(net[i].degree(weight='w')).values(),reverse=True)
        for j in sorted(net[i].degree(weight='w').items(),key=operator.itemgetter(1),reverse=True):
            wdegrank[i][j[0]] = swd.index(j[1])+1
        
        swid = sorted(dict(net[i].in_degree(weight='w')).values(),reverse=True)
        for j in sorted(net[i].in_degree(weight='w').items(),key=operator.itemgetter(1),reverse=True):
            widegrank[i][j[0]] = swid.index(j[1])+1
        
        swod = sorted(dict(net[i].out_degree(weight='w')).values(),reverse=True)
        for j in sorted(net[i].out_degree(weight='w').items(),key=operator.itemgetter(1),reverse=True):
            wodegrank[i][j[0]] = swod.index(j[1])+1

        weights = {}
        for j in net[i].edges():
            weights[(j[0],j[1])] = net[i].get_edge_data(*j)['w']
        sw = sorted(weights.values(),reverse=True)
        for j in sorted(weights.items(),key=operator.itemgetter(1),reverse=True):
            wrank[i][j[0]] = sw.index(j[1])+1
        
        print('Betweenness...')
        betw[i] = networkx.betweenness_centrality(net[i])
    
        print('Eigenvector centrality...')
        eig[i] = networkx.eigenvector_centrality(net[i])

        print('Edge betweenness...')
        edgebetw[i] = networkx.edge_betweenness_centrality(net[i])
        
        eigrank[i] = {}
        seig = sorted(eig[i].values(),reverse=True)
        for j in sorted(eig[i].items(),key=operator.itemgetter(1),reverse=True):
            eigrank[i][j[0]] = seig.index(j[1])+1
    
        betwrank[i] = {}
        sbetw = sorted(betw[i].values(),reverse=True)
        for j in sorted(betw[i].items(),key=operator.itemgetter(1),reverse=True):
            betwrank[i][j[0]] = sbetw.index(j[1])+1
        
        edgebetwrank[i] = {}
        sedgebetw = sorted(edgebetw[i].values(),reverse=True)
        for j in sorted(edgebetw[i].items(),key=operator.itemgetter(1),reverse=True):
            edgebetwrank[i][j[0]] = sedgebetw.index(j[1])+1
    
if recalculate == 1 or len(recalcset) > 0:
    for k in monarchs:
        bigrank[k] = []
        rankvec[k] = {}
        for i in net[k].nodes():
            bigrank[k].append((i,name[i],net[k].degree(i),net[k].out_degree(i),net[k].in_degree(i),net[k].degree(i,weight='w'),net[k].out_degree(i,weight='w'),net[k].in_degree(i,weight='w'),eig[k][i],betw[k][i],eigrank[k][i],betwrank[k][i]))
            rankvec[k][i] = (degrank[k][i],odegrank[k][i],idegrank[k][i],wdegrank[k][i],wodegrank[k][i],widegrank[k][i],eigrank[k][i],betwrank[k][i])

        bigedgerank[k] = []
        for i in net[k].edges():
            bigedgerank[k].append((i[0],name[i[0]],i[1],name[i[1]],net[k].get_edge_data(*i)['w'],edgebetw[k][(i[0],i[1])],edgebetwrank[k][(i[0],i[1])]))
    
if recalculate == 1 or len(recalcset) > 0:
    fbr = open('bigrank.out','w')
    for i in bigrank:
        for j in bigrank[i]:
            fbr.write(str(i)+'\t'+str(j[0])+'\t')
            for k in j[2:]:
                fbr.write(str(k)+'\t')
            fbr.write('\n') 
            #fbr.write(str(eigrank[i][j[0]])+'\t'+str(betwrank[i][j[0]])+'\n')
    fbr.close()

    fbr = open('bigedgerank.out','w')
    for i in bigedgerank:
        for j in bigedgerank[i]:
            fbr.write(str(i)+'\t'+str(j[0])+'\t'+str(j[2])+'\t')
            for k in j[4:]:
                fbr.write(str(k)+'\t')
            fbr.write('\n')
    fbr.close()

    fp = open('period','w')
    for i in monarchs:
        if i not in ['eli','mar','edw','hen','all']:
            fp.write(str(i)+'\t'+str(mfdate[i])+' '+str(mtdate[i])+'\n')
    fp.close()


from bottle import static_file
@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='<INSERT PATH TO STATIC DIRECTORY>/static')

@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='<INSERT PATH TO STATIC DIRECTORY/static')

@route('/')
def hello():
    global current,name,frl,tol
    return display(current,frl[period][current],tol[period][current],name,'Welcome!',period,xmlprint,image)

@route('/current=<currenttmp>')
def execcom(currenttmp='None'):
    global current
    global frl
    global tol
    global name
    global view
    global period
    global image
    image = ''
    current = currenttmp
    if current not in frl[period]:
        frl[period][current] = []
    if current not in tol[period]:
        tol[period][current] = []
    view = 'indiv'
    return display(current,frl[period][current],tol[period][current],name,'',period,xmlprint,image)

@route('/search',method='POST')
def execcom():
    global xmlprint
    global searchterms
    xmlprint = '@search'
    searchterms = request.forms.get('search').replace('+',' ')#.lower()
    #logic = request.forms.get('logic')
    os.system('python whindexsearch.py \''+str(searchterms)+'\'')
    #os.system('python indexsearch.py '+str(logic)+' '+str(searchterms))
    return display(current,frl[period][current],tol[period][current],name,'',period,xmlprint,image)

@route('/similar=<similartmp>')
def execcom(similartmp='None'):
    global current
    global frl
    global tol
    global name
    global view
    global period
    global image
    current = similartmp
    view = 'similar'
    return displaysimilar(item,name,period,xmlprint,current)

@route('/switchdist=<disttypetmp>')
def execcom(disttypetmp='None'):
    global current
    global frl
    global tol
    global name
    global view
    global period
    global image
    global disttype
    disttype = disttypetmp
    view = 'similar'
    return displaysimilar(item,name,period,xmlprint,current)

@route('/item=<itemtmp>')
def execcom(itemtmp='None'):
    global item
    global view
    global name
    global period
    item = int(itemtmp)
    if view != 'edge':
        view = 'list'
        return displaylist(item,name,period,xmlprint)
    else:
        view = 'edge'
        return displayedgelist(item,name,period,xmlprint)

@route('/womenonly=<womenonlytmp>')
def execcom(womenonlytmp='None'):
    global womenonly
    womenonly = int(womenonlytmp)
    return displaylist(item,name,period,xmlprint)

@route('/edge')
def execcom():
    global item
    global view
    global name
    item = 1
    view = 'edge'
    return displayedgelist(item,name,period,xmlprint)

@route('/node')
def execcom():
    global item
    global view
    global name
    item = 2
    view = 'list'
    return displaylist(item,name,period,xmlprint)

@route('/period=<periodtmp>')
def execcom(periodtmp='None'):
    global period
    global xmlprint
    xmlprint = ''
    period = periodtmp
    if view == 'edge':
        return displayedgelist(item,name,period,xmlprint)
    if view == 'list':
        return displaylist(item,name,period,xmlprint)
    if view == 'indiv':
        return display(current,frl[period][current],tol[period][current],name,'',period,xmlprint,image)
    if view == 'similar':
        return displaysimilar(item,name,period,xmlprint,current)

@route('/setperiod',method='POST')
def execcom(setperiodtmp='None'):
    global mfdate
    global mtdate
    global xmlprint
    xmlprint = ''
    mfdate['cus'] = request.forms.get('fdate')
    mtdate['cus'] = request.forms.get('tdate')
    recalccus()
    period = 'cus'
    if view == 'edge':
        return displayedgelist(item,name,period,xmlprint)
    if view == 'list':
        return displaylist(item,name,period,xmlprint)
    if view == 'indiv':
        return display(current,frl[period][current],tol[period][current],name,'',period,xmlprint,image)
    if view == 'similar':
        return displaysimilar(item,name,period,xmlprint,current)

@route('/save',method='POST')
def execcom(savenametmp='None'):
    global mfdate
    global mtdate
    global monfull
    global monarchs
    savename = request.forms.get('savename').replace(' ','_')
    mfdate[savename] = mfdate['cus'][:]
    mtdate[savename] = mtdate['cus'][:]
    if savename not in monarchs:
        monarchs.append(savename)
    monfull[savename] = savename.replace('_',' ')
    copycus(savename)
    period = savename
    if view == 'edge':
        return displayedgelist(item,name,period,xmlprint)
    if view == 'list':
        return displaylist(item,name,period,xmlprint)
    if view == 'indiv':
        return display(current,frl[period][current],tol[period][current],name,'',period,xmlprint,image)
    if view == 'similar':
        return displaysimilar(item,name,period,xmlprint,current)

@route('/plot',method='POST')
def execcom(plottmp='None'):
    global x,y
    x = request.forms.get('x')
    y = request.forms.get('y')
    return displaylist(item,name,period,xmlprint)

@route('/xmlprint=<xmlprinttmp>')
def execcom(xmlprinttmp='None'):
    global xmlprint
    xmlprint = xmlprinttmp
    view = 'indiv'
    return display(current,frl[period][current],tol[period][current],name,'',period,xmlprint,image)
    #if view == 'edge':
    #    return displayedgelist(item,name,period,xmlprint)
    #if view == 'list':
    #    return displaylist(item,name,period,xmlprint)
    #if view == 'indiv':
    #    return display(current,frl[period][current],tol[period][current],name,'',period,xmlprint,image)

@route('/delete=<deletetmp>')
def execcom(deletetmp='None'):
    global mfdate
    global mtdate
    global monfull
    global monarchs
    global period
    deletetmp = deletetmp.replace(' ','_')
    mfdate.pop(deletetmp)
    mtdate.pop(deletetmp)
    monarchs.remove(deletetmp)
    monfull.pop(deletetmp)
    rmcus(deletetmp)
    if period == deletetmp:
        period = 'all'
    if view == 'edge':
        return displayedgelist(item,name,period,xmlprint)
    if view == 'list':
        return displaylist(item,name,period,xmlprint)
    if view == 'indiv':
        return display(current,frl[period][current],tol[period][current],name,'',period,xmlprint,image)
    if view == 'similar':
        return displaysimilar(item,name,period,xmlprint,current)


"""
@route('/find', method='POST')
def findword():
    global current
    global union
    global wlist
    currenttmp = request.forms.get('find')
    if currenttmp in msgnet.nodes():
        current = currenttmp
        message = ''
    else:
        message = 'The word \''+currenttmp+'\' does not appear in the (filtered) data.'
    return display(current,union,wlist,dem,corl,message,xmlprint,image)
"""

@route('/image=<imagetmp>')
def execcom(imagetmp='None'):
    global image
    global changeto
    changeto = ''
    image = imagetmp
    return display(current,frl[period][current],tol[period][current],name,'',period,xmlprint,image)    

run(host='localhost', port=8082, debug=True)
