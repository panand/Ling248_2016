#Tom Roberts
#HW assignment 2

import os
from collections import Counter
from operator import itemgetter
from lxml import html

corpus = "C:/Users/rotom/Desktop/grad_school/2015_2016/winter/comp_methods/semcor3.0/"
word_list = ['do','make','work']
split = 1
trainer = corpus + 'training/'+str(split)+'/'
test = corpus + 'test/' + str(split)+'/'

class MaxLikelihoodClassifier:

    def __init__(self, train_dir, test_dir, debug=False):

        self.train_dir = train_dir
        self.test_dir = test_dir
        self.train_set_size = len(os.listdir(train_dir))
        self.test_set_size = len(os.listdir(train_dir))
        self.debug = debug

    def get_sense_distribution(self, corpus):

        #returns a Counter whose keys are lemma, sense pairs

        sense_dist = Counter()
        
        for file in os.listdir(corpus):
            with open(corpus+file, 'r') as f:
                #need to use lxml package to parse degenerate xml files
                parsed = html.fromstring(f.read()) 
                for item in parsed.getiterator():
                    attribs = item.attrib
                    #count lemma/sense pairs 
                    #ignore all xml trees without lemma/lexsn attributes
                    try:
                        sense_map = (attribs['lemma'],attribs['lexsn'])
                        sense_dist[sense_map] += 1
                    except:
                        continue

##        if self.debug:
##            for count in sense_dist.most_common():
##                print str(count[1]) + '\t' + count[0][0] + '\t' + count[0][1]
            
        return sense_dist

    def train_dist(self):
        return self.get_sense_distribution(self.train_dir)

    def test_dist(self):
        return self.get_sense_distribution(self.test_dir)

    def subset_counts(self, counter, wordlist):
        #returns a subset of total lemma/sense pairs for a  list of particular lemmas
        #rewrites results in the meantime
        subsetted_counts = Counter({k:v for k,v in counter.items() if k[0] in wordlist})
        
        if self.debug:
            for count in subsetted_counts.most_common():
                output = open(corpus + "prob2_split_" + str(split) + ".txt", 'a')
                countline = str(count[1]) + '\t' + count[0][0] + '\t' + count[0][1]
                print countline
                output.write(countline + '\n')
        return subsetted_counts

class NaiveClassifier(MaxLikelihoodClassifier):

    def __init__(self):
        #initiate a hash that maps words to their most frequent senses
        self.most_freq_senses = {}
        super(MaxLikelihoodClassifier, self).__init__()

    def get_most_common_sense(self, counter, word):

        #get the most common sense of a word given a (word,sense) tuple and counts in a counter
        counter = counter.most_common()
        for (lemma,sense) in counter:
            if lemma == word:
                return sense

    def compute_accuracy(self, counter):
        accuracy_dict = Counter()
        #given a counter of the usual type, compute accuracy in terms of classification
        for (lemma, sense) in counter:
            most_common_sense = self.get_most_common_sense(counter,lemma)
            if sense == most_common_sense:
                accuracy_dict[(lemma, 'accurate')] += counter(lemma,sense)
            else:
                accuracy_dict[(lemma, 'inaccurate ')] += counter(lemma,sense)
        return accuracy_dict
                
            

class BagOfWordsClassifier(MaxLikelihoodClassifier):

    pass
        
        

if __name__ == '__main__':
    
    #nc.computer_accuracy(trainer())

    #Problem 2 outputs
    for i in range(1,5):
        split = i
        trainer = corpus + 'training/'+str(split)+'/'
        test = corpus + 'test/' + str(split)+'/'
        mlc = MaxLikelihoodClassifier(trainer, test, True)
        mlc.subset_counts(mlc.train_dist(),word_list)

    #Problem 3 is broken, please stand by
        
        
        
        
                    
                    

    
            
        
