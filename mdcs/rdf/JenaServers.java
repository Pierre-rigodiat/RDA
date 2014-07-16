//###############################################################################
//
//File Name: JenaServers.java
//Application: rdf
//Description: 
//
//
//Author:    Guillaume Sousa
//          guillaume.sousa@nist.gov
//Co-Author: Sharief Youssef
//          sharief.youssef@nist.gov
//
//Sponsor: National Institute of Standards and Technology (NIST)
//
//###############################################################################

import com.hp.hpl.jena.query.Dataset;
import com.hp.hpl.jena.tdb.TDBFactory;

public class JenaServers {
	
	/**
	 * Address of the server endpoint
	 * TODO: be sure it is the same address/port as in the client
	 */
	public static String RDFSERVER_ENDPOINT; // = "tcp://127.0.0.1:5555";
	
	/**
	 * Address of the server endpoint
	 * TODO: be sure it is the same address/port as in the client
	 */
	public static String SPARQLSERVER_ENDPOINT; // = "tcp://127.0.0.1:5556";
	
	/**
	 * Path to the triplestore directory
	 */
	public static String TDB_DIRECTORY;
	
	/**
	 * URI of the project
	 * TODO: be sure it is the same project URI as in publisher
	 */
	public static String PROJECT_URI; // = "http://www.example.com/";
	
	
	public static void main(String[] args) throws Exception {
		// JenaServers -rdfserver_endpoint "tcp://127.0.0.1:5555" -sparqlserver_endpoint "tcp://127.0.0.1:5556" -tdb_directory "C:\Users\GAS2\workspace_prod\MGI_Project\mdcs\data\ts" -project_uri "http://www.example.com/"
		if (args.length < 8) {
		    System.out.println("USAGE: rdfserver -rdfserver_endpoint <SERVER_ENDPOINT> -sparqlserver_endpoint <SERVER_ENDPOINT> -tdb_directory <TDB_DIRECTORY> -project_uri <PROJECT_URI>");
		    return;
		} else {
		    for (int i=0;i<8;i=i+2) {
			if (args[i].equals("-rdfserver_endpoint")) {
			    RDFSERVER_ENDPOINT = args[i+1];
			    //System.out.println("server endpoint assigned");
			} else if (args[i].equals("-sparqlserver_endpoint")) {
			    SPARQLSERVER_ENDPOINT = args[i+1];
			    //System.out.println("server endpoint assigned");
			} else if (args[i].equals("-tdb_directory")) {
			    TDB_DIRECTORY = args[i+1];
			    //System.out.println("tdb assigned");
			} else if (args[i].equals("-project_uri")){
			    PROJECT_URI = args[i+1];
			    //System.out.println("project uri assigned");
			} else {
				System.out.println("USAGE: rdfserver -rdfserver_endpoint <SERVER_ENDPOINT> -sparqlserver_endpoint <SERVER_ENDPOINT> -tdb_directory <TDB_DIRECTORY> -project_uri <PROJECT_URI>");
			    return;
			}
		    }
		}
		
		
		// Make a TDB-backed dataset				 
		String directory = TDB_DIRECTORY;
		// TODO: need to create the folders before this command
		Dataset dataset = TDBFactory.createDataset(directory) ;
		dataset.end();
		
		RdfServer rdfServer = new RdfServer(RDFSERVER_ENDPOINT, TDB_DIRECTORY, PROJECT_URI);
		Thread rdfServerThread = new Thread(rdfServer);
		rdfServerThread.start();
		
		SparqlServer sparqlServer = new SparqlServer(SPARQLSERVER_ENDPOINT, TDB_DIRECTORY);
		Thread sparqlServerThread = new Thread(sparqlServer);
		sparqlServerThread.start();
	}
}