#!/usr/bin/python

from collections import defaultdict, Counter
import pdb
from itertools import product
from operator import itemgetter

pi = None
b = None
a = None

def loadPi():
    f = "pi.tab"
    r = Counter()
    
    fd = open(f, "r")
    for l in fd:
        state,num,prob = l.split('\t')
        r[state] = float(prob)
    
    return r
    
def loadA():
    f = "a.tab"
    r = defaultdict(lambda: defaultdict(float))
    
    fd = open(f, "r")
    for l in fd:
        statei, statej,num,prob = l.split('\t')
        r[statei][statej] = float(prob)
    return r


def loadB():
    f = "b.tab"
    r = defaultdict(lambda: defaultdict(float))
    
    fd = open(f, "r")
    for l in fd:
        statei, termk,num,prob = l.split('\t')
        r[statei][termk] = float(prob)
    
    return r

def viterbiLoop(obss, model):
    pass
def viterbi(time, state, obss, model, store):
    
    pass

def computeBestPath(model):
    pass
    
def alpha(time, state, obss, model, store):
    pass

def computeObsProbAlpha(model):
    pi, a, b = model
    
    states = a.keys()
    terms = set()
    for d in b.values():
        terms.update(set(d.keys()))
    
    try:
        while 1:
            inp = raw_input("What is your string?")
            inp = inp.lower()
            inputTerms = inp.split(' ')

            uniqTerms = set(inputTerms)
            diff = uniqTerms - terms
            if diff != set(): #there are some illegal terms
                print diff
                print "These aren't legal words for this model."
            else:
                o = inputTerms
                length = len(o)
                totalProb = 0.0
                store = {}
                for s in states:
                    v = alpha(length-1, s, o, model, store)
                    #print s, v
                    totalProb += v
                print totalProb
                for key,val in sorted([x for x in store.items() if x[1] != 0], key=itemgetter(0)):
                    print key, val
    except EOFError:
        return


def computeObsProb(model):
    pi, a, b = model
    
    states = a.keys()
    terms = set()
    for d in b.values():
        terms.update(set(d.keys()))
    
    try:
        while 1:
            inp = raw_input("What is your string?")
            inp = inp.lower()
            inputTerms = inp.split(' ')

            uniqTerms = set(inputTerms)
            diff = uniqTerms - terms
            if diff != set(): #there are some illegal terms
                print diff
                print "These aren't legal words for this model."
            else:
                o = inputTerms
                length = len(o)
                totalProb = 0.0
                for x in product(states, repeat =length ):
                    piVal = pi[x[0]]
                    outputProb = b[x[0]][o[0]]
                    transProb = 1
                    
                    if length > 1: #handle the first transition and the last output
                        transProb *= a[x[0]][x[1]]
                        #outputProb *= b[x[-1]][o[-1]]                        
                    
                    for i in range(1,length):
                        try:
                            transProb *= a[x[i]][x[i+1]]
                        except IndexError:
                            pass
                        outputProb *= b[x[i]][o[i]]
                    
                    xTotal = piVal * transProb * outputProb
                    totalProb += xTotal
                    print x, piVal, transProb, outputProb, xTotal
                print totalProb
    except EOFError:
        return

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Take a sentences of form word_pos and compute pos->pos transition probabilities and pos->term output probabilities')
                       
    args = parser.parse_args()
    

    pi = loadPi()
    a = loadA()
    b = loadB()
    
    model = (pi, a, b)
    
    #computeObsProbAlpha(model)
    computeBestPath(model)
