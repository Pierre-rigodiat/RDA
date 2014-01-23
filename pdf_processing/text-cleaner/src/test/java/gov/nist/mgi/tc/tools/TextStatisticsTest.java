package gov.nist.mgi.tc.tools;

import static org.junit.Assert.assertTrue;
import static org.junit.Assert.fail;

import java.io.IOException;

import org.junit.Test;

public class TextStatisticsTest {
	private static String randomText = "This is a simple text line";

	@Test
	public void testComputeLine() {
		TextStatistics tStats;
		try {
			tStats = new TextStatistics();
			tStats.computeLine(randomText);
		} catch (IOException e) {
			fail("IOException raised");
			return;
		}
		
		double wordNb = StringTools.count(randomText, " ") + 1;
		double wordTotalSize = 0;		
		for(String word:tStats.getLineWords(randomText))
		{
			wordTotalSize += word.length();
		}
		
		assertTrue(tStats.getAvgLineLength() == randomText.length());
		assertTrue(tStats.getAvgWordPerLine() == wordNb);
		assertTrue(tStats.getAvgWordSize() == wordTotalSize / wordNb);
	}
	
	@Test
	public void testRemoveLineStats() {
		TextStatistics tStats;
		try {
			tStats = new TextStatistics();
			tStats.computeLine(randomText);
		} catch (IOException e) {
			fail("IOException raised");
			return;
		}
		
		tStats.removeLineStats(randomText);
		
		assertTrue(tStats.getAvgLineLength() == 0);
		assertTrue(tStats.getAvgWordPerLine() == 0);
		assertTrue(tStats.getAvgWordSize() == 0);
	}
}
