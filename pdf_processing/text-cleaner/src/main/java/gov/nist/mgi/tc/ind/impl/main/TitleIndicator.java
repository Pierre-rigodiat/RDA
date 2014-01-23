package gov.nist.mgi.tc.ind.impl.main;

import gov.nist.mgi.tc.ind.models.RegexIndicator;

/**
 * Indicator detecting titles
 * 
 * @author P. Dessauw
 */
public class TitleIndicator extends RegexIndicator {

	public TitleIndicator() {
		super("[A-Z][a-z ]+");
	}

}
