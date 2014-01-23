package gov.nist.mgi.tc.tools;

/**
 * Collection of tools to compute strings
 * 
 * @author Philippe Dessauw
 */
public class StringTools {
	/**
	 * Available character types
	 * 
	 * @author Philippe Dessauw
	 */
	public enum CharType {
		LOWER, UPPER, NUMBER, SPECIAL
	}

	/**
	 * Count the number of occurences of subString in input
	 * 
	 * @param input
	 * @return
	 */
	public static int count(String input, String subString) {
		if (input == null || subString == null) {
			return 0;
		} else {
			int counter = 0;
			int i = -1;
			while ((i = input.indexOf(subString, i + 1)) != -1) {
				counter++;
			}
			return counter;
		}
	}

	/**
	 * Detect if a string is in upper case
	 * 
	 * @param input
	 * @return true if the line is in upper case
	 */
	public static boolean isUpper(String input) {
		return input.equals(input.toUpperCase());
	}

}
