<?php
// XXX Avoid infinite includes in lib
require_once $_SESSION['config']['_ROOT_'].'/inc/classes/helpers/Tree.php';

require_once $_SESSION['config']['_ROOT_'].'/inc/lib/XmlParserFunctions.php';

require_once $_SESSION['config']['_ROOT_'].'/inc/classes/Logger.php';
//require_once 'lib/StringFunctions.php';

/**
 * An XSD Parser able to generate several element:
 *  - an XML form to fill in
 * 	- an XML file
 * TODO Configure the debugging
 * TODO Rewrite the parser (function names, use pointer to apply style, etc)
 * TODO Clean the array from unused data (parent, SEQUENCE, COMPLEXTYPE, SCHEMA...)
 * TODO Use the Tree class
 * TODO Handle several namespaces
 */ 
class XsdParser {
	private $elementPerPage = 30;
	
	private $DEBUG;
	private $loggerInstance;
	private $xsdFile;

	private $elementList;
	private $contentList;
	//private $repeatedElement;
	private $namespace;
	private $root;
	
	private $xmlString; // xxx not sure that it is very useful
	private $actions; // todo maybe remove it
	
	// todo figure out a way to not set those element as class attributes
	private $hasElementToDiscover;
	private $level;
	private $path;

	/**
	 * Parser constructor...
	 * 
	 */
	// TODO Check datatype to avoid PHP errors using of this class
	// TODO Generate error if we do not have the correct number of arguments
	public function __construct()
	{
		// todo remove or handle it elsewhere
		$this->elementPerPage = 20;
		$this->pageNumber = 1;
		$this->currentPage = $this->pageNumber;
		//$this->maxPage = $this->pageNumber;
		$this->elementNumber = 0;
		
		
		/* Checking the number of arguments and instantiating the object */
		$num_args=func_num_args();

		switch($num_args)
		{
			case 1:
				// file name [+ no debug]				
				$this->xsdFile = func_get_arg(0);
				$this->DEBUG = false;
				$this->root = -1;
				$this->namespace = null;

				break;
			case 2:
				// file name + debug
				$this->xsdFile = func_get_arg(0);
				$this->DEBUG = func_get_arg(1);
				$this->root = -1;
				$this->namespace = null;

				break;
			case 3:
				// element list + root element + namespace [+ no debug]
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
		
		/* Build the logger with the appropriate level */
		$level = 'info';
		if($this->DEBUG) $level = 'notice';
		
		try
		{
			$this->loggerInstance = new Logger($level, $_SESSION['config']['_ROOT_'].'/logs/xmlparser.log'); // xxx what if the $_SESSION doesn't exist
		}
		catch (Exception $ex)
		{
			echo '<b>Impossible to build the Logger:</b><br/>'.$ex->getMessage();
		}
		
		$this->loggerInstance->log_debug('XsdParser created', basename(__FILE__));
			
		return;
	}

	/**
	 *
	 */
	private function parse() {
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
	// TODO rename function into linkElements
	private function completeChildrenList($elementId)
	{
		$undisplayableType=array('SIMPLETYPE', 'RESTRICTION');
		
		$currentElement = $this->elementList[$elementId];
		$currentElementName = substr($currentElement['name'], strlen($this->namespace));
		
		if($this->DEBUG) echo "Reading ID".$currentElement['id']."...<br/>";
		
		$attributesArray = $currentElement['attributes'];
		
		// TODO Remove it and correctly handle tables
		if(isset($attributesArray['TYPE']) && $attributesArray['TYPE']=="Table")
		{
			$this->elementList[$elementId]['attributes']['MODULE'] = "tables";
			return;
		}

		// If the element is not yet linked to the children list
		if(isset($attributesArray['TYPE']) && !startsWith($attributesArray['TYPE'], $this->namespace) && sizeof($currentElement['children'])==0)
		{
			$this->hasElementToDiscover = true;
			if($this->DEBUG) echo 'Linking '.$attributesArray['NAME'].'(type='.$attributesArray['TYPE'].')...<br/>';
			
			foreach($this->elementList as $searchedElement)
			{
				// If the element name is the same as the type of the element searched, parent ID and children list is updated
				if(isset($searchedElement['attributes']['NAME']) && $searchedElement['attributes']['NAME']==$attributesArray['TYPE']
						&& !isset($searchedElement['attributes']['TYPE']) && $searchedElement['name']==strtoupper($this->namespace)."COMPLEXTYPE")
				{
					array_push($this->elementList[$elementId]['children'], $searchedElement['id']);
					$this->elementList[$searchedElement['id']]['parent'] = $elementId; // xxx Test if it works well with big schemas
					
					if($this->DEBUG) echo 'Found '.$searchedElement['attributes']['NAME'].'(id='.$searchedElement['id'].')...<br/>';
				}
			}
		}
		
		// todo make the code more generic
		if(in_array($currentElementName,$undisplayableType))
		{
			$parentId = $this->elementList[$elementId]['parent'];
			
			$this->elementList[$parentId]['children'] = $this->elementList[$elementId]['children'];
			
			foreach($this->elementList[$elementId]['children'] as $child)
			{
				$this->elementList[$child]['parent'] = $parentId;
			}
		}
		else if($currentElementName=='ENUMERATION') // todo be more generic
		{
			$parentId = $this->elementList[$elementId]['parent'];
			
			if(!isset($this->elementList[$parentId]['attributes']['CHOICE'])) $this->elementList[$parentId]['attributes']['CHOICE'] = array();
			
			array_push($this->elementList[$parentId]['attributes']['CHOICE'], $this->elementList[$elementId]['attributes']['VALUE']);
			
			$this->elementList[$parentId]['children'] = array();
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
			
			return;
		}
	}
	
	
	// todo remove this from here
	private $elementNumber;
	public $pageNumber;
	private $currentPage;

	/**
	 *
	 * @param unknown_type $elementId
	 */
	// xxx this is a display function
	// xxx put it away
	private function organizeTree($elementId)
	{
		$undisplayableItemName = array('SIMPLETYPE', 'COMPLEXTYPE', 'SEQUENCE', 'RESTRICTION', 'ENUMERATION');
		
		if(!defined("filter_attribute")) // Avoid to redefine the function
		{
			define("filter_attribute", true);
			
			function filter_attribute($var)
			{
				$attr_not_disp = array('NAME', 'id', 'TYPE'); // TYPE is first removed but if needed it will be pushed into the array			
				return !in_array($var, $attr_not_disp);
			}
		}

		$element = $this->elementList[$elementId];
		$elementName = substr($element['name'], strlen($this->namespace));
		
		if(!isset($element['attribute']['TYPE']) || !startsWith($element['attribute']['TYPE'], $this->namespace))
		{
			$this->level+=1;
			//echo '****LEVEL DOWN****<br/>';
		}

		if(!in_array($elementName, $undisplayableItemName))
		{
			$elementName = ucfirst($this->elementList[$elementId]['attributes']['NAME']);
			$this->elementList[$elementId]['attributes']['NAME']=$elementName;
				
			$this->elementList[$elementId]['attributes'] += array("id" => $elementId);
			$attributes = serialize($this->elementList[$elementId]['attributes']);
				
			/*echo $elementId.' -- '.($level/3).' -- '.$elementList[$elementId]['name'].' -- ';
			 print_r($elementList[$elementId]['attributes']);*/
			//echo '<a href="">+</a> <a href="">-</a>';
				
			if($elementId==$this->root) echo '<h5>'.$elementName.'</h5>';
			else 
			{
				$this->elementNumber = $this->elementNumber + 1; // todo remove
				
				echo '<b>'.$elementName.'</b>';
				
				echo '<span class="hide">'.$elementId.'</span>'; // XXX see if there is another way to do it or not
			
				// Displays attributes on the first page
				echo ' <span class="attr">'; // XXX The display is not really adaptable.... Use a function apply_style or smth
				
	
				$attr_name_array = array_filter(array_keys($this->elementList[$elementId]['attributes']), "filter_attribute");
				$type_attr = array();
				
				if(isset($this->elementList[$elementId]['attributes']['TYPE']) && startsWith($this->elementList[$elementId]['attributes']['TYPE'], $this->namespace))
				{
					// Attribute type is truncated
					$type_attr = explode(':', $this->elementList[$elementId]['attributes']['TYPE']);				
					array_push($attr_name_array, 'TYPE');
				}
				
				foreach($attr_name_array as $attr_name)
				{
					echo $attr_name.': ';
							
					if($attr_name=='TYPE') echo $type_attr[1];
					else if($attr_name=='CHOICE') print_r($this->elementList[$elementId]['attributes'][$attr_name]); // todo change this display
					else echo $this->elementList[$elementId]['attributes'][$attr_name];
						
					if(end($attr_name_array)!=$attr_name) echo ' | ';	
				}
				
				echo '</span>';

				//echo ' <a href="#edition_popup" class="edit" onclick="configurePopUp(\''.htmlspecialchars($attributes).'\')">Edit</a>';
				echo ' <a href="#" class="edit">Edit</a>'; // TODO Use the icon instead (appropriate div)
			}
		}
		else if($elementName=='ENUMERATION')
		{
			echo '<b>VALUE:</b> '.$this->elementList[$elementId]['attributes']['VALUE'];
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

	private function identifyRootAndNamespace()
	{
		$rootElementArray = array();

		// Cleaning the array and identifying the important element
		foreach($this->elementList as $element)
		{
			if($this->namespace==null && $element['parent'] == -1)
			{
				// Finding the namespace name
				foreach(array_keys($element['attributes']) as $key)
				{
					if($element['attributes'][$key] == 'http://www.w3.org/2001/XMLSchema')
					{
						$key_part = explode(':', $key);
						$this->namespace = strtolower($key_part[1]).':';
					}
				}

				if($this->DEBUG) echo $this->namespace . ' is the schema namespace<br/>';
			}
			else if($element['parent'] == 0) // Finding the root element
			{
				if($element['name']==strtoupper($this->namespace).'ELEMENT')
				{
					array_push($rootElementArray, array($element['id'],$element['attributes']['NAME']));
				}
			}
		}
		
		/* Multiple root detection */
		if(count($rootElementArray) == 1)
		{
			$this->root = $rootElementArray[0][0];
			if($this->DEBUG) echo $rootElementArray[0][1] . ' (id=' . $this->root . ') is the root element<br/>';
		}
		else if(count($rootElementArray) >= 2)
		{			
			if($this->DEBUG) echo count($rootElementArray) . ' root elements detected, only one must be chosen<br/>';	
			
			echo '<h3>Multiple root elements</h3>';
			echo 'Choose the root element and continue to load the schema<br/>';
			echo '<select id="root">';
			
			foreach($rootElementArray as $possibleRootElement)
			{
				echo '<option value="'.$possibleRootElement[0].'">'.$possibleRootElement[1].'</option>';
			}
			
			echo '</select> <input type="button" class="button" id="setRoot" value="Continue loading" />';
			
			return;	
		}
		else
		{
			// todo display an error message
			if($this->DEBUG) echo 'No root elements detected, unable to continue...<br/>';
			return;
		}
	}


	/**
	 * Build the validation page which will create the form
	 *
	 * XXX It will create the XSD form configuration
	 * todo rename the function to loadSchema
	 * 
	 */
	public function buildForm()
	{
		$this->elementList = $this->parse();
		
		if($this->DEBUG)
		{
			foreach($this->elementList as $element) {
				print_r($element);
				echo '<br/>';
			}
		}

		if($this->root<0 || $this->namespace==null) $this->identifyRootAndNamespace();
		if($this->root<0) return; // Multiple roots existing

		$this->hasElementToDiscover = true;

		// Linking every element
		while($this->hasElementToDiscover)
		{
			$this->hasElementToDiscover = false;
			$this->completeChildrenList($this->root);
		}
		
		if($this->DEBUG)
		{
			foreach($this->elementList as $element) {
				print_r($element);
				echo '<br/>';
			}
		}

		$this->elementNumber = 0;
		$this->level=-1;
		$this->pageNumber=1;
		
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
	// xxx Function is in the wrong class (it is a display class)
	private function organizeTree2($elementId)
	{
		$undisplayableItemName = array('SIMPLETYPE', 'COMPLEXTYPE', 'SEQUENCE', 'RESTRICTION', 'ENUMERATION'); // xxx todo put it as a global class variable

		$element = $this->elementList[$elementId];
		$elementName = substr($element['name'], strlen($this->namespace));

		if(!isset($element['attribute']['TYPE']) || !startsWith($element['attribute']['TYPE'], $this->namespace))
		{
			$this->level+=1;
			//echo '****LEVEL DOWN****<br/>';
		}
		
		// todo try to figure out a better way to do it
		if(isset($this->elementList[$elementId]['attributes']['MODULE'])) return;

		// todo move it into the display		
		/*if($this->elementNumber== -1) return;
		
		if($this->elementNumber>=$this->elementPerPage && $this->level == 3)
		{
			$this->currentPage += 1;
			$this->elementNumber = 0;
			
			echo 'Page'.$this->currentPage;
					
			if($this->currentPage>$this->pageNumber)
			{
				$this->elementNumber = -1;
				echo '<input type="hidden" id="hasNext" name="hasNext" value"true"/>';
				
				$_SESSION['page'] = $this->pageNumber;
				
				return;
			}
		}
	
		$donotdisplay = false;*/


		if(!in_array($elementName, $undisplayableItemName))
		{
			$this->elementNumber = $this->elementNumber + 1;
			
			/*if($this->currentPage<$this->pageNumber && $elementId!=$this->root) $donotdisplay=true;
			
			
			if(!$donotdisplay)
			{*/
				//if($this->level%3==2) echo '<li>';
			echo '<div class="'.$elementId.'">';
				
				
			$elementName = ucfirst($this->elementList[$elementId]['attributes']['NAME']);
			//$this->elementList[$elementId]['attributes']['NAME']=$elementName; xxx See if we really need that

			//$attributes = serialize($this->elementList[$elementId]['attributes'] + array("id" => $elementId));

			/*echo $elementId.' -- '.($level/3).' -- '.$elementList[$elementId]['name'].' -- ';
			 print_r($elementList[$elementId]['attributes']);*/
			//echo '<a href="">+</a> <a href="">-</a>';

			echo '<b>'.$elementName.'</b>';
			
			if(isset($this->elementList[$elementId]['attributes']['AUTO_GEN']) && $this->elementList[$elementId]['attributes']['AUTO_GEN']=='true')
				echo '<i>(auto-generated)</i>';
			//print_r($this->elementList[$elementId]['attributes']);
			//echo ' '.$attributes;

			if(isset($this->elementList[$elementId]['attributes']['TYPE']) && startsWith($this->elementList[$elementId]['attributes']['TYPE'], $this->namespace))
			{
				if(isset($this->elementList[$elementId]['attributes']['DEFAULT']))
				{
					$value = $this->elementList[$elementId]['attributes']['DEFAULT'];
				}
				else
				{					
					// TODO Handle every data type available in XSD					
					$splitArrayType = explode(':', $this->elementList[$elementId]['attributes']['TYPE']);
					$elementType = $splitArrayType[1];
										
					
					switch($elementType)
					{
						case 'string':
							$value = 'string';
							break;
						case 'integer':
							$value = '0';
							break;
						case 'double':
							$value = '0.0';
							break;
						default:
							$value = '** Datatype not handle **';
							break;
					}
				}
					
				// Compute the father ID
				$pathElementArray = explode('/', $this->path);
				$iteration = count($pathElementArray) - 3; // We substitute 3 element to get the father path
				
				$fatherPath = '';
				for($i=0; $i<$iteration; $i++)
				{
					$fatherPath .= $pathElementArray[$i].'/';
				}
					
				$fatherPath = substr($fatherPath, 0, -1).'[0]';
				
				// todo define base multiplicity here
				
				// XXX class attribute must be defined another way... Work with templates
				echo ' <input type="text" class="text '.$fatherPath.'" value="'.$value.'" ';
				
				if(isset($this->elementList[$elementId]['attributes']['AUTO_GEN']) && $this->elementList[$elementId]['attributes']['AUTO_GEN']=='true')
					echo 'disabled="disabled"/><input type="hidden" class="text '.$fatherPath.'" value="'.$value.'" name="'.$this->path.'[0]" id="'.$this->path.'[0]"/> <input type="button" class="autogen '.$elementType.'" value="Generate"/>';
				else
					echo 'name="'.$this->path.'[0]" id="'.$this->path.'[0]" />';
			}

			if(isset($this->elementList[$elementId]['attributes']['CHOICE'])) 
			{
				// Compute the father ID
				$pathElementArray = explode('/', $this->path);
				$iteration = count($pathElementArray) - 3; // We substitute 3 element to get the father path
				
				$fatherPath = '';
				for($i=0; $i<$iteration; $i++)
				{
					$fatherPath .= $pathElementArray[$i].'/';
				}
					
				$fatherPath = substr($fatherPath, 0, -1).'[0]';
				
				// todo define base multiplicity here
				
				// XXX class attribute must be defined another way... Work with templates
				echo ' <select class="'.$fatherPath.'" id="'.$this->path.'[0]" name="'.$this->path.'[0]">';
				
				foreach($this->elementList[$elementId]['attributes']['CHOICE'] as $optionName)
				{
					echo '<option value="'.$optionName.'">'.$optionName.'</option>';
				}
				
				echo '</select>';
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
				
			echo '</div>';
				
				
			//}
			
		}
		else if($elementName=='ENUMERATION') echo $this->elementList[$elementId]['attributes']['VALUE'];

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
			/*if(!$donotdisplay)
			{*/
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
			//}

			$this->level-=1;
				
			// TODO Do a path function for that
			$lastPathElement =  strrpos($this->path, '/') - strlen($this->path);
			$this->path = substr($this->path, 0, $lastPathElement);

		}
	}


	/**
	 * Build the HTML Form
	 * 
	 * If $elementValues is specified, it fill the form with values
	 * $elementValues must have the $_SESSION['app']['data_tree'] format
	 * 
	 * 
	 */
	// todo rename the function as buildHTMLForm
	public function buildHTML()
	{
		//$this->pageNumber = 1;
		
		$this->level=-1;
		$this->path=$this->root;
		
		$this->organizeTree2($this->root);

		//return null; todo implement the return
	}

	/**
	 * XXX Experimental stuff to remove in future version
	 * 
	 */
	private $weirdPath;
	private $xmlElementArray;
	
	private function displayXMLELement2($elementId) 
	{
		$element = $this->elementList[$elementId];
		
		if($element['name']!=strtoupper($this->namespace).'COMPLEXTYPE' && $element['name']!=strtoupper($this->namespace).'SEQUENCE')
		{
			$path = str_replace('0/0/0', '0', $this->weirdPath);
		
			/*echo $this->path.'('.$path.'):'.$element['attributes']['NAME'].' '.$element['parent'];	
			echo '<br/>';*/
			
			$lastPathElement =  strrpos($path, '/') - strlen($path);
			$fatherId = substr($path, 0, $lastPathElement);
			
			if($fatherId!='')
			{
				if(!isset($this->xmlElementArray['tree'][$fatherId])) $this->xmlElementArray['tree'][$fatherId] = array($path);
				else array_push($this->xmlElementArray['tree'][$fatherId], $path);
			}
			
			if(!isset($this->xmlElementArray['link'])) $this->xmlElementArray['link'] = array();
			$this->xmlElementArray['link'][$path] = $this->path;
		}
		
		if(sizeof($element['children'])!=0)
		{
			$elementNumber = 0;
			foreach($this->elementList[$elementId]['children'] as $child)
			{
				$this->path .= '/'.$child;
				
				$this->weirdPath .= '/'.$elementNumber;
				$elementNumber+=1;
				
				$this->displayXMLELement2($child);
			}
		}
		
		// TODO Do a path function for that
		$lastPathElement =  strrpos($this->path, '/') - strlen($this->path);
		$this->path = substr($this->path, 0, $lastPathElement);
		
		$lastPathElement =  strrpos($this->weirdPath, '/') - strlen($this->weirdPath);
		$this->weirdPath = substr($this->weirdPath, 0, $lastPathElement);			
	}

	private function updateElement($index, $oldElement, $newElement)
	{
		// Update the link
		$newIndex = preg_replace('#^'.$oldElement.'#', $newElement, $index);
		//echo 'Link '.$newIndex."=".$index;
		$this->xmlElementArray['link'][$newIndex] = $this->xmlElementArray['link'][$index];
		
		if(isset($this->xmlElementArray['tree'][$index]))
		{
			$lastPathElement =  strrpos($index, '/') - strlen($index);
			$fatherId = substr($index, 0, $lastPathElement);
			
			// Update index
			$this->xmlElementArray['tree'][$newIndex] = $this->xmlElementArray['tree'][$index];
			
			$listSize = count($this->xmlElementArray['tree'][$newIndex]);
			
			// Changing each children an update grandchildren
			for($i=0; $i<$listSize; $i++)
			{
				$this->updateElement($this->xmlElementArray['tree'][$newIndex][$i], $oldElement, $newElement);
				$this->xmlElementArray['tree'][$newIndex][$i] = preg_replace('#^'.$oldElement.'#', $newElement, $this->xmlElementArray['tree'][$newIndex][$i]);
			}
		}
	}

	private function duplicateElement($weirdPath)
	{
		$lastPathElement =  strrpos($weirdPath, '/') - strlen($weirdPath);
		$fatherId = substr($weirdPath, 0, $lastPathElement);
		$elementId = substr($weirdPath, $lastPathElement+1);
		
		if($fatherId!='')
		{
			$elementNb = count($this->xmlElementArray['tree'][$fatherId]);
			
			// Adding a new element in the father array
			array_push($this->xmlElementArray['tree'][$fatherId], $fatherId.'/'.$elementNb);
			
			// Update children path (+1)			
			for($i=$elementNb-1;$i>$elementId;$i--)
			{
				$this->updateElement($fatherId.'/'.$i, $fatherId.'/'.$i, $fatherId.'/'.($i+1));
			}
			
			// Copy the element
			$this->updateElement($fatherId.'/'.$elementId, $fatherId.'/'.$elementId, $fatherId.'/'.($elementId+1));
			
			/*echo 'id='.$elementId.'<br/>';
			echo $elementNb.' elem. identified<br/>';*/
		}
		else // If the duplicate element is the root one
		{
			// TODO configure an error message
			// The root element cannot be duplicated
		}
		
	}
	
	private function updateElement2($index, $oldElement, $newElement)
	{
		// Update the link
		$newIndex = preg_replace('#^'.$oldElement.'#', $newElement, $index);
		//echo 'Link '.$newIndex."=".$index;
		
		$lastPathElement =  strrpos($index, '/') - strlen($index);
		$fatherId = substr($index, 0, $lastPathElement);
		$elementId = substr($index, $lastPathElement+1);
		
		if($elementId != 0) $this->xmlElementArray['tree'][$fatherId][$elementId-1] = $newIndex;
		//else 
		
		$this->xmlElementArray['link'][$newIndex] = $this->xmlElementArray['link'][$index];
		unset($this->xmlElementArray['link'][$index]);
		
		if(isset($this->xmlElementArray['tree'][$index]))
		{
			$this->xmlElementArray['tree'][$newIndex] = $this->xmlElementArray['tree'][$index];
			unset($this->xmlElementArray['tree'][$index]);
			
			$listSize = count($this->xmlElementArray['tree'][$newIndex]);
			
			// Changing each children an update grandchildren
			for($i=0; $i<$listSize; $i++)
			{
				$this->updateElement2($this->xmlElementArray['tree'][$newIndex][$i], $oldElement, $newElement);
				$this->xmlElementArray['tree'][$newIndex][$i] = preg_replace('#^'.$oldElement.'#', $newElement, $this->xmlElementArray['tree'][$newIndex][$i]);
			}
		}/*
		else {
			echo 'not set';
		}*/
	}

	private function eraseChildren($element)
	{
		if(isset($this->xmlElementArray['tree'][$element])) // If the element has children
		{
			foreach($this->xmlElementArray['tree'][$element] as $child)
			{
				$this->eraseChildren($child);
				unset($this->xmlElementArray['link'][$child]);
			}
			
			unset($this->xmlElementArray['tree'][$element]);
		}
	}	
	
	private function removeElement($weirdPath)
	{
		$lastPathElement =  strrpos($weirdPath, '/') - strlen($weirdPath);
		$fatherId = substr($weirdPath, 0, $lastPathElement);
		
		$elementId = $weirdPath[strlen($weirdPath)-1];
		
		if($fatherId!='')
		{
			$elementNb = count($this->xmlElementArray['tree'][$fatherId]);
			
			// Removing the element in the father array
			unset($this->xmlElementArray['tree'][$fatherId][$elementId]); // Removing from tree
			$this->xmlElementArray['tree'][$fatherId] = array_values($this->xmlElementArray['tree'][$fatherId]);
			unset($this->xmlElementArray['link'][$weirdPath]); // Removing from link
			$this->eraseChildren($weirdPath);
			
			// Update children path (+1)			
			for($i=$elementId+1;$i<$elementNb;$i++)
			{
				//echo 'update '.$fatherId.'/'.$i.', '.$fatherId.'/'.$i.', '.$fatherId.'/'.($i-1).'<br/>';
				$this->updateElement2($fatherId.'/'.$i, $fatherId.'/'.$i, $fatherId.'/'.($i-1));
			}
			
			/*echo 'id='.$elementId.'<br/>';
			echo $elementNb.' elem. identified<br/>';*/
		}
		else // If the duplicate element is the root one
		{
			// TODO configure an error message
			// The root element cannot be remove
		}
	}

	private function readActions($actionList)
	{
		foreach($actionList as $action)
		{
			//echo $action.'<br/>';
			$actionInfo = explode("|", $action);
			
			switch($actionInfo[0])
			{
				case 'add':
					$this->duplicateElement($actionInfo[1]);
					break;
				case 'remove':
					$this->removeElement($actionInfo[1]);
					break;
				default:
					// TODO configure an error message
					break;
			}
		}
	}
	
	private function bXml($weirdPathId)
	{
		$path = $this->xmlElementArray['link'][$weirdPathId];
		
		$lastPathElement =  strrpos($path, '/') - strlen($path);
		$elementId = substr($path, $lastPathElement+1);
		$element = $this->elementList[$elementId];
		
		$this->xmlString .= '<'.$element['attributes']['NAME'];
		
		// todo make it modular
		if($this->root == $elementId) $this->xmlString .= ' xmlns:hdf5=\\"http://hdfgroup.org/HDF5/XML/schema/HDF5-File\\"';
		
		$this->xmlString .= '>';
		
		// TODO Remove it when the tables can be handle
		if($element['attributes']['NAME']=='Table')
		{
			foreach($_SESSION['app']['xml']['tables'] as $table)
			{
				$this->xmlString .= str_replace('"', '\\"', htmlspecialchars_decode($table));
			}
		}
		
		if(isset($this->xmlElementArray['tree'][$weirdPathId]))
		{
			foreach($this->xmlElementArray['tree'][$weirdPathId] as $children)
			{
				$this->bXml($children);
			}
		}
		else {
			$this->xmlString .= $this->contentList[$path][0];
			
			unset($this->contentList[$path][0]);
			if($this->contentList[$path]) $this->contentList[$path] = array_values($this->contentList[$path]);
		}
		
		$this->xmlString .= '</'.$element['attributes']['NAME'].'>';
	}
	
	private $tableContent; // todo remove it after that

	/**
	 *
	 * @param array $xmlContent
	 */
	public function buildXML(array $xmlContent, array $actionsPerformed)
	{
		$this->level=-1;
		$this->path=$this->root;

		$this->contentList = $xmlContent;
		$this->actions = $actionsPerformed;
		
		$this->weirdPath = '0';
		$this->xmlElementArray = array();

		$this->xmlString = '';

		$this->displayXMLELement2($this->root);
		
		$this->readActions($actionsPerformed);
		
		$this->bXml(0);
		
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