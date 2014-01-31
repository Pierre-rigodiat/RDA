package gov.nist.mgi.tc.tools;

import gov.nist.mgi.tc.ind.impl.main.AlphaNumIndicator;
import gov.nist.mgi.tc.ind.impl.main.BegginingWithSpecCharIndicator;
import gov.nist.mgi.tc.ind.impl.main.CardinalNumberIndicator;
import gov.nist.mgi.tc.ind.impl.main.CleanTextIndicator;
import gov.nist.mgi.tc.ind.impl.main.SmallWordsIndicator;
import gov.nist.mgi.tc.ind.impl.main.TitleIndicator;
import gov.nist.mgi.tc.ind.impl.main.TooSmallLineIndicator;
import gov.nist.mgi.tc.spcheck.SpellCheckWorker;
import gov.nist.mgi.tc.text.Text;
import gov.nist.mgi.tc.text.TextStatistics;
import gov.nist.mgi.tc.tools.GradedLine.Grade;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

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
	private static int THREAD_COUNT = 4;
	
	private static String TXT_REQUIRED_MIME_TYPE = "text/plain";

	private static String GRBGE_SUFFIX = "-grbge";
	private static String CLEAN_SUFFIX = "-clean";

	private static double PARAGRAPH_LIMIT_GRADE = 2.5;

	private static Logger tcLogger = LogManager.getLogger(TextCleaner.class);

	private File cleanedFile;
	private File garbageFile;

	private Text text;
	private TextStatistics textStats;

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
				|| !TXT_REQUIRED_MIME_TYPE.equals(Files
						.probeContentType(article.toPath()))) {
			tcLogger.fatal("IllegalArgumentException: First parameter is not valid.");
			throw new IllegalArgumentException("First parameter is not valid");
		}

		String baseFileName = FilenameUtils.removeExtension(article
				.getAbsolutePath());
		String extName = FilenameUtils.getExtension(article.getAbsolutePath());

		// Creating new files (final ones)
		this.cleanedFile = new File(baseFileName + CLEAN_SUFFIX + "." + extName);
		this.garbageFile = new File(baseFileName + GRBGE_SUFFIX + "." + extName);

		// TODO Check if the files aleady exists. If so, save it in a backup
		// folder or display an warning message

		// Read input and process text statistics
		tcLogger.debug("(Step 1) Reading input...");
		this.text = new Text(article);
		
		this.textStats = new TextStatistics();
		for(GradedLine line:this.text.getText())
		{
			this.textStats.computeLine(line.getLine());
		}
		
		tcLogger.debug("TextCleaner initialized");
	}

	/**
	 * Clean the text
	 * 
	 * @throws IOException
	 */
	public void processText() throws IOException {
		tcLogger.debug("(Step 2) Processing text...");
		
		// Use indicators
		this.processStrongIndicators();
		this.processCleanSentences();
		this.processWeakIndicators();
		
		// Check spelling
		this.checkSpelling();

		tcLogger.debug("(Step 3) Writing lines...");
		
		// Open file writers
		BufferedWriter cleanWriter = new BufferedWriter(new FileWriter(
				this.cleanedFile));
		BufferedWriter grbgeWriter = new BufferedWriter(new FileWriter(
				this.garbageFile));

		// Printing lines to the correct file
		for (List<Integer> paragraphs : this.text.getParagraphs()) {
			double paragraphGrade = 0;

			for (Integer lineId : paragraphs) {
				GradedLine line = this.text.getLine(lineId);
				
				switch (line.getGrade()) {
				case A:
					paragraphGrade += 4;
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
				default:
					break;
				}
			}

			paragraphGrade /= paragraphs.size();
			tcLogger.trace("Paragraph grade: " + paragraphGrade);

			if (paragraphGrade >= PARAGRAPH_LIMIT_GRADE) {
				// Write paragraph to the cleaned file
				for (Integer lineId : paragraphs) {
					GradedLine line = this.text.getLine(lineId);
					
					cleanWriter.append(line.getLine() + "\n");
				}

				cleanWriter.append("\n");
			} else {
				// Write paragraph to the garbage file
				for (Integer lineId : paragraphs) {
					GradedLine line = this.text.getLine(lineId);
					grbgeWriter.append(line.getLine() + "\n");
				}

				grbgeWriter.append("\n");
			}

		}

		// Release memory
		tcLogger.debug("(Step 4) Closing app...");
		cleanWriter.close();
		grbgeWriter.close();

		tcLogger.exit();
	}

	/**
	 * Use strong indicator to clean the text. If one of the indicator is
	 * matching, the line is stamped as garbage.
	 */
	private void processStrongIndicators() {
		tcLogger.entry();

		IndicatorList strongIndList = new IndicatorList();
		strongIndList.register(new CardinalNumberIndicator());
		strongIndList.register(new AlphaNumIndicator(this.textStats));
		strongIndList.register(new TooSmallLineIndicator(this.textStats));
		
		for(GradedLine line:this.text.getText())
		{
			if (this.textStats.getStatsForLine(line.getLine()) == null
					|| strongIndList.match(line.getLine())) {
				tcLogger.trace("GRBGE " + line.getLine());

				this.textStats.removeLineStats(line.getLine());
				line.setGrade(Grade.E);
			}
		}

		tcLogger.debug("Strong indicators processed, "+(int)this.textStats.getLineNb()+" lines remaining");
	}

	/**
	 * Process indicators to detect clean sentences
	 */
	private void processCleanSentences() {
		tcLogger.entry();

		IndicatorList cleanIndList = new IndicatorList();
		cleanIndList.register(new CleanTextIndicator(this.textStats));
		cleanIndList.register(new TitleIndicator());

		for(GradedLine line:this.text.getText())
		{
			if (line.getGrade() != Grade.E && line.getGrade() != Grade.A
					&& cleanIndList.match(line.getLine())) {
				tcLogger.trace("CLEAN " + line.getLine());
				
				line.setGrade(Grade.A);
			}
		}

		tcLogger.debug("Clean indicators processed");
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
	private void processWeakIndicators() {
		tcLogger.entry();

		IndicatorList weakIndList = new IndicatorList();
		weakIndList.register(new BegginingWithSpecCharIndicator()); // Cut too
																	// much
		weakIndList.register(new SmallWordsIndicator(this.textStats));
		
		for(GradedLine line:this.text.getText())
		{
			if (line.getGrade() != Grade.E && line.getGrade() != Grade.A) {
				if (this.textStats.getStatsForLine(line.getLine()) == null
						|| weakIndList.match(line.getLine())) {
					tcLogger.trace("GRBGE " + line.getLine());
					
					this.textStats.removeLineStats(line.getLine());
					line.setGrade(Grade.E);
				}
			}
		}

		tcLogger.debug("Weak indicators processed, "+(int)this.textStats.getLineNb()+" lines remaining");
	}
	
	/**
	 * 
	 * @throws IOException
	 */
	private void checkSpelling() throws IOException {
		// Split the text and initialize the process pool
		this.text.splitText(THREAD_COUNT);
		ExecutorService spCheckService = Executors.newFixedThreadPool(THREAD_COUNT);
		
		tcLogger.debug("Launching "+THREAD_COUNT+" thread(s)...");
		
		for(List<Integer> linePool:this.text.getPools())
		{
			// Building the pool line
			List<GradedLine> lines = new ArrayList<GradedLine>();
			
			for(int line:linePool)
			{
				lines.add(this.text.getLine(line));
			}
			
			spCheckService.submit(new SpellCheckWorker(lines, this.textStats));
		}

		// Wait for every process to shutdown
		spCheckService.shutdown();
		while (!spCheckService.isTerminated())
			;
		
		tcLogger.debug("Check spelling processed, "+(int)this.textStats.getLineNb()+" lines remaining");
	}

}
