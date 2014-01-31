package gov.nist.mgi.tc.spcheck;

import gov.nist.mgi.tc.tools.StringTools;

import java.io.IOException;
import java.util.List;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.languagetool.JLanguageTool;
import org.languagetool.Language;
import org.languagetool.MultiThreadedJLanguageTool;
import org.languagetool.language.AmericanEnglish;
import org.languagetool.rules.Rule;
import org.languagetool.rules.RuleMatch;

/**
 * Class to perform a spell check on the text. Use JLanguageTool.
 * 
 * @author P. Dessauw
 */
public class SpellChecker {
	private static Logger scLogger = LogManager.getLogger(SpellChecker.class);

	private static SpellChecker spellCheckerInstance = null;
	private MultiThreadedJLanguageTool languageTool;

	/*
	 * private static String[] DO_NOT_SHOW = { "SPELLING", "UNKNOWN",
	 * "UPPERCASE_SENTENCE_START", "EN_UNPAIRED_BRACKETS",
	 * "COMMA_PARENTHESIS_WHITESPACE" };
	 */

	/**
	 * Retrieve the SpellChecker instance
	 * 
	 * @return
	 * @throws IOException
	 */
	public synchronized static SpellChecker getInstance() throws IOException {
		if (spellCheckerInstance == null)
			spellCheckerInstance = new SpellChecker();

		return spellCheckerInstance;
	}

	/**
	 * Constructor
	 * 
	 * @throws IOException
	 */
	public SpellChecker() throws IOException {
		// Default language
		Language lang = new AmericanEnglish();

		// JLanguageTool setup
		this.languageTool = new MultiThreadedJLanguageTool(lang);
		
		this.languageTool.setListUnknownWords(true);
		this.languageTool.getAllRules();

		scLogger.debug("SpellChecker created");
	}
	
	public SpellChecker(Language lang) throws IOException
	{
		// JLanguageTool setup
		this.languageTool = new MultiThreadedJLanguageTool(lang);
		this.languageTool.setThreadPoolSize(100);
		
		this.languageTool.setListUnknownWords(true);
		this.languageTool.getAllRules();

		scLogger.debug("SpellChecker created");
	}

	/**
	 * Retrieve the number of words containing an error
	 * 
	 * @param sentence
	 * @return
	 * @throws IOException
	 */
	public double getErrorRate(String sentence) throws IOException {
		scLogger.trace("getErrorRate(" + sentence + ")");

		// Use JLanguageTool to check the text and count unknown words
		
		List<RuleMatch> matches = this.languageTool.check(sentence);
		List<String> unknownWords = this.languageTool.getUnknownWords();

		String[] tokens = sentence.split(" ");

		double matchCount = matches.size();
		double tokenCount = tokens.length;

		// Review errors
		for (RuleMatch match : matches) {
			Rule matchingRule = match.getRule();
			int startIndex = match.getColumn() - 1;
			int endIndex = match.getEndColumn() - 1;

			String problem = sentence.substring(startIndex, endIndex);

			if (!matchingRule.isSpellingRule() || StringTools.isUpper(problem)) {
				matchCount -= 1;
			} else
				scLogger.trace(problem + " | " + matchingRule.getId() + " | "
						+ match.getSuggestedReplacements());
		}

		scLogger.debug("Error rate: " + matchCount / tokenCount);
		scLogger.debug("Unknown words: " + unknownWords.size());

		return matchCount / tokenCount;
	}
}
