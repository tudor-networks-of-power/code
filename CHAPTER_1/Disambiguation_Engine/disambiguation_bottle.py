#!/usr/bin/env python                                                          
print('Content-Type: text/html')
print
 
import sys
import os
import random
#import networkx
import operator
#import matplotlib
#import pylab
import math
import cgi
import time
from collections import defaultdict
from bottle import route, run, template, request


once = 0

changeto = ''
highlight = '1'
wholelist = 0
xmlp = ''
search = ''
image = ''

@route('/')
def execcom():
    image = ''
    return display(changeto,highlight,wholelist,xmlp,search,image)

from bottle import static_file

@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='<INSERT ROOT PATH TO HERE>/static')

@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='<INSERT ROOT PATH TO HERE>/static')

@route('/wholelist=<wholelisttmp>')
def execcom(wholelisttmp='None'):
    global wholelist
    global search
    global changeto
    changeto = ''
    search = ''
    wholelist = int(wholelisttmp)
    flog = open('log','a')
    flog.write(str(time.ctime())+'\t')
    flog.write('wholelist='+str(wholelist)+'\t')
    flog.close()
    return display(changeto,highlight,wholelist,xmlp,search,image)

@route('/changeto=<changetotmp>')
def execcom(changetotmp='None'):
    global changeto
    changeto = changetotmp
    flog = open('log','a')
    flog.write(str(time.ctime())+'\t')
    flog.write('changeto='+str(changeto)+'\t')
    flog.close()
    return display(changeto,highlight,wholelist,xmlp,search,image)

@route('/changetofield',method='POST')
def execcom(changetotmp='None'):
    global changeto
    changetotmp = request.forms.get('changeto')
    changeto = changetotmp
    flog = open('log','a')
    flog.write(str(time.ctime())+'\t')
    flog.write('changeto='+str(changeto)+'\t')
    flog.close()
    return display(changeto,highlight,wholelist,xmlp,search,image)

@route('/highlight=<highlighttmp>')
def execcom(highlighttmp='None'):
    global highlight
    global changeto
    changeto = ''
    highlight = highlighttmp
    flog = open('log','a')
    flog.write(str(time.ctime())+'\t')
    flog.write('highlight='+str(highlight)+'\t')
    flog.close()
    return display(changeto,highlight,wholelist,xmlp,search,image)

@route('/highlightsearch',method='POST')
def execcom(highlighttmp='None'):
    global highlight
    global changeto
    changeto = ''
    highlighttmp = request.forms.get('highlight')
    highlight = highlighttmp
    flog = open('log','a')
    flog.write(str(time.ctime())+'\t')
    flog.write('highlightsearch='+str(highlight)+'\t')
    flog.close()
    return display(changeto,highlight,wholelist,xmlp,search,image)

@route('/xml=<xmltmp>')
def execcom(xmltmp='None'):
    global xml
    global changeto
    changeto = ''
    xmlp = xmltmp.replace('@','/')
    flog = open('log','a')
    flog.write(str(time.ctime())+'\t')
    flog.write('xmlp='+str(xmlp)+'\t')
    flog.close()
    return display(changeto,highlight,wholelist,xmlp,search,image)

@route('/search=<searchtmp>')
def execcom(searchtmp='None'):
    global search
    global wholelist
    global changeto
    changeto = ''
    wholelist = 0
    search = searchtmp
    flog = open('log','a')
    flog.write(str(time.ctime())+'\t')
    flog.write('search='+str(search)+'\t')
    flog.close()
    return display(changeto,highlight,wholelist,xmlp,search,image)

@route('/image=<imagetmp>')
def execcom(imagetmp='None'):
    global image
    global changeto
    changeto = ''
    image = imagetmp
    flog = open('log','a')
    flog.write(str(time.ctime())+'\t')
    flog.write('image='+str(image)+'\t')
    flog.close()
    return display(changeto,highlight,wholelist,xmlp,search,image)

showhide = {}
showhide[0] = 'Show'
showhide[1] = 'Hide'

def display(changetotmp,highlighttmp,wholelisttmp,xmlptmp,searchtmp,imagetmp):
    global changeto
    global highlight
    global wholelist
    global xmlp
    global search
    global image

    changeto = changetotmp
    highlight = highlighttmp
    wholelist = wholelisttmp
    xmlp = xmlptmp
    search = searchtmp
    image = imagetmp

    flog = open('log','a')
    flog.write(str(time.ctime())+'\t')
    xml = {}
    f = open('id_lookup')
    for line in f:
        l = line.strip().split('\t')
        if len(l) == 2:
            xml[l[0]] = '<INSERT ROOT PATH TO XML DIRECTORY>'+l[1]
    f.close()    
    
    ll = []
    f = open('people_docs')
    for line in f:
        l = line.strip().split('\t')
        ll.append(l)
    f.close()    
    
    flog.write('Length: '+str(len(ll))+'\n')
    
    corruptstr = ''
    if len(ll) != 37101:
        flcount = 0
        corrupt = -1
        for i in ll:
            flcount += 1
            if i[0] != str(flcount):
                corrupt = flcount
                break
        flog.write('corrupted after '+str(corrupt)+'!\n')
        flcount = 37102
        corrupt = -1
        llr = ll[:]
        llr.reverse()
        for i in llr:
            flcount -= 1
            if i[0] != str(flcount):
                corrupt = flcount
                break
        flog.write('corrupted before '+str(corrupt)+'!\n')
        corruptstr = 'file corrupted!'
        os.system('cp people_docs_safe people_docs')
        ll = []
        f = open('people_docs')
        for line in f:
            l = line.strip().split('\t')
            ll.append(l)
        f.close()    
    flog.close()
    
    if changeto != '':
        if len(ll) == 37101:
            os.system('cp people_docs people_docs_safe')
        f = open('people_docs','w')
        for l in range(len(ll)):
            #print(str(ll[l][0]))
            #print(highlight,changeto)
            if ll[l][0] == highlight and changeto != '':
                ll[l][2] = changeto
                old = ll[l][2]
            for i in ll[l]:
                f.write(str(i)+'\t')
            f.write('\n')
        f.close()    
    
        #ff.open('edits','a')
        #ff.write(str(old)+'\t'+'changeto')
        #ff.close()
    
    c = 0
    s = ''
    s += '<html>'+corruptstr+'<head><STYLE type = \"text/css\" media = \"screen\"\n<!--\n-->\n</STYLE><LINK HREF=\"static/disamstyle.css\" rel=\"stylesheet\" type=\"text/css\" media=\"all\" title=\"Standard\"></head><div class="title"><b>The Disambiguation Engine</b></div>'
    wholestr = '<a href="/wholelist='+str(1-wholelist)+'">'+str(showhide[wholelist])+' whole list</a>'

    s += '<div class="query"><form name="highlight" action="/highlightsearch" method="post"><input type="text" name="highlight" size="10" value=""><input type="submit" value="Jump"></form>'
    s += wholestr+'</div>'
    s += '<div class="locallist"><table>'
    urnge = 3
    drnge = 20
    xmll = ''

    start = int(highlight)-urnge
    end = int(highlight)+drnge
    
    if start < 0:
        start = 0
    if end > len(ll):
        end = len(ll)
    
    for l in ll[start:end]:
        c += 1
        #print(l[0],highlight,l[0] == highlight)
        if l[0] == highlight:
            s += '<tr bgcolor="#AAAAAA">'
        if l[0] != highlight:
            s += '<tr>'
        s += '<a name="'+str(c)+'">'
        s += '<td valign="top"><a href="/changeto='+str(l[0])+'">'+str(l[0])+'</a></td>'
        if l[0] != highlight:
            s += '<td valign="top" style="width:300px"><a href="/highlight='+str(c+start)+'#'+str(highlight)+'">'+str(l[1])+'</a></td>'
        if l[0] == highlight:
            s += '<td valign="top" style="width:300px">'
            for i in l[1].split():
                if i[0].isupper():
                    s += '<a href="/search='+str(i.replace(',',''))+'">'+str(i)+' </a>'
                if not i[0].isupper():
                    s += str(i)+' '
            s += '</td>'
    
        b = ''
        bb = ''
        if l[0] == highlight and changeto != '':
            b = '<b>'
            bb = '</b>'
        s += '<td valign="top" style="width:70px">'+b+str(l[2])+bb+'</td>' 
        s += '<td valign="top" style="width:400px">'
        if l[0] == highlight:
            s += '<form name="changeto" action="/changetofield" method="POST"><input type="text" name="changeto" size="10" value="'+str(l[2])+'"><input type="submit" value="Edit"></form>'
        s += '</td>'
        #print('<td valign="top" style="width:500px">')
        if l[0] == highlight:
            xmll = l[3]
        #print('</td></tr>')
    s += '</table></div>'
    
    #print(xmlp)

    if len(xmll.split()) > 0 and xmlp not in xmll.split():
        xmlp = xmll.split()[0]
    
    #print('@',xmlp)

    s += '<div class="xmllist">'
    for i in xmll.split():
        if i in xml:
            bs = ''
            bs2 = ''
            if i == xmlp:
                bs = '<b>'
                bs2 = '</b>'
            s += str(bs)+'<a href="/xml='+str(i).replace('/','@')+'">'+str(i.replace('_',' '))+'</a>'+str(bs2)+'<br>'
        if i not in xml:
            s += str(i)+'<br>'
    s += '</div>'

    if wholelist == 1 and search == '':
        s += '<div class="wholelist">'
        f = open('people_docs')
        for line in f:
            ls = line.strip().split('\t')
            #if len(ls) < 4:
            #    print(line)
            #    sys.exit()
            lsn = len(ls[3].split())
            if lsn > 6:
                for i in ls[:3]:
                    s += str(i)+' '
                s += '('+str(lsn)+' manuscripts)'
            if lsn <= 6:
                for i in ls[:4]:
                    s += str(i)+' '
            s += '<br>'
        f.close()    
        s += '</div>'    
    
    if search != '':
        s += '<div class="wholelist">'
        f = open('people_docs')
        for line in f:
            if search in line:
                ls = line.strip().split('\t')
                lsn = len(ls[3].split())
                if lsn > 6:
                    xmlstr = ''
                    #if xmlp != '':
                    #    xmlstr = '&xml='+str(xmlp)
                    s += '<a href="/highlight='+str(ls[0])+'">'
                    for i in range(3):
                        s += str(ls[i])+' '
                    s += '('+str(lsn)+' manuscripts)'
                    s += '</a>'
                if lsn <= 6:
                    xmlstr = ''
                    #if xmlp != '':
                    #    xmlstr = '&xml='+str(xmlp)
                    s += '<a href="/highlight='+str(ls[0])+'">'
                    for i in ls[:4]:
                        s += str(i.replace('_',' '))+' '
                    s += '</a>'
                s += '<br>'
        f.close()    
        s += '</div>'    
    
    xmlparse = {}
    xmlparse['docid'] = 'Document ID'
    xmlparse['cdoc'] = 'Document Ref.'
    xmlparse['cauth'] = 'Author'
    xmlparse['crep'] = 'Recipient'
    xmlparse['cd'] = 'Day'
    xmlparse['cyr'] = 'Year'
    xmlparse['cpl'] = 'Place'
    xmlparse['ctit'] = 'Title'
    
    linklist = []
    linklast = 0
    
    if xmlp != '':
        s += '<div class="xml">'
        
        f = open(xml[xmlp])
        out = 0
        count = 0
        for lineraw in f:
            line = lineraw.strip()
            #s += '@@'+str(line)
            #print(line)
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
                #print('<a href="../Images/'+str(link)+'">Image '+str(count)+'</a><br>')
                #print('<a href="/&highlight='+str(highlight)+xmlstr+'&wholelist='+str(wholelist)+'&image='+str(link)+'#'+str(highlight)+'">Image '+str(count)+'</a><br>')
                #print('<a href="../test.txt">test</a>')
                linklist.append(link)
                linklast = 1
    
            if linklast == 1 and  '<linkseq ' not in line:
                s += '<a href="/image=1">Images ('+str(len(linklist))+')</a><br>'
                linklast = 0
                #print(linklist)
    
            if '<ctxt>' in line:
                out = 1
            if out == 1:
                s += line.strip().replace('<ctxt>','').replace('</ctxt>','')
            if '</ctxt>' in line:
                out = 0
            #s += str(out)+'@<br>'
        s += '</xml>'
        s += '</div>'
        
    
    if image != '':
        os.system('rm -f <INSERT PATH TO static DIRECTORY>*.jpg')
        s += '<div class="dark"></div>'
        os.system('cp <INSERT PATH TO IMAGE DRIVE>/SPO'+str(corpus)+'/Images/'+linklist[int(image)-1]+' <INSERT PATH TO STATIC DIRECTORY>')    

        s += '<div class="image"><div class="actualimage"><a href="../static/'+linklist[int(image)-1].split('/')[-1]+'" target="blank"><img  width=100% src="../static/'+linklist[int(image)-1].split('/')[-1]+'"></a></div>'
        s += '<div class="x"><a href="/#'+str(highlight)+'">X</a></div>'
        if int(image) > 1:
            s += '<div class="prev"><a href="/image='+str(int(image)-1)+'#'+str(highlight)+'">prev</a></div>'
        if int(image) < len(linklist):
            s += '<div class="next"><a href="/image='+str(int(image)+1)+'#'+str(highlight)+'">next</a></div>'
        s += '</div>'
    
        
    s += '</html>'
    return s
    print(s)
    
run(host='localhost', port=8081, debug=True)
