import re
import pdb
import glob
import json


def process(f):
    titleRE = re.compile(r'(wsj_\d+) \(line (\d+), ant (\w+)')
    antRE = re.compile(r'(<font color=(green|blue)><b>)([^<]+)(</b></font>)')
    vpeRE = re.compile(r'(<font color=blue><b>)([^<]+)(</b></font>)')
    
    fh = open(f)
    ann = {}
    anns = []
    for l in fh:
        l = l.rstrip('\n')
        l = l.replace('</p>', '')
        r = titleRE.search(l)
        if r:
            if ann:
                if ann["vpeMarkup"] == ann["anteMarkup"]:
                    l = ann["anteMarkup"]
                    m = antRE.search(l)
                    if m.group(2) == 'green': #antecedent
                        start, end = m.span(3)
                        markupStart, markupEnd = m.span()
                        ann["anteSpan"] = (markupStart, markupStart + len(ann["ante"]))
                        ann["anteText"] = l[:markupStart] + l[start:end] + l[markupEnd:]
                        l = l[:markupStart] + l[start:end] + l[markupEnd:]
                        
                        m = antRE.search(l)
                        start, end = m.span(3)
                        markupStart, markupEnd = m.span()
                        ann["vpeSpan"] = (markupStart, markupStart + len(ann["vpe"]))
                        ann["anteText"] = ann["vpeText"] = l[:markupStart] + l[start:end] + l[markupEnd:]
                        
                    else:
                        start, end = m.span(3)
                        markupStart, markupEnd = m.span()
                        ann["vpeSpan"] = (markupStart, markupStart + len(ann["vpe"]))
                        ann["vpeText"] = l[:markupStart] + l[start:end] + l[markupEnd:]
                        l = l[:markupStart] + l[start:end] + l[markupEnd:]
                        
                        m = antRE.search(l)
                        if not m:
                            pdb.set_trace() 
                        start, end = m.span(3)
                        markupStart, markupEnd = m.span()
                        ann["anteSpan"] = (markupStart, markupStart + len(ann["ante"]))
                        ann["anteText"] = ann["vpeText"] = l[:markupStart] + l[start:end] + l[markupEnd:]
                                                
                anns.append(ann)
            ann = {}
            
            ann["file"], ann["line"], ann["antType"] = r.groups()
            continue
        else:
            for m in antRE.finditer(l):
                if m.group(2) == 'green': #antecedent
                    ann["anteMarkup"] =l
                    start, end = m.span(3)
                    ann["ante"] = m.group(3)
                    markupStart, markupEnd = m.span()
                    ann["anteSpan"] = (markupStart, markupStart + len(ann["ante"]))
                    ann["anteText"] = l[:markupStart] + l[start:end] + l[markupEnd:]
                    #l = l[:markupStart] + l[start:end] + l[markupEnd:]
                else:
                    ann["vpeMarkup"] =l
                    start, end = m.span(3)
                    ann["vpe"] = m.group(3)
                    markupStart, markupEnd = m.span()
                    ann["vpeSpan"] = (markupStart, markupStart + len(ann["vpe"]))
                    ann["vpeText"] = l[:markupStart] + l[start:end] + l[markupEnd:]
                    
    #do the last one
    if ann == {}:
        pdb.set_trace()
    if ann["vpeMarkup"] == ann["anteMarkup"]:
        l = ann["anteMarkup"]
        m = antRE.search(l)
        if m.group(2) == 'green': #antecedent
            start, end = m.span(3)
            markupStart, markupEnd = m.span()
            ann["anteSpan"] = (markupStart, markupStart + len(ann["ante"]))
            ann["anteText"] = l[:markupStart] + l[start:end] + l[markupEnd:]
            l = l[:markupStart] + l[start:end] + l[markupEnd:]

            m = antRE.search(l)
            start, end = m.span(3)
            markupStart, markupEnd = m.span()
            ann["vpeSpan"] = (markupStart, markupStart + len(ann["vpe"]))
            ann["anteText"] = ann["vpeText"] = l[:markupStart] + l[start:end] + l[markupEnd:]

        else:
            start, end = m.span(3)
            markupStart, markupEnd = m.span()
            ann["vpeSpan"] = (markupStart, markupStart + len(ann["vpe"]))
            ann["vpeText"] = l[:markupStart] + l[start:end] + l[markupEnd:]
            l = l[:markupStart] + l[start:end] + l[markupEnd:]

            m = antRE.search(l)
            if not m:
                pdb.set_trace() 
            start, end = m.span(3)
            markupStart, markupEnd = m.span()
            ann["anteSpan"] = (markupStart, markupStart + len(ann["ante"]))
            ann["anteText"] = ann["vpeText"] = l[:markupStart] + l[start:end] + l[markupEnd:]

    anns.append(ann)

                
    return anns
    
if __name__ == '__main__':
    dir = "../BosSpen/html/"
    files = glob.glob(dir + "*.html")
    allAnns = []
    for f in files:
        anns = process(f)
        allAnns.extend(anns)
    for a in allAnns:
        # print "[%s]" % (a["vpeText"][a["vpeSpan"][0]:a["vpeSpan"][1]])
        #         print "[%s]" % (a["anteText"][a["anteSpan"][0]:a["anteSpan"][1]])
        #         for x in a:
        #             print x, a[x]
        print json.dumps(a)