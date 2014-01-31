package gov.nist.mgi.tc.text;

import gov.nist.mgi.tc.tools.GradedLine;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

public class Text {
	private static Logger textLogger = LogManager.getLogger(Text.class);
	
	private List<GradedLine> lines;
	private List<List<Integer>> paragraphs;
	private List<List<Integer>> linePools;

	public Text(File textFile) throws IOException {
		textLogger.entry();
		
		this.lines = new ArrayList<GradedLine>();
		this.paragraphs = new ArrayList<List<Integer>>();
		this.linePools = null;

		this.readText(textFile);

		textLogger.exit();
	}

	private void readText(File input) throws IOException {
		textLogger.entry();

		// Init
		BufferedReader inputReader = new BufferedReader(new FileReader(input));

		String line = inputReader.readLine();
		int lineIndex = 0;
		List<Integer> paragraph = new ArrayList<Integer>();

		// Reading
		while (line != null) {
			if (line.equals("")) { // Empty line => New paragraph
				if (paragraph.size() != 0) // To register a paragraph, it has to
											// contain data
				{
					textLogger.trace("Paragraph added - " + paragraph.size() +" lines - "+paragraph);

					this.paragraphs.add(paragraph);
					paragraph = new ArrayList<Integer>(); // Reset paragraph
															// content
				}
			} else { // Line belongs to the current paragraph
				this.lines.add(new GradedLine(line));
				paragraph.add(lineIndex);
				
				lineIndex += 1;
			}

			line = inputReader.readLine(); // Next line
		}

		inputReader.close();

		textLogger.info("Input read (" + this.lines.size() + " lines, " + this.paragraphs.size() + " paragraphs)");
	}

	public void splitText(int maxPoolNb) {
		textLogger.entry();
		
		if(maxPoolNb <= 0)
			throw new IllegalArgumentException("Max section number should be positive");
		
		int linesPerSection = this.lines.size() / maxPoolNb + 1;
		this.linePools = new ArrayList<List<Integer>>();		
		
		textLogger.debug("Splitting in "+maxPoolNb+" sections w/ "+linesPerSection+" lines per section");
		
		int currentLine = 0;
		for(int currentSection=0; currentSection<maxPoolNb; currentSection++)
		{
			int linesInSection = 0;
			List<Integer> section = new ArrayList<Integer>();
			
			while(linesInSection < linesPerSection && currentLine < this.lines.size())
			{
				section.add(currentLine);
				currentLine += 1;
				linesInSection += 1;
			}
			
			textLogger.trace("Section "+currentSection+" * "+linesInSection+" lines "+section);			
			this.linePools.add(section);
		}
		
	}
	
	public GradedLine getLine(int lineIndex)
	{
		return this.lines.get(lineIndex);
	}
	
	public List<GradedLine> getText()
	{
		return this.lines;
	}

	public List<List<Integer>> getPools() {
		return this.linePools;
	}
	
	public List<List<Integer>> getParagraphs()
	{
		return this.paragraphs;
	}
}
