package gov.nist.mgi.tc.ind.impl.main;

import gov.nist.mgi.tc.ind.models.StatsIndicator;
import gov.nist.mgi.tc.tools.StringTools.CharType;
import gov.nist.mgi.tc.tools.TextStatistics;

/**
 * Indicator computing the char type which is the most present (excepting special chars).
 * Then it compares this maximum to the number of other chars. 
 * It matches if the max is not significantly higher.
 * 
 * @author P. Dessauw
 */
public class TooManyCharTypeIndicator extends StatsIndicator {
	public static double CHAR_TYPE_LIMIT=0.5;

	public TooManyCharTypeIndicator(TextStatistics textStats) {
		super(textStats);
	}

	public boolean match(String line) {		
		double uppCount = this.count(line, CharType.UPPER);
		double lowCount = this.count(line, CharType.LOWER);
		double nbrCount = this.count(line, CharType.NUMBER);
		double spcCount = this.count(line, CharType.SPECIAL);
		
		if(spcCount == 0) return false;
		
		double[] refCount = {
			uppCount,
			lowCount,
			nbrCount
		};
		
		double refCountMax = 0;
		for(int i=0; i<refCount.length; i++)
		{
			if(refCount[i] > refCountMax)
				refCountMax = refCount[i];
		}
		
		if(refCountMax == 0) return true;
		
		double rate = (uppCount + lowCount + nbrCount + spcCount - refCountMax) / refCountMax;
		return rate > CHAR_TYPE_LIMIT;
	}

}
