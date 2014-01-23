package gov.nist.mgi.tc.tools;

import static org.junit.Assert.*;

import org.junit.Test;

public class StringToolsTest {
	private static String randomText_1 = "THIS IS UPPER";
	private static String randomText_2 = "THIS is UPPER";
	
	@Test
	public void testCount()
	{
		assertTrue(StringTools.count(randomText_1, "I") == 2);
		assertTrue(StringTools.count(randomText_1, "t") == 0);
		assertTrue(StringTools.count(randomText_1, "Z") == 0);
	}
	
	@Test
	public void testIsUpper()
	{
		assertTrue(StringTools.isUpper(randomText_1));
		assertFalse(StringTools.isUpper(randomText_2));
	}
}
