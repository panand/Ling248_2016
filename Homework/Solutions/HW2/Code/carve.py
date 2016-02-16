#!/usr/bin/python

import pickle
from experiment import *
from collections import Counter, defaultdict
from operator import itemgetter
from math import log10 as log
from sets import Set

import pdb

def checkItem(setup, dp):
    try:
        print dp.value
        return dp.value in setup["words"] or setup["words"] == "*" or not "words" in setup
    except AttributeError:
        return False

def carve(setup, type):
    dataFile = setup[type]
    df = open(dataFile, "r")
    allData = pickle.load(df)
            
    return [dp for dp in allData if checkItem(setup, dp)]

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Run an experiment using a json.')
    parser.add_argument('experimentfile', metavar='e', type=str, 
                       help='the json specifying the parameters of the experiment')

    parser.add_argument('outfile', metavar='f', type=str, 
                                          help='output filename')
    
    args = parser.parse_args()
    
    import json
    expSetup = json.load(open(args.experimentfile))

    data = carve(expSetup, "test")
    fout = open(args.outfile, "w")
    try:
        pickle.dump(data, fout, protocol=2)
    except Exception as e:
        pdb.set_trace()
    fout.close()
    