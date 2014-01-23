package gov.nist.mgi.tc.ind.impl.main;

import gov.nist.mgi.tc.ind.models.StatsIndicator;
import gov.nist.mgi.tc.tools.StringTools.CharType;
import gov.nist.mgi.tc.tools.TextStatistics;

/**
 * Indicator stating if a line is clean based on - the length of the line - the
 * number of upper and lower chars
 * 
 * @author P. Dessauw
 */
public class CleanTextIndicator extends StatsIndicator {
	private static double LINE_LENGTH_RATE = 0.5;
	private static double CHAR_RATE = 0.6;

	public CleanTextIndicator(TextStatistics textStats) {
		super(textStats);
	}

	public boolean match(String line) {
		double length = line.length();

		return length >= this.stats.getAvgLineLength() * LINE_LENGTH_RATE
				&& (this.count(line, CharType.LOWER) / length > CHAR_RATE || this
						.count(line, CharType.UPPER) / length > CHAR_RATE);
	}
}
