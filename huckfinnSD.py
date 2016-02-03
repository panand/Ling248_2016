#!/usr/bin/python

from __future__ import division
import fileinput
import re
import nltk
import math

'''Run this script from the command line: e.g. in Linux: cat huck_finn.pos | ./huck_finn.py - >myresults'''

'''Problem 7'''

getRidOfPOS = re.compile(r'_[A-Z]*')
punc = re.compile(r'[^a-zA-Z_]')
skipdict = nltk.defaultdict(lambda:(nltk.defaultdict(lambda: nltk.defaultdict(lambda:0))))



for line in fileinput.input():
    line = re.sub(r'\n','', line)
    line_as_list=re.sub(r'\s+',r' ',line).split(' ')
    for skip in [1,2,3,4,5]:
        for i in range(len(line_as_list)-skip):
            pair = getRidOfPOS.sub(r'',line_as_list[i]), getRidOfPOS.sub(r'',line_as_list[i+skip])
            if punc.search(pair[0]) or punc.search(pair[1]):
                continue
            else:
                skipdict[pair[0]][pair[1]][skip] += 1
                skipdict[pair[1]][pair[0]][-skip] += 1

sdlist = []
for w1 in skipdict.keys():
    for w2 in skipdict[w1].keys():
        if w1 == w2:
            continue
        total = 0
        partial = 0
        for i in [-5,-4,-3,-2,-1,1,2,3,4,5]:
            total += skipdict[w1][w2][i]
            partial += skipdict[w1][w2][i] * i
        if total < 6:
            continue #I filtered out pairs that occurred infrequently. If the pair only occurred once it produced an aritifically high SD>
        mean = partial / total
        total2 = 0
        for i in [-5,-4,-3,-2,-1,1,2,3,4,5]:
            total2 += skipdict[w1][w2][i]*(i - mean)**2
        sd = math.sqrt(total2 / total)
        sdlist.append((sd, mean, w1, w2))

width = max(len(w[2]) for w in sdlist)
print '{:{width}} {:{width}} {:>6} {:>6}'.format('Word 1', 'Word 2', 'SD', 'Mean', width=width)
print
for datum in sorted(sdlist,reverse=True):
    print '{:{width}} {:{width}} {:.4f} {:.4f}'.format(datum[2], datum[3], datum[0], datum[1], width=width)










