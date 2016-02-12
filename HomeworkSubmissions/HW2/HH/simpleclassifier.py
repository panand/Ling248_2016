from bs4 import BeautifulSoup
from collections import Counter
import collections
from collections import defaultdict
import os
cnt=Counter()
newdic={} #make dictionary
lemmalist=[]
docountacc=0
docounterr=0
docount=0
makecountacc=0
makecounterr=0
makecount=0
workcountacc=0
workcounterr=0
for filename in os.listdir(os.getcwd()):
    code=open(filename,'r')
    soup = BeautifulSoup(code, 'lxml')
    for words in soup.find_all('wf'):
        if words.get('lemma')=='do':
            if words.get('lexsn')=='2:41:01::':
                docountacc+=1
                print 'correct', filename
            else:
                docounterr+=1
                print 'error', filename
    for words in soup.find_all('wf'):
        if words.get('lemma')=='make':
            if words.get('lexsn')== '2:41:00::':
                makecountacc+=1
            else:
                makecounterr+=1
    for words in soup.find_all('wf'):
        if words.get('lemma')=='work':
            if words.get('lexsn')== '1:04:00::':
                workcountacc+=1
            else:
                workcounterr+=1 

print 'do correct hit', docountacc,'do error count', docounterr
print 'make correct hit', makecountacc,'make error count', makecounterr
print 'work correct hit', workcountacc,'work error count', workcounterr

    
