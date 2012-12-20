<?php

require_once 'json/JSON.php';

class Spark {
	public function parkerText($text) {
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
	
	public static function encode(DOMnode $node, $level = 0) {
		$r = array();
		if ($node->childNodes) {
			$text = '';
			$skipParker = 0;
			foreach ($node->childNodes as $child) {
				$idx = $child->nodeName;
				if (($child->nextSibling) ? ($child->nextSibling->nextSibling) : false) {
					/*var_dump($idx);
					var_dump($child->nextSibling->nextSibling->nodeName);*/
					if (($idx != '#text') && ($idx == $child->nextSibling->nextSibling->nodeName))
						$skipParker=1;
				}
					if (! is_null($cr = self::encode($child, $level+1))) {
						if (!$level) {
							$r=$cr;
						}
						//Display the content of the next child as an array
						elseif ($skipParker) {
							$r[] = $cr;
						}
						//Grab the text of the node
						elseif (($child->nodeType == XML_TEXT_NODE)||($child->nodeType == XML_CDATA_SECTION_NODE)) {
							$text .= $cr;
						}
						//Basic JSON display of data
							else {
								$r[$idx] = $cr;
							}
					}
			}
			
			foreach ($r as $idx => $v) {
				// Reduce 1-element numeric arrays
				if (is_array($v) && (count($v) == 1) && isset($v[0])) {
					if (count($r) != 1) {
						$r[$idx] = $v[0];
					}
					//Case of the Spark convention
					else {
						$r=array(0 => $v);
					}
				}
				//Reduce 0-element arrays to null
				if (is_array($v) && (count($v) == 0)) {
					$r[$idx] = null;
				}
			}
			
			//Return the correct type according to the Parker convention
			if (self::parkerText($text) != null) {
				$r[] = self::parkerText($text);
			}

		}
			// No children -- just return text;
			else {
				if (($node->nodeType == XML_TEXT_NODE)||($node->nodeType == XML_CDATA_SECTION_NODE)) {
					return self::parkerText($node->textContent);
				}
			}
			
			if ($level == 0) {
				//var_dump($i);
				$json = new Services_Json();
				return $json->encode($r);
			} else {
				return $r;
			}	
	
	}
	
}

?>