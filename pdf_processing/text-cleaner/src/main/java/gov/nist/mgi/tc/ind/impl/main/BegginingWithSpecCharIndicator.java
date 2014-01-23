package gov.nist.mgi.tc.ind.impl.main;

import gov.nist.mgi.tc.ind.models.RegexIndicator;

/**
 * Indicator stating if a line begins with a special character
 * 
 * @author P. Dessauw
 */
public class BegginingWithSpecCharIndicator extends RegexIndicator {

	public BegginingWithSpecCharIndicator() {
		super("[,'-].+");
	}

}
