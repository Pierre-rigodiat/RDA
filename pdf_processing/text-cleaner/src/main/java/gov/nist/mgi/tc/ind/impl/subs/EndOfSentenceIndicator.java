package gov.nist.mgi.tc.ind.impl.subs;

import gov.nist.mgi.tc.ind.models.RegexIndicator;

/**
 * Indicator detecting end of sentence lines
 * 
 * @author P. Dessauw
 */
public class EndOfSentenceIndicator extends RegexIndicator {

	public EndOfSentenceIndicator() {
		super(".+[.:]$");
	}
	
}
