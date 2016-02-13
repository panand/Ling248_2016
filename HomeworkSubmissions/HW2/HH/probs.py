from bs4 import BeautifulSoup
from collections import Counter
import collections
from collections import defaultdict

wordlist=[]
probdicdo={}
probdicmake={}
probdicwork={}

dic2=eval(open("countlemmado.txt").read()) #This is what I got from problem4_1.py
dic3=eval(open("countlemmamake.txt").read()) #This is what I got from problem4_1.py
dic4=eval(open("countlemmawork.txt").read()) #This is what I got from problem4_1.py
dicsense={'do': {'2:36:02::': 25, '2:41:03::': 2, '2:41:02::': 20, '2:36:02::;2:41:01::': 1, '2:41:04::': 116, '2:36:01::': 169, '2:36:00::': 8, '2:42:02::': 2, '2:42:01::': 6, '2:42:00::': 52, '2:41:04::;2:41:01::': 4, '2:38:00::': 1, '2:41:01::': 474, '2:29:04::': 2, '2:29:09::': 1}, 'make': {'2:29:08::': 5, '2:36:04::': 2, '1:09:00::': 1, '2:32:00::': 56, '2:36:05::': 12, '2:36:09::': 15, '2:36:12::': 8, '2:42:05::': 7, '2:31:13::': 4, '2:36:13::': 3, '2:36:15::': 15, '2:30:15::': 4, '2:42:00::': 7, '2:36:08::': 57, '2:36:11::': 5, '2:41:03::': 4, '2:29:00::': 1, '2:38:00::;2:38:02::': 1, '2:38:02::': 11, '2:41:00::': 437, '2:31:00::': 31, '2:40:01::': 12, '2:30:00::': 401, '2:36:13::;2:36:05::': 2, '2:38:05::': 1, '2:36:01::': 46, '2:36:00::': 227, '2:41:13::': 3, '2:30:02::': 2, '2:38:00::': 3, '2:40:02::': 2}, 'work': {'1:09:00::': 11, '2:38:02::': 2, '1:06:00::;1:04:00::': 1, '1:04:01::': 26, '2:35:02::': 20, '2:41:03::': 30, '2:29:00::': 8, '1:06:00::': 71, '2:41:05::': 3, '2:32:00::': 1, '2:41:00::': 60, '1:04:00::': 77, '1:06:01::': 3, '2:41:01::': 1, '1:19:00::': 5, '2:30:00::': 4, '2:41:02::': 66, '2:41:04::': 4, '2:36:01::': 3, '2:36:00::': 9, '2:38:00::': 5, '2:41:06::': 25}}
    
for key in dic2: #this is for do
    sense=key[0]
    word=key[1]
    denom=dicsense['do'][sense]
    if key[1]!='do':
        probdicdo.setdefault(sense,{})
        probdicdo[sense].setdefault(word, 0)
        probdicdo[sense][word]=dic2[key]/float(denom)
        
for key in dic3: #this is for make
    sense=key[0]
    word=key[1]
    denom=dicsense['make'][sense]
    if key[1]!='make':
        probdicmake.setdefault(sense,{})
        probdicmake[sense].setdefault(word, 0)
        probdicmake[sense][word]=dic3[key]/float(denom)
        
for key in dic4: #this is for work
    sense=key[0]
    word=key[1]
    denom=dicsense['work'][sense]
    if key[1]!='work':
        probdicwork.setdefault(sense,{})
        probdicwork[sense].setdefault(word, 0)
        probdicwork[sense][word]=dic3[key]/float(denom)
        
f=open('probdo.txt', 'w')
f.write(str(probdicdo))
f=open('probmake.txt', 'w')
f.write(str(probdicmake))
f=open('probwork.txt', 'w')
f.write(str(probdicwork))
