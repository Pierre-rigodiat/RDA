package gov.nist.mgi.tc.tools;

import gov.nist.mgi.tc.ind.models.Indicator;

import java.util.ArrayList;
import java.util.List;

/**
 * Class maintaining a list of Indicators
 * 
 * @author Philippe Dessauw
 */
public class IndicatorList {
	/**
	 * List of indicator
	 */
	private List<Indicator> indList;

	/**
	 * Regular constructor
	 */
	public IndicatorList() {
		this.indList = new ArrayList<Indicator>();
	}

	/**
	 * Add indicator to the list
	 * 
	 * @param ind
	 */
	public void register(Indicator ind) {
		this.indList.add(ind);
	}

	/**
	 * Check if all indicators are matching
	 * 
	 * @param line
	 * @return true if all indicators match, false otherwise
	 */
	public boolean match(String line) {
		return matchRate(line) > 0;
	}

	/**
	 * Check if all indicators are matching and returns the percentage of
	 * matching indicators
	 * 
	 * @param line
	 * @return percentage of matching indicators
	 */
	public double matchRate(String line) {
		double totalInd = this.indList.size();
		double matchInd = 0;

		for (Indicator ind : this.indList) {
			if (ind.match(line))
				matchInd += 1;
		}

		return matchInd / totalInd;
	}

}
