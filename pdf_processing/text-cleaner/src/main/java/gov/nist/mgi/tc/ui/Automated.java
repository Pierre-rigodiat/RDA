package gov.nist.mgi.tc.ui;

import gov.nist.mgi.tc.tools.TextCleaner;

import java.io.File;
import java.io.FileFilter;
import java.io.IOException;
import java.nio.file.Files;

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
	private static String TXT_REQUIRED_MIME_TYPE = "text/plain";

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

		File argument = new File(args[0]);
		autoLogger.debug("Cleaning " + args[0] + "...");

		if (argument.isDirectory()) {
			autoLogger.debug(args[0] + " is a directory");
			long startTime = System.currentTimeMillis();

			FileFilter txtFileFilter = new FileFilter() {
				public boolean accept(File file) {
					try {
						autoLogger.trace(file.toPath() + " => " + Files.probeContentType(file.toPath()));
						return TXT_REQUIRED_MIME_TYPE.equals(Files.probeContentType(file.toPath()));
					} catch (IOException e) {
						autoLogger.fatal("IOException raised");
						return false;
					}
				}
			};

			File[] txtFiles = argument.listFiles(txtFileFilter);

			for (File txtFile : txtFiles) {
				autoLogger.debug("Processing " + args[0] + "...");
				
				TextCleaner tc = new TextCleaner(txtFile);
				tc.processText();
			}

			long stopTime = System.currentTimeMillis();

			autoLogger.debug("Directory cleaned. Executed in "
					+ (stopTime - startTime) + "ms");
		} else {
			long startTime = System.currentTimeMillis();

			TextCleaner tc = new TextCleaner(new File(args[0]));
			tc.processText();

			long stopTime = System.currentTimeMillis();

			autoLogger.debug("File cleaned. Executed in "
					+ (stopTime - startTime) + "ms");
		}
	}
}