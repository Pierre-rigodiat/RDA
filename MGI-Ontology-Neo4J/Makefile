
.SUFFIXES: .owl .ntriples .pro .bin .clauses .sh

CWM = ~/Tools/cwm-1.2.1/cwm
SWIPL = swipl

all: load.sh

NFILES = Biochem.ntriples Document.ntriples Experiments.ntriples MaterialProcessing.ntriples Materials.ntriples OntologyRequirements.ntriples

$(NFILES): %.ntriples: %.owl
	$(CWM) --rdf $< --ntriples > $@


PFILES = Biochem.pro Document.pro Experiments.pro MaterialProcessing.pro Materials.pro OntologyRequirements.pro

$(PFILES): %.pro: %.ntriples
	bin/ntriples2clauses.pl $< > $@


BFILES = Biochem.bin Document.bin Experiments.bin MaterialProcessing.bin Materials.bin OntologyRequirements.bin

$(BFILES): %.bin: %.pro
	$(SWIPL) -o $@ -c $< bin/smush.pro 


CFILES = Biochem.clauses Document.clauses Experiments.clauses MaterialProcessing.clauses Materials.clauses OntologyRequirements.clauses
	
$(CFILES): %.clauses: %.bin
	$(SWIPL) -x $< -g clean_up,halt -t 'halt(1)' > $@


load.sh : $(CFILES)
	cat $(CFILES) | sort -ru | bin/clauses2load.pl > load.sh


clean:
	rm -f $(NFILES) $(PFILES) $(BFILES) $(CFILES) load.sh

