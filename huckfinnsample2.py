#!/usr/bin/python

from __future__ import division
import fileinput
import re
import nltk
import math


'''Run this script from the command line: e.g. in Linux: cat huck_finn.pos | ./huck_finn.py - >myresults'''

'''Problem 5'''

getRidOfPOS = re.compile(r'_[A-Z]*')
punc = re.compile(r'[^a-zA-Z_]')
skipdictUnordered = nltk.defaultdict(lambda:(nltk.defaultdict(lambda: 0)))



for line in fileinput.input():
    line = re.sub(r'\n','', line)
    line_as_list=re.sub(r'\s+',r' ',line).split(' ')
    for skip in [2,5,10]:
        skipstr = str(skip)
        for i in range(len(line_as_list)-skip):
            pair = getRidOfPOS.sub(r'',line_as_list[i]), getRidOfPOS.sub(r'',line_as_list[i+skip])
            unorderedPair = tuple(sorted([getRidOfPOS.sub(r'',line_as_list[i]), getRidOfPOS.sub(r'',line_as_list[i+skip])]))
            if punc.search(pair[0]) or punc.search(pair[1]):
                continue
            else:
                skipdictUnordered[skipstr][unorderedPair] += 1





for skipstr in ['2','5','10']:
    bigramList = []
    print skipstr, 'skips unordered'
    print
    for pair in skipdictUnordered[skipstr].keys():
        bigramList.append((skipdictUnordered[skipstr][pair],pair[0],pair[1]))
    width = max(len(w[1]) for w in bigramList)
    for count, pair0, pair1 in sorted(bigramList,reverse=True):
        print '{:{width}} {:{width}} {:3}'.format(pair0, pair1, count, width=width)
    print





