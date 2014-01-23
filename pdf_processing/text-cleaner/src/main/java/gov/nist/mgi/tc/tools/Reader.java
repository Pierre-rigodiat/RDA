package gov.nist.mgi.tc.tools;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.List;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

/**
 * Read a file and retrieve the content as a list of GradedLine
 * 
 * @author P. Dessauw
 * 
 */
public class Reader {
	private static Logger readerLogger = LogManager.getLogger(Reader.class);
	private static String TXT_MIME_TYPE = "text/plain";

	private File input;

	/**
	 * Constructor
	 * 
	 * @param inputFile
	 * @throws IOException
	 */
	public Reader(File inputFile) throws IOException {
		readerLogger.entry();

		this.input = inputFile;

		// Basic checks on the file
		if (!this.input.exists()
				|| !this.input.isFile()
				|| !Files.probeContentType(this.input.toPath()).equals(
						TXT_MIME_TYPE)) {
			readerLogger
					.fatal("IllegalArgumentException: Input file does not exist or has an incorrect format");
			throw new IllegalArgumentException(
					"Input file does not exist or has an incorrect format");
		}

		readerLogger.exit();
	}

	/**
	 * Read the text
	 * 
	 * @param stats
	 * @return the text divided into paragraphs
	 * @throws IOException
	 */
	public List<List<GradedLine>> getText(TextStatistics stats)
			throws IOException {
		readerLogger.entry();

		List<List<GradedLine>> paragraphList = new ArrayList<List<GradedLine>>();
		BufferedReader inputReader = new BufferedReader(new FileReader(
				this.input));

		String line = inputReader.readLine();
		List<GradedLine> paragraph = new ArrayList<GradedLine>();

		while (line != null) {
			if (line.equals("")) {
				if (paragraph.size() != 0)
					paragraphList.add(paragraph);

				paragraph = new ArrayList<GradedLine>();
			} else {
				stats.computeLine(line);
				paragraph.add(new GradedLine(line));
			}

			line = inputReader.readLine();
		}

		inputReader.close();

		readerLogger.exit();

		return paragraphList;
	}

	/**
	 * Read the text
	 * 
	 * @param stats
	 * @return the text as a list of line
	 * @throws IOException
	 */
	public List<GradedLine> getLineList(TextStatistics stats)
			throws IOException {
		readerLogger.entry();

		List<GradedLine> lineList = new ArrayList<GradedLine>();
		BufferedReader inputReader = new BufferedReader(new FileReader(
				this.input));

		String line = inputReader.readLine();

		while (line != null) {
			stats.computeLine(line);
			lineList.add(new GradedLine(line));

			line = inputReader.readLine();
		}

		inputReader.close();

		readerLogger.exit();

		return lineList;
	}

}
