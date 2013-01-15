// TODO Review the whole file tree
// XXX js/util/php.js + js/util/xpath.js etc.

// ************************************
// php.js functions


function utf8_decode (str_data) {
	// Converts a UTF-8 encoded string to ISO-8859-1  
	// 
	// version: 1109.2015
	// discuss at: http://phpjs.org/functions/utf8_decode
	// +   original by: Webtoolkit.info (http://www.webtoolkit.info/)
	// +      input by: Aman Gupta
	// +   improved by: Kevin van Zonneveld (http://kevin.vanzonneveld.net)
	// +   improved by: Norman "zEh" Fuchs
	// +   bugfixed by: hitwork
	// +   bugfixed by: Onno Marsman
	// +      input by: Brett Zamir (http://brett-zamir.me)
	// +   bugfixed by: Kevin van Zonneveld (http://kevin.vanzonneveld.net)
	// *     example 1: utf8_decode('Kevin van Zonneveld');
	// *     returns 1: 'Kevin van Zonneveld'
	var tmp_arr = [],
	i = 0,
	ac = 0,
	c1 = 0,
	c2 = 0,
	c3 = 0;

	str_data += '';

	while (i < str_data.length) {
		c1 = str_data.charCodeAt(i);
		if (c1 < 128) {
			tmp_arr[ac++] = String.fromCharCode(c1);
			i++;
		} else if (c1 > 191 && c1 < 224) {
			c2 = str_data.charCodeAt(i + 1);
			tmp_arr[ac++] = String.fromCharCode(((c1 & 31) << 6) | (c2 & 63));
			i += 2;
		} else {
			c2 = str_data.charCodeAt(i + 1);
			c3 = str_data.charCodeAt(i + 2);
			tmp_arr[ac++] = String.fromCharCode(((c1 & 15) << 12) | ((c2 & 63) << 6) | (c3 & 63));
			i += 3;
		}
	}

	return tmp_arr.join('');
}

function unserialize (data) {
	// Takes a string representation of variable and recreates it  
	// 
	// version: 1109.2015
	// discuss at: http://phpjs.org/functions/unserialize
	// +     original by: Arpad Ray (mailto:arpad@php.net)
	// +     improved by: Pedro Tainha (http://www.pedrotainha.com)
	// +     bugfixed by: dptr1988
	// +      revised by: d3x
	// +     improved by: Kevin van Zonneveld (http://kevin.vanzonneveld.net)
	// +        input by: Brett Zamir (http://brett-zamir.me)
	// +     improved by: Kevin van Zonneveld (http://kevin.vanzonneveld.net)
	// +     improved by: Chris
	// +     improved by: James
	// +        input by: Martin (http://www.erlenwiese.de/)
	// +     bugfixed by: Kevin van Zonneveld (http://kevin.vanzonneveld.net)
	// +     improved by: Le Torbi
	// +     input by: kilops
	// +     bugfixed by: Brett Zamir (http://brett-zamir.me)
	// -      depends on: utf8_decode
	// %            note: We feel the main purpose of this function should be to ease the transport of data between php & js
	// %            note: Aiming for PHP-compatibility, we have to translate objects to arrays
	// *       example 1: unserialize('a:3:{i:0;s:5:"Kevin";i:1;s:3:"van";i:2;s:9:"Zonneveld";}');
	// *       returns 1: ['Kevin', 'van', 'Zonneveld']
	// *       example 2: unserialize('a:3:{s:9:"firstName";s:5:"Kevin";s:7:"midName";s:3:"van";s:7:"surName";s:9:"Zonneveld";}');
	// *       returns 2: {firstName: 'Kevin', midName: 'van', surName: 'Zonneveld'}
	var that = this;
	var utf8Overhead = function (chr) {
		// http://phpjs.org/functions/unserialize:571#comment_95906
		var code = chr.charCodeAt(0);
		if (code < 0x0080) {
			return 0;
		}
		if (code < 0x0800) {
			return 1;
		}
		return 2;
	};


	var error = function (type, msg, filename, line) {
		throw new that.window[type](msg, filename, line);
	};
	var read_until = function (data, offset, stopchr) {
		var buf = [];
		var chr = data.slice(offset, offset + 1);
		var i = 2;
		while (chr != stopchr) {
			if ((i + offset) > data.length) {
				error('Error', 'Invalid');
			}
			buf.push(chr);
			chr = data.slice(offset + (i - 1), offset + i);
			i += 1;
		}
		return [buf.length, buf.join('')];
	};
	var read_chrs = function (data, offset, length) {
		var buf;

		buf = [];
		for (var i = 0; i < length; i++) {
			var chr = data.slice(offset + (i - 1), offset + i);
			buf.push(chr);
			length -= utf8Overhead(chr);
		}
		return [buf.length, buf.join('')];
	};
	var _unserialize = function (data, offset) {
		var readdata='';
		var readData;
		var chrs = 0;
		var ccount;
		var stringlength;
		var keyandchrs;
		var keys;

		if (!offset) {
			offset = 0;
		}
		var dtype = (data.slice(offset, offset + 1)).toLowerCase();

		var dataoffset = offset + 2;
		var typeconvert = function (x) {
			return x;
		};

		switch (dtype) {
		case 'i':
			typeconvert = function (x) {
			return parseInt(x, 10);
		};
		readData = read_until(data, dataoffset, ';');
		chrs = readData[0];
		readdata = readData[1];
		dataoffset += chrs + 1;
		break;
		case 'b':
			typeconvert = function (x) {
			return parseInt(x, 10) !== 0;
		};
		readData = read_until(data, dataoffset, ';');
		chrs = readData[0];
		readdata = readData[1];
		dataoffset += chrs + 1;
		break;
		case 'd':
			typeconvert = function (x) {
			return parseFloat(x);
		};
		readData = read_until(data, dataoffset, ';');
		chrs = readData[0];
		readdata = readData[1];
		dataoffset += chrs + 1;
		break;
		case 'n':
			readdata = null;
			break;
		case 's':
			ccount = read_until(data, dataoffset, ':');
			chrs = ccount[0];
			stringlength = ccount[1];
			dataoffset += chrs + 2;

			readData = read_chrs(data, dataoffset + 1, parseInt(stringlength, 10));
			chrs = readData[0];
			readdata = readData[1];
			dataoffset += chrs + 2;
			if (chrs != parseInt(stringlength, 10) && chrs != readdata.length) {
				error('SyntaxError', 'String length mismatch');
			}

			// Length was calculated on an utf-8 encoded string
			// so wait with decoding
			readdata = that.utf8_decode(readdata);
			break;
		case 'a':
			readdata = {};

			keyandchrs = read_until(data, dataoffset, ':');
			chrs = keyandchrs[0];
			keys = keyandchrs[1];
			dataoffset += chrs + 2;

			for (var i = 0; i < parseInt(keys, 10); i++) {
				var kprops = _unserialize(data, dataoffset);
				var kchrs = kprops[1];
				var key = kprops[2];
				dataoffset += kchrs;

				var vprops = _unserialize(data, dataoffset);
				var vchrs = vprops[1];
				var value = vprops[2];
				dataoffset += vchrs;

				readdata[key] = value;
			}

			dataoffset += 1;
			break;
		default:
			error('SyntaxError', 'Unknown / Unhandled data type(s): ' + dtype);
		break;
		}
		return [dtype, dataoffset - offset, typeconvert(readdata)];
	};

	return _unserialize((data + ''), 0)[2];
}

//************************************************************************************************
// XPath
// firebug.js

/**
 * Gets an XPath for an element which describes its hierarchical location.
 */
this.getElementXPath = function(element)
{
	if (element && element.id)
		return '//*[@id="' + element.id + '"]';
	else
		return this.getElementTreeXPath(element);
};

this.getElementTreeXPath = function(element)
{
	var paths = [];

	// Use nodeName (instead of localName) so namespace prefix is included (if any).
	for (; element && element.nodeType == 1; element = element.parentNode)
	{
		var index = 0;
		for (var sibling = element.previousSibling; sibling; sibling = sibling.previousSibling)
		{
			// Ignore document type declaration.
			if (sibling.nodeType == Node.DOCUMENT_TYPE_NODE)
				continue;

			if (sibling.nodeName == element.nodeName)
				++index;
		}

		var tagName = element.nodeName.toLowerCase();
		var pathIndex = (index ? "[" + (index+1) + "]" : "");
		paths.splice(0, 0, tagName + pathIndex);
	}

	return paths.length ? "/" + paths.join("/") : null;
};

this.getElementCSSPath = function(element)
{
	var paths = [];

	for (; element && element.nodeType == 1; element = element.parentNode)
	{
		var selector = this.getElementCSSSelector(element);
		paths.splice(0, 0, selector);
	}

	return paths.length ? paths.join(" ") : null;
};

this.cssToXPath = function(rule)
{
	var regElement = /^([#.]?)([a-z0-9\\*_-]*)((\|)([a-z0-9\\*_-]*))?/i;
	var regAttr1 = /^\[([^\]]*)\]/i;
	var regAttr2 = /^\[\s*([^~=\s]+)\s*(~?=)\s*"([^"]+)"\s*\]/i;
	var regPseudo = /^:([a-z_-])+/i;
	var regCombinator = /^(\s*[>+\s])?/i;
	var regComma = /^\s*,/i;

	var index = 1;
	var parts = ["//", "*"];
	var lastRule = null;

	while (rule.length && rule != lastRule)
	{
		lastRule = rule;

		// Trim leading whitespace
		rule = this.trim(rule);
		if (!rule.length)
			break;

		// Match the element identifier
		var m = regElement.exec(rule);
		if (m)
		{
			if (!m[1])
			{
				// XXXjoe Namespace ignored for now
				if (m[5])
					parts[index] = m[5];
				else
					parts[index] = m[2];
			}
			else if (m[1] == '#')
				parts.push("[@id='" + m[2] + "']");
			else if (m[1] == '.')
				parts.push("[contains(concat(' ',normalize-space(@class),' '), ' " + m[2] + " ')]");

			rule = rule.substr(m[0].length);
		}

		// Match attribute selectors
		m = regAttr2.exec(rule);
		if (m)
		{
			if (m[2] == "~=")
				parts.push("[contains(@" + m[1] + ", '" + m[3] + "')]");
			else
				parts.push("[@" + m[1] + "='" + m[3] + "']");

			rule = rule.substr(m[0].length);
		}
		else
		{
			m = regAttr1.exec(rule);
			if (m)
			{
				parts.push("[@" + m[1] + "]");
				rule = rule.substr(m[0].length);
			}
		}

		// Skip over pseudo-classes and pseudo-elements, which are of no use to us
		m = regPseudo.exec(rule);
		while (m)
		{
			rule = rule.substr(m[0].length);
			m = regPseudo.exec(rule);
		}

		// Match combinators
		m = regCombinator.exec(rule);
		if (m && m[0].length)
		{
			if (m[0].indexOf(">") != -1)
				parts.push("/");
			else if (m[0].indexOf("+") != -1)
				parts.push("/following-sibling::");
			else
				parts.push("//");

			index = parts.length;
			parts.push("*");
			rule = rule.substr(m[0].length);
		}

		m = regComma.exec(rule);
		if (m)
		{
			parts.push(" | ", "//", "*");
			index = parts.length-1;
			rule = rule.substr(m[0].length);
		}
	}

	var xpath = parts.join("");
	return xpath;
};

this.getElementsBySelector = function(doc, css)
{
	var xpath = this.cssToXPath(css);
	return this.getElementsByXPath(doc, xpath);
};

this.getElementsByXPath = function(doc, xpath)
{
	var nodes = [];

	try {
		var result = doc.evaluate(xpath, doc, null, XPathResult.ANY_TYPE, null);
		for (var item = result.iterateNext(); item; item = result.iterateNext())
			nodes.push(item);
	}
	catch (exc)
	{
		// Invalid xpath expressions make their way here sometimes.  If that happens,
		// we still want to return an empty set without an exception.
	}

	return nodes;
};

this.getRuleMatchingElements = function(rule, doc)
{
	var css = rule.selectorText;
	var xpath = this.cssToXPath(css);
	return this.getElementsByXPath(doc, xpath);
};