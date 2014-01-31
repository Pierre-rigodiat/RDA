package gov.nist.mgi.tc.tools;

import static org.junit.Assert.assertTrue;
import gov.nist.mgi.tc.ind.impl.main.BegginingWithSpecCharIndicator;
import gov.nist.mgi.tc.ind.impl.main.CleanTextIndicator;
import gov.nist.mgi.tc.text.TextStatistics;

import java.io.IOException;

import opennlp.tools.util.InvalidFormatException;

import org.junit.Test;

public class IndicatorListTest {
	private static String randomText = "Hello world!";	
	
	@Test
	public void testMatchRate() throws InvalidFormatException, IOException
	{
		TextStatistics tStats = new TextStatistics();
		tStats.computeLine(randomText);
		
		IndicatorList indList = new IndicatorList();
		indList.register(new BegginingWithSpecCharIndicator());
		indList.register(new CleanTextIndicator(tStats));
		
		assertTrue(indList.matchRate(randomText) == 0.5);
	}
}
