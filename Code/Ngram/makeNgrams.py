import sys
from collections import defaultdict

import pdb

def error(msg):
    print msg
    sys.exit(1)

def ngram(toks, n):
    assert(n>0)
    return [toks[i:i+n] for i in range(len(toks)-n+1)]    

def getNgrams(fname, n, specialNgrams):
    ngramCounts = defaultdict(int)
    
    try:
        fd = open(fname, "r")
    except:
        error("Cannot open file %s\n" % fname)
    
    for l in fd:
        winl = l.rstrip('\n\r').split(' ')
        if specialNgrams:
            winl = filter(lambda x:  x in specialNgrams, winl)

        # if '\n' in winl or '\r' in winl:
        #     pdb.set_trace()

        ngramsInLine = ngram(winl, n)
        
        for ng in ngramsInLine:
            if ng == '' or ' ' in ng:
                pdb.set_trace()
            ngramCounts[' '.join(ng)] += 1
    
    for ng,cnt in ngramCounts.items():
        print "%s\t%d" % (ng,cnt)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print 'Usage: python makeNgrams.py file n\n'
        sys.exit(1)
    else:
        script, fname, n = sys.argv
    
    specialNgrams = [",_,", "and_CC", "._.", "I_PRP", "the_DT", "a_DT"]#, "to_TO", "it_PRP", "was_VBD", "n't_RB", "he_PRP", "of_IN", "in_IN", ";_:", "``_``", "''_''", "you_PRP", "me_PRP", "but_CC", "on_IN", "for_IN", "him_PRP", "--_:", "could_MD", "had_VBD", "said_VBD", "got_VBD", "would_MD", "all_DT", "up_RP", "out_RP", "so_RB", "they_PRP", "his_PRP$", "my_PRP$", "?_.", "'_''", "then_RB", "with_IN", "by_IN", "that_DT", "'s_POS", "He_PRP", "went_VBD", "about_IN", "`_``", "no_DT", "as_IN", "that_IN"]
    
    getNgrams(fname, int(n), specialNgrams)