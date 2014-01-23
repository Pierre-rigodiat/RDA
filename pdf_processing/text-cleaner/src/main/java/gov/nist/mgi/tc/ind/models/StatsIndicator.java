package gov.nist.mgi.tc.ind.models;

import gov.nist.mgi.tc.tools.StringTools;
import gov.nist.mgi.tc.tools.StringTools.CharType;
import gov.nist.mgi.tc.tools.TextStatistics;

import java.util.Map;

public abstract class StatsIndicator implements Indicator {
	protected TextStatistics stats;

	public StatsIndicator(TextStatistics textStats) {
		this.stats = textStats;
	}

	/**
	 * Count the number of the specific set of character
	 * @param line
	 * @param type
	 * @return The number of character
	 */
	public double count(String line, CharType type) {
		Map<CharType, Double> charTypeStats = this.stats.getStatsForLine(line);
		return charTypeStats.get(type);
	}

	/**
	 * Count the number of spaces
	 * @param line
	 * @return The number of spaces
	 */
	public double spaceCount(String line) {
		return StringTools.count(line, " ");
	}
}
