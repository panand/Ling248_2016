import pdb
import re
import json
import glob

tokMap = {"-LCB-": "{", "-RCB-": "}", "-LSB-": "[", "-RSB-": "]", "-LRB-": "(", "-RRB-": ")",}

puncRE = re.compile(r'\W+')
endPuncRE = re.compile(r'(^(\W+)|(\W+)$)')
auxForms = {}
auxForms["have"] = ["has", "had", "have"]
auxForms["be"] = ["be", "is", "are", "was", "were", "'s"]
auxForms["do"] = ["do", "does", "did"]
auxForms["can"] = ["ca", "can"]
auxForms["will"] = ["will", "wo"]

treeDir = "../../ptb/ptb_text/mrg/wsj/"

def getTreeFile(f):
    start = f[4:6]
    return "%s/%s/%s.txt" % (treeDir, start, f)

def listRightIndex(alist, value):
    look = re.compile(r'^' + value)
    for i in range(len(alist)):
        if look.search(alist[-1*i]):
            return len(alist) - i
    raise ValueError


def tokenizeBS(bs):
    fh = open(bs)
    lines = []
    for l in fh:
        l = l.rstrip('\n')
        ellip = l.index(' ...')
        fieldsStr = l[:ellip]
        snippetStr = l[ellip:]
        fields = fieldsStr.split(' ')
        tokens = snippetStr.split(' ')[2:] #leave of starting ...
        if '...' in tokens[-1]:
            if '....' not in tokens[-1]: #leave off ending ... but not ....
                tokens = tokens[:-1]
            else:
                tokens[-1] = tokens[-1].replace('....', '')

        lrep = {"file": fields[0], "toks": tokens, "anteInds": (int(fields[3]), int(fields[4])), "elidedInds": (int(fields[1]), int(fields[2])), "aux": fields[5], "anteType": fields[6], "connector": fields[7]}
        aux = fields[5]
        elidedInds = (int(fields[1]), int(fields[2]))
        elidedLen = elidedInds[1] - elidedInds[0]
        # if aux in auxForms:
        #     possAux = [x for x in auxForms[aux] if len(x) == elidedLen]
        # else:
        #     possAux = [aux]
        # possVPE = []
        # for au in possAux:
        #     try:
        #         v = listRightIndex(tokens, au)
        #         possVPE.append((v, au))
        #     except ValueError:
        #         pass
        # if len(possVPE) != 1:
        #     pdb.set_trace()        
        # else:
        #     lrep["auxForm"] = possVPE[0][1]
        #     lrep["VPETokInd"] = possVPE[0][0]
        lines.append(lrep)
    return lines

def makeBSString(toks):
    s= ''.join(toks)
    x = puncRE.sub('', s)
    return x

def special(tok):
    return tok[0] == "*" or tok == '0'

def makeTokenString(toks, window, start=0):
    tokensWithOffsets = []
    for i in range(start, len(toks)):
        if toks[i] in tokMap:
            tokensWithOffsets.append((i, tokMap[toks[i]]))
        elif not special(toks[i]):
            tokensWithOffsets.append((i, toks[i]))
    
    subToks = tokensWithOffsets[:min(window, len(tokensWithOffsets))]
    string = ''.join([x[1] for x in subToks])
    string = puncRE.sub('', string)
    try:
        indices = (subToks[0][0], subToks[-1][0])
    except:
        pdb.set_trace()
    return (indices,string)

def tokenizeOur(f):
    fh = open(f)
    lines = []
    for l in fh:
        lineNo, string = l.split('\t')
        
        tokens = string.split(' ')[:-1] #leave off the \n
        lrep = {"file": f, "toks": tokens, "line": lineNo}
        lines.append(lrep)
    return lines

def find(fInFile, ann, lookat, targetString, window=5):
    candSet = []
    indices = []
    r = None
    for c in fInFile:
        for i in range(len(c["toks"])):
            tok = c["toks"][i]
            try:
                nextTok = c["toks"][i+1]
            except IndexError:
                nextTok = ""
            if tok == lookat or tok+nextTok == lookat:
                 candSet.append(c)
                 indices.append(i)
    if indices == []:
        return None
    for i in range(len(candSet)):
        inds, string = makeTokenString(candSet[i]["toks"], window, indices[i])
        if string in targetString and inds[1]-inds[0] >= 3:
            #print string
            #print targetString
            #print candSet[i]["toks"][inds[0]:inds[1]+1]
            cand = candSet[i]
            tokIndex = inds
            #pdb.set_trace()
            r = {"bsSnippet": ann, "line": cand, "offset": tokIndex}
            #r["VPEIndex"] = cand["toks"].index(snipp["vpe"], tokIndex[0])
            return r
    if r == None:
        return None
        print "ERROR"
        print ann
        print lookat
        for i in range(len(c["toks"])):
            print makeTokenString(candSet[i]["toks"], window, indices[i])        
    

def merge(bs, allSnippets):
    files = set([x["file"] for x in bs])
    
    window = 5
    alignment = []
    
    for search in files:
        bsInFile = [x for x in bs if search in x["file"]]
        treeFile = getTreeFile(search)
        try:
            f = tokenizeOur(treeFile)
        except IOError:
            continue
        fInFile = [x for x in f if search in x["file"]]
        snippetsInFile = [x for x in allSnippets if search in x["file"]]
        for ann in bsInFile:
            try:
                r = None
                foundFlag = False
                BStoks = ann["toks"]
                BSstring = ' '.join(BStoks)
                snippCands = [x for x in snippetsInFile if BSstring in x["vpeText"]]
                if len(snippCands) != 1:
                    raise EOFError
        
        
                snipp = snippCands[0]
        
                anteWindow = 2
                anteToks = snipp["anteText"].split(' ')
                anteCharStart, anteCharEnd = snipp["anteSpan"]
                anteTokStart = snipp["anteText"][:anteCharStart].count(' ')
                anteTokEnd = snipp["ante"].count(' ') + anteTokStart
                anteStart = endPuncRE.sub('', anteToks[anteTokStart])
                anteEnd = endPuncRE.sub('', anteToks[anteTokEnd])
                lStart = max(anteTokStart-anteWindow, 0)
                lookat = endPuncRE.sub('', anteToks[lStart])
                lEnd = min(anteTokEnd+anteWindow, len(anteToks))
                targetString = makeBSString(anteToks[lStart:lEnd])
        
                ra = find(fInFile, ann, lookat, targetString)
                if not ra:
                    continue
                tokIndex = ra["offset"]
                cand = ra["line"]
                tStart = cand["toks"].index(anteStart, tokIndex[0])
                tEnd = cand["toks"].index(anteEnd, tStart)+1
                ra["AnteIndex"] = (tStart, tEnd)
        
                vpeWindow = 3
                vpeToks = snipp["vpeText"].split(' ')
                vpeCharStart, vpeCharEnd = snipp["vpeSpan"]
                vpeTokStart = snipp["vpeText"][:vpeCharStart].count(' ')
                vpeTokEnd = snipp["vpe"].count(' ') + vpeTokStart
                lStart = max(vpeTokStart-vpeWindow, 0)
                lookat = endPuncRE.sub('', vpeToks[lStart])
                lEnd = min(vpeTokEnd+vpeWindow, len(vpeToks))
                targetString = makeBSString(vpeToks[lStart:lEnd])
        
                rv = find(fInFile, ann, lookat, targetString)
                if not rv:
                    continue
            
                tokIndex = rv["offset"]
                cand = rv["line"]
                rv["VPEIndex"] = cand["toks"].index(snipp["vpe"], tokIndex[0])
        
                r = {"ante": ra, "vpe": rv, "snipp": snipp}
                anteStruct = {"text": snipp["ante"], "sentToks": ra["line"]["toks"], "indices": ra["AnteIndex"], "line": ra["line"]["line"]}
                vpeStruct = {"text": snipp["vpe"], "sentToks": rv["line"]["toks"], "index": rv["VPEIndex"], "line": ra["line"]["line"]}
        
                g = {"file": snipp["file"], "ante": anteStruct, "vpe":vpeStruct}
        
                alignment.append(g)
            except:
                pass
    return alignment

def loadAllSnippets(f):
    fh = open(f)
    a = []
    for l in fh:
        s = json.loads(l)
        a.append(s)
    return a

if __name__ == '__main__':
    our = "wsj_0765.txt"
    bs = "wsj_0765.extract"
    snippetsF = "allSnippets"
    
    
    allSnippets = loadAllSnippets(snippetsF)

    dir = "../BosSpen/vpe/wsj/"
    files = glob.glob(dir + "*.ann")
    allAnns = []
    for f in files:
        bsLines = tokenizeBS(f)
        results = merge(bsLines, allSnippets)
        for x in results:
            print x