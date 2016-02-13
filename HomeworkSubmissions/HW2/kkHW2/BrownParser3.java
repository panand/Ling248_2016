//BrownParser3.java
//For problem 4: 
// TRY to get the Naive Bayes bag of words classifier to work


package naiveBayes;

import java.io.*;
import java.util.*;

	
public class BrownParser3 {
	
	public static void main(String[] args) throws IOException {
		File trainDirectory = new File("Test1/training");				//change here for different splits
		File testDirectory = new File("Test1/testing");		
		File[] corpusFiles = trainDirectory.listFiles();			
		File[] testFiles = testDirectory.listFiles();					 

		ArrayList<ArrayList<String>> allSentences = new ArrayList<ArrayList<String>>();		
		ArrayList<ArrayList<String>> trainingSentences = new ArrayList<ArrayList<String>>();
		ArrayList<ArrayList<String>> testSentences = new ArrayList<ArrayList<String>>();
		
		for(File f : corpusFiles) {
			trainingSentences = goLineByLine(f, trainingSentences);				//here's the training sentences
		}
		for(File g : testFiles) {
			testSentences = goLineByLine(g, testSentences);						//here's the test sentences
		}
			
		allSentences.addAll(testSentences);										//put train+test into allSentences
		allSentences.addAll(trainingSentences);
		
		System.out.println("Read all sentences.");
		
		//The Bayesian model logic:
		//prob(sense_j|words)  --is proportional to--  prob(sense_j)*PI_i(prob(word_i|sense_j))
		//prob(sense_j) = count(sense_j)/count(all senses) = count(sense_j)/count(all words)
		//prob(word_i|sense_j) = count(word_i in sentences containing sense_j)/count(all words in sentences containing sense_j)
		//So if we're interested in prob(sense_j|words), we need to find the total word count in all sentences,
		//the count of every instance of sense_j, the count of all words in sentences containing sense_j,
		//and the individual counts of each word_i in sentences containing sense_j.
		//To calculate count(all words) and count(all words in sentences containing sense_j) we can use the method countAll;
		//to calculate count(sense_j) we can use countifLexsn; and to calculate count(word_i in sentences containing sense_j)
		//we can use countIfLemma.  For count(all words) and count(sense_j), we feed in the set of all sentences; and for
		//count(all words in sentences containing sense_j) and count(word_i in sentences containing sense_j) we feed in only
		//those sentences containing sense_j.
		
		ArrayList<ArrayList<String>> trainingSentencesWithDo = getSentencesWithLemma("do", trainingSentences);
		ArrayList<String> lexsnsOfDo = getLexsnFromLemma("do", trainingSentencesWithDo);
		int totalLexsnCount = countAll(trainingSentences);									//count(all senses)
		int[] lexsnsOfDoCount = new int[lexsnsOfDo.size()];									//count(sense_j)
		for(int i = 0; i < lexsnsOfDoCount.length; i++)										//put into arraylist
			lexsnsOfDoCount[i] = countIfLexsn(lexsnsOfDo.get(i), trainingSentences);
		
		//Make a Hashmap from lexsns of do to their probability among all lexsns
		HashMap<String, Double> lexsnsOfDoProb = new HashMap<String, Double>();				//***prob(sense_j)***
		for(int i = 0; i < lexsnsOfDoCount.length; i++){
			double prob = Double.valueOf(((double) lexsnsOfDoCount[i] / (double) totalLexsnCount));
			lexsnsOfDoProb.put(lexsnsOfDo.get(i), prob);
		}	
		System.out.println("Figured out prob(lexsn) for all lexsns of do.");
		System.out.println(lexsnsOfDoProb.keySet().toString());
		
		//Make a Hashmap from lexsns of do to the count of all words in sentences containing those lexsns
		HashMap<String, Integer> sentencesWithLexsnsOfDoCount
			= new HashMap<String, Integer>();												//count(all words in sentences containing sense_j)
		for(int i = 0; i < lexsnsOfDoCount.length; i++)
			sentencesWithLexsnsOfDoCount.put(lexsnsOfDo.get(i), 
					Integer.valueOf(countAll(getSentencesWithLexsn(lexsnsOfDo.get(i), trainingSentences))));
		System.out.println("Made Hashmap with all do-lexsn-sentence word counts.");
		
		//Make a Hashmap from lexsns of do to Hashmaps from words in sentences containing those lexsns to their counts in those sentences
		HashMap<String, HashMap<String, Integer>> lemmasInSentencesWithLexsnsOfDoCount
			= getLemmaCountsFromLexsns(lexsnsOfDo, trainingSentences);						//count(word_i in sentences containing sense_j)
		System.out.println("Made count hashmap for lemmas in do-lexsn-sentences.");
		
		//Make a Hashmap from lexsns of do to Hashmaps from words in sentences containing those lexsns to their probabilities in those sentences
		HashMap<String, HashMap<String, Double>> lemmasInSentencesWithLexsnsOfDoProb
			= getLemmaProbsFromLexsns(sentencesWithLexsnsOfDoCount, lemmasInSentencesWithLexsnsOfDoCount);		//***prob(word_i|sense_j)***
		System.out.println("Figured out conditional probabilities of lemmas in do-lexsn-sentences.");
		
		BufferedWriter outFile = new BufferedWriter(new FileWriter(new File("doClassifierOutput.txt")));
		ArrayList<ArrayList<String>> testSentencesWithDo = getSentencesWithLemma("do", trainingSentences);
		for(ArrayList<String> sentence : testSentencesWithDo) {
			ArrayList<String> testWords = getLemmas(sentence);
			String result = classifier(testWords, lexsnsOfDoProb, lemmasInSentencesWithLexsnsOfDoProb);
			outFile.write(testWords.toString() + "\t" + getLexsnFromLemmaInSentence("do", sentence).toString() + "\t" + result + "\n");
		}
		outFile.close();
		System.out.println("Got results.");
	}

	//=======================//
	//	   	METHODS			 //
	//=======================//
	
	// Parse the document into a list of sentences each containing a list of unparsed XML word lines
	public static ArrayList<ArrayList<String>> goLineByLine(File doc, ArrayList<ArrayList<String>> sentences) throws IOException {
		BufferedReader br = new BufferedReader(new FileReader(doc));
		String nextLine = br.readLine();
		while(nextLine != null) {
			if(nextLine.startsWith("<s"))
				sentences.add(new ArrayList<String>());
			if(nextLine.matches("<wf.*lemma=.*"))
				sentences.get(sentences.size() - 1).add(nextLine);			
			nextLine = br.readLine();
		}		
		br.close();
		return sentences;
	}
	
	//Given a list of sentences, return those sentences containing the supplied lemma
	public static ArrayList<ArrayList<String>> getSentencesWithLemma(String lemma, ArrayList<ArrayList<String>> sentences) {
		ArrayList<ArrayList<String>> containLemma = new ArrayList<ArrayList<String>>();
		for(ArrayList<String> s : sentences) {
			boolean hasLemma = false;
			for(String w : s) {
				if(w.matches(".*lemma="+lemma+" .*")) {
					hasLemma = true;
					break;
				}
			}
			if(hasLemma)
				containLemma.add(s);
		}
		return containLemma;
	}

	//Given a list of sentences, return those sentences containing the supplied lexsn
	public static ArrayList<ArrayList<String>> getSentencesWithLexsn(String lexsn, ArrayList<ArrayList<String>> sentences) {
		ArrayList<ArrayList<String>> containLexsn = new ArrayList<ArrayList<String>>();
		for(ArrayList<String> s : sentences) {
			boolean hasLexsn = false;
			for(String w : s) {
				if(w.matches(".*lexsn="+lexsn+"[ >].*")) {
					hasLexsn = true;
					break;
				}
			}
			if(hasLexsn)
				containLexsn.add(s);
		}
		return containLexsn;
	}

	//Given a sentence, return the set of lexsns corresponding to the supplied lemma
	public static ArrayList<String> getLexsnFromLemmaInSentence(String lemma, ArrayList<String> sentence) {
		ArrayList<String> lexsns = new ArrayList<String>();
		HashMap<String, String> lexsnAggregator = new HashMap<String, String>();
		for(String w : sentence) {
			if(w.matches(".*lemma="+lemma+" .*")) {
				String lexsn = w.split("lexsn=")[1].split("[ >]")[0];
				String value = lexsnAggregator.put(lexsn, lexsn);
				if(value == null)
					lexsns.add(lexsn);
			}
		}
		return lexsns;
	}

	//Given a list of sentences, return the set of lexsns corresponding to the supplied lemma
	public static ArrayList<String> getLexsnFromLemma(String lemma, ArrayList<ArrayList<String>> sentences) {
		ArrayList<String> lexsns = new ArrayList<String>();
		HashMap<String, String> lexsnAggregator = new HashMap<String, String>();
		for(ArrayList<String> s : sentences) {
			for(String w : s) {
				if(w.matches(".*lemma="+lemma+" .*")) {
					String lexsn = w.split("lexsn=")[1].split("[ >]")[0];
					String value = lexsnAggregator.put(lexsn, lexsn);
					if(value == null)
						lexsns.add(lexsn);
				}
			}
		}
		return lexsns;
	}

	//Given a sentence (ie, a list of unparsed XML word lines), return the list of lemmas it contains
	public static ArrayList<String> getLemmas(ArrayList<String> sentence) {
		ArrayList<String> lemmaList = new ArrayList<String>();
		for(String w : sentence) {
			String lemma = w.split("lemma=")[1].split("[ >]")[0];
			lemmaList.add(lemma);
		}
		return lemmaList;
	}

	//Given a list of sentences, return the total word count
	public static int countAll(ArrayList<ArrayList<String>> sentences) {
		int count = 0;
		for(ArrayList<String> s : sentences)
			count += s.size();
		return count;
	}
	
	//Given a list of sentences, return the word count of the supplied lemma
	public static int countIfLemma(String lemma, ArrayList<ArrayList<String>> sentences) {
		int count = 0;
		for(ArrayList<String> s : sentences)
			for(String w : s)
				if(w.matches(".*lemma="+lemma+" .*"))
					count++;
		return count;
	}
	
	//Given a set of sentences, return the word count of the supplied lexsn
	public static int countIfLexsn(String lexsn, ArrayList<ArrayList<String>> sentences) {
		int count = 0;
		for(ArrayList<String> s : sentences)
			for(String w : s)
				if(w.matches(".*lexsn="+lexsn+"[ >].*"))
					count++;
		return count;
	}
	
	//Given a set of lexsns and a list of sentences, return a map from lexsns to maps from lemmas to their counts in sentences containing the lexsns
	public static HashMap<String, HashMap<String, Integer>> getLemmaCountsFromLexsns(ArrayList<String> lexsns, ArrayList<ArrayList<String>> sentences) {
		HashMap<String, HashMap<String, Integer>> lemmaCountsFromLexsns = new HashMap<String, HashMap<String, Integer>>();
		for(String lexsn : lexsns) {
			HashMap<String, Integer> lemmaCountsFromLexsn = new HashMap<String, Integer>();
			ArrayList<ArrayList<String>> sentencesWithLexsn = getSentencesWithLexsn(lexsn, sentences);
			for(ArrayList<String> sentenceWithLexsn : sentencesWithLexsn) {
				ArrayList<String> lemmas = getLemmas(sentenceWithLexsn);
				for(String lemma : lemmas) {
					if(lemmaCountsFromLexsn.get(lemma) == null) {
						lemmaCountsFromLexsn.put(lemma, Integer.valueOf(1));
					} else {
						int count = lemmaCountsFromLexsn.get(lemma).intValue();
						lemmaCountsFromLexsn.put(lemma, Integer.valueOf(count++));
					}
				}
			}
			lemmaCountsFromLexsns.put(lexsn, lemmaCountsFromLexsn);
		}
		return lemmaCountsFromLexsns;
	}
	
	//Given a set of lexsn counts and a map from lexsns to maps from lemmas to their counts in sentences containing the lexsns,
	//return a map from lexsns to maps from lemmas to their (conditional) probabilities of appearing in sentences containing the lexsns
	public static HashMap<String, HashMap<String, Double>> getLemmaProbsFromLexsns(HashMap<String, Integer> lexsnCounts, HashMap<String, HashMap<String, Integer>> lemmaCountsFromLexsnSentences) {
		HashMap<String, HashMap<String, Double>> lemmaProbsFromLexsns = new HashMap<String, HashMap<String, Double>>();
		for(String lexsn : lexsnCounts.keySet()) {
			HashMap<String, Double> lemmaProbsFromLexsn = new HashMap<String, Double>();
			for(String lemma : lemmaCountsFromLexsnSentences.get(lexsn).keySet()) {
				lemmaProbsFromLexsn.put(lemma, 
						Double.valueOf(lemmaCountsFromLexsnSentences.get(lexsn).get(lemma).doubleValue() / lexsnCounts.get(lexsn).doubleValue()));
			}
			lemmaProbsFromLexsns.put(lexsn, lemmaProbsFromLexsn);
		}
		return lemmaProbsFromLexsns;
	}
	
	public static String classifier(ArrayList<String> testWords, HashMap<String, Double> lexsnsProb, HashMap<String, HashMap<String, Double>> lemmasInSentencesWithLexsnsProb) {
		String guess = "x";
		double maxLexsnProb = 0;
		for(String lexsn : lexsnsProb.keySet()) {
			double currentLexsnProb = lexsnsProb.get(lexsn).doubleValue();
			HashMap<String, Double> wordsProb = lemmasInSentencesWithLexsnsProb.get(lexsn);
			for(String testWord : testWords) {
				if(wordsProb.get(testWord) != null) {
					currentLexsnProb *= wordsProb.get(testWord).doubleValue();
				}
			}
			if(currentLexsnProb > maxLexsnProb) {
				maxLexsnProb = currentLexsnProb;
				guess = lexsn;
			}
		}
		return guess;
	}

}
