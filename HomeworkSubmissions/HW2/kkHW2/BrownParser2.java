//BrownParser2.java
//parses Brown corpus files
//implements jtidy-r938.jar to clean up and parse xml tagged files (need to install)
//	-->Problem 2: get joint counts for make, do work for the four test splits
//

package naiveBayes;
import java.io.*;

import javax.xml.parsers.ParserConfigurationException;

import java.util.*;

import org.w3c.tidy.*;
import org.w3c.dom.Document;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;


public class BrownParser2 {

	/* Uses the brown2 directory to construct a sorted list of joint counts for lemmas and
	their lexsn values. */

	public static void main(String[] args) throws ParserConfigurationException, SAXException, IOException {
			
		File currentDirectory = new File("Test1/testing/");			// CHANGE FOR different test/train splits	 
		File[] corpusFiles = getDirContents(currentDirectory);
		ArrayList<LemmaLexsnPair> pairs = new ArrayList<LemmaLexsnPair>();
		for(File file : corpusFiles){
			pairs = parseXML(file, pairs);
		}
		
		HashMap<String, HashMap<String, LemmaLexsnPair>> outerMap = new HashMap<String, HashMap<String, LemmaLexsnPair>>();
		Iterator<LemmaLexsnPair> iter = pairs.iterator();
		
		for(int i = 0; i < pairs.size(); i++) {
			LemmaLexsnPair pair = pairs.get(i);
			HashMap<String, LemmaLexsnPair> embeddedMap; 
			if(outerMap.containsKey(pair.lemma)){						// if there's a lemma
				embeddedMap = outerMap.get(pair.lemma);					// check to see if there's a sense
				if(embeddedMap.containsKey(pair.lexsn)) {				// if there is a sense,
					embeddedMap.get(pair.lexsn).increment();			// increment the count of that sense
					pairs.remove(pair);
					i--;
				} else {												// if there isn't a sense	
					embeddedMap.put(pair.lexsn, pair);					// add it
				}
			} else {													
				embeddedMap = new HashMap<String, LemmaLexsnPair>();	// if there isn't already an entry
				embeddedMap.put(pair.lexsn, pair);						// make a sense entry and lemma/sense object
				outerMap.put(pair.lemma, embeddedMap);					// then put it in the hashmap
			}
		}
		LemmaLexsnPair.countabetize();
		Collections.sort(pairs);										
		LemmaLexsnPair.alphabetize();
		Collections.sort(pairs);
		printList(pairs, new File("Test1/TEST-make-do-work-counts.list"));		//CHANGE SAVE DIRECTORY HERE 		
	}
		
		
	//=======================//
	//   	Class stuff   	 //
	//=======================//	

	//creates an object containing lemma + lexsn, as well as count for that object,
	//also a method for incrementing the count

	static class LemmaLexsnPair implements Comparable<LemmaLexsnPair> {
	
		static int totalCount = 0;
		static boolean comparecountz = true;
		
		int count;
		String lemma;
		String lexsn;
		String pos;
		
		LemmaLexsnPair(String lemma2, String lexsn2){
			count = 1;
			lemma = lemma2;
			lexsn = lexsn2;
			totalCount++;
		}
		
		static void alphabetize(){
			comparecountz = false;
		}
		
		static void countabetize(){
			comparecountz = true;
		}
		
		void increment() {
			count++;
		}
		
		
		public int compareTo(LemmaLexsnPair otherpair) {
			if(comparecountz){
				if(count > otherpair.count)
					return 1;
				if (count == otherpair.count) 
					return 0;
				return -1;
			} else {
				return lemma.compareTo(otherpair.lemma);
			}
		}
	}
	
	


	//=======================//
	//	   	METHODS			 //
	//=======================//

		//parses the XML files
		//have to include some bullshit so that attribute values are easily extracted (need quotes)
		//this includes having the right classpath to a .jar file   
	
		public static ArrayList<LemmaLexsnPair> parseXML(File doc, ArrayList<LemmaLexsnPair> theArray) throws ParserConfigurationException, SAXException, IOException {
			
			Tidy t = new Tidy();										//cleans up the shitty xml
			t.setXmlTags(true);
			t.setShowErrors(0);
			t.setShowWarnings(false);
			Document parsed = t.parseDOM(new FileReader(doc), new FileWriter(new File("new.xml")));
			NodeList nodeList = parsed.getElementsByTagName("wf");
	        int size = nodeList.getLength();
	        for(int i = 0; i < size; i++) {
	        	if(nodeList.item(i).getAttributes().getNamedItem("lemma") != null &&
	        			nodeList.item(i).getAttributes().getNamedItem("lexsn") != null) {
	        		 String lemma = nodeList.item(i).getAttributes().getNamedItem("lemma").getNodeValue();
	        		 String lexsn = nodeList.item(i).getAttributes().getNamedItem("lexsn").getNodeValue();
	        		 if(lemma.equals("do") || lemma.equals("make") || lemma.equals("work")){
	        			LemmaLexsnPair thePair = new LemmaLexsnPair(lemma, lexsn);
	        		 	theArray.add(thePair);
	        		 }
	        	}
	        }
			return theArray;
		}
	
		public static File[] getDirContents(File directory) {
			File[] files = directory.listFiles();
			for (File file : files) {
				if (file.isDirectory()) {
					System.out.println("directory: " + file.getPath());
					getDirContents(file);
				} else {
					System.out.println("	file: " + file.getPath());	

				}
			}
			return files;
		}

		// prints the output to a file.
		public static void printList(ArrayList<LemmaLexsnPair> theList, File outFile) throws IOException {
			BufferedWriter buffer = new BufferedWriter(new FileWriter(outFile));
			for(int i = theList.size() - 1; i >= 0; i--){
				LemmaLexsnPair pair = theList.get(i);
				buffer.write(pair.count + "\t" + pair.lemma + "\t" + pair.lexsn + "\n");
			}
			buffer.close();
		}
		
		
}
