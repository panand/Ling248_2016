import os, copy
from collections import Counter, defaultdict

semcor_dir = '../Ling248_2016-master/Data/semcor3.0/'

## Problem 0. Looking in the brown2 directory, please construct a sorted (most to least) list of joint counts for lemmas and their lexsns. Your file should match words-and-senses.list in this directory.

## Function that takes a list of lines (from an xml file) and builds a counter of each lemma/sense combination in it.
def lines_to_lxs_counter(lines):
	#print "running lines_to_lxs_counter"
	c = Counter()
	for line in lines:
		
		if line[0:3] != '<wf':
			continue
		# Get the part of the line that follows the lemma tag
		lemma_split = line.split('lemma=')
		if len(lemma_split)<2: 	# if "lemma=" wasn't found in this line, then move on
			continue
		lemmaplus = lemma_split[1]
		
		# Isolate the lemma itself
		lemma = lemmaplus.split(' ')[0]
		
		# Isolate the lexsn: this requires splitting twice since the lexsn can be followed by
		# either a space + another tag, or a closing '>'
		lexsn = lemmaplus.split('lexsn=')[1].split(' ')[0].split('>')[0]
		c[lemma +' '+lexsn] += 1
	#print c
	return c
	
def apply_to_dir(d, results, foo):

	for tf in os.listdir(d):
		f = open(d+'/'+tf, 'r')
		lines = f.read().split('\n')
		f.close()
	
		results = results + foo(lines)
	return results

## Function that takes a directory and returns a counter of all the lemma x sense combinations in all the files in that directory
## **Stop using this to speed things up!**
def directory_to_lxs_counter(d):
	lxs = Counter()
	return apply_to_dir(d, lxs, lines_to_lxs_counter)	
	
def write_counter_to_file(ctr, fname, append_mode):
	ctr_str = []
	for lxs in ctr.most_common():
		s = str(lxs[1])+'\t'+lxs[0]
		ctr_str.append(s)
	ctr_str = '\n'.join(ctr_str)+'\n'

	if append_mode:
		f = open(fname,'a')
	else:
		f = open(fname,'w')
	f.write(ctr_str)
	f.close()

print "Doing Problem 0..."	
b2_lxs = directory_to_lxs_counter(semcor_dir+'brown2/tagfiles')
write_counter_to_file(b2_lxs, 'problem0.txt', False)

#################################################################################
## Do some set up
print "Doing set-up that follows up on Problem 1..."
## Read in the contents of all the files in directory d, concatenating their lines into one list of lines.
def concatenate_tagfiles(d):
	results = []
	
	file_list = os.listdir(d)
	for tf in file_list:
		f = open(d+'/'+tf,'r')
		lines = f.read().split('\n')
		f.close()
		results.extend(lines)
		
	return (results, len(file_list))
	
brownALL = semcor_dir+'brownALL/tagfiles_split'
test_dev_dirs = [(brownALL+str(i)+'/dev', brownALL+str(i)+'/test') for i in range(1,5)]
words = ['do', 'make', 'work']


# Extract all the lines of each file in each dev and each test directory into a list of strings so we don't have to keep reading the files over and over again.
test_texts = []
dev_texts = []
for td in test_dev_dirs:
	# get dev text (as list of lines) and save it in dev_texts, paired with how many files it represents: (text, num_files)
	devtext = concatenate_tagfiles(td[0])
	dev_texts.append(devtext)
	# get test text (as list of lines) and save it in test_texts, along with how many files it represents: (text, num_files)
	test_texts.append(concatenate_tagfiles(td[1]))

# Create lemma x sense counters for each development set
dev_counters = range(0,4)	
for text in dev_texts:
	i = dev_texts.index(text)
	dev_counters[i] = lines_to_lxs_counter(text[0])
	#print dev_counters[i]['do 2:41:01::']


#################################################################################

# problem 2. We will be examining the following three words: do, make, work. For each of these, compute the joint counts for each of the senses one encounters throughout the training split. This is probably best stored as a two-dimensional hash.

print "Doing Problem 2..."

## Function that takes a counter c where the keys take the form 'lemma  sense'
## and returns the subset of c where the lemma is w
def get_lemma_subset(c, w):
	cw = Counter()
	for e in c:
		lemma = e.split(' ')[0]
		sense = e.split(' ')[1]
		# if the lemma is the one we're interested in, then add this entry to our word-specific counter
		if lemma == w:
			cw[sense] += c[e]
	return cw

	
# Set up a list in which to save the counts found for each development set
p2_counts_by_dev = range(0,4)
# For each dev. set...
for ts in dev_counters:
	devset_num = dev_counters.index(ts)
	# create a dictionary whose keys will be do, make, work
	do_make_work_dict = {}
	for w in words:
		# get counts of the senses for each word
		w_cntr = get_lemma_subset(ts, w)
		# Add the resulting Counter to the dictionary under the appropriate word
		do_make_work_dict[w] = w_cntr

		# Now write our results to a file, starting from scratch if we're on the first word 
		# and appending to the existing file if we're on a later word.
		w_file = 'problem2_split'+str(devset_num+1)+'.txt'
		write_counter_to_file(w_cntr, w_file, (words.index(w)>0))
		
	# Also save the do/make/work dictionary for this development set into a list of dictionaries
	p2_counts_by_dev[devset_num] = do_make_work_dict
		

#################################################################################
## Problem 3. Now, let's write our first classifier. For this, assume that we always choose the most common sense for a given word, given the hash you constructed above. For each of the three words above, compute the accuracy of this classifier on the relevant test splits. Make a table of the word, the number of train files, and the accuracy of the classifier.

print "Doing Problem 3..."

## Take the lines of a semcor xml file and return a table showing each instance of lemma with its sense
def make_lxs_table(word, lines):
	c = []
	for line in lines:
		if line[0:3] != '<wf' or word not in line:
			continue
		if 'lemma=' not in line:
			continue
		# Get the part of the line that follows the lemma tag
		lemmaplus = line.split('lemma=')[1]
		
		# Isolate the lemma itself
		lemma = lemmaplus.split(' ')[0]
		if lemma != word:
			continue
		# Isolate the lexsn: this requires splitting twice since the lexsn can be followed by
		# either a space + another tag, or a closing '>'
		lexsn = lemmaplus.split('lexsn=')[1].split(' ')[0].split('>')[0]
		token = line.split('>')[1].split('<')[0]	#the actual token on this line is what shows up between the xml tags
		c.append([word+': '+token, lexsn])
	return c
	
## Utility: Take a list of lists and print it as a table
def print_table(table, path):
	rows = []
	for row in table:
		rows.append('\t'.join(row))
	text = '\n'.join(rows)
	f = open(path, 'w')
	f.write(text)
	f.close()


## Given a dev_set and a word, return the most common sense of the word in that dev_set (Problem 3's classifer)
## Context is not necessary.
def p3_classifer(ds_num, w):
	w_counter = p2_counts_by_dev[ds_num][w]				# Get the counter of senses for word w in dev. set ds_num
	most_common_entry = w_counter.most_common(1)[0]		# Counter.most_common(n) returns a list of length n (here, 1). 
	most_common_key = most_common_entry[0]				# An entry is a (key, value) tuple
	return most_common_key
	
	
def run_p3_classifer(ds_num, w):
	modeled_sense = p3_classifer(ds_num, w)
	
	# Make a table of all the occurrences of the word of interest in the test set of interest
	w_table = make_lxs_table(w, test_texts[ds_num][0])
	for row in w_table:
		actual_sense = row[1]
		classified_correctly = 0
		if actual_sense == modeled_sense:
			classified_correctly = 1
		row.extend([modeled_sense, classified_correctly])
		#print row
	num_rows = len(w_table)
	num_correct = sum(x[3] for x in w_table)
	accuracy = 1.0*num_correct/num_rows
	
	classifer_score = [w,str(ds_num+1),str(len(dev_texts[ds_num][0])),str(accuracy)]
	return classifer_score


## For each dev/test split for the words [do,make,work], report the specified classifer's accuracy in that test set (plus some info about the test set).
def classify_and_report_4splits(classifer_results, problem_num):
	## Header for the output table
	acc_table = [['word','devset','num. train files','p'+str(problem_num)+'accuracy']]
	
	for dt in dev_texts:
		ds_num = dev_texts.index(dt)
		num_dev_files = dt[1]
		for w in words:
			
			classifer_row = classifer_results(ds_num, w) 		
			acc_table.append(classifer_row)
		
	print_table(acc_table, 'problem'+str(problem_num)+'_accuracy.txt')
	



## Now run the various problem 3 classifers and output their accuracies to this file.
classify_and_report_4splits(run_p3_classifer, 3)
		

#################################################################################
## Problem 4. We will now implement the Naive Bayes bag of words classifier. To do this, we must compute both P(s_i) and P(w_j|s_i) as discussed today. We will assume we are ONLY looking at senses for the word in question (so only cases with do, make, and work). Let us assume that our window is the sentence: We will be looking at all of the words within the sentence containing the relevant word. You can store these scores in a 2D hash for each word (so, for "do", you will have a dictionary from senses of do to words to probabilities. As in Problem 3, run this across the 4 train-test splits and produce a table of your results.

print 'Doing Problem 4...'

## Take a devset number and a word to look up, and return a dictionary from senses to co-occurring words to counts of those words
## Intended for use with p4_classifer
def get_p4_counts(ds_num,w):
	dev_text = dev_texts[ds_num][0]
	snum = 0
	words_in_sent = []
	w_in_sent = []	# a list of the occurrences of w in the sentence, with associated senses and positions
	
	# tallies go in a 2d-dictionary from senses to co-occurring words to counts of those words
	w_dict = defaultdict(lambda: Counter())
	
	line_num = 0
	while line_num < len(dev_text):
		line = dev_text[line_num]
		tag = line[0:4]
		
		# if the sentence is over, then do some analysis, then empty out the list of words in the current sentence
		if tag == '</s>':
			# If there is at least 1 occurrence of w in this sentence, tally up the words in the sentence
			for wi in w_in_sent:
				wi_sense = wi[1]
				wi_pos = wi[2]
				for coword in words_in_sent:
					if words_in_sent.index(coword) == wi_pos:
						continue	# move on if we're at the word we're analyzing.
					w_dict[wi_sense][coword] += 1	# increment the count of times this co-word appeared in the sentence with this sense of w
					#print ' '.join([w,wi_sense,coword])
			
			#Now reset the list of words to be empty & the w-flag to false, since we'll be starting a new sentence.
			words_in_sent = []
			w_in_sent = []
			
		elif tag == '<wf ':
			# Get the part of the line that follows the lemma tag
			lemma_split = line.split('lemma=')
			if len(lemma_split)<2: 	# if "lemma=" wasn't found in this line, then move on
				line_num = line_num+1
				continue
			lemmaplus = lemma_split[1]
		
			# Isolate the lemma itself
			lemma = lemmaplus.split(' ')[0]
			
			# If the current word is the one we're classifying, record its sense and position in the sentence
			if lemma == w:
				w_position = len(words_in_sent)		# length of words_in_sent is the position in the list w will end up at.
				
				# Isolate the lexsn: this requires splitting twice since the lexsn can be followed by a space + another tag, or a closing '>'
				lexsn = lemmaplus.split('lexsn=')[1].split(' ')[0].split('>')[0]
				
				w_in_sent.append([lemma, lexsn, w_position])	# right now putting lemma in this list is redundant, 
																# but if I re-write this to stop classifying one word at a time, it'll be useful!
				
			# Add the word to the list of current words.
			words_in_sent.append(lemma)
		
		line_num = line_num+1	# Incrememt the counter so we can move on to the next line.
	
	return w_dict
	
## Given a word, a sense, a list of co-words, return the probability of that sense occurring in a sentence with those cowords based on the probabilities in prob_dict
## sense: the sense whose probability we're evaluating
## sense_count: the number of times this sense occurred in the training set
## prob_dict is a dictionary (for this sense) from co-occurring words to probabilities that they'll co-occur in this dictionary
def get_sense_probability(sense, sense_count, prob_dict, cowords):
	sense_prob = sense_count
	
	for word in cowords:
		if word in prob_dict:
			cond_prob = prob_dict[word]
		# If we haven't seen this co-word appear with this sense at all, then just ignore it (multiply by 1 instead of by a real count or probability)
		else: cond_prob = 1
		
		sense_prob = sense_prob * cond_prob
		
	return sense_prob


## Utility: Take a list of lists and print it as a table
def print_table2(table, path):
	rows = ['\t'.join(['cowords','actual sense','predicted sense','correct'])]
	for row in table:
		srow = copy.deepcopy(row)
		for i in range(0,len(srow)):
			if isinstance(srow[i],list):
				srow[i] = ' '.join(srow[i])
			elif isinstance(srow[i],int):
				srow[i] = str(srow[i])
		rows.append('\t'.join(srow))
	text = '\n'.join(rows)
	f = open(path, 'w')
	f.write(text)
	f.close()


## Given a test set and a word w, and a dictionary from senses to co-words to probabilities,
## Return a table in which each row represents an occurrence of w and contains: 
##		* the words in the sentence it's in, 
##		* its actual sense, 
## 		* the sense predicted by the classifier, and whether it was correct.
def run_p4_classifer(prob_dict, ts_num, w):
	test_text = test_texts[ts_num][0]
	snum = 0
	words_in_sent = []
	w_in_sent = []	# a list of the occurrences of w in the sentence, with associated senses and positions
	
	# where we'll store the info we collect
	w_table = []
	
	line_num = 0
	while line_num < len(test_text):
		line = test_text[line_num]
		#print line
		tag = line[0:4]
		
		# if the sentence is over, then do some analysis, then empty out the list of words in the current sentence
		if tag == '</s>':
			# If there is at least 1 occurrence of w in this sentence, tally up the words in the sentence
			for wi in w_in_sent:
				actual_sense = wi[1]
				wi_pos = wi[2]
				words_left = words_in_sent[0:wi_pos]
				words_right = words_in_sent[wi_pos+1:len(words_in_sent)]
				wi_cowords = words_left+words_right
				
				## find the sense with the greatest probability according to the probability dictionary
				winning_score = 0
				winning_sense = ''
				for sense in prob_dict:
					sense_count = p2_counts_by_dev[ts_num][w][sense]
					score = get_sense_probability(sense, sense_count, prob_dict, wi_cowords)
					if score > winning_score:
						winning_score = score
						winning_sense = sense
						
				#print winning_sense
				correct = 0
				if winning_sense == actual_sense:
					correct = 1
				
				# Add a row to the table representing the context and sense for this instance of w
				w_row = [wi_cowords, actual_sense, winning_sense, correct]
				#print w_row
				w_table.append(w_row)
				
			
			#Now reset the list of words to be empty & the w-flag to false, since we'll be starting a new sentence.
			words_in_sent = []
			w_in_sent = []
			
		elif tag == '<wf ':
			# Get the part of the line that follows the lemma tag
			lemma_split = line.split('lemma=')
			if len(lemma_split)<2: 	# if "lemma=" wasn't found in this line, then move on
				line_num = line_num+1
				continue
			lemmaplus = lemma_split[1]
		
			# Isolate the lemma itself
			lemma = lemmaplus.split(' ')[0]	
			
			# If the current word is the one we're classifying, record its sense and position in the sentence
			if lemma == w:
				w_position = len(words_in_sent)		# length of words_in_sent is the position in the list w will end up at.
				
				# Isolate the lexsn: this requires splitting twice since the lexsn can be followed by
				# either a space + another tag, or a closing '>'
				lexsn = lemmaplus.split('lexsn=')[1].split(' ')[0].split('>')[0]
				
				w_in_sent.append([lemma, lexsn, w_position])	# right now putting lemma in this list is redundant, 
																# but if I re-write this to stop classifying one word at a time, it'll be useful!
				
			# Add the word to the list of current words.
			words_in_sent.append(lemma)
		
		line_num = line_num+1	# Increment the counter so we can move on to the next line.
		
	print_table2(w_table, 'p4_tables/'+'_'.join([w,'in','split',str(ts_num+1),'.txt']))
	
	return w_table
			

## Take a dataset and a word to classify in the set.
## Return a dictionary of dictionaries from senses to co-occurring words to probabilities.
## Relies on p2_counts_by_dev and get_p4_counts(ds_num,w).
def p4_probability_table(ds_num, w):
	sense_counts = p2_counts_by_dev[devset_num][w]
	wxcoword_probs = get_p4_counts(ds_num,w)

	for sense in wxcoword_probs:
		sense_count = sense_counts[sense]
		
		# convert the Counters to dictionaries so they can hold non-integers
		wxcoword_probs[sense] = dict(wxcoword_probs[sense])
		prob_dict = wxcoword_probs[sense]
		
		for coword in prob_dict:
			# problem: in one dev/test set, <make 2:29:00::> has 0 appearances in training and then does show up in testing... Solution: round dividing by 0 up to 1.
			
			# Convert the counts to probabilities
			if sense_count > 0:
				prob_dict[coword] = float(prob_dict[coword])/sense_count
				print "probability of sense "+sense+" is: "+str(prob_dict[coword])
			else:
				print ' '.join([str(ds_num+1), w, sense, str(sense_count)]) 
				print sense_counts
				prob_dict[coword] = 1
	
	return wxcoword_probs
	

## Take the dev-set number and word, and for that combination:
## * build the classifer:
## 	  * get the co-occurrence counts (p4_counts)
## 	  * divide them by the relevant sense-counts (use: p2_counts_by_dev[devset_num][word])
## 		p2_counts_by_dev[devset_num][word]: Counter from senses of w to counts in the devset
## * run it on the appropriate test set
## * Return the accuracy for this classifier/word combination 	
def score_p4_classifer(ds_num, w):
	prob_dict = p4_probability_table(ds_num, w)
	classifer_results = run_p4_classifer(prob_dict, ds_num, w)
	accuracy = float(sum(x[3] for x in classifer_results))/len(classifer_results)
	classifer_score = [w,str(ds_num+1),str(len(dev_texts[ds_num][0])),str(accuracy)]	
	return classifer_score		#accuracy to report to classify_and_report_4splits(classifer, problem_num)
	
classify_and_report_4splits(score_p4_classifer, 4)
