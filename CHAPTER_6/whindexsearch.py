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

query = QueryParser("content", ix.schema).parse(sys.argv[1])
results = searcher.search(query, limit=None)
#print(results[:])
print(len(results[:]))

ff = open('out','w')
if len(results[:]) == 0:
    ff.write('No_results\n')
for i in results[:]:
    ff.write(str(i['path'][52:])+'\n')
ff.close()

