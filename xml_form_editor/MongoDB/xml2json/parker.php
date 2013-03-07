<?php
function encodeParker($domNode)
{
	//echo nl2br(htmlspecialchars($domNode->saveXML()));
	

	$result = array();
	
	//echo "<hr/>";
	$result = encodeP($domNode);
	
	//echo "<hr/>";
	return $result;
}

function parkerText($text) {
	if (strlen(trim($text))) {
		if (is_numeric(trim($text))) {
			return ($text + 0);
		}
		elseif (!strcasecmp(trim($text),'true')) {
			return true;
		}
		elseif (!strcasecmp(trim($text),'false')) {
			return false;
		}
		else {
			return $text;
		}
	}
	else return null;
}

function encodeP($domNode)
{
	$r = array();
	if ($domNode->childNodes)
	{
		$text = '';
		$skip = 0;
		foreach($domNode->childNodes as $child)
		{
			$idx = $child->nodeName;
			
			//Test if the next node at the same tree level of the child has the same name. If yes, we should node display the child name and display the content of these nodes in an array
			if (($child->nextSibling) ? ($child->nextSibling->nextSibling) : false) {
				if (($idx != '#text') && ($idx == $child->nextSibling->nextSibling->nodeName))
					$skip = 1;
			}
			if($skip && $idx != '#text')
			{
				//echo "[";
				
				$r[] = encodeP($child);
				
				//echo "]";
			}
			else
			{
				if(($child->nodeType == XML_TEXT_NODE)||($child->nodeType == XML_CDATA_SECTION_NODE))
				{
					$text = parkerText($child->textContent);
					if ($text)
					{
						//echo '="'.$text.'"';
					
						$r = $text;
					}
				}
				else
				{
					//echo "[".$idx;
					
					$r[$idx] = encodeP($child);
	
					//echo "]";
				}
			}
		}
	}
	
	else 
	{
		if (($domNode->nodeType == XML_TEXT_NODE)||($domNode->nodeType == XML_CDATA_SECTION_NODE)) 
		{
			$r = parkerText($domNode->textContent);
		}
	}
	if(is_array($r) && !count($r))
	{
		$r = null;
	}
	return $r;
	
}

function decodeParker($json_string)
{
	$array = json_decode($json_string, true);
	$domDocument = new DOMDocument();
	$domDocument->formatOutput = true;
	//print_r($array);
	//echo "<hr/>";

	decodeP($array, $domDocument, $domDocument);

	//echo "<hr/>";
	//echo nl2br(htmlspecialchars($domDocument->saveXML()));
	
	return $domDocument;
}

function decodeP ($array, $parent, $domDocument) {
	// TODO Check type of $array
	
	foreach($array as $key => $child)
	{
		if (is_string($key)) 
		{
			$newElement = $domDocument->createElement($key);
			$parent->appendChild($newElement);
			
			if (is_array($child))
			{
				
				//echo $key.'[';
				decodeP($child, $newElement, $domDocument);
				//echo ']';
			}
			else // Text element
			{
			$text = $domDocument->createTextNode($child);
			$newElement->appendChild($text);
				
			//echo $key.'="'.$child.'"';
			}
		}
		else 
		{
			$newElement = $domDocument->createElement('entry');
			$parent->appendChild($newElement);
			
			//echo 'entry[';
			decodeP($child, $newElement, $domDocument);
			//echo ']';
		}
	}
}