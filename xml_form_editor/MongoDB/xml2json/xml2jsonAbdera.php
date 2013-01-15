|<?php

require_once 'json/JSON.php';

/**
Copyright (c) 2006 David Sklar

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/


class Abdera {
    public static function encode(DOMNode $node, $level = 0) {
        $r = array();
        if ($node->childNodes) {
            $text = '';
            $skip = 0;
            $hasChild = 0;
            foreach ($node->childNodes as $child) {
                $idx = $child->nodeName;
                //Test if the next node at the same tree level of the child has the same name. If yes, we should node display the child name and display the content of these nodes in an array
                if (($child->nextSibling) ? ($child->nextSibling->nextSibling) : false) {
                	var_dump($child->nodeName);
                	var_dump($child->nextSibling->nextSibling->nodeName);
                	var_dump($child->textContent);
                	if (($idx != '#text') && ($idx == $child->nextSibling->nextSibling->nodeName))
                		$skip = 1;
                }
                if (! is_null($cr = self::encode($child, $level+1))) {
                	$hasChild = 1;
                	if ($skip)
                		$r[$idx][] = $cr;
                  			elseif (($child->nodeType == XML_TEXT_NODE)||($child->nodeType == XML_CDATA_SECTION_NODE)) {
                    			$text .= $cr;
							} else {
								if ($node->attributes && $node->attributes->length)
									$r['children'][][$idx] = $cr;
								else
                        			$r[$idx] = $cr;
							}
                }
            }
             var_dump($r);
            // Reduce 1-element numeric arrays
            foreach ($r as $idx => $v) {
                if (is_array($v) && (count($v) == 1) && isset($v[0])) {
                    $r[$idx] = $v[0];
                }
            }
            
            // Any accumulated text that isn't just whitespace?
            if (strlen(trim($text))) { 
            	if ($node->attributes && $node->attributes->length) {
            		$r['children'][] = $text;
            	}
            	else
            		$r[] = $text;
            }

            // Attributes?
            if ($node->attributes && $node->attributes->length) {
            	if (strlen(trim($text)) || $hasChild) {
	                foreach ($node->attributes as $attr) 
	                   	$r['attributes'][$attr->nodeName] = $attr->value;
            	}
            	else {
            		foreach ($node->attributes as $attr)
            			$r[$attr->nodeName] = $attr->value;
            	}
            }
         var_dump($r);   
        }
        // No children -- just return text;
        else {
            if ((($node->nodeType == XML_TEXT_NODE)||($node->nodeType == XML_CDATA_SECTION_NODE)) ? (trim($node->textContent) != null) : false) {
                return $node->textContent;
            }
            else return null;
        }
        if ($level == 0) {
            $json = new Services_Json();
            return '('.$json->encode($r).');';
        } else {
            return $r;
        }
    }
}
