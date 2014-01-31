package gov.nist.mgi.tc.ind.impl.main;

import gov.nist.mgi.tc.ind.impl.subs.EndOfSentenceIndicator;
import gov.nist.mgi.tc.ind.models.StatsIndicator;
import gov.nist.mgi.tc.text.TextStatistics;

/**
 * Indicator detecting lines smaller than the average
 * 
 * @author P. Dessauw
 */
public class TooSmallLineIndicator extends StatsIndicator {
	private static double MIN_LINE_LENGTH = 0.1;

	public TooSmallLineIndicator(TextStatistics textStats) {
		super(textStats);
	}

	public boolean match(String line) {
		return line.length() < this.stats.getAvgLineLength() * MIN_LINE_LENGTH && !(new EndOfSentenceIndicator()).match(line);
	}

}
