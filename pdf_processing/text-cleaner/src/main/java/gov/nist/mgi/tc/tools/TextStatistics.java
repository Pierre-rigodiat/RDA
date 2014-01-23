package gov.nist.mgi.tc.tools;

import gov.nist.mgi.tc.tools.StringTools.CharType;

import java.io.File;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import opennlp.tools.tokenize.Tokenizer;
import opennlp.tools.tokenize.TokenizerME;
import opennlp.tools.tokenize.TokenizerModel;
import opennlp.tools.util.InvalidFormatException;

/**
 * Class computing statistics about lines of text
 * 
 * @author Philippe Dessauw
 * 
 */
public class TextStatistics {
	private static Logger tsLogger = LogManager.getLogger(TextStatistics.class);

	private static String LOWER_REGEX = "[a-z]";
	private static String LOWER_REPL = "a";

	private static String UPPER_REGEX = "[A-Z]";
	private static String UPPER_REPL = "A";

	private static String NUMBER_REGEX = "[0-9]";
	private static String NUMBER_REPL = "0";

	private static String SP_CHAR_REGEX = "[^a-zA-Z0-9]";
	private static String SP_CHAR_REPL = "#";

	private Tokenizer tknizer;

	/**
	 * Text statistics
	 */
	private double avgLineLength;
	private double avgWordPerLine;
	private double avgWordSize;
	private double totalWordLength;
	private double totalLength;
	private double totalWordNb;
	private double lineNb;
	private Map<String, Map<CharType, Double>> linesStats;

	/**
	 * Constructor
	 * 
	 * @throws IOException
	 * @throws InvalidFormatException
	 * 
	 */
	public TextStatistics() throws InvalidFormatException, IOException {
		tsLogger.entry();

		// Init stats
		this.avgLineLength = 0;
		this.avgWordPerLine = 0;
		this.avgWordSize = 0;
		this.totalLength = 0;
		this.totalWordLength = 0;
		this.totalWordNb = 0;
		this.lineNb = 0;

		this.linesStats = new HashMap<String, Map<CharType, Double>>();

		String modelPath = getClass().getResource("en-token.bin").getPath();

		// Init tokenizer (better word detections than a simple space count)
		tsLogger.debug("Loading \"" + modelPath + "\"...");
		TokenizerModel tknModel = new TokenizerModel(new File(modelPath));
		this.tknizer = new TokenizerME(tknModel);

		tsLogger.exit();
	}

	/**
	 * Register a line in the list and compute its statistics.
	 * 
	 * @param line
	 * @throws IOException
	 * @throws InvalidFormatException
	 */
	public void computeLine(String line) throws InvalidFormatException,
			IOException {
		// Computing word number
		String[] wordList = this.tknizer.tokenize(line);
		double wordNb = this.getTotalWordNb();

		// Setting total word number
		this.setTotalWordNb(wordNb + wordList.length);

		// Computing number of different character
		Map<CharType, Double> charNumbers = new HashMap<CharType, Double>();

		String markedWord;
		double lowerNb = 0;
		double upperNb = 0;
		double numberNb = 0;
		double spCharNb = 0;
		double lineWordLength = 0;

		for (String word : wordList) {
			markedWord = word.replaceAll(LOWER_REGEX, LOWER_REPL);
			markedWord = markedWord.replaceAll(UPPER_REGEX, UPPER_REPL);
			markedWord = markedWord.replaceAll(NUMBER_REGEX, NUMBER_REPL);
			markedWord = markedWord.replaceAll(SP_CHAR_REGEX, SP_CHAR_REPL);

			lowerNb += StringTools.count(markedWord, LOWER_REPL);
			upperNb += StringTools.count(markedWord, UPPER_REPL);
			numberNb += StringTools.count(markedWord, NUMBER_REPL);
			spCharNb += StringTools.count(markedWord, SP_CHAR_REPL);

			lineWordLength += word.length();
		}

		charNumbers.put(CharType.LOWER, lowerNb);
		charNumbers.put(CharType.UPPER, upperNb);
		charNumbers.put(CharType.NUMBER, numberNb);
		charNumbers.put(CharType.SPECIAL, spCharNb);

		this.linesStats.put(line, charNumbers);

		// Computing line number
		this.setLineNb(this.getLineNb() + 1);

		// Computing total length
		this.setTotalLength(this.getTotalLength() + line.length());

		// Computing average word number
		this.setAvgWordPerLine(this.getTotalWordNb() / this.getLineNb());

		// Computing average word size
		this.setTotalWordLength(this.getTotalWordLength() + lineWordLength);

		this.setAvgWordSize(this.getTotalWordLength() / this.getTotalWordNb());

		// Computing average line length
		this.setAvgLineLength(this.getTotalLength() / this.getLineNb());

		tsLogger.trace("\"" + line + "\" computed");
	}

	/**
	 * Remove a line and its stats from the list
	 * 
	 * @param line
	 */
	public void removeLineStats(String line) {
		if (this.linesStats.containsKey(line)) // Existence test
		{
			// Compute new statistics for the text
			this.setLineNb(this.lineNb - 1);
			this.setTotalLength(this.totalLength - line.length());

			if (lineNb != 0)
				this.setAvgLineLength(this.totalLength / this.lineNb);
			else
				this.setAvgLineLength(0);

			String[] wordList = this.tknizer.tokenize(line);
			this.setTotalWordNb(this.totalWordNb - wordList.length);

			for (String word : wordList) {
				this.setTotalWordLength(this.getTotalWordLength()
						- word.length());
			}

			if (lineNb != 0) {
				this.setAvgWordPerLine(this.totalWordNb / this.lineNb);
				this.setAvgWordSize(this.getTotalWordLength()
						/ this.getTotalWordNb());
			} else {
				this.setAvgWordPerLine(0);
				this.setAvgWordSize(0);
			}

			// Remove the line from the list
			this.linesStats.remove(line);
		}
	}

	/**
	 * Use the tokenizer to get the word list
	 * 
	 * @param line
	 * @return word list
	 */
	public String[] getLineWords(String line) {
		// FIXME the tokenizer is used several times it consume a lot of
		// processing time.
		// TODO Find a way to store words in the datastructure
		return this.tknizer.tokenize(line);
	}

	private double getTotalLength() {
		return totalLength;
	}

	private void setTotalLength(double totalLength) {
		this.totalLength = totalLength;
	}

	private double getTotalWordNb() {
		return totalWordNb;
	}

	private void setTotalWordNb(double totalWordNb) {
		this.totalWordNb = totalWordNb;
	}

	private double getLineNb() {
		return lineNb;
	}

	private void setLineNb(double lineNb) {
		this.lineNb = lineNb;
	}

	public double getAvgLineLength() {
		return avgLineLength;
	}

	public void setAvgLineLength(double avgLineLength) {
		this.avgLineLength = avgLineLength;
	}

	public double getAvgWordPerLine() {
		return avgWordPerLine;
	}

	public void setAvgWordPerLine(double avgWordPerLine) {
		this.avgWordPerLine = avgWordPerLine;
	}

	private void setTotalWordLength(double totalWordLength) {
		this.totalWordLength = totalWordLength;
	}

	private double getTotalWordLength() {
		return this.totalWordLength;
	}

	public void setAvgWordSize(double avgWordSize) {
		this.avgWordSize = avgWordSize;
	}

	public double getAvgWordSize() {
		return this.avgWordSize;
	}

	public Map<CharType, Double> getStatsForLine(String line) {
		return this.linesStats.get(line);
	}

	/**
	 * A string representing the object
	 */
	public String toString() {
		String statsString = "+------ STATS ------+\n";

		statsString += "| lines = " + (int) this.getLineNb() + "\n";
		statsString += "| avg. line length = " + this.getAvgLineLength() + "\n";
		statsString += "| avg. word number = " + this.getAvgWordPerLine()
				+ "\n";
		statsString += "| avg. word size = " + this.getAvgWordSize() + "\n";
		// statsString += "| lines stats = "+this.linesStats+"\n";

		statsString += "+------ ----- ------+";

		return statsString;
	}
}
