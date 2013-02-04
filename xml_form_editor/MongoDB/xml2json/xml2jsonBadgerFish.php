|<?php

require_once 'json/JSON.php';

/**
Copyright (c) 2006 David Sklar

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/


class BadgerFish {
    public static function encode(DOMNode $node, $level = 0) {
        static $xpath;
        if (is_null($xpath)) {
            $xpath = new DOMXPath($node);
        }
        $r = array();
        
        if ($node->childNodes) {       	
            $text = '';
            foreach ($node->childNodes as $child) {
                $idx = $child->nodeName;
                if (! is_null($cr = self::encode($child, $level+1))) {
					if (($child->nodeType == XML_TEXT_NODE)||($child->nodeType == XML_CDATA_SECTION_NODE)) {
                        $text .= $cr;
                    } else {
                        $r[$idx][] = $cr;
                    }
                }
            }
            
            // Reduce 1-element numeric arrays
            foreach ($r as $idx => $v) {
                if (is_array($v) && (count($v) == 1) && isset($v[0])) {
                    $r[$idx] = $v[0];
                }
            }
            
            // Any accumulated text that isn't just whitespace?
            if (strlen(trim($text))) { $r['$'] = $text; }
            
            // Attributes?
            if ($node->attributes && $node->attributes->length) {
            	foreach ($node->attributes as $attr) { 
            		$r['@'.$attr->nodeName] = $attr->value;
            	}
            }
            
            
            // Namespaces?
            if ($elem=$xpath->query('namespace::*[name() != "xml"]', $node)) {
            	foreach ($elem as $ns) {
            		if ($ns->localName != 'xmlns') {
            			$r['@xmlns'][$ns->localName] = $ns->namespaceURI;
           			} else {
           				$r['@xmlns']['$'] = $ns->namespaceURI;
           			}
            	}
            }
        }
        // No children -- just return text;
        else {
            if (($node->nodeType == XML_TEXT_NODE)||($node->nodeType == XML_CDATA_SECTION_NODE)) {
                return $node->textContent;
            }
        }
        if ($level == 0) {
            $json = new Services_Json();
            $xpath = null;
            return $json->encode($r);
            /*var_dump($json->encode($r));
            var_dump(json_encode($r));
            return;*/
        } else {
            return $r;
        }
    }
	
    public function cleanTag($key) {
    	return preg_replace('/[\@0-9]/', '', $key);
    }
    
	public static function decode($array, $level = 0){
	   	static $return;
	   	$return = new DOMDocument();
	   	$text = "";
	   	if ($level == 0) {
	   		//$json = new Services_Json();
	   		$array = json_decode($array, true);
	   		//$dom = new DOMDocument();
	   		print_r($array);echo "<br/>";
	   	}
	   	//$return = $dom;
	   	if (is_array($array)) {
		   	foreach($array as $key => $child){
		   		echo gettype($child)."<br/>";
		   		if (! is_null($cr = self::decode($child, $level + 1))) {
		   			$newKey=self::cleanTag($key);
			   		if(is_array($child) && $newKey != '') {
			   			echo $newKey;
			   			$tag = $return->createElement($newKey);
			   			$return->appendChild($tag);
			   		}
			   		elseif (gettype($child) == "string" || gettype($child) == "integer") {
			   			$text .= $child;
			   		}
		   		}
		   	}
		   	
		   	if (strlen(trim($text))) {
		   		$textElem = $return->createTextNode($text);
		   		$return->appendChild($textElem);
		   	}
	   	}
	   	elseif (gettype($array) == "string" || gettype($array) == "integer") {
	   		return ''.$array;
	   	}
	   	//if ($level != 0)
			return $return;
	   	/*else
			return $dom;*/
	}
    
    
     
}
