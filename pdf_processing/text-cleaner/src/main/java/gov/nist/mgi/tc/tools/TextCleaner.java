package gov.nist.mgi.tc.tools;

import gov.nist.mgi.tc.ind.impl.main.AlphaNumIndicator;
import gov.nist.mgi.tc.ind.impl.main.BegginingWithSpecCharIndicator;
import gov.nist.mgi.tc.ind.impl.main.CardinalNumberIndicator;
import gov.nist.mgi.tc.ind.impl.main.CleanTextIndicator;
import gov.nist.mgi.tc.ind.impl.main.EmptyLineIndicator;
import gov.nist.mgi.tc.ind.impl.main.SmallWordsIndicator;
import gov.nist.mgi.tc.ind.impl.main.TitleIndicator;
import gov.nist.mgi.tc.ind.impl.main.TooSmallLineIndicator;
import gov.nist.mgi.tc.tools.GradedLine.Grade;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.util.List;

import org.apache.commons.io.FilenameUtils;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

/**
 * Clean a file using a three steps process
 * 
 * @author P. Dessauw
 * 
 */
public class TextCleaner {
	private static String TXT_REQUIRED_MIME_TYPE = "text/plain";
	private static String GRBGE_SUFFIX = "-grbge";
	private static String CLEAN_SUFFIX = "-clean";
	//private static String UNSURE_SUFFIX = "-unsure";
	
	private static double PARAGRAPH_LIMIT_GRADE = 2.5;
	
	private static Logger tcLogger = LogManager.getLogger(TextCleaner.class);

	private File inputFile;
	private File cleanedFile;
	private File garbageFile;
	//private File unsureFile;

	private TextStatistics textStats;
	private List<List<GradedLine>> text;

	/**
	 * Constructor
	 * 
	 * @param article
	 * @throws IOException
	 */
	public TextCleaner(File article) throws IOException {
		tcLogger.entry();

		// Check file compliance
		if (!article.exists()
				|| !article.isFile()
				|| !Files.probeContentType(article.toPath()).equals(
						TXT_REQUIRED_MIME_TYPE)) {
			tcLogger.fatal("IllegalArgumentException: First parameter is not valid.");
			throw new IllegalArgumentException("First parameter is not valid");
		}

		this.inputFile = article;

		String baseFileName = FilenameUtils.removeExtension(article
				.getAbsolutePath());
		String extName = FilenameUtils.getExtension(article.getAbsolutePath());

		// Creating new files (final ones)
		this.cleanedFile = new File(baseFileName + CLEAN_SUFFIX + "." + extName);
		this.garbageFile = new File(baseFileName + GRBGE_SUFFIX + "." + extName);
		//this.unsureFile = new File(baseFileName + UNSURE_SUFFIX + "." + extName);

		// TODO Check if the files aleady exists. If so, save it in a backup
		// folder

		this.textStats = new TextStatistics();

		tcLogger.exit();
	}

	/**
	 * Clean the text
	 * 
	 * @throws IOException
	 */
	public void processText() throws IOException {
		tcLogger.debug("(Step 1) Reading input...");
		Reader inputReader = new Reader(this.inputFile);
		this.text = inputReader.getText(this.textStats);

		tcLogger.debug("(Step 2) Opening files...");
		BufferedWriter cleanWriter = new BufferedWriter(new FileWriter(
				this.cleanedFile));
		BufferedWriter grbgeWriter = new BufferedWriter(new FileWriter(
				this.garbageFile));
		/*BufferedWriter unsureWriter = new BufferedWriter(new FileWriter(
				this.unsureFile));*/

		tcLogger.debug("(Step 3) Processing text...");
		this.processStrongIndicators();
		this.processCleanSentences();
		this.processWeakIndicators();

		tcLogger.debug("(Step 4) Writing lines...");

		// Printing lines to the correct file
		for (List<GradedLine> paragraphs : this.text) {
			double paragraphGrade = 0;
			
			for (GradedLine line : paragraphs) {
				switch (line.getGrade()) {
				case A:
					paragraphGrade += 4;
					/*tcLogger.debug("CLEAN \"" + line.getLine() + "\"");
					cleanWriter.append(line.getLine() + "\n");*/
					break;
				case B:
					paragraphGrade += 3;
					break;
				case C:
					paragraphGrade += 2;
					break;
				case D:
					paragraphGrade += 1;
					break;
				//case E:
					/*tcLogger.debug("GARBAGE \"" + line.getLine() + "\"");
					grbgeWriter.append(line.getLine() + "\n");*/
					//break;
				default:
					/*tcLogger.debug("UNSURE " + line.getGrade() + " \""
							+ line.getLine() + "\"");
					unsureWriter.append(line.getLine() + "\n");*/
					break;
				}
			}
			
			paragraphGrade /= paragraphs.size();
			tcLogger.debug("Paragraph grade: "+paragraphGrade);
			
			if(paragraphGrade >= PARAGRAPH_LIMIT_GRADE)
			{
				// Write paragraph to the cleaned file
				for (GradedLine line : paragraphs) {
					cleanWriter.append(line.getLine() + "\n");
				}
				
				cleanWriter.append("\n");
			}
			else
			{
				// Write paragraph to the garbage file
				for (GradedLine line : paragraphs) {
					grbgeWriter.append(line.getLine() + "\n");					
				}
				
				grbgeWriter.append("\n");
			}
			

		}

		tcLogger.debug("(Step 5) Closing app...");
		cleanWriter.close();
		grbgeWriter.close();
		//unsureWriter.close();

		tcLogger.exit();
	}

	/**
	 * Use strong indicator to clean the text. If one of the indicator is
	 * matching, the line is stamped as garbage.
	 */
	private void processStrongIndicators() {
		tcLogger.entry();

		IndicatorList strongIndList = new IndicatorList();
		strongIndList.register(new EmptyLineIndicator());
		strongIndList.register(new CardinalNumberIndicator());
		strongIndList.register(new AlphaNumIndicator(this.textStats));
		strongIndList.register(new TooSmallLineIndicator(this.textStats));

		for (List<GradedLine> paragraphs : this.text) {
			for (GradedLine line : paragraphs) {
				if (this.textStats.getStatsForLine(line.getLine()) == null
						|| strongIndList.match(line.getLine())) {
					tcLogger.trace("GARBAGE \"" + line.getLine() + "\"");

					this.textStats.removeLineStats(line.getLine());
					line.setGrade(Grade.E);
				}
			}
		}

		tcLogger.exit();
	}

	/**
	 * Process indicators to detect clean sentences
	 */
	private void processCleanSentences() {
		tcLogger.entry();

		IndicatorList cleanIndList = new IndicatorList();
		cleanIndList.register(new CleanTextIndicator(this.textStats));
		cleanIndList.register(new TitleIndicator());

		for (List<GradedLine> paragraphs : this.text) {
			for (GradedLine line : paragraphs) {
				if (line.getGrade() != Grade.E && line.getGrade() != Grade.A
						&& cleanIndList.match(line.getLine())) {
					line.setGrade(Grade.A);
				}
			}

		}

		tcLogger.exit();
	}

	/**
	 * Process weak indicators. If one of the indicator is matching, the line is
	 * stamped as garbage.
	 * 
	 * FIXME Should not work this way. TODO Register more indicators. TODO
	 * Introduce the concept of rate.
	 * 
	 * 
	 * @throws IOException
	 * 
	 */
	private void processWeakIndicators() throws IOException {
		tcLogger.entry();

		IndicatorList weakIndList = new IndicatorList();
		weakIndList.register(new BegginingWithSpecCharIndicator()); // Cut too
																	// much
		weakIndList.register(new SmallWordsIndicator(this.textStats));

		SpellChecker spCheck = SpellChecker.getInstance();

		for (List<GradedLine> paragraphs : this.text) {
			for (GradedLine line : paragraphs) {
				if (line.getGrade() != Grade.E && line.getGrade() != Grade.A) {
					double error = spCheck.getErrorRate(line.getLine());

					if (error >= 0.5) {
						this.textStats.removeLineStats(line.getLine());
						line.setGrade(Grade.E);
					}
				}
			}

		}

		for (List<GradedLine> paragraphs : this.text) {
			for (GradedLine line : paragraphs) {
				if (line.getGrade() != Grade.E && line.getGrade() != Grade.A) {
					if (this.textStats.getStatsForLine(line.getLine()) == null
							|| weakIndList.match(line.getLine())) {
						this.textStats.removeLineStats(line.getLine());
						line.setGrade(Grade.E);
					}
				}
			}

		}

		tcLogger.exit();
	}

}
