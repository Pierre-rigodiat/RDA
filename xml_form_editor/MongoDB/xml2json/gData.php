<?php
function encodeGData($domNode)
{
	//echo nl2br(htmlspecialchars($domNode->saveXML()));
	
	$result = array();
	
	//echo "<hr/>";
	$result = encodeG($domNode);
	
	//echo "<hr/>";
	return $result;
}

function encodeG($domNode)
{
	$r = array();
	if ($domNode->childNodes)
	{
		// Attributes?
		if ($domNode->attributes && $domNode->attributes->length)
		{
			foreach ($domNode->attributes as $attr) {
				//echo "(".$attr->nodeName."=".$attr->value.")";
		
				$r[$attr->nodeName] = $attr->value;
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
					//echo '[$t="'.$text.'"]';
	
					$r['$t'] = $text;
				}
			}
			else
			{
				//echo "[".$idx;
	
				$r[$idx][] = encodeG($child);
	
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
	
	return $r;
}

function decodeGData($json_string)
{
	$array = json_decode($json_string, true);
	$domDocument = new DOMDocument();
	$domDocument->formatOutput = true;
	//print_r($array);
	//echo "<hr/>";

	decodeG($array, $domDocument, $domDocument);

	//echo "<hr/>";
	//echo nl2br(htmlspecialchars($domDocument->saveXML()));
	
	return $domDocument;
}

function displayAttr2($key, $value, $parent, $domDocument)
{

	$attribute = $domDocument->createAttribute($key);
	$attribute -> value = $value;
	$parent -> appendChild($attribute);


	//echo '('.$key.'='.$value.')';
}

function decodeG($array, $parent, $domDocument)
{
	// TODO Check type of $array
	
	foreach($array as $key => $child)
	{
		if(is_string($key) && is_string($child) && $key != '$t' ) // Attribute
		{
				displayAttr2($key, $child, $parent, $domDocument);
		}
		else if(is_string($key) && $key == '$t') // Text element
		{
			$text = $domDocument->createTextNode($child);
			$parent->appendChild($text);
				
			//echo '"'.$child.'"';
		}
		else
		{
			if(is_array($child))
			{
				//$result = '';
				if(is_string($key))
				{
					$newElement = $domDocument->createElement($key);
					$parent->appendChild($newElement);
						
					//$result.=$key;
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
					//echo $result.'[';
					decodeG($child, $newElement, $domDocument);
					//echo ']';
			}
			else
			{
				//echo $key.'='.$child;
			}
		}
	}
}

