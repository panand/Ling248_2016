#!/usr/bin/python

import os
import xml.etree.ElementTree as ET
import re
import pdb
from experiment import *
import pickle

repairRE = re.compile(r'=([^>\s]+)')

def extractData(dirname, outfile):
    datapoints = []
    def replMatch(m):
        return '="%s"' % m.groups()[0]
        
    for fname in os.listdir(dirname):
        fd = open(os.path.join(dirname, fname))
#        parsed = html.fromstring(mytext)
#        for x in parsed.getiterator(): print x.tag, x.attrib, x.text, x.tail

        data = fd.read()
        dataFixed = repairRE.sub(replMatch, data) #put quotes around attributes
        dataFixed = dataFixed.replace('<punc>&</punc>', '<punc>&amp;</punc>')
        dataFixed = dataFixed.replace('""', '"')
        dataFixed = dataFixed.replace('rdf= ', 'rdf="" ')

        try:
            tree = ET.fromstring(dataFixed) #parse into xml
            #now look for all sentences
            #look for <context> <p> <s> treelets"
            for sent in tree.findall('context/p/s'):
                sentNum = sent.attrib['snum']
                words = sent.getchildren()
                tokens = [Token(word.attrib, word.text) for word in words]
                for tok in tokens:
                    dp = Datapoint(tok)
                    dp.setContext(tokens)
                    dp.file = fname
                    dp.sentNum = sentNum
                    datapoints.append(dp)
                fd.close()
        except:
            print fname
            fo = open(fname, "w")
            fo.write(dataFixed)
            fo.close()
            next
    try:
        fout = open(outfile, "w")
        pickle.dump(datapoints, fout, protocol=2)
        fout.close()
    except:
        print "Error saving"


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Take a directory of semcor files and spit out a pickled representation of each token as its own Datapoint object, with context.')
    parser.add_argument('dirname', metavar='d', type=str, 
                       help='the directory with the files')
    
    parser.add_argument('outfile', metavar='o', type=str, 
                       help='the location of the pickled object')
                       
    args = parser.parse_args()
    
    extractData(args.dirname, args.outfile)
    print args.dirname
    