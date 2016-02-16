#!/usr/bin/python

import pickle
from experiment import *
from collections import Counter, defaultdict
from operator import itemgetter
from math import log10 as log
from sets import Set

import pdb
import sys

class MLE:
    def __init__(self, setup, data):
        self.counts = defaultdict(lambda: defaultdict(int))
        for dp in data:
            self.counts[dp.value][dp.lexsn] += 1
        
        self.model = {}
        for i in self.counts.items():
            word, valDistrib = i
            val, num = max(valDistrib.items(), key=itemgetter(1))
            self.model[word] = val
            print word, val
                            
    def run(self, setup, dp):
        return self.model[dp.value]
                
class NaiveBayes:
    def __init__(self, setup, data):
        self.senseCounts = defaultdict(lambda: defaultdict(float))
        self.conditionalCounts = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
        for dp in data:
            self.senseCounts[dp.value][dp.lexsn] += 1

            for w in dp.result.features:
                self.conditionalCounts[dp.value][dp.lexsn][w] +=1.0        
        
        if "smoothing" in setup: #we will only smooth the conditionalCounts (where the dimensionality is high)
            fd = open(setup["smoothing"], "r")
            unig = pickle.load(fd)
            alpha = 0.000005
            
            for tok in unig:
                for word, senseDict in self.conditionalCounts.items():
                    for sense, condCounts in senseDict.items():
                        condCounts[tok] += alpha
                
    def run(self, setup, dp):
        counts = self.senseCounts[dp.value]
        condCounts = self.conditionalCounts[dp.value]
        space = condCounts.keys()
        spaceVals = {}
    
        #intialize to counts of sense (this is the P(s_i) term)
        for sense in space:
            spaceVals[sense] = log(counts[sense])
            
        for sense in space:
            for w in dp.result.features:
                if w in condCounts[sense]:
                    spaceVals[sense] += log(condCounts[sense][w]) #multiply by joint count of w and sense 
                    spaceVals[sense] -= log(counts[sense]) # divide by marginal count of sense
        
        sense, val = max(spaceVals.items(), key = itemgetter(1))
        return sense
        

def extractFeatures(data):
    for dp in data:
        wds = [w.value for w in dp.context]
        dp.result.features = Counter()
        dp.result.features.update(wds)

def trainModel(setup, data):
    modelType = setup["modelType"]
    func = getattr(sys.modules[__name__], modelType)
    model = func(setup, data)
    return model
    
def runModel(setup, model, data):
    for item in data:
        item.result.recordResult(model.run(setup, item))

def checkItem(setup, dp):
    try:
        if not dp.lexsn: #there are elements that are not tagged still
            return False
        else:
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
    terms = Set([x[0] for x in allposs])
    for term in terms:
        possVals = Set([x[1] for x in allposs if x[0]==term])
        vs[term].update(possVals)

def runExperiment(setup):
    
    trainData = loadData(setup, "train")
    testData = loadData(setup, "test")
    
    valueSpace = defaultdict(Set)
    
    updateValueSpace(valueSpace, trainData)
    updateValueSpace(valueSpace, testData)
    
    extractFeatures(trainData)
    extractFeatures(testData)
    
    model = trainModel(setup, trainData)
    runModel(setup, model, testData)
    
    return testData, valueSpace

def analyzeExperiment(valueSpace, results):
    words = valueSpace.keys()

    resByWord = defaultdict(list)
    
    for dp in results:
        resByWord[dp.value].append(dp)
     
    grandTotal = 0.0 
    avgAcc = 0.0  
    for item in valueSpace.keys():
        cf = ConfusionMatrix(valueSpace[item], item)
        for dp in resByWord[item]:
            cf.addItem(*dp.result.getResults())
            
        cf.computeMetrics()
        acc = cf.accuracy
        grandTotal += cf.total
        avgAcc += acc* cf.total

        print item, acc
        print cf.display()
        print
    
    print "AVERAGE ACCURACY: %f" % (avgAcc/grandTotal)

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