package gov.nist.mgi.tc.tools;

import static org.junit.Assert.*;

import gov.nist.mgi.tc.spcheck.SpellChecker;

import java.io.IOException;

import org.junit.Test;

public class SpellCheckerTest {
	private static String randomText = "This si a error";

	@Test
	public void testSingleton() {
		try {
			SpellChecker spellChecker_1 = SpellChecker.getInstance();
			SpellChecker spellChecker_2 = SpellChecker.getInstance();
			
			assertTrue(spellChecker_1 == spellChecker_2);
		} catch (IOException e) {
			fail("IOException raised");
		}
	}
	
	@Test
	public void testErrorRate() {
		try {
			SpellChecker spCheck = SpellChecker.getInstance();

			// XXX Only spelling rules are considered as an error
			assertTrue(spCheck.getErrorRate(randomText) == 0.25);
		} catch (IOException e) {
			fail("IOException raised");
		}
	}
}
