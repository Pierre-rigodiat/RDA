<?php
// XXX Avoid infinite includes in lib
require_once 'lib/XmlParserFunctions.php';
//require_once 'lib/StringFunctions.php';

/**
 * An XSD Parser able to generate several element:
 *  - an XML form to fill in
 * 	- an XML file
 * TODO Configure the debugging
 * TODO Rewrite the parser
 * TODO Clean the array from unused data (parent, SEQUENCE, COMPLEXTYPE, SCHEMA...)
 *
 */
class XsdParser {
	private $DEBUG;
	private $loggerInstance;
	private $xsdFile;

	private $elementList;
	private $contentList;
	private $repeatedElement;
	private $namespace;
	private $root;
	private $hasElementToDiscover;
	private $xmlString;
	private $level;
	private $path;

	// TODO Check datatype to avoid PHP errors using of this class
	public function __construct()
	{
		$num_args=func_num_args();

		switch($num_args)
		{
			case 1:
				// file name + no debug
				$this->xsdFile = func_get_arg(0);
				$this->DEBUG = false;

				break;
			case 2:
				// file name + debug
				$this->xsdFile = func_get_arg(0);
				$this->DEBUG = func_get_arg(1);

				break;
			case 3:
				// element list + root element + namespace + no debug
				$this->elementList = func_get_arg(0);
				$this->root = func_get_arg(1);
				$this->namespace = func_get_arg(2);
				$this->DEBUG = false;

				break;
			case 4:
				// element list + root element + namespace + debug
				$this->elementList = func_get_arg(0);
				$this->root = func_get_arg(1);
				$this->namespace = func_get_arg(2);
				$this->DEBUG = func_get_arg(3);

				break;
			default:
				break;
		}

		// XXX Debug not working yet
		if($this->DEBUG)
			$this->loggerInstance = new Logger(/*'logs/xmlparser.log'*/);
			
		return;
	}

	/**
	 *
	 */
	public function parse() {
		global $level, $id, $stack, $elementList;

		// Initialize the XML parser
		$parser=xml_parser_create();

		// Set handlers (see /lib/XmlParserFunctions)
		xml_set_element_handler($parser,"start","stop");
		xml_set_character_data_handler($parser,"char");

		$fp=fopen($this->xsdFile,"r");

		// Read data
		while ($data=fread($fp,4096))
		{
			xml_parse($parser,$data,feof($fp)) or
			die (sprintf("XML Error: %s at line %d",
					xml_error_string(xml_get_error_code($parser)),
					xml_get_current_line_number($parser)));
		}

		//Free the XML parser
		xml_parser_free($parser);

		fclose($fp);

		return $elementList;
	}

	/**
	 *
	 * @param unknown_type $elementId
	 */
	private function completeChildrenList($elementId)
	{
		$currentElement = $this->elementList[$elementId];
		/*echo 'TEst: ';
		 print_r($currentElement);
		echo '<br/>';*/
		$attributesArray = $currentElement['attributes'];

		// If the element is not yet linked to the children list
		if(isset($attributesArray['TYPE']) && !startsWith($attributesArray['TYPE'], $this->namespace) && sizeof($currentElement['children'])==0)
		{
			$this->hasElementToDiscover = true;

			/*if(isset($_GET['debug']))
			 {*/
			//echo 'Completing '.$attributesArray['NAME'].'(type='.$attributesArray['TYPE'].')...<br/>';
			//}

			foreach($this->elementList as $searchedElement)
			{
				if(isset($searchedElement['attributes']['NAME']) && $searchedElement['attributes']['NAME']==$attributesArray['TYPE']
						&& !isset($searchedElement['attributes']['TYPE']) && $searchedElement['name']==strtoupper($this->namespace)."COMPLEXTYPE")
				{
					array_push($this->elementList[$elementId]['children'], $searchedElement['id']);

					/*if(isset($_GET['debug']))
					 {*/
					 //echo 'Found '.$searchedElement['attributes']['NAME'].'(id='.$searchedElement['id'].')...<br/>';
					/*}*/
				}
			}
		}

		if(sizeof($currentElement['children'])==0)
		{
			return;
		}
		else
		{
			foreach($currentElement['children'] as $child)
			{
				$this->completeChildrenList($child);
			}
		}
	}

	/**
	 *
	 * @param unknown_type $elementId
	 */
	private function organizeTree($elementId)
	{
		//global $elementList, $namespace, $level;

		$element = $this->elementList[$elementId];

		if(!isset($element['attribute']['TYPE']) || !startsWith($element['attribute']['TYPE'], $this->namespace))
		{
			$this->level+=1;
			//echo '****LEVEL DOWN****<br/>';
		}

		if($element['name']!=strtoupper($this->namespace).'COMPLEXTYPE' && $element['name']!=strtoupper($this->namespace).'SEQUENCE')
		{
			$elementName = ucfirst($this->elementList[$elementId]['attributes']['NAME']);
			$this->elementList[$elementId]['attributes']['NAME']=$elementName;
				
			$attributes = serialize($this->elementList[$elementId]['attributes'] + array("id" => $elementId));
				
			/*echo $elementId.' -- '.($level/3).' -- '.$elementList[$elementId]['name'].' -- ';
			 print_r($elementList[$elementId]['attributes']);*/
			//echo '<a href="">+</a> <a href="">-</a>';
				
			echo $elementName;
			//print_r($this->elementList[$elementId]['attributes']);
			echo ' '.$attributes;
				
			/*$index = 0;
			 foreach($this->elementList[$elementId]['attributes'] as $attr)
			 {
			if($attributesNameArray[$index]!="NAME")
			{
			if($attributesNameArray[$index]=="TYPE" && startsWith($attr, strtolower($this->namespace)))
			{
			$type = explode(":", $attr);
			echo ' --TYPE='.$type[1].'--';
			echo '<input type="hidden" id="attr[TYPE]['.$elementName.']" name="attr[type]['.$elementName.']" value="'.$type[1].'">';
			}
			else if($attributesNameArray[$index]!="TYPE")
			{
			echo ' --'.$attributesNameArray[$index].'='.$attr.'--';
			echo '<input type="hidden" id="attr['.$attributesNameArray[$index].']['.$elementName.']" name="attr['.$attributesNameArray[$index].']['.$elementName.']" value="'.$attr.'">';
			}
			}

			$index+=1;
			}*/

			if($elementId!=$this->root)
			{
				echo ' <a href="#edition_popup" onclick="configurePopUp(\''.htmlspecialchars($attributes).'\')">Edit</a>';
			}

		}

		if(sizeof($this->elementList[$elementId]['children'])==0)
		{
			$this->level-=1;

			//echo '****LEVEL UP****<br/>';
			return;
		}
		else
		{
			if($this->level%3==0) echo '<ul>';

			foreach($this->elementList[$elementId]['children'] as $child)
			{
				if($this->level%3==2) echo '<li>';
					
				$this->organizeTree($child);
					
				if($this->level%3==2) echo '</li>';
			}

			if($this->level%3==0) echo '</ul>';

			$this->level-=1;

		}
	}


	/**
	 * Build the validation page which will create the form
	 *
	 * XXX It will create the XSD form configuration
	 */
	public function buildForm()
	{
		$this->elementList = $this->parse();
		//print_r($this->elementList);

		$this->namespace = null;
		$this->root = -1;

		// Cleaning the array and identifying the important element
		foreach($this->elementList as $element)
		{
			if($this->namespace==null && $element['parent'] == -1)
			{
				/* Trying to find the namespace name */
				foreach(array_keys($element['attributes']) as $key)
				{
					if($element['attributes'][$key] == 'http://www.w3.org/2001/XMLSchema')
					{
						$key_part = explode(':', $key);
						$this->namespace = strtolower($key_part[1]).':';
					}
				}

				/*if(isset($_GET['debug']))
				 {*/
				echo $this->namespace . ' is the schema namespace<br/>';
				//}
			}
			else if($element['parent'] == 0)
			{
				if($element['name']==strtoupper($this->namespace).'ELEMENT')
				{
					$this->root = $element['id'];

					/*if(isset($_GET['debug']))
					 {*/
					echo $element['attributes']['NAME'] . ' (id=' . $element['id'] . ') is the root element<br/>';
					/*}*/
					break;
				}
			}
		}

		$this->hasElementToDiscover = true;

		// Linking every element
		while($this->hasElementToDiscover)
		{
			//echo 'Lol TEST<br/>';
			$this->hasElementToDiscover = false;
			$this->completeChildrenList($this->root);

			//flush();
		}

		$this->level=-1;
		$this->organizeTree($this->root);

		return;
	}

	public function displayForm()
	{
		$this->level=-1;
		$this->organizeTree($this->root);

		return;
	}



	/**
	 * This function build the entire HTML form
	 *
	 * TODO Change the function name
	 * @param unknown_type $elementId
	 */
	private function organizeTree2($elementId)
	{
		//global $elementList, $namespace, $level;

		$element = $this->elementList[$elementId];

		if(!isset($element['attribute']['TYPE']) || !startsWith($element['attribute']['TYPE'], $this->namespace))
		{
			$this->level+=1;
			//echo '****LEVEL DOWN****<br/>';
		}

		if($element['name']!=strtoupper($this->namespace).'COMPLEXTYPE' && $element['name']!=strtoupper($this->namespace).'SEQUENCE')
		{
			//if($this->level%3==2) echo '<li>';
			echo '<div class="'.$elementId.'">';
				
				
			$elementName = ucfirst($this->elementList[$elementId]['attributes']['NAME']);
			$this->elementList[$elementId]['attributes']['NAME']=$elementName;

			$attributes = serialize($this->elementList[$elementId]['attributes'] + array("id" => $elementId));

			/*echo $elementId.' -- '.($level/3).' -- '.$elementList[$elementId]['name'].' -- ';
			 print_r($elementList[$elementId]['attributes']);*/
			//echo '<a href="">+</a> <a href="">-</a>';

			echo $elementName.': ';
			//print_r($this->elementList[$elementId]['attributes']);
			echo ' '.$attributes;

			if(startsWith($this->elementList[$elementId]['attributes']['TYPE'], $this->namespace))
			{
				echo ' <input type="text" name="'.$this->path.'-0" id="'.$this->path.'-0" value="xxx"/>'; // XXX We need to specifie the id and name of this element;
			}
				
				
			// XXX What if minoccurs > 1 ???
			// XXX What if maxoccurs == 0
			// XXX The base64 number is computed every time we must reduce that
			if(isset($this->elementList[$elementId]['attributes']['MAXOCCURS']) && $this->elementList[$elementId]['attributes']['MAXOCCURS']!=1)
			{
				echo '<input type="hidden" name="maxoccurs" id="maxoccurs" value="'.$this->elementList[$elementId]['attributes']['MAXOCCURS'].'"/>';
				echo ' <img src="data:image/gif;base64,'.getIconBase64(0, 1)/*getIconBase64(1, 3)*//*getIconBase64(13, 11)*/.'" alt="add" class="addItem"/>';
			}
				
			if(isset($this->elementList[$elementId]['attributes']['MINOCCURS']) && $this->elementList[$elementId]['attributes']['MINOCCURS']!=1)
			{
				echo '<input type="hidden" name="minoccurs" id="minoccurs" value="'.$this->elementList[$elementId]['attributes']['MINOCCURS'].'"/>';
				echo ' <img src="data:image/gif;base64,'.getIconBase64(7, 14).'" alt="remove" class="removeItem"/>';
			}
				
			// TODO Handle auto-generated items
				
			echo '</div>';

		}

		if(sizeof($this->elementList[$elementId]['children'])==0)
		{
			$this->level-=1;
				
			// TODO Do a path function for that
			$lastPathElement =  strrpos($this->path, '/') - strlen($this->path);
			$this->path = substr($this->path, 0, $lastPathElement);

			//echo '****LEVEL UP****<br/>';
			return;
		}
		else
		{
			if($this->level%3==0) echo '<ul>';

			foreach($this->elementList[$elementId]['children'] as $child)
			{
				//if($this->level%3==2) echo '<li class="'.$this->level.'">';
				if($this->level%3==2) echo '<li>';

				$this->path .= '/'.$child;

				$this->organizeTree2($child);
					
				if($this->level%3==2) echo '</li>';
			}

			if($this->level%3==0) echo '</ul>';

			$this->level-=1;
				
			// TODO Do a path function for that
			$lastPathElement =  strrpos($this->path, '/') - strlen($this->path);
			$this->path = substr($this->path, 0, $lastPathElement);

		}
	}



	public function buildHTML()
	{
		$this->level=-1;
		$this->path=$this->root;
		$this->organizeTree2($this->root);

		return null;
	}


	private function displayXMLELement($elementId)
	{
		$element = $this->elementList[$elementId];

		$repeat = 1;
		//print_r($element);

		if(isset($this->repeatedElement['e'.$elementId]))
		{
			$repeat = $this->repeatedElement['e'.$elementId];
		}


		// TODO Take the number of element in account
		if(!isset($element['attribute']['TYPE']) || !startsWith($element['attribute']['TYPE'], $this->namespace))
		{
			$this->level+=1;
			//echo '****LEVEL DOWN****<br/>';
		}
		
		if(sizeof($element['children'])==0)
		{
			$keys_array = preg_grep('`^'.str_replace('/', '\/', $this->path).'\-`', array_keys($this->contentList));
			$keys_array = array_values($keys_array);
			
			/*echo $this->path.' == ';
			print_r($keys_array);
			echo '<br/>';*/
		}

		for($i=0; $i < $repeat; $i++)
		{
			if(sizeof($element['children'])==0)
			{					
				$this->xmlString .= '<'.$element['attributes']['NAME'].'>'.$this->contentList[$keys_array[0]].'</'.$element['attributes']['NAME'].'>';					
				unset($this->contentList[$keys_array[0]]);
				
				$this->level-=1;

				

				//echo '****LEVEL UP****<br/>';
					
				//return;
			}
			else
			{	
				if($element['name']!=strtoupper($this->namespace).'COMPLEXTYPE' && $element['name']!=strtoupper($this->namespace).'SEQUENCE')
				{
					$this->xmlString .= '<'.$element['attributes']['NAME'].'>';
				}

				foreach($this->elementList[$elementId]['children'] as $child)
				{
					$this->path .= '/'.$child;

					$this->displayXMLELement($child);
				}

				if($element['name']!=strtoupper($this->namespace).'COMPLEXTYPE' && $element['name']!=strtoupper($this->namespace).'SEQUENCE')
				{
					$this->xmlString .= '</'.$element['attributes']['NAME'].'>';
				}

				$this->level-=1;
					
				// TODO Do a path function for that
				/*$lastPathElement =  strrpos($this->path, '/') - strlen($this->path);
				$this->path = substr($this->path, 0, $lastPathElement);	*/
			}
		}
		
		// TODO Do a path function for that
		$lastPathElement =  strrpos($this->path, '/') - strlen($this->path);
		$this->path = substr($this->path, 0, $lastPathElement);
		
		//unset($this->repeatedElement['e'.$elementId]);
	}

	/**
	 *
	 * @param array $xmlContent
	 */
	public function buildXML(array $xmlContent, array $repeatedElement)
	{
		$this->level=-1;
		$this->path=$this->root;

		$this->contentList = $xmlContent;

		$this->repeatedElement = $repeatedElement; // XXX Memory management needed

		$this->xmlString = '';

		$this->displayXMLELement($this->root);

		return $this->xmlString;
	}


	/**
	 * Getter for the elementList
	 * @return The current list of all elements
	 */
	public function getElementList()
	{
		return $this->elementList;
	}

	/**
	 * Replace the current list of all element by another one
	 * @param Array $newElementList
	 * @return null
	 */
	// TODO Control the content of the list
	public function setElementList($newElementList)
	{
		$this->elementList = $newElementList;
	}

	/**
	 *
	 */
	public function getRoot()
	{
		return $this->root;
	}

	// TODO Control the format of the root
	public function setRoot($newRoot)
	{
		$this->root = $newRoot;
	}

	public function getNamespace()
	{
		return $this->namespace;
	}

	// TODO Control the namespace format
	// If it ends by : we had to remove it...
	public function setNamespace($newNamespace)
	{
		$this->namespace = $newNamespace;
	}
}
?>