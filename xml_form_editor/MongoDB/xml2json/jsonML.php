<?php
function encodeJSONML($domNode)
{
	//echo nl2br(htmlspecialchars($domNode->saveXML()));

	$xpath = new DOMXPath($domNode);
	$result = array();
	$namespace = array();
	$namespace['xmlns'] = '';

	//echo "<hr/>";
	$result = encodeJ($domNode, $xpath, $namespace);
	$result = $result[0];

	//echo "<hr/>";
	return $result;
}

function encodeJ($domNode, $xpath, $namespace)
{
	$r = array();
	if ($domNode->childNodes)
	{
		$prefChild = '';
		
		$insert = array();
		// Namespaces?
		if ($elem=$xpath->query('namespace::*[name() != "xml"]', $domNode))
		{
			foreach ($elem as $ns) {
				if ($ns->localName == 'xmlns' && $ns->namespaceURI != $namespace['xmlns']) {
					$insert['xmlns'] = $ns->namespaceURI;
					$namespace['xmlns'] = $ns->namespaceURI;
				} else {
					$new = 1;
					foreach ($namespace as $prefix => $uri){
						if($prefix == $ns->localName && $new)
							$new = 0;
					}
					if ($new) {
						$insert['xmlns:'.$ns->localName] = $ns->namespaceURI;
						$namespace[$ns->localName] = $ns->namespaceURI;
					}
				}
			}
		}
	
		// Attributes?
		if ($domNode->attributes && $domNode->attributes->length)
		{
			//$prefChild = ',';
			//echo "{";
			//$pref = '';
			foreach ($domNode->attributes as $attr) {
				//echo $pref.'"'.$attr->nodeName.'" = "'.$attr->value.'"';
				//$pref = ", ";
				
				$insert[$attr->nodeName] = $attr->value;
			}
			//echo "}";
		}
		
		//Insert the namespaces and attributes in the same array
		if ($insert != array())
			$r[] = $insert;
	
		$text = '';

		foreach($domNode->childNodes as $child)
		{
			$idx = $child->nodeName;
			if(($child->nodeType == XML_TEXT_NODE)||($child->nodeType == XML_CDATA_SECTION_NODE))
			{
				$text = trim($child->textContent);
				if (strlen($text))
				{
					//echo '"'.$text.'"';
	
					$r[] = $text;
				}
			}
			else
			{
				//echo $prefChild.' ["'.$idx.'", ';
				//$prefChild = ',';

				$insert = array();
				$next = encodeJ($child, $xpath, $namespace);
				$insert = array($idx);
				if ($next != array())
				{
					foreach ($next as $arrayChild){
						if ($arrayChild != null)
							$insert[] = $arrayChild;
						//$r[] = encodeJ($child, $xpath, $namespace);
					}
				}
				//echo "]";
				
				$r[] = $insert;
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
	
	return $r;
	
}

function decodeJSONML($json_string)
{
	$array = json_decode($json_string, true);
	$domDocument = new DOMDocument();
	$domDocument->formatOutput = true;
	//print_r($array);
	//echo "<hr/>";

	decodeJ($array, $domDocument, $domDocument);

	//echo "<hr/>";
	//echo nl2br(htmlspecialchars($domDocument->saveXML()));
	
	return $domDocument;
}

function decodeJ($array, $parent, $domDocument)
{
	foreach($array as $key => $child)
	{
		if (is_int($key)) //Case of a child
		{
			if (!$key) //The element at the 0 position is the parent, the next ones are its children
			{
			$newParent = $domDocument->createElement($child);
			$parent->appendChild($newParent);
			$parent = $newParent;
			}
			else
			{
				if (is_string($child)) //Text element
				{
					$text = $domDocument->createTextNode($child);
					$parent->appendChild($text);
				}
				else //Child element
				{
					decodeJ($child, $parent, $domDocument);
				}
			}
		}
		else //Attributes and namespaces
		{
			$attribute = $domDocument->createAttribute($key);
			$attribute -> value = $child;
			$parent -> appendChild($attribute);
		}
	}
	
}