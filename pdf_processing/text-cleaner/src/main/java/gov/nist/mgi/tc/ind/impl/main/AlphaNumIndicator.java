package gov.nist.mgi.tc.ind.impl.main;

import gov.nist.mgi.tc.ind.models.StatsIndicator;
import gov.nist.mgi.tc.text.TextStatistics;
import gov.nist.mgi.tc.tools.StringTools.CharType;

/**
 * Indicator computing the special char rate It matches when the ratio is too
 * high
 * 
 * @author P. Dessauw
 */
public class AlphaNumIndicator extends StatsIndicator {
	private static double SP_CHAR_RATE = 0.5;

	public AlphaNumIndicator(TextStatistics textStats) {
		super(textStats);
	}

	public boolean match(String line) {
		double length = line.length();

		double uppCount = count(line, CharType.UPPER);
		double lowCount = count(line, CharType.LOWER);
		double nbrCount = count(line, CharType.NUMBER);

		return (uppCount + lowCount + nbrCount) / length <= SP_CHAR_RATE;
	}
}
