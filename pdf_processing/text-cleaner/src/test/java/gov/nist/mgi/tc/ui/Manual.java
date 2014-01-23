package gov.nist.mgi.tc.ui;

import gov.nist.mgi.tc.tools.TextCleaner;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

/**
 * Test the cleaning for one file
 * 
 * @author Philippe Dessauw
 */
public class Manual {
	private static Logger mLogger = LogManager.getLogger(Manual.class);
	private static String INPUT_FILE_PATH = "src/test/resources/gov/nist/mgi/tc/articles";

	/**
	 * Read the input given by the user
	 * 
	 * @return
	 * @throws IOException
	 */
	public static File readInput(BufferedReader inputReader) throws IOException {
		System.out.print("Input file: ");

		// Creating file object and testing it to see if it meets the
		// requirements
		File inputFile = new File(INPUT_FILE_PATH + File.separator
				+ inputReader.readLine());
		if (!inputFile.exists() || !inputFile.isFile()) {
			System.err
					.println("<< Input file does not exist or is not a file >>");
			inputFile = null;
		}

		return inputFile;
	}

	/**
	 * Main function
	 * 
	 * @param args
	 * @throws IOException
	 */
	public static void main(String[] args) throws IOException {
		System.out.println("*** Garbage finder UI ****");

		// Reading input
		mLogger.debug("Waiting for input...");

		BufferedReader inputReader = new BufferedReader(new InputStreamReader(
				System.in));
		File inputFile = null;

		while (inputFile == null)
			inputFile = readInput(inputReader);

		inputReader.close(); // Closing the reader

		mLogger.debug("Input setup. Initializing cleaning process...");

		// Cleaning the text
		TextCleaner tc = new TextCleaner(inputFile);
		tc.processText();

		mLogger.debug("Cleaning done");
	}

}
