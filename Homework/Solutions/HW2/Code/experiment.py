class Token:
    def __init__(self, attrib, text):
        self.text = text
        attribs = ["pos", "cmd", "lemma", "lexsn", "wnsn"]
        for a in attribs:
            try:
                setattr(self,a,attrib[a])
            except KeyError:
                setattr(self,a, None)

class Datapoint:
    def __init__(self, token):
        self.token = token
        self.word = token.text
        if(token.lemma):
            self.lemma = token.lemma
            self.value = self.lemma
        else:
            self.lemma = None
            self.value = self.word
            
        if(token.lexsn):
            self.lexsn = token.lexsn
        else:
            self.lexsn = None
            
        self.result = ExpRun()
            
    
    def setContext(self, context):
        self.context = context

class ExpRun:
    def __init__(self):
        self.features =  None
        self.truth = None
        self.result = None
        self.correct = None
                
    def recordTruth(self, truth):
        self.truth = truth
    
    def recordResult(result):
        self.result = result
        if self.result == self.truth:
            self.correct = True
        else:
            self.correct = False
            
    def getResults(self):
        return (self.truth, self.result)

class ConfusionMatrix:
    def __init__(self, labels):
        self.labels = labels
        self.vals = {}
        
        self.true = {}
        self.predicted = {}
        
        self.correctByLabel = {}
        self.precisions = {}
        self.recalls = {}
        self.fscores = {}
        
        self.correct = 0.0
        self.avgPrec = 0.0
        self.avgRec = 0.0
        self.avgFScore = 0.0
        self.accuracy = 0.0
        

        for l in labels:
            self.true[l] = 0.0
            self.predicted[l] = 0.0
            
            self.correctByLabel[l] = 0.0
            self.precisions[l] = 0.0
            self.recalls[l] = 0.0
            self.fscores[l] = 0.0

            self.vals[l] = {}
            for m in labels:
                self.vals[l][m] = 0.0
        
        self.total = 0.0
    
    def addItem(self, true, predicted):
        self.vals[true][predicted] += 1
        self.total +=1
        
        self.true[true] += 1
        self.predicted[predicted] += 1
        
        if true == predicted:
            self.correct += 1
            self.correctByLabel[true] += 1
    
    def computeMatrics(self):
        self.accuracy = self.correct / self.total
        labels = self.labels
        numLabels = len(labels)
        
        for l in labels:
            try:
                self.precisions[l] = self.correctByLabel[l] / self.predicted[l]
            except ZeroDivisionError:
                self.precisions[l] = 1 #if you call nothing l, then you can't be imprecise
                
            self.recalls[l] = self.correctByLabel[l] / self.true[l]
            
            try:
                self.fscore[l] = 2/( 1/self.precisions[l] + 1/self.recalls[l])
            except ZeroDivisionError:
                self.fscore[l] = 0 #if either of the above is zero, then F-score is 0
        
            self.avgPrecision += self.precisions[l] / numLabels
            self.avgRecall += self.recalls[l] / numLabels
            self.avgFScore += self.fscores[l] / numLabels
            
    def display(self):
        
        def getHeader(labels):
            return "\t" + '\t'.join(labels) + '\n'
        
        def getRow(label, labels, vals):
            rowVals = [str(int(vals[label][x])) for x in labels]
            rowText = '\t'.join(rowVals)
            return "%s\t%s\n" % (label, rowVals)
            
        strOut = ""
        labels = self.labels
        vals = self.vals
        
        strOut += getHeader(labels)
        
        for l in labels:
            strOut += getRow(l, labels, vals)
        
        return strOut
            