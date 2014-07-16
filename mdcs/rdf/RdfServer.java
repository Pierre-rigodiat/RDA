//###############################################################################
//
// File Name: RdfServer.java
// Application: rdf
// Description: 
//
//
// Author:    Guillaume Sousa
//            guillaume.sousa@nist.gov
// Co-Author: Sharief Youssef
//            sharief.youssef@nist.gov
//
// Sponsor: National Institute of Standards and Technology (NIST)
//
//###############################################################################

import java.io.ByteArrayInputStream;
import java.io.InputStream;
import org.zeromq.ZMQ;

import com.hp.hpl.jena.query.Dataset;
import com.hp.hpl.jena.query.ReadWrite;
import com.hp.hpl.jena.rdf.model.Model;
import com.hp.hpl.jena.rdf.model.ModelFactory;
import com.hp.hpl.jena.tdb.TDBFactory;


public class RdfServer implements Runnable{
	
	/**
	 * Address of the server endpoint
	 */
	private String serverEndpoint;
	
	/**
	 * Path to the triplestore directory
	 */
	private String tdbDirectory;
	
	/**
	 * URI of the project
	 */
	private String projectURI;
	
	
	public RdfServer(String serverEndpoint, String tdbDirectory, String projectURI){
		this.serverEndpoint = serverEndpoint;
		this.tdbDirectory = tdbDirectory;
		this.projectURI = projectURI;
	}
	
	@Override
	public void run() {
		System.out.println("RDF server launched...");

		//TODO: be sure it is the same context number as in the client
		ZMQ.Context context = ZMQ.context(7);
		// Socket to talk to clients
		ZMQ.Socket responder = context.socket(ZMQ.REP);		 
		responder.bind(serverEndpoint);
		
		while (true) {
		    try{ 
	    	// Wait for next request from the client
			byte[] rdf = responder.recv();
			System.out.println("RDF file received...");				 	
	    	
			// Make a TDB-backed dataset				 
			String directory = tdbDirectory;
			// TODO: need to create the folders before this command
			Dataset dataset = TDBFactory.createDataset(directory) ;
			
			// create an empty model
			Model modelRDF = ModelFactory.createDefaultModel();
			// read the RDF/XML string
			InputStream rdfIS = new ByteArrayInputStream(rdf);			 				
			modelRDF.read(rdfIS, projectURI);
			// begin a writing transaction
			dataset.begin(ReadWrite.WRITE) ;
			// get the model from the triple store
			Model modelTDB = dataset.getDefaultModel() ;
			// get the current size of the triple store
			int datasetSize = modelTDB.getGraph().size();
			// add the triples from the RDF/XML file to the triple store
			modelTDB.add(modelRDF);
			// get the new size of the triple store
			int nbTriplesInserted = modelTDB.getGraph().size() - datasetSize;
			// commit the changes
			dataset.commit();    
			// end the transaction
			dataset.end();
			
			System.out.println("OK: Triples inserted...");
			// Send reply back to client
			String reply = String.valueOf(nbTriplesInserted);
			responder.send(reply.getBytes(), 0);
		    }catch (Exception e){
		    System.out.println("Not OK: Sending errors...");
			// Send reply back to client
			String reply = e.getMessage();
			responder.send(reply.getBytes(), 0);
		    } 
		}
		
	}
}
