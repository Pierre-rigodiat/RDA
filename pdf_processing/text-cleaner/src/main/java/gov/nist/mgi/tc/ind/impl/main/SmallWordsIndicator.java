package gov.nist.mgi.tc.ind.impl.main;

import gov.nist.mgi.tc.ind.models.StatsIndicator;
import gov.nist.mgi.tc.tools.TextStatistics;

/**
 * Indicator computing the length of each word in a sentence.
 * If the average word length is too small it 
 * 
 * @author P. Dessauw
 */
public class SmallWordsIndicator extends StatsIndicator {	
	private static double LINE_LENGTH_LIMIT = 0.3;
	private static double SMALL_SIZE_WORD_LIMIT = 0.7;
	
	public SmallWordsIndicator(TextStatistics textStats) {
		super(textStats);
	}

	public boolean match(String line) {
		String[] wordList = this.stats.getLineWords(line);
		int lowCharNumberWord = 0;
		
		// State which words are small words
		for(String word:wordList)
		{
			if(word.length() < this.stats.getAvgWordSize())
				lowCharNumberWord += 1;
		}
		
		return line.length() < this.stats.getAvgLineLength() * LINE_LENGTH_LIMIT && lowCharNumberWord > wordList.length * SMALL_SIZE_WORD_LIMIT;
	}

}
