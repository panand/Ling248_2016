#Homework 1

Due: Tue, Jan. 26 (in class)

To do this: Please run your programs and bring your outputs to class for discussion. We'll talk through what you found. If you can summarize the issues you had/collocations you found, that will help.

## Basic comments

In this homework you will be asked to do some simple counting for the purposes of probability computations and collocations. We will use Huckleberry Finn, which is quite an odd text (it's also small, so be forewarned).

You can find the materials under Data in github. Note that the pos file has tokens of the form token[underscore]pos. In doing the below exercises, you can treat this as one token (i.e., keep the part of speech information to help disambiguate). It would be useful to familiarize yourself with the Penn Treebank tags (google it!).

## Computing basic probabilities

Problem 1. In this problem, we will do something like what we did with COCA. Find the top 5 verbs in Huckleberry Finn. Since I didn't give you lemmas, we are talking inflected verbs. Now, construct the nominal vocabulary: the set of all possible noun (_NN*) types immediately to the right of any of the 5 verbs above. Please construct a count table that shows the count of each possible (verb noun) bigram. Because of the number of nouns, I suggest a table where the rows are the nouns and the columns are the verbs.

Problem 2. Now construct the joint distribution table for the count table above.

Problem 3. Finally, construct a table showing the conditional probability of the nouns given a verb (i.e., P(V N| V=verb)). 

## Computing collocations

Problem 4. Simulate the Justeson & Katz collocation method: Compute the overall bigram counts and sort by number of bigrams. Find various patterns to exclude uninteresting bigrams. What patterns did you use?

Problem 5. Do the above exercise for skip bigrams in windows of size 2, 3, 4, 5, and 10. Assume here that "w1 ... w2" and "w2 ... w1" are distinct skip bigrams. Comment on what happens? 

Problem 6. For windows of size 2, 5 and 10, now assume the bigrams are directionless by sorting the words in the bigram: For example, "see ... vine" and "vine ... see" both reduce to the skip bigram "see vine".

Problem 7. Now implement the Smadja's standard deviation method and construct a table like Table 5.5, sorted by standard deviation. Did you find anything that the previous two problems didn't give you?