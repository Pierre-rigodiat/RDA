package gov.nist.mgi.tc.ind.impl.main;

import gov.nist.mgi.tc.ind.models.RegexIndicator;

/**
 * Indicator detecting empty lines
 * 
 * @author P. Dessauw
 */
public class EmptyLineIndicator extends RegexIndicator {
	public EmptyLineIndicator() {
		super("^$");
	}
}
