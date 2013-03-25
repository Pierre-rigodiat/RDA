<!DOCTYPE html>
<html>
	<head>
	<meta http-equiv="content-type" content="text/html; charset=UTF-8"/>
	
	<link rel="stylesheet" type="text/css" href="resources/css/icons.css" media="screen" />
	<link rel="stylesheet" type="text/css" href="http://code.jquery.com/ui/1.9.2/themes/base/jquery-ui.css" />
	<link rel="stylesheet" type="text/css" href="resources/css/ptester.css" media="screen" />
	
	<script src="//ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>
	<script src="//ajax.googleapis.com/ajax/libs/jqueryui/1.9.2/jquery-ui.min.js"></script>
	
	<script src="front/ptester.js"></script>
	
		<title>MongoDB Insertion</title>
	</head>

	<body id="content-wrapper">
	<h1>MongoDB Insertion</h1>
		<div id="block">
			<label>Choose a translation</label>
			<select id="encode_data">
				<option value="encodeBadgerFish" selected="selected">BadgerFish</option>
				<option value="encodeJSONML">JSONML</option>
 				<option value="encodeGData">GData</option>
				<option value="encodeParker">Parker</option>
				<option value="encodeSpark">Spark</option>
			</select>
			<div class="icon legend encode data">Encode</div>
			<div class="icon legend save mongodb">Save to database</div>
		</div>
		
		<div id="encode_result"></div>
		
	<h1>Retrieve Data</h1>
		<div id="block">
			<label>MongoDB Query</label>
			<select id="query_element">
				<option value="diffusingSpecies">Diffusing Species</option>
				<option value="materialName">Material Name</option>
				<option value="constituentElement">Constituent Element</option>
			</select>
			<textarea rows="1" id="query_target"></textarea>
		<div class="icon legend retrieve data">Retrieve data</div>
		</div>
		
		<div id="query_result"></div>
	
	</body>
</html>