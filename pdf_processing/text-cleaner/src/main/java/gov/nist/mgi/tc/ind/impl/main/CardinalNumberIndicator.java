package gov.nist.mgi.tc.ind.impl.main;

import gov.nist.mgi.tc.ind.models.RegexIndicator;

/**
 * Indicator stating if a line is a page number, or a list of numbers This
 * second version is still a test version and need to be further tested
 * 
 * @author P. Dessauw
 */
public class CardinalNumberIndicator extends RegexIndicator {

	public CardinalNumberIndicator() {
		super("^[0-9efEaAoOsSt.,= \\-]+$");
	}

}
