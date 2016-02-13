#!/usr/bin/python

import pickle
from experiment import *
from collections import Counter, defaultdict
from operator import itemgetter
from math import log10 as log
from sets import Set

import pdb

class MLE:
    def __init__(self, setup, data):
        self.counts = defaultdict(lambda: defaultdict(int))
        for dp in data:
            self.counts[dp.value][dp.lexsn] += 1
        
        self.model = {}
        for i in self.counts.items:
            index, element = max(enumerate(distrib), key=itemgetter(1))
            self.model[element] = i[index]
                            
    def run(self, setup, dp):
        return self.model[dp.value]
                
class NaiveBayes:
    def __init__(self, setup, data):
        self.senseCounts = defaultdict(lambda: defaultdict(int))
        self.conditionalCounts = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
        for dp in data:
            self.counts[dp.value][dp.lexsn] += 1

            for w in dp.results.features:
                self.conditionalCounts[dp.value][dp.lexsn][w] +=1        
                
    def run(self, setup, dp):
        counts = self.senseCounts[dp.value]
        condCounts = self.conditionalCounts[dp.value]
        space = condCounts.keys()
        spaceVals = {}
    
        #intialize to counts of sense (this is the P(s_i) term)
        for sense in space:
            spaceVals[sense] = log(counts[sense])
            
        for sense in space:
            for w in dp.results.features:
                if w in condCounts[sense]:
                    spaceVals[sense] += log(condCounts[sense][w]) #multiply by joint count of w and sense 
                    spaceVals[sense] -= log(counts[sense]) # divide by marginal count of sense
        
        sense, val = max(spaceVals.items(), key = itemgetter(1))
        return sense
        

def extractFeatures(data):
    for dp in data:
        wds = [w.value for w in dp.context]
        dp.result.features = Counter()
        for w in wds:
            dp.result.features.add(w)

def trainModel(setup, data):
    modelType = setup["modelType"]
    func = getattr(sys.modules[__name__], modelType)
    model = func(setup, data)
    return model
    
def runModel(setup, model, data):
    for item in data:
        item.result.recordResult(model.run(setup, item.features))

def checkItem(setup, dp):
    try:
        return dp.value in setup["words"] or setup["words"] == "*" or not "words" in setup
    except AttributeError:
        return False

def loadData(setup, type):
    dataFile = setup[type]
    df = open(dataFile, "r")
    allData = pickle.load(df)
    return [dp for dp in allData if checkItem(setup, dp)]

def updateValueSpace(vs, data):
    allposs = [(dp.value,dp.lexsn) for dp in data]
    terms = Set([x[0] for x in allpos])
    for term in terms:
        possVals = Set([x[1] for x in allpos if x[0]==term])
        vs[term].update(possVals)

def runExperiment(setup):
    
    pdb.set_trace()
    trainData = loadData(setup, "train")
    testData = loadData(setup, "test")
    
    valueSpace = defaultdict(Set)
    
    updateValueSpace(valueSpace, trainData)
    updateValueSpace(valueSpace, testData)
    
    extractFeatures(trainData)
    extractFeatures(testData)
    
    trainModel(setup, trainData)
    runModel(setup, testData)
    
    return testData, valueSpace

def analyzeExperiment(valueSpace, results):
    words = valueSpace.keys()

    resByWord = defaultdict(list)
    
    for dp in results:
        resByWord[dp.value].append(dp)
        
    for item in valueSpace.keys():
        cf = ConfusionMatrix(valueSpace[item])
        for dp in resByWord[item]:
            cf.addItem(*dp.result.getResults())
            
    cf.computeMatrics()
    print cf.accuracy

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Run an experiment using a json.')
    parser.add_argument('experimentfile', metavar='e', type=str, 
                       help='the json specifying the parameters of the experiment')
    
    args = parser.parse_args()
    import json                       
    
    expSetup = json.load(open(args.experimentfile))

    results, valueSpace = runExperiment(expSetup)
    analyzeExperiment(valueSpace, results)