<?php

/**
 * Mongodb Class
 * @param $username: the user name to access the database
 * @param $password: the user password to access the database
 * @param $server: the server ip address
 * @param $port: the port number to access the server
 * @param $database: the database name
 */
Class MongoDBStream {

private $server;
private $databaseName;
private $username;
private $password;
private $port;
private $connection;
private $databaseObject;


	/**
	 * Class constructor
 	 */
	function __construct() {
		$argc = func_num_args();
		$argv = func_get_args();
		
		switch($argc) {
			case 0:
				$this->server = "127.0.0.1";
				$this->port = 27017;
			case 1:
				$this->server = $argv[0];
				$this->port = 27017;
				break;
			case 2:
				$this->server = $argv[0];
				$this->port = 27017;
				$this->databaseName = $argv[1];;
				break;
			case 3:
				$this->server = $argv[0];
				$this->port = 27017;
				$this->username = $argv[1];
				$this->password = $argv[2];
				break;
			case 4:
				$this->server = $argv[0];
				$this->port = 27017;
				$this->databaseName = $argv[1];
				$this->username = $argv[2];
				$this->password = $argv[3];
				break;
			case 5:
				$this->server = $argv[0];
				$this->databaseName = $argv[1];
				$this->port = $argv[2];
				$this->username = $argv[3];
				$this->password = $argv[4];
				break;
			default:
				echo "Invalid argument number: Should be more than 5\n";
				break;
		}
		
		$this->connect();
	}
	
	public function getDatabaseName() {
		return $this->databaseName;
	}
	
	public function getDatabaseObject() {
		return $this->databaseObject;
	}
	
	public function getConnection() {
		return $this->connection;
	}
	
	public function setDatabaseName($databaseName) {
		$this->databaseName = $databaseName;
	}
	
	function getCollection($collectionName) {
		return new MongoCollection($this->databaseObject, $collectionName);
	}
	
	/**
	 * Method to connect to the mongod instance
	 */
	private function connect() {
		try
		{
			// Attempt to connect with a persistent connection. Must be used as it enhances database performance
			if (!($this->username == null || $this->password == null))
				$connection = new Mongo("mongodb://{$this->username}:{$this->password}@{$this->server}:{$this->port}");
			else
				$connection = new Mongo("mongodb://{$this->server}:{$this->port}");
			$this->connection = $connection;
		}
		catch (MongoConnectionException $e)
		{
			echo "Cannot connect to {$this->server}:{$this->port}\n";
		}
	}
	
	/**
	 * Method to connect to the database
	 */
	public function openDB() {
		try
		{
			// Attempt to connect with a persistent connection. Must be used as it enhances database performance
			if (isset($this->databaseName) && isset($this->connection) && trim($this->databaseName) != "")
				$this->databaseObject=new MongoDB($this->connection,$this->databaseName);
			else
			{
				echo "Database Name not set\n";
				return;
			}
		}
		catch (Exception $e)
		{
			echo "Cannot connect to {$this->databaseName} database\n";
			return;
		}		
	}
// There is no explicit need to disconnect from the database

	/**
	 * Method to insert a JSON document into the database
	 * @param $doc: string that describe the path of the file
	 * @param $collection: the collection in which the document is pushed
	 */
	function insertJson($doc, $collectionName) {
		if (!preg_match('/.+\.json/', $doc))
		{
			echo 'Please select a JSON file for the insertion\n';
			return;
		}
		else
			{
			// Get the JSON file content
			$jsonString = file_get_contents($doc);
			$jsonContents = file($doc);
			if (!$jsonContents || !$jsonString)
				{
					echo "Cannot load {$doc} file\n";
					return;
				}

			// Insert it into the collection
			try
			{
				if (isset($this->databaseObject)) {
				$collectionObject = new MongoCollection($this->databaseObject, $collectionName);
				//Check if the element already exists
				$cursor = $collectionObject->find(array("0" => $jsonString));
				if (!$cursor->hasNext()) {
					$collectionObject->insert($jsonContents, array("safe" => 1));
					echo "Document inserted";
				}
				else
				{
					echo "Cannot insert an already stored document\n";
					return;
				}
				//Display the element of the query. Used for debugging
				/*foreach ($cursor as $element)
				var_dump($element);
				$collectionObject->remove($jsonContents);*/
				}
				else
				{
					echo "Database Object not set\n";
					return;
				}
			}
			catch(MongoCursorException $e)
			{
				echo "Cannot insert an already stored document\n";
			}
			}
	}

	/**
	 * Method to insert a XML document into the database
	 * @param $doc: string that describe the path of the file
	 * @param $collection: the collection in which the document is pushed
	 */
	function insertXml($doc, $collectionName) {
		if (!preg_match('/.+\.xml/', $doc))
		{
			echo 'Please select an XML file for the insertion\n';
			return;
		}
		else
			{
			// Get the XML file content
			//$xmlContents = file_get_contents($doc);
			/*$patterns = array();
			$patterns[0] = '/xsd:/';
			$patterns[1] = '/hdf5:/';
			$replacements = array();
			$replacements[0] = 'xsd_';
			$replacements[1] = 'hdf5_';
			$insertedXml = preg_replace($patterns, $replacements, $xmlContents);
			if (!$xmlContents || !$insertedXml) {
				echo "Cannot load {$doc} file\n";
				return;
			}*/
			$dom=DOMDocument::load($doc);
			// Translate the XML content into JSON content
			//$jsonContents = xml2jsonIBM::transformXmlStringToJson($xmlContents);
			$jsonContents = BadgerFish::encode($dom);
			
			//file_put_contents("test_dump.txt", $dom->saveXML());
			
			if (!$jsonContents) {
				echo "Could not transform xml to json\n";
				return;
			}
			$jsonArray = array();
			$jsonArray = str_split($jsonContents, strlen($jsonContents));

			// Insert it into the collection
			var_dump($jsonContents);
			echo $jsonContents."\n";
			/*try
			{ 
				if (isset($this->databaseObject)) {
				$collectionObject = new MongoCollection($this->databaseObject, $collectionName);
				//Check if the element already exists
				$cursor = $collectionObject->find(array("0" => $jsonContents));
				if (!$cursor->hasNext()){
					$collectionObject->insert($jsonArray, array("safe" => 1));
					echo "Insert successful\n";
					}
				else
				{
					echo "Cannot insert an already stored document\n";
					return;
				}
				}
				else
				{
					echo "Database Object not set\n";
					return;
				}
			}
			catch(MongoCursorException $e)
			{
				echo "Cannot insert an already stored document\n";
			}*/
			}
	}
	
	function retrieveXml($doc, $collectionName) {
		$json_data = file_get_contents($doc);
		
		$xmlContents = BadgerFish::decode($json_data);
		if (!$xmlContents) {
			echo "Could not transform json to xml";
			return;
		}
		
		var_dump($xmlContents);
		var_dump($xmlContents->saveXML());
		return;
	}
	
	
}

?>
