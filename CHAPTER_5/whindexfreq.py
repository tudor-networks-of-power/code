#!/usr/bin/env python                                                           
import sys
import os
import random
import networkx
import operator
import math
import time
from collections import defaultdict
from unidecode import unidecode
from namedentities import *

from whoosh.index import create_in
from whoosh.fields import *
from whoosh.index import open_dir
from whoosh.query import *
from whoosh.qparser import QueryParser

ix = open_dir("indexdir2")
searcher = ix.searcher()
schema = Schema(title=TEXT(stored=True), path=ID(stored=True))

f = open(sys.argv[1])
docs = []
for line in f:
    if line.strip() != '':
        docs.append('/Users/sebastianahnert/Desktop/DisambiguationEngine/'+line.strip())

docsnum = []
for i in docs:
    docsnum.append(searcher.document_number(path=i))

nt = 150
if len(sys.argv) == 3:
    nt = int(sys.argv[2])

s = searcher.key_terms(docsnum,"content",numterms=nt)

stopwords = ['the','but','they','that', 'how', 'for', 'and','who','whom','which','were','was']

ff = open(sys.argv[1]+'.whfreq','w')
c = 1
for i in s:
    if c < nt + 1:
        if i[0] not in stopwords and 'cmpg' not in i[0] and 'x201' not in i[0] and 'x0' not in i[0] and i[0] not in ['ctxt','cun']:
            print(str(c)+'. '+str(i[0])+'\t'+str(i[1]))
            c += 1
    ff.write(str(c)+'. '+str(i[0])+'\t'+str(i[1])+'\n')
ff.close()
