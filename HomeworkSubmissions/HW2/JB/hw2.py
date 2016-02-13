import os, collections

semcor_dir = '../Ling248_2016-master/Data/semcor3.0/'

## Problem 0. Looking in the brown2 directory, please construct a sorted (most to least) list of joint counts for lemmas and their lexsns. Your file should match words-and-senses.list in this directory.

## Function that takes a list of lines (from an xml file) and builds a counter of each lemma/sense combination in it.
def lines_to_lxs_counter(lines):
	#print "running lines_to_lxs_counter"
	c = collections.Counter()
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
	lxs = collections.Counter()
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
	cw = collections.Counter()
	for e in c:
		lemma = e.split(' ')[0]
		# if the lemma is the one we're interested in, then add this entry to our word-specific counter
		if lemma == w:
			cw[e] += c[e]
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


## Classifer that simply selects the most common sense for each word, regardless of context etc. (Problem 3's classifer)
def p3_classifer(ds_num, w):
	w_counter = p2_counts_by_dev[ds_num][w]				# Get the counter of senses for word w in dev. set ds_num
	most_common_entry = w_counter.most_common(1)[0]		# Counter.most_common(n) returns a list of length n (here, 1). 
	most_common_key = most_common_entry[0]				# An entry is a (key, value) tuple
	p3_sense = most_common_key.split(' ')[1]			# Keys have the form 'lemma sense' and we want just the sense.
	return [p3_sense for i in range(0,sum(w_counter.values()))]

## take a classifer function and apply it within each dev/test split for the words [do,make,work], and compile and print a table of its performance in that test set.
## The classifer takes the dev. set number and the word, and returns a list of modeled senses, one for each instance of that word, in the order in which they appear in the dev. set.
def classify_and_report_4splits(classifer, problem_num):
	acc_table = [['word','devset','num. train files','p3 accuracy']]
	for dt in dev_texts:
		ds_num = dev_texts.index(dt)
		num_dev_files = dt[1]
		for w in words:
			model = classifer(ds_num, w) 		
			# Make a table of all the occurrences of the word of interest in the test set of interest
			w_table = make_lxs_table(w, test_texts[ds_num][0])
			for row in w_table:
				actual_sense = row[1]
				modeled_sense = model[w_table.index(row)]
				classified_correctly = 0
				if actual_sense == modeled_sense:
					classified_correctly = 1
				row.extend([modeled_sense, classified_correctly])
				#print row
			num_rows = len(w_table)
			num_correct = sum(x[3] for x in w_table)
			accuracy = 1.0*num_correct/num_rows
			acc_table.append([w,str(ds_num+1),str(len(dt[0])),str(accuracy)])
		
	print_table(acc_table, 'problem'+str(problem_num)+'_accuracy.txt')
	
classify_and_report_4splits(p3_classifer, 3)
		

#################################################################################
## Problem 4. We will now implement the Naive Bayes bag of words classifier. To do this, we must compute both P(s_i) and P(w_j|s_i) as discussed today. We will assume we are ONLY looking at senses for the word in question (so only cases with do, make, and work). Let us assume that our window is the sentence: We will be looking at all of the words within the sentence containing the relevant word. You can store these scores in a 2D hash for each word (so, for "do", you will have a dictionary from senses of do to words to probabilities. As in Problem 3, run this across the 4 train-test splits and produce a table of your results.

def p4_classifer(ds_num, w):
	dev_text = dev_texts[ds_num][0]
	i = 0
	snum = 0
	words_in_sent = []
	
	while i<len(dev_text):
		line = dev_text[i]
		# if the sentence is over, then do some analysis, then empty out the list of words in the current sentence
		if '</s>' in line:
			#TODO do analysis here
			words_in_sent = []
		elif '<wf ' in line:
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
			
			#add the word to the list of current words
			
			#TODO


