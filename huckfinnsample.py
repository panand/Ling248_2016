#!/usr/bin/python

from __future__ import division
import fileinput
import re
import nltk
import math

'''Run this script from the command line: e.g. in Linux: cat huck_finn.pos | ./huck_finn.py - >myresults'''

'''Problems 1 - 5'''

verbDict = nltk.defaultdict(lambda: 0)
isAVerb = re.compile(r'_V[ A-Z][A-Z]*')
isANoun = re.compile(r'_NN[ A-Z]*')
nvSeq = nltk.defaultdict(lambda: nltk.defaultdict(lambda: 0))
nounList = []
vnbigrams = 0
bigrams = nltk.defaultdict(lambda: 0)
bigramList = []
getRidOfPOS = re.compile(r'_[A-Z]*')
punc = re.compile(r'[^a-zA-Z_]')
skipdict = nltk.defaultdict(lambda:(nltk.defaultdict(lambda: 0)))
skipdictUnordered = nltk.defaultdict(lambda:(nltk.defaultdict(lambda: 0)))



for line in fileinput.input():
    line = re.sub(r'\n','', line)
    line_as_list=re.sub(r'\s+',r' ',line).split(' ')
    prevV = None
    prev = None
    for w in line_as_list:
        wonly = getRidOfPOS.sub(r'', w)
        #I ignored punctuation here but one has the choice not to:
        if prev != None and not punc.search(w) and not punc.search(prev):
            bigrams[(prev,wonly)] += 1
        prev = wonly    
        if isAVerb.search(w):
            wMinusPOS = isAVerb.sub(r'',w)
            verbDict[wMinusPOS] += 1
            prevV = wMinusPOS
        else:
            if isANoun.search(w) and prevV != None:
                wMinusPOS = isANoun.sub(r'', w)
                nvSeq[prevV][wMinusPOS] += 1
                vnbigrams += 1
                if wMinusPOS not in nounList:
                    nounList.append(wMinusPOS)
            prevV = None
    for skip in [2,3,4,5,10]:
        skipstr = str(skip) #I made the keys string versions of integers but you actually don't need to.
        for i in range(len(line_as_list)-skip):
            pair = getRidOfPOS.sub(r'',line_as_list[i]), getRidOfPOS.sub(r'',line_as_list[i+skip])
            unorderedPair = tuple(sorted([getRidOfPOS.sub(r'',line_as_list[i]), getRidOfPOS.sub(r'',line_as_list[i+skip])]))
            if punc.search(pair[0]) or punc.search(pair[1]):
                continue #I ignored punctuation as tokens.
            else:
                skipdict[skipstr][pair] += 1
                skipdictUnordered[skipstr][unorderedPair] += 1




verbsByFreq = []
for w in verbDict.keys():
    verbsByFreq.append((verbDict[w], w))
top5Vs = sorted(verbsByFreq,reverse=True)[0:5]
print 'Top 5 verbs:'
print
width = max(len(v) for v in top5Vs)
for count, v in top5Vs:
    print '{:{width}} {:2}'.format(v, count, width=width)
print
width = max(len(n) for n in nounList)
print '{:{width}}'.format('Noun', width=width),
for _, v in top5Vs:
    print '{:>5}'.format(v),
print
print
for n in nounList:
    print '{:{width}}'.format(n, width=width),
    for _, v in top5Vs:
        print '{:5}'.format(nvSeq[v][n]),
    print
for n in nounList:
    for _, v in top5Vs:
        print 'p(',v, ',', n, '|', v, ') =', nvSeq[v][n] / vnbigrams



for pair in bigrams.keys():
    bigramList.append((bigrams[pair],pair[0],pair[1]))

width = max([max(len(w[1]) for w in bigramList), max(len(w[2]) for w in bigramList)])
for count, pair0, pair1 in sorted(bigramList,reverse=True):
    print '{:{width}} {:{width}} {:3}'.format( pair0, pair1, count, width=width)

for skipstr in skipdict.keys():
    bigramList = []
    print skipstr, 'skips'
    print
    for pair in skipdict[skipstr].keys():
        bigramList.append((skipdict[skipstr][pair],pair[0],pair[1]))
    for count, pair0, pair1 in sorted(bigramList,reverse=True):
        print '{:{width}} {:{width}} {:3}'.format(pair0, pair1, count, width=width)
    print

for skipstr in [2,5,10]:
    bigramList = []
    print skipstr, 'skips unordered'
    print
    for pair in skipdictUnordered[skipstr].keys():
        bigramList.append((skipdictUnordered[skipstr][pair],pair[0],pair[1]))
    for count, pair0, pair1 in sorted(bigramList,reverse=True):
        print '{:{width}} {:{width}} {:3}'.format(pair0, pair1, count, width=width)
    print





