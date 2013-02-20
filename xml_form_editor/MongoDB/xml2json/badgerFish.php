<?php
function encodeBadgerFish($domNode)
{
	//echo nl2br(htmlspecialchars($domNode->saveXML()));
	
	$xpath = new DOMXPath($domNode);
	$result = array();
	
	//echo "<hr/>";
	$result = encodeB($domNode, $xpath);
	
	//echo "<hr/>";
	return json_encode($result);
}

function encodeB($domNode, $xpath)
{
	$r = array();
	if ($domNode->childNodes)
	{
		// Namespaces?
		if ($elem=$xpath->query('namespace::*[name() != "xml"]', $domNode))
		{
			foreach ($elem as $ns) {
				if ($ns->localName == 'xmlns') {
					$r['@xmlns']['$'] = $ns->namespaceURI;
				} else {
					$r['@xmlns'][$ns->localName] = $ns->namespaceURI;
				}
			}
		}
		
		// Attributes?
		if ($domNode->attributes && $domNode->attributes->length)
		{
			foreach ($domNode->attributes as $attr) {
				//echo "(@".$attr->nodeName."=".$attr->value.")";
		
				$r['@'.$attr->nodeName] = $attr->value;
			}
		}
		
		$text = '';
		foreach($domNode->childNodes as $child)
		{
			$idx = $child->nodeName;
			if(($child->nodeType == XML_TEXT_NODE)||($child->nodeType == XML_CDATA_SECTION_NODE))
			{
				$text = trim($child->textContent);
				if (strlen($text))
				{
					//echo '[$="'.$text.'"]';
				
					$r['$'] = $text;
				}
			}
			else
			{
				//echo "[".$idx;
				
				$r[$idx][] = encodeB($child, $xpath);

				//echo "]";
			}
		}
		
	}
	
	else 
	{
		if (($domNode->nodeType == XML_TEXT_NODE)||($domNode->nodeType == XML_CDATA_SECTION_NODE)) 
		{
			$r = $domNode->textContent;
		}
	}
	
	// Reduce 1-element numeric arrays
	foreach ($r as $idx => $v) {
		if (is_array($v) && (count($v) == 1) && isset($v[0])) {
			$r[$idx] = $v[0];
		}
	}
	
	if(is_array($r) && $r == array()) //Case of the null object, print {} instead of []
	{
		$r = (object) array();
	}
	
	return $r;
}

function decodeBadgerFish($json_string)
{
	$array = json_decode($json_string, true);
	$domDocument = new DOMDocument();
	$domDocument->formatOutput = true;
	print_r($array);
	echo "<hr/>";
	
	decodeB($array, $domDocument, $domDocument);
	
	echo "<hr/>";
	echo nl2br(htmlspecialchars($domDocument->saveXML()));
}

function displayAttr($key, $value, $parent, $domDocument)
{
	$key = preg_replace('/[\@]/', '', $key);
	
	$attribute = $domDocument->createAttribute($key);
	$attribute -> value = $value;
	$parent -> appendChild($attribute);
	
	
	echo '('.$key.'='.$value.')';
}

function decodeB($array, $parent, $domDocument)
{
	// TODO Check type of $array
	
	foreach($array as $key => $child)
	{
		if(preg_match('/@(.*)/', $key)) // Attribute
		{
			if(is_array($child))
			{
				foreach($child as $attrKey => $attrValue)
				{
					if($attrKey != '$') $key .= ':'.$attrKey;
					displayAttr($key, $attrValue, $parent, $domDocument);
				}
			}
			else
			{
				displayAttr($key, $child, $parent, $domDocument);
			}
		}
		else if(is_string($key) && $key == '$') // Text element
		{
			$text = $domDocument->createTextNode($child);
			$parent->appendChild($text);
			
			echo '"'.$child.'"';
		}
		else
		{
			if(is_array($child))
			{
				$result = '';
				if(is_string($key))
				{
					$newElement = $domDocument->createElement($key);
					$parent->appendChild($newElement);
					
					$result.=$key;
				}
				else
				{
					if($key != 0) // 
					{
						$grandParent = $parent -> parentNode;
						$newElement = $domDocument->createElement($parent->tagName);
							
						$grandParent -> appendChild($newElement);	 	
					}
					else
					{
						$newElement = $parent;
					}
				}
				echo $result.'[';
					decodeB($child, $newElement, $domDocument);
				echo ']';
			}
			else
			{
				echo $key.'='.$child;
			}
		}
		
		
	}
	
}
