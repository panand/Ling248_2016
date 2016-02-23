#!/usr/bin/python

from collections import defaultdict, Counter

def extractData(fd):
    a = defaultdict(lambda: defaultdict(float))
    normalizer = Counter()
    b = defaultdict(lambda: defaultdict(float))
    pi = defaultdict(float)
    piNorm = 0.0

    for l in fd:
        winl = l.rstrip('\n\r').split(' ')

        winl = filter(lambda x: x != "", winl)
        posSplit = [x.split('__') for x in winl]
        posAlone = [x[1] for x in posSplit]
        
        pi[posSplit[0][1]] += 1
        piNorm += 1
        
        for i in range(len(winl)):
            term,pos = posSplit[i]
            b[pos][term] += 1
            normalizer[pos] += 1
            
            try: #work for all but last
                qi = pos
                qj = posAlone[i+1]
                a[qi][qj] += 1
            except:
                pass
                
    afile = open("a.tab", "w")
    bfile = open("b.tab", "w")
    pifile = open("pi.tab", "w")


    for posi in a.keys():
        
        v = pi[posi]
        vnorm = v/piNorm
        pifile.write("%s\t%d\t%f\n" %(posi, v, vnorm))
        
        for posj in a[posi].keys():
            v = a[posi][posj]
            vnorm = v/normalizer[posi]
            afile.write("%s\t%s\t%d\t%f\n" %(posi, posj, v, vnorm))
        
        for w in b[posi].keys():
            v = b[posi][w]
            vnorm = v/normalizer[posi]
            bfile.write("%s\t%s\t%d\t%f\n" %(posi, w, v, vnorm))
    
    afile.close()
    bfile.close()
    pifile.close()


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Take a sentences of form word_pos and compute pos->pos transition probabilities and pos->term output probabilities')
    parser.add_argument('file', metavar='file', type=str, 
                       help='the corpus file')
                       
    args = parser.parse_args()
    
    fd = open(args.file, "r")
    
    extractData(fd)
    
    fd.close()
    