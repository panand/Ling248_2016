#Homework 2

###Due Feb. 11, 2016 (in class)

##Some notes

* Please do this in whatever language you desire. I don't really care.
* Let me know if you have any issues by Tuesday.

##Initial exercises

This is to get used to the format of SemCor. Please unzip and untar semcor3.0.tar.gz. You are encouraged to poke around, but the important files are in the brown.* directories under tagfiles. Look at 1 or 2 of the files in there. As you can see, they are XML, with the following structure:

contextfile -> context -> para -> s -> wf/punc

So the files are broken up into paragraphs and sentences, which is potentially very convenient.

The important entries are the <wf> tags. Here, the important information is in the xml attributes. The important ones are pos (part of speech), lemma (think morpheme), wnsn (the ordinal sense number in wordnet), lexsn (the wordnet-wide unique id for the synset).

I should note that in doing SemCor, the Wordnet team encountered words with novel senses. These are all marked with lexsns of the form 5:00:**. In addition, some of them show mappings to the senses of other wordnet words. In the WSD tasks below, I'd like us to exclude them. But for Problem 1, I've included them.

Problem 0. Looking in the brown2 directory, please construct a sorted (most to least) list of joint counts for lemmas and their lexsns. Your file should match words-and-senses.list in this directory.

##Main task

Problem 1. In what follows, please conduct all your experiments on ALL of the data. The simplest way to do this is to put all the tag files in one (new) common directory. There should be 352 of these files. Please divide your data into 4 different test-dev splits, where the test part of each split is as below: 

* brown1/br-a* - br-d* (this should be 16 files)
* brown1/br-a* - br-h* (this should be 30 files)
* brown1/br-a* - br-j* (this should be 63 files)
* brown1/* (this should be 103 files)

Note that these aren't random splits. That's fine for now. There are virtues and disadvantages for this decision we can talk about when we discuss results.

It's good to make these splits into separate directories so you can preserve your full experimental state. I'd advocate for each of these constructing the subdirectories test and train, and putting the relevant files in them.

Problem 2. Now, let's do a bit of additional housekeeping. We will be examining the following three words: do, make, work. For eachof these, compute the joint counts for each of the senses one encounters throughout the training split. This is probably best stores as a two-dimensional hash.
 
Problem 3. Now, let's write our first classifier. For this, assume that we always choose the most common sense for a given word, given the hash you constructed above. For each of the three words above, compute the accuracy of this classifier on the relevant test splits. Make a table of the word, the number of train files, and the accuracy of the classifier.

Problem 4. We will now implement the Naive Bayes bag of word classifier. To do this, we must compute both P(s_i) and P(w_j|s_i) as discussed today. We will assume we are ONLY looking at senses for the word in question (so only cases with do, make, and work). Let us assume that our window is the sentence: We will be looking at all of the words within the sentence containing the relevant word. You can store these scores in a 2D hash for each word (so, for "do", you will have a dictionary from senses of do to words to probabilities. As in Problem 3, run this across the 4 train-test splits and produce a table of your results.

You will here encounter a few problems. The first is that your probabilities may end up infinitesimal. I don't think this will happen if we are looking at sentences, but if it does, use the old trick I mentioned in class: store the log of the various probabilities and add them together. You'll still be looking for the argmax.

Another, more serious, problem is that you may end up with zero counts here. That is, you may find a word that you haven't seen yet, in which case you have no idea how it relates to your sense counts. This is the problem of smoothing: of trying to relate our counts to the actual distribution we are sampling from. For now, ignore any word with a zero count value. This is a terrible thing to do, but absent a theory of smoothing, this is best we'll manage.

If you want, you can implement add-1 smoothing as discussed in Chapter 6. 
