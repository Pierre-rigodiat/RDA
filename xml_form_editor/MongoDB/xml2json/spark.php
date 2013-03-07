<?php
function encodeSpark($domNode)
{
	//echo nl2br(htmlspecialchars($domNode->saveXML()));
	
	
	$result = array();
	
	//echo "<hr/>";
	foreach($domNode->childNodes as $child)
	{
		$result = encodeS($child);
	}
	
	//echo "<hr/>";
	return $result;
}

function encodeS($domNode)
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
	
				$r[] = encodeS($child);
	
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
						
					$r[$idx] = encodeS($child);
	
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
	
	// Reduce 1-element numeric arrays
	//Case of the Spark convention
	if(is_array($r))
	{
		foreach ($r as $idx => $v) {
			if(count($r) == 1)
			{
				$r=array(0 => $v);
			}
		}
	}
	
	return $r;
	
}

function decodeSpark($json_string)
{
	$array = json_decode($json_string, true);
	$domDocument = new DOMDocument();
	$domDocument->formatOutput = true;
	$body = $domDocument->createElement('body');
	$domDocument->appendChild($body);
	//print_r($array);
	//echo "<hr/>";

	decodeS($array, $body, $domDocument);

	//echo "<hr/>";
	//echo nl2br(htmlspecialchars($domDocument->saveXML()));
	
	return $domDocument;
}

function decodeS($array, $parent, $domDocument)
{
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
				decodeS($child, $newElement, $domDocument);
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
			$newElement = $domDocument->createElement('item');
			$parent->appendChild($newElement);
			
			if (is_array($child))
			{
					
				//echo 'item[';
				decodeS($child, $newElement, $domDocument);
				//echo ']';
			}
			else
			{
				$text = $domDocument->createTextNode($child);
				$newElement->appendChild($text);
				
				//echo $key.'="'.$child.'"';
			}
		}
	}
}

