//###############################################################################
//
// File Name: sparqlserver.java
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


public class sparqlserver {
	
  //TODO: be sure it is the same address/port as in the client
  public static String SERVER_ENDPOINT; // = "tcp://127.0.0.1:5556";
	
  // TODO: replace by the real folder name in the project
  public static String TDB_DIRECTORY; // = "C:\Users\GAS2\workspace_prod\MGI_Project\mdcs\data\ts";
	
  // sparqlserver -server_endpoint "tcp://127.0.0.1:5556" -tdb_directory "C:\Users\GAS2\workspace_prod\MGI_Project\mdcs\data\ts"
  public static void main(String[] args) throws Exception {
		if (args.length < 4) {
		    System.out.println("USAGE: sparqlserver -server_endpoint <SERVER_ENDPOINT> -tdb_directory <TDB_DIRECTORY>");
		    return;
		} else {
		    for (int i=0;i<4;i=i+2) {
			if (args[i].equals("-server_endpoint")) {
			    SERVER_ENDPOINT = args[i+1];
			    //System.out.println("server endpoint assigned");
			} else if (args[i].equals("-tdb_directory")) {
			    TDB_DIRECTORY = args[i+1];
			    //System.out.println("tdb assigned");
			} else {
			    System.out.println("USAGE: sparqlserver -server_endpoint <SERVER_ENDPOINT> -tdb_directory <TDB_DIRECTORY>");
			    return;
			}
		    }
		}
		System.out.println("SPARQL server launched...");
	
		//TODO: be sure it is the same context number as in the client
		ZMQ.Context context = ZMQ.context(7);
		// Socket to talk to clients
		ZMQ.Socket responder = context.socket(ZMQ.REP);		 
		responder.bind(SERVER_ENDPOINT);
			 
		while (true) {
		    try{ 
				// Wait for next request from the client
				byte[] queryBytes = responder.recv();
				System.out.println("Received SPARQL query");
				String queryStr = new String(queryBytes, "UTF-8");
				char format = queryStr.charAt(0);
				System.out.println(queryStr);
				System.out.println(format);
				queryStr = queryStr.substring(1);
				System.out.println(queryStr);
				Query query = QueryFactory.create(queryStr);
				
				// Make a TDB-backed dataset				 
				String directory = TDB_DIRECTORY;
				// TODO: need to create the folders before this command
				Dataset dataset = TDBFactory.createDataset(directory) ;
			
				// begin a reading transaction
				dataset.begin(ReadWrite.READ) ;
				// get the model from the triple store
				Model modelTDB = dataset.getDefaultModel();
				
				QueryExecution qexec = QueryExecutionFactory.create(query, modelTDB);
				try {
					ResultSet results = qexec.execSelect();	
					//0: TEXT
					//1: XML
					//2: CSV
					//3: TSV
					//4: JSON
					if (format == '1'){
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
				} 
				finally {
					// close the query execution
					qexec.close();
					// end the transaction
					dataset.end();
				}
		    }catch (Exception e){
			// Send reply back to client
			String reply = e.getMessage();
			responder.send(reply.getBytes(), 0);
		    } 
		}
  }
}