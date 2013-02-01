The materials ontology is divided into multiple topical ontologies, the more general of which may be used for different purposes.

The file dependencies are:

	MaterialsProcessing.owl
uses

	Materials.owl and Experiments.owl

which both use

	Document.n3 and Biochem.n3

which uses

	OntologyRequirements.owl

To load them into Protege, they should be loaded in the reverse order, i.e., OntologyRequirements first.
