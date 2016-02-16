class Token:
    def __init__(self, attrib, text):
        self.text = text
        attribs = ["pos", "cmd", "lemma", "lexsn", "wnsn"]
        for a in attribs:
            try:
                setattr(self,a,attrib[a])
            except:
                setattr(self,a, None)
        
        if "lemma" in attrib:
            self.value = self.lemma
        else:
            self.value = self.text

class Datapoint:
    def __init__(self, token):
        self.token = token
        self.word = token.text
        self.value = token.value
            
        if(token.lexsn):
            self.lexsn = token.lexsn
        else:
            self.lexsn = None
            
        self.result = ExpRun()
        self.result.recordTruth(self.lexsn)
            
    
    def setContext(self, context):
        self.context = context
        
    def setMetadata(self, fname, sentNum):
        self.fname = fname
        self.sentNum = sentNum

class ExpRun:
    def __init__(self):
        self.features =  None
        self.truth = None
        self.result = None
        self.correct = None
                
    def recordTruth(self, truth):
        self.truth = truth
    
    def recordResult(self, result):
        self.result = result
        if self.result == self.truth:
            self.correct = True
        else:
            self.correct = False
            
    def getResults(self):
        return (self.truth, self.result)

class ConfusionMatrix:
    def __init__(self, labels, itemType):
        self.itemType = itemType
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
        try:
            self.vals[true][predicted] += 1
        except Exception as e:
            import pdb
            pdb.set_trace()
        self.total +=1
        
        self.true[true] += 1
        self.predicted[predicted] += 1
        
        if true == predicted:
            self.correct += 1
            self.correctByLabel[true] += 1
    
    def computeMetrics(self):
        self.accuracy = self.correct / self.total
        labels = self.labels
        numLabels = len(labels)
        
        for l in labels:
            try:
                self.precisions[l] = self.correctByLabel[l] / self.predicted[l]
            except ZeroDivisionError:
                self.precisions[l] = 1 #if you call nothing l, then you can't be imprecise
            try:
                self.recalls[l] = self.correctByLabel[l] / self.true[l]
            except ZeroDivisionError:
                self.recalls[l] = 1 #in this case, it is something in the training set never found in the test set
            
            try:
                self.fscores[l] = 2/( 1/self.precisions[l] + 1/self.recalls[l])
            except ZeroDivisionError:
                self.fscores[l] = 0 #if either of the above is zero, then F-score is 0
        
            self.avgPrec += self.precisions[l] / numLabels
            self.avgRec += self.recalls[l] / numLabels
            self.avgFScore += self.fscores[l] / numLabels
            
    def display(self):
        
        def maxWidth(ls):
            return max([len(x) for x in ls])
        
        def getHeader(labels, width):
            
            strCode = "%" + str(width) + "s"
            formatStr = strCode * (len(labels) + 1)
            l = [""]
            l.extend(labels)
            return formatStr % tuple(l) + '\n'

        def getFooter(labels, width):
            
            intCode = "%" + str(width) + "d"
            strCode = "%" + str(width) + "s"
            formatStr = intCode * (len(labels)+1)
            rowVals = [self.true[x] for x in labels]
            rowVals.append(self.total)
            valText = formatStr % tuple(rowVals)
            return strCode % "" + valText + "\n"

        
        def getRow(label, labels, vals, width):
            intCode = "%" + str(width) + "d"
            strCode = "%" + str(width) + "s"
            formatStr = intCode * (len(labels)+1)
            rowVals = [vals[x][label] for x in labels]
            rowVals.append(self.predicted[label])
            valText = formatStr % tuple(rowVals)
            return strCode % label + valText + "\n"
        
        strOut = ""
        labels = self.labels
        vals = self.vals
        width = maxWidth(labels) + 3   
        
        strOut += getHeader(labels, width)
        
        for l in labels:
            strOut += getRow(l, labels, vals, width)
        
        strOut += getFooter(labels, width)
        return strOut
            