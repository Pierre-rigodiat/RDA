package gov.nist.mgi.tc.spcheck;

import gov.nist.mgi.tc.text.TextStatistics;
import gov.nist.mgi.tc.tools.GradedLine;
import gov.nist.mgi.tc.tools.GradedLine.Grade;

import java.io.IOException;
import java.util.List;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

/**
 * Class to perform a spell check on a part of the text.
 * Designed to improve performances
 * 
 * @author P. Dessauw
 */
public class SpellCheckWorker implements Runnable {
	private static Logger scwLogger = LogManager.getLogger(SpellCheckWorker.class);

	private List<GradedLine> text;
	private TextStatistics stats;
	private SpellChecker spCheck;
	
	public SpellCheckWorker(List<GradedLine> text, TextStatistics stats) throws IOException
	{		
		this.text = text;
		this.stats = stats;
		this.spCheck = new SpellChecker();
		
		scwLogger.debug("Worker initialized");
	}

	@Override
	public void run() {
		for (GradedLine line : this.text) {
			if (line.getGrade() != Grade.E && line.getGrade() != Grade.A) {
				scwLogger.debug(Thread.currentThread().getName()+" - "+line.getLine());
				
				double error = 1;
				try {
					
					error = spCheck.getErrorRate(line.getLine());
				} catch (IOException e) {
					scwLogger.fatal("IOException raised");
				}

				if (error >= 0.5) {
					this.stats.removeLineStats(line.getLine());
					scwLogger.trace(line.getLine()+" - E");
					line.setGrade(Grade.E);
				}
			}
		}
		
		scwLogger.debug(Thread.currentThread().getName()+" - Finished");
		Thread.currentThread().interrupt();
	}
}
