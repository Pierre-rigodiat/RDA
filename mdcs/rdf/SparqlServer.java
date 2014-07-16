//###############################################################################
//
// File Name: SparqlServer.java
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

import java.io.ByteArrayOutputStream;
import java.io.OutputStream;

import org.zeromq.ZMQ;

import com.hp.hpl.jena.query.* ;
import com.hp.hpl.jena.sparql.resultset.CSVOutput;
import com.hp.hpl.jena.sparql.resultset.JSONOutput;
import com.hp.hpl.jena.sparql.resultset.TSVOutput;
import com.hp.hpl.jena.tdb.TDBFactory;
import com.hp.hpl.jena.query.Dataset;
import com.hp.hpl.jena.query.ReadWrite;
import com.hp.hpl.jena.rdf.model.Model;


public class SparqlServer implements Runnable {
	
	/**
	 * Address of the server endpoint
	 */
	private String serverEndpoint;
	
	/**
	 * Path to the triplestore directory
	 */
	private String tdbDirectory;

	public SparqlServer(String serverEndpoint, String tdbDirectory){
		this.serverEndpoint = serverEndpoint;
		this.tdbDirectory = tdbDirectory;
	}
	
	@Override
	public void run() {
		System.out.println("SPARQL server launched...");
		
		//TODO: be sure it is the same context number as in the client
		ZMQ.Context context = ZMQ.context(7);
		// Socket to talk to clients
		ZMQ.Socket responder = context.socket(ZMQ.REP);		 
		responder.bind(serverEndpoint);
			 
		while (true) {
		    try{ 
				// Wait for next request from the client
				byte[] queryBytes = responder.recv();
				System.out.println("SPARQL query received...");
				String queryStr = new String(queryBytes, "UTF-8");
				char format = queryStr.charAt(0);
				queryStr = queryStr.substring(1);
				System.out.println(queryStr);
				Query query = QueryFactory.create(queryStr);
				
				// Make a TDB-backed dataset				 
				String directory = tdbDirectory;
				// TODO: need to create the folders before this command
				Dataset dataset = TDBFactory.createDataset(directory) ;
			
				// begin a reading transaction
				dataset.begin(ReadWrite.READ) ;
				// get the model from the triple store
				Model modelTDB = dataset.getDefaultModel();
				
				QueryExecution qexec = QueryExecutionFactory.create(query, modelTDB);	
				try{
					System.out.println("Execute SPARQL query...");
					ResultSet results = qexec.execSelect();		
					System.out.println("OK: Sending results...");
					//0: TEXT
					//1: XML
					//2: CSV
					//3: TSV
					//4: JSON
					if (format == '0'){
						String reply = ResultSetFormatter.asText(results);
						responder.send(reply.getBytes(), 0);
					}
					else if (format == '1'){
						String reply = ResultSetFormatter.asXMLString(results);
						responder.send(reply.getBytes(), 0);
					}else if (format == '2'){
						CSVOutput csvOutput = new CSVOutput();
						ByteArrayOutputStream os = new ByteArrayOutputStream();
						csvOutput.format(os, results);
						responder.send(os.toByteArray(), 0);
					}else if (format == '3'){
						TSVOutput tsvOutput = new TSVOutput();
						ByteArrayOutputStream os = new ByteArrayOutputStream();
						tsvOutput.format(os, results);
						responder.send(os.toByteArray(), 0);
					}else if (format == '4'){
						JSONOutput jsonOutput = new JSONOutput();
						ByteArrayOutputStream os = new ByteArrayOutputStream();
						jsonOutput.format(os, results);
						responder.send(os.toByteArray(), 0);
					}else{
						String reply = ResultSetFormatter.asText(results);
						responder.send(reply.getBytes(), 0);
					}
				}finally{
			    	// close the query execution
					qexec.close();	
					// end the transaction
					dataset.end();
			    }		
		    }catch (Exception e){
		    	System.out.println("Not OK: Sending errors...");
		    	// Send reply back to client
		    	String reply = e.getMessage();
		    	responder.send(reply.getBytes(), 0);
		    }
		}

	}
}