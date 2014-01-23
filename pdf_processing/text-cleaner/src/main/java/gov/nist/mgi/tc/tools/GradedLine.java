package gov.nist.mgi.tc.tools;

/**
 * Class defining a couple (String, Grade)
 * 
 * @author Philippe Dessauw
 */
public class GradedLine {
	/**
	 * Set of different grades
	 * 
	 * @author Philippe Dessauw
	 */
	public enum Grade {
		A, // Clean (not affected by being close to garbage)
		B, // Suspicious
		C, // Suspicious & close to gbge
		D, // Suspicious & next to gbge
		E // Garbage
	}

	private String line;
	private Grade grade;

	/**
	 * Constructor, applying a B grade by default
	 * 
	 * @param line
	 */
	public GradedLine(String line) {
		this.line = line;
		this.grade = Grade.B;
	}

	/**
	 * Getter for the grade
	 * 
	 * @return The grade of the line
	 */
	public Grade getGrade() {
		return grade;
	}

	/**
	 * Getter for the line
	 * 
	 * @return The current line
	 */
	public String getLine() {
		return line;
	}

	/**
	 * Setter for the grade
	 * 
	 * @param grade
	 */
	public void setGrade(Grade grade) {
		this.grade = grade;
	}

	/**
	 * String representing the object
	 */
	public String toString() {
		return this.line + " | " + this.grade;
	}
}