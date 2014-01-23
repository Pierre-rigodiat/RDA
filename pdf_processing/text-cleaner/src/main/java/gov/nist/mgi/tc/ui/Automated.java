package gov.nist.mgi.tc.ui;

import gov.nist.mgi.tc.tools.TextCleaner;

import java.io.File;
import java.io.IOException;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

/**
 * Automatically clean the text
 * 
 * @author P. Dessauw
 * 
 */
public class Automated {
	private static Logger autoLogger = LogManager.getLogger(Automated.class);

	/**
	 * Main function
	 * 
	 * @param args
	 * @throws IOException
	 * @throws IllegalAccessException
	 */
	public static void main(String[] args) throws IOException,
			IllegalAccessException {
		if (args.length != 1) {
			autoLogger.fatal("Argument count is not good (" + args.length
					+ " submitted, 1 expected)");
			throw new IllegalArgumentException("Argument count not good");
		}

		autoLogger.debug("Cleaning " + args[0] + "...");

		long startTime = System.currentTimeMillis();

		TextCleaner tc = new TextCleaner(new File(args[0]));
		tc.processText();

		long stopTime = System.currentTimeMillis();

		autoLogger.debug("File cleaned. Executed in " + (stopTime - startTime)
				+ "ms");
	}
}