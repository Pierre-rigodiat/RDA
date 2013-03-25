<?php

/**
 * Mongodb Class
 * @param $username: the user name to access the database
 * @param $password: the user password to access the database
 * @param $server: the server ip address
 * @param $port: the port number to access the server
 * @param $database: the database name
 */
Class MongoDBStream
{

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
	function __construct()
	{
		$argc = func_num_args();
		$argv = func_get_args();

		switch($argc)
		{
			case 0 :
				$this -> server = "127.0.0.1";
				$this -> port = 27017;
				break;
			case 1 :
				$this -> server = $argv[0];
				$this -> port = 27017;
				break;
			case 2 :
				$this -> server = $argv[0];
				$this -> port = 27017;
				$this -> databaseName = $argv[1];
				;
				break;
			case 3 :
				$this -> server = $argv[0];
				$this -> port = 27017;
				$this -> username = $argv[1];
				$this -> password = $argv[2];
				break;
			case 4 :
				$this -> server = $argv[0];
				$this -> port = 27017;
				$this -> databaseName = $argv[1];
				$this -> username = $argv[2];
				$this -> password = $argv[3];
				break;
			case 5 :
				$this -> server = $argv[0];
				$this -> databaseName = $argv[1];
				$this -> port = $argv[2];
				$this -> username = $argv[3];
				$this -> password = $argv[4];
				break;
			default :
				echo "Invalid argument number: Should be more than 5\n";
				break;
		}

		$this -> connect();
	}

	public function getDatabaseName()
	{
		return $this -> databaseName;
	}

	public function getDatabaseObject()
	{
		return $this -> databaseObject;
	}

	public function getConnection()
	{
		return $this -> connection;
	}

	public function setDatabaseName($databaseName)
	{
		$this -> databaseName = $databaseName;
	}

	function getCollection($collectionName)
	{
		return new MongoCollection($this -> databaseObject, $collectionName);
	}

	/**
	 * Method to connect to the mongod instance
	 */
	private function connect()
	{
		try
		{
			// Attempt to connect with a persistent connection. Must be used as it enhances database performance
			if (!($this -> username == null || $this -> password == null))
				$connection = new Mongo("mongodb://{$this->username}:{$this->password}@{$this->server}:{$this->port}");
			else
				$connection = new Mongo("mongodb://{$this->server}:{$this->port}");
			$this -> connection = $connection;
		}
		catch (MongoConnectionException $e)
		{
			echo "Cannot connect to {$this->server}:{$this->port}\n";
		}
	}

	/**
	 * Method to connect to the database
	 */
	public function openDB()
	{
		try
		{
			// Attempt to connect with a persistent connection. Must be used as it enhances database performance
			if (isset($this -> databaseName) && isset($this -> connection) && trim($this -> databaseName) != "")
				$this -> databaseObject = new MongoDB($this -> connection, $this -> databaseName);
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
	function insertJsonFromFile($doc, $collectionName)
	{
		if (!preg_match('/.+\.json/', $doc))
		{
			echo 'Please select a JSON file for the insertion<br/>';
			return;
		}
		else
		{
			// Get the JSON file content
			$jsonString = file_get_contents($doc);
			insertJson($jsonString, $collectionName);
		}
	}

	/**
	 *
	 * @param string $jsonString
	 * @param string $collectionName
	 */
	function insertJson($jsonArray, $collectionName)
	{
		// Insert it into the collection
		if (isset($this -> databaseObject))
		{
			$collectionObject = new MongoCollection($this -> databaseObject, $collectionName);
			$collectionObject -> save($jsonArray, array("w" => 1));
		}
		else
		{
			throw new Exception("Database Object not set", -1);
		}
	}

	/**
	 * Method to insert a XML document into the database, used as a test function. Do not use in production.
	 * @param $doc: string that describe the path of the file
	 * @param $collection: the collection in which the document is pushed
	 */
	function insertXml($doc, $collectionName)
	{
		if (!preg_match('/.+\.xml/', $doc))
		{
			echo 'Please select an XML file for the insertion<br/>';
			return;
		}
		else
		{
			$dom = DOMDocument::load($doc);
			// Translate the XML content into JSON content
			$jsonArray = encodeJSONML($dom);

			if ($jsonArray == array())
			{
				echo "Could not transform xml to json<br/>";
				return;
			}

			// Insert it into the collection
			//print_r($jsonArray); echo "<br/>";
			//echo json_encode($jsonArray)."<br/>";
			//insertJson($jsonArray, $collectionName);
		}
	}

	function retrieveXml($doc, $collectionName)
	{
		$json_data = file_get_contents($doc);

		$xmlContents = decodeJSONML($json_data);
		if (!$xmlContents)
		{
			echo "Could not transform json to xml";
			return;
		}

		echo nl2br(htmlspecialchars($xmlContents -> saveXML()));
		//file_put_contents("xmlBadger.xml", $xmlContents->saveXML());
		return;
	}

	function queryData($query, $collectionName)
	{
		try
		{
			if (isset($this -> databaseObject))
			{
				$collectionObject = new MongoCollection($this -> databaseObject, $collectionName);
				//Execute the query
				return $collectionObject -> find($query, array('_id' => 0));
			}
			else
			{
				throw new Exception("Database Object not set", -2);
			}
		}
		catch(MongoCursorException $e)
		{
			throw new Exception("Issue with the query", -1);
		}
	}

}
?>