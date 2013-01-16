/* Copyright (c) 2007 Lev Muchnik <LevMuchnik@gmail.com>. All rights reserved.
 * You may copy and modify this script as long as the above copyright notice,
 * this condition and the following disclaimer is left intact.
 * This software is provided by the author "AS IS" and no warranties are
 * implied, including fitness for a particular purpose. In no event shall
 * the author be liable for any damages arising in any way out of the use
 * of this software, even if advised of the possibility of such damage.
 * $Date: 2007-10-03 19:08:15 -0700 (Wed, 03 Oct 2007) $
 */
/* NIST Modification brought
 * 	- No "commercial" link after the tree display
 * � NIST 2012
 */

function LoadXML(ParentElementID,URL) 
{
		var xmlHolderElement = GetParentElement(ParentElementID);
		if (xmlHolderElement==null) { return false; }
		ToggleElementVisibility(xmlHolderElement);
		return RequestURL(URL,URLReceiveCallback,ParentElementID);
}

function LoadXMLDom(ParentElementID,xmlDoc) 
{
	if (xmlDoc) {
		var xmlHolderElement = GetParentElement(ParentElementID);
		if (xmlHolderElement==null) { return false; }
		while (xmlHolderElement.childNodes.length) { xmlHolderElement.removeChild(xmlHolderElement.childNodes.item(xmlHolderElement.childNodes.length-1));	}
		var Result = ShowXML(xmlHolderElement,xmlDoc.documentElement,0);
	
		// XXX We have to remove the credentials
		//var ReferenceElement = document.createElement('div');
		//var Link = document.createElement('a');		
		//Link.setAttribute('href','http://www.levmuchnik.net/Content/ProgrammingTips/WEB/XMLDisplay/DisplayXMLFileWithJavascript.html');
		//var TextNode = document.createTextNode('Source: Lev Muchnik');
		//Link.appendChild(TextNode);

		//xmlHolderElement.appendChild(Link);
		return Result;
	}
	else { return false; }
}

function LoadXMLString(ParentElementID,XMLString) 
{
	//console.log('LoadXMLString('+ParentElementID+','+XMLString+')');
	
	xmlDoc = CreateXMLDOM(XMLString);
	
	console.log(xmlDoc);
	
	return LoadXMLDom(ParentElementID,xmlDoc) ;
}

////////////////////////////////////////////////////////////
// HELPER FUNCTIONS - SHOULD NOT BE DIRECTLY CALLED BY USERS
////////////////////////////////////////////////////////////
function GetParentElement(ParentElementID)
{
	if (typeof(ParentElementID)=='string') {	return document.getElementById(ParentElementID);	}
	else if (typeof(ParentElementID)=='object') { return ParentElementID;} 
	else { return null; }
}
function URLReceiveCallback(httpRequest,xmlHolderElement)
{
	  try {
            if (httpRequest.readyState == 4) {
                if (httpRequest.status == 200) {
					var xmlDoc = httpRequest.responseXML;
					if (xmlHolderElement && xmlHolderElement!=null) {
							xmlHolderElement.innerHTML = '';
							return LoadXMLDom(xmlHolderElement,xmlDoc);
					}
                } else {
                    return false;
                }
            }
        }
        catch( e ) {
            return false;
        }	
}
function RequestURL(url,callback,ExtraData) { // based on: http://developer.mozilla.org/en/docs/AJAX:Getting_Started
        var httpRequest=null;
        if (window.XMLHttpRequest) { // Mozilla, Safari, ...
            httpRequest = new XMLHttpRequest();
            if (httpRequest.overrideMimeType) { httpRequest.overrideMimeType('text/xml'); }
        } 
        else if (window.ActiveXObject) { // IE
            try { httpRequest = new ActiveXObject("Msxml2.XMLHTTP");   } 
            catch (e) {
				   try { httpRequest = new ActiveXObject("Microsoft.XMLHTTP"); } 
				   catch (e) {}
            }
        }
        if (!httpRequest) { return false;   }
        httpRequest.onreadystatechange = function() { callback(httpRequest,ExtraData); };
        httpRequest.open('GET', url, true);
        httpRequest.send('');
		return true;
    }

function CreateXMLDOM(XMLStr) 
{
	if (window.ActiveXObject)
	 {
		  xmlDoc=new ActiveXObject("Microsoft.XMLDOM"); 
		  xmlDoc.loadXML(XMLStr);	
		  return xmlDoc;
	}
	else if (document.implementation && document.implementation.createDocument)	  {
		  var parser=new DOMParser();
		  return parser.parseFromString(XMLStr,"text/xml");
	}
	else {
		return null;
	}
}		

var IDCounter = 1;
var NestingIndent = 15;
function ShowXML(xmlHolderElement,RootNode,indent)
{
	if (RootNode==null || xmlHolderElement==null) { return false; }
	var Result  = true;
	var TagEmptyElement = document.createElement('div');
	TagEmptyElement.className = 'Element';
	TagEmptyElement.style.position = 'relative';
	TagEmptyElement.style.left = NestingIndent+'px';
	if (RootNode.childNodes.length==0) { 
    var ClickableElement = AddTextNode(TagEmptyElement,'','Clickable') ;
    ClickableElement.id = 'div_empty_' + IDCounter;	  
    AddTextNode(TagEmptyElement,'<','Utility') ;
    AddTextNode(TagEmptyElement,RootNode.nodeName ,'NodeName');
    for (var i = 0; RootNode.attributes && i < RootNode.attributes.length; ++i) {
      CurrentAttribute  = RootNode.attributes.item(i);
      AddTextNode(TagEmptyElement,' ' + CurrentAttribute.nodeName ,'AttributeName') ;
      AddTextNode(TagEmptyElement,'=','Utility') ;
      AddTextNode(TagEmptyElement,'"' + CurrentAttribute.nodeValue + '"','AttributeValue') ;
    }
    AddTextNode(TagEmptyElement,' />') ;
    xmlHolderElement.appendChild(TagEmptyElement);	
    //SetVisibility(TagEmptyElement,true);    
	}
	else { // mo child nodes
    
    var ClickableElement = addImageNode(TagEmptyElement,'add','Clickable') ; // XXX Remplacer par une image
    ClickableElement.onclick  = function() {ToggleElementVisibility(this); };
    ClickableElement.id = 'div_empty_' + IDCounter;	
		
    AddTextNode(TagEmptyElement,'<','Utility') ;
    AddTextNode(TagEmptyElement,RootNode.nodeName ,'NodeName'); 
    for (var i = 0; RootNode.attributes && i < RootNode.attributes.length; ++i) {
      CurrentAttribute  = RootNode.attributes.item(i);
      AddTextNode(TagEmptyElement,' ' + CurrentAttribute.nodeName ,'AttributeName') ;
      AddTextNode(TagEmptyElement,'=','Utility') ;
      AddTextNode(TagEmptyElement,'"' + CurrentAttribute.nodeValue + '"','AttributeValue') ;
    }

    AddTextNode(TagEmptyElement,'>  </','Utility') ;
    AddTextNode(TagEmptyElement,RootNode.nodeName,'NodeName') ;
    AddTextNode(TagEmptyElement,'>','Utility') ;
    xmlHolderElement.appendChild(TagEmptyElement);	
    SetVisibility(TagEmptyElement,false);
    //----------------------------------------------
    
    var TagElement = document.createElement('div');
    TagElement.className = 'Element';
    TagElement.style.position = 'relative';
    TagElement.style.left = NestingIndent+'px';
    ClickableElement = addImageNode(TagElement,'remove','Clickable'); // XXX Remplacer par une image
    ClickableElement.onclick  = function() {ToggleElementVisibility(this); };
    ClickableElement.id = 'div_content_' + IDCounter;		
    ++IDCounter;
    AddTextNode(TagElement,'<','Utility') ;
    AddTextNode(TagElement,RootNode.nodeName ,'NodeName') ;
    
    for (var i = 0; RootNode.attributes && i < RootNode.attributes.length; ++i) {
        CurrentAttribute  = RootNode.attributes.item(i);
        AddTextNode(TagElement,' ' + CurrentAttribute.nodeName ,'AttributeName') ;
        AddTextNode(TagElement,'=','Utility') ;
        AddTextNode(TagElement,'"' + CurrentAttribute.nodeValue + '"','AttributeValue') ;
    }
    AddTextNode(TagElement,'>','Utility') ;
    TagElement.appendChild(document.createElement('br'));
    var NodeContent = null;
    for (var i = 0; RootNode.childNodes && i < RootNode.childNodes.length; ++i) {
      if (RootNode.childNodes.item(i).nodeName != '#text') {
        Result &= ShowXML(TagElement,RootNode.childNodes.item(i),indent+1);
      }
      else {
        NodeContent =RootNode.childNodes.item(i).nodeValue;
      }					
    }			
    if (RootNode.nodeValue) {
      NodeContent = RootNode.nodeValue;
    }
    if (NodeContent) {	
      var ContentElement = document.createElement('div');
      ContentElement.style.position = 'relative';
      ContentElement.style.left = NestingIndent+'px';			
      AddTextNode(ContentElement,NodeContent ,'NodeValue') ;
      TagElement.appendChild(ContentElement);
    }			
    AddTextNode(TagElement,'  </','Utility') ;
    AddTextNode(TagElement,RootNode.nodeName,'NodeName') ;
    AddTextNode(TagElement,'>','Utility') ;
    xmlHolderElement.appendChild(TagElement);	
  }
	
	// if (indent==0) { ToggleElementVisibility(TagElement.childNodes(0)); } - uncomment to collapse the external element
	return Result;
}
function AddTextNode(ParentNode,Text,Class) 
{
	NewNode = document.createElement('span');
	if (Class) {  NewNode.className  = Class;}
	if (Text) { NewNode.appendChild(document.createTextNode(Text)); }
	if (ParentNode) { ParentNode.appendChild(NewNode); }
	return NewNode;		
}

// TODO Change for div element add/remove
// XXX Adding by NIST
function addImageNode(parentNode, type, className)
{	
	node = document.createElement('img');
	
	switch(type)
	{
		case 'add':
			node.setAttribute('src', 'data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAACUUlEQVQokZWSX2hScRTHz9W5uZlzms02nH82wv3PKFeO5qAYQqOHHlrPg156ihZE0J/XInqKvQhBDwU9VC+VyCzb+rNyNEJxstqmd7pdU3N679V7U3/3Tw+7SMIe6rwd+J7z+XK+BxNFEf6nGv5uSDYXTS2Hk0GSLfACr1So7CbnEZNTrzbUNFiNsJYOz0Wf6zTttg57c+O+Kl/Nlogv64Eyg84fmz5qcdYNrKXDr8KPD3ePHjIMx6i1NLuNBKRp1LS3GBd/+NY34xddl0e6T0qWSDbnjz4bsDis7f2BbS/LsEjklMomBpU2i7Eh8/Hib/rRh1nT/u6Dmk4ZAKwQXxuUSsuBvk+pt2VUZhF7ZeTWpeFrVCWfp9LB1PwJ2ykSZRdW/QAgA4BwcslssH0vRHJ0jmYpiins2iXwZLXMMPTONoWP9o75V7ySpTyT61eoEjSOhPJ1593aQWanngLAjHeKIGODekeaCkgEjucYRJeqFJKjPW8v8gIGIsdzEqGlSU3kE6omNcnmZ95NM79oz4UXu7sBQIbJO1vNyQyubdFJBLvJGcKDJpVVRBWM57RtqtpugQdMxLo0Vl/ozcTgpJRDrpi557upVMsdPeOLuI8XOF7gBB4DEBVy+XjP5FzodZxIeaafGHUmKbhl/LNn/r5e3zbWO7FF4gQZFwXBqO0xasy+0MvIxsbtc3dOD7jrXmMp9vHh+wc7lYyrz2Vo7QCArXzC/y3QiKmunrmxq64bAICfJLGw6p+LeLN0hhdQa7PWPXTWPTzZpTPv8Xz/WH8AA8ItNSarPAgAAAAASUVORK5CYII=');
			node.setAttribute('alt', 'add');
			break;
		case 'remove':
			node.setAttribute('src', 'data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAACJ0lEQVQokZVSS28SYRS9MzDQwgAVEhBoS9Q2JkRpF7UGWkWNj4XUP+CiC2Ncd92dGxNXxrgxLnysfC9MbdKa4INgIjRpusEQoQgIFjqD5TWvj+/7XEhqIV3o3d3knJxzzz0MpRT+Z/R7FyRst9aS9cRnVBMJJToLbw3O2E6EjM6DuxhmV6G9sb794qnZ4+InJlmblSoKqpbF6LsmJsNXrx2YCvUQ2hvr1SeP7LMzfCDQyaVopQCaxvB2dmRUWH5b+lk8dH3BMX2qawkJgvD8mWN6ynzcjz68lmSFwcho4BipiX+kh0JBbbW5+fieyXdk0OVhAaCV/GI0603H/Ci2jFWZqBInNciOiBs1okhafNUZPsdWypXYStdS/uaiY8Kv7yhSIY1S2b5YjE4b6xxt1+XvQjZ496UeANQdUW8ywbc0qKrrwas+Qnk+wrXQwGRQ/hoHABYAqIZwo0GadQNW9s2+0yEAQBjUPZq12eRCbtBs7RTF8nykH86yRq+vnts0WOxdBevJkLCWAPc4bqgcz+0FY0ox1XG+8Xwq6j4b6RKGgrOa2y18ihovRIjGMjodAGBgMKZA9Lbzc/n3Sx2e95y58vdxtWQ8e/+2neOd4YtaPqPmsgSRgbExw/DhYvRNsVUILNzyhC71VENMxDIP70Bta+Ro0ODyAoBUzmdSH4nV4r+x+AfdQwAAeatUia2UYkvqryrVkM5h94bnPKcvm92+fcr3j/MbY+YNcy1xI5AAAAAASUVORK5CYII=');
			node.setAttribute('alt', 'remove');
			break;
		default:
			break;
	}
	
	parentNode.appendChild(node);
	
	return node;
}



function CompatibleGetElementByID(id)
{
	if (!id) { return null; }
	if (document.getElementById) { // DOM3 = IE5, NS6
		return document.getElementById(id);
	}
	else {
		if (document.layers) { // Netscape 4
			return document.id;
		}
		else { // IE 4
			return document.all.id;
		}
	}
}
function SetVisibility(HTMLElement,Visible)
{
	if (!HTMLElement) { return; }
	var VisibilityStr  = (Visible) ? 'block' : 'none';
	if (document.getElementById) { // DOM3 = IE5, NS6
		HTMLElement.style.display =VisibilityStr; 
	}
	else {
		if (document.layers) { // Netscape 4
			HTMLElement.display = VisibilityStr; 
		}
		else { // IE 4
			HTMLElement.id.style.display = VisibilityStr; 
		}
	}
}
function ToggleElementVisibility(Element)
{
	if (!Element|| !Element.id) { return; }
	try {
		ElementType = Element.id.slice(0,Element.id.lastIndexOf('_')+1);
		ElementID = parseInt(Element.id.slice(Element.id.lastIndexOf('_')+1));
	}
	catch(e) { return ; }
	var ElementToHide = null;
	var ElementToShow= null;
	if (ElementType=='div_content_') {
		ElementToHide = 'div_content_' + ElementID;
		ElementToShow = 'div_empty_' + ElementID;
	}
	else if (ElementType=='div_empty_') {
		ElementToShow= 'div_content_' + ElementID;
		ElementToHide  = 'div_empty_' + ElementID;
	}
	ElementToHide = CompatibleGetElementByID(ElementToHide);
	ElementToShow = CompatibleGetElementByID(ElementToShow);
	if (ElementToHide) { ElementToHide = ElementToHide.parentNode;}
	if (ElementToShow) { ElementToShow = ElementToShow.parentNode;}
	SetVisibility(ElementToHide,false);
	SetVisibility(ElementToShow,true);
}