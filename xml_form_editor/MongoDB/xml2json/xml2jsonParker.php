<?php

require_once 'json/JSON.php';

class Parker {
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
			$skip = 0;
			foreach ($node->childNodes as $child) {
				$idx = $child->nodeName;
				//Test if the next node at the same tree level of the child has the same name. If yes, we should node display the child name and display the content of these nodes in an array
				if (($child->nextSibling) ? ($child->nextSibling->nextSibling) : false) {
					/*var_dump($child->nodeName);
					var_dump($child->nextSibling->nextSibling->nodeName);*/
					if (($idx != '#text') && ($idx == $child->nextSibling->nextSibling->nodeName))
							$skip = 1;
				}
					if (! is_null($cr = self::encode($child, $level+1))) {
						//Display the content of the next child as an array
						if ($skip)
							$r[] = $cr;
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

			
			//Return the correct type according to the Parker convention
			if (self::parkerText($text) != null){
				$r[] = self::parkerText($text);
			}
			
			foreach ($r as $idx => $v) {
				//Reduce 1-element arrays
				if (is_array($v) && (count($v) == 1) && isset($v[0])) {
					$r[$idx] = $v[0];
				}
				//Reduce 0-element arrays to null
				if (is_array($v) && (count($v) == 0)) {
					$r[$idx] = null;
				}
			}
			

		}
			// No children -- just return text;
			else {
				if (($node->nodeType == XML_TEXT_NODE)||($node->nodeType == XML_CDATA_SECTION_NODE)) {
					return self::parkerText($node->textContent);
				}
			}
			if ($level == 0) {
				$json = new Services_Json();
				return $json->encode($r);
			} else {
				return $r;
			}	
	
	}
	
}

?>