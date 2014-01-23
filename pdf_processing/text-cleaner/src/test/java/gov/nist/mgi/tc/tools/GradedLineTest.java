package gov.nist.mgi.tc.tools;

import static org.junit.Assert.assertTrue;
import gov.nist.mgi.tc.tools.GradedLine.Grade;

import org.junit.Test;

public class GradedLineTest {
	private String simpleLine = "This is a simple test";
	
	private GradedLine simpleInit()
	{
		return new GradedLine(this.simpleLine);
	}

	@Test
	public void testLineInitialization() 
	{
		GradedLine gLine = simpleInit();
		
		assertTrue(gLine.getLine() == this.simpleLine);
	}
	
	@Test
	public void testGradeInitialization() 
	{
		GradedLine gLine = simpleInit();
		
		assertTrue(gLine.getGrade() == Grade.B);
	}
	
	@Test
	public void testSetGrade()
	{
		Grade newGrade = Grade.A;
		GradedLine gLine = simpleInit();
		
		gLine.setGrade(newGrade);
		
		assertTrue(gLine.getGrade() == newGrade);
	}
}
