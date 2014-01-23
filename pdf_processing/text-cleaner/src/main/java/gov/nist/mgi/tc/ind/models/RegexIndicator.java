package gov.nist.mgi.tc.ind.models;

/**
 * Class to check a line against one regexp
 * 
 * @author Philippe Dessauw
 */
public abstract class RegexIndicator implements Indicator {
	private String regExp;

	public RegexIndicator(String inputRegExp) {
		this.regExp = inputRegExp;
	}

	public boolean match(String line) {
		return line.matches(this.regExp);
	}
}
