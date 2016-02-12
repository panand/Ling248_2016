from bs4 import BeautifulSoup
from collections import Counter
import collections
from collections import defaultdict
import os
cntdo=Counter()
cntmake=Counter()
cntwork=Counter()
cntword=Counter()
newdic={} #make dictionary
dolemmalist=[]
makelemmalist=[]
worklemmalist=[]

for filename in os.listdir(os.getcwd()):
    code=open(filename,'r')
    soup = BeautifulSoup(code, 'lxml')

    sentences=soup.find_all('s')
    for s in sentences:
        words=s.find_all('wf')
        for w in words:
            if w.get('lemma')=="do": #Find sentences with do
                sense=w.get('lexsn') #get a sense of that do
                dosentences=BeautifulSoup(str(s),'lxml') #retrieve a sentence and read it
                interestwords=dosentences.find_all('wf') #parse words
                for i in interestwords: #For each word in a sentence with do
                    if i.get("lemma")!=None: #if there is info of lemma
                         dolemmalist.append((sense, i.get("lemma"))) #make a pair of that word and a sense of do 
            elif w.get('lemma')=="make":
                sense=w.get('lexsn')
                makesentences=BeautifulSoup(str(s),'lxml')
                interestwords=makesentences.find_all('wf')
                for i in interestwords:
                    if i.get("lemma")!=None:
                         makelemmalist.append((sense, i.get("lemma")))
            elif w.get('lemma')=="work":
                sense=w.get('lexsn')
                makesentences=BeautifulSoup(str(s),'lxml')
                interestwords=makesentences.find_all('wf')
                for i in interestwords:
                    if i.get("lemma")!=None:
                         worklemmalist.append((sense, i.get("lemma")))

for i in dolemmalist:
    cntdo[i]+=1
for i in makelemmalist:
    cntmake[i]+=1
for i in worklemmalist:
    cntwork[i]+=1  


                
                
                
                
