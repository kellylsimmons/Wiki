# -*- coding: utf-8 -*-
"""
Created on Tue Jun 30 09:30:05 2015

@author: student
"""

import urllib
from html2text import html2text
import pandas as pd
from random import random, sample
import timeit
import numpy as np

pages = sample(xrange(100),5)
paths = []
for ident in pages:
    y = str(ident)
    x = "https://en.wikipedia.org/w/index.php?curid="+y+"&action=info#mw-pageinfo-watchers"
    paths.append(x)
    
data = []
for path in paths: 
    test = []
    for line in html2text(urllib.urlopen(path).read().decode('utf-8','ignore')).split('\n'):
        if 'Display title' in line:
            try:
                test.append(str(line.split('|')[1].strip()))
            except UnicodeEncodeError:
                test.append(path)
        elif 'Total number of edits' in line:
            try:
                test.append(int(line.split('|')[1].strip()))
            except ValueError:
                test.append(np.nan)
        elif 'Total number of distinct authors' in line:
            try:
                test.append(int(line.split('|')[1].strip()))
            except ValueError:
                test.append(np.nan)
        elif 'Recent number of edits (within past 30 days)' in line:
            try: 
                test.append(int(line.split('|')[1].strip()))
            except ValueError:
                test.append(np.nan)
        elif 'Recent number of distinct authors' in line:
            try:
                test.append(int(line.split('|')[1].strip()))
            except ValueError:
                test.append(np.nan)
    #filtering out articles with only one author
    if test and test[2]>1:
        data.append(test)

# making data frame
cnames = ('page_title','total_edits','total_authors','recent_edits','recent_authors')
wiki = pd.DataFrame(data,columns=cnames)

#looking 

wiki['authors_to_edits']=wiki['total_authors']/wiki['total_edits']
wiki.sort('authors_to_edits')