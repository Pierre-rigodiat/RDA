package gov.nist.mgi.tc.ind.models;

/**
 * Indicator interface
 * 
 * @author Philippe Dessauw
 */
public interface Indicator {
	/**
	 * Check if a line match the condition of the indicator Condition are
	 * defined in the implementing class
	 * 
	 * @param line
	 * @return true if conditions are met, false otherwise
	 */
	public boolean match(String line);
}
