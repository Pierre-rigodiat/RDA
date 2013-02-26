<!DOCTYPE html>
<html>
	<head>
	<meta http-equiv="content-type" content="text/html; charset=UTF-8"/>
	
	<link rel="stylesheet" type="text/css" href="resources/css/icons.css" media="screen" />
	<link rel="stylesheet" type="text/css" href="http://code.jquery.com/ui/1.9.2/themes/base/jquery-ui.css" />
	
	<script src="//ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>
	<script src="//ajax.googleapis.com/ajax/libs/jqueryui/1.9.2/jquery-ui.min.js"></script>
	
	<script src="front/ptester.js"></script>
	
		<title>MongoDB Insertion</title>
	</head>

	<body id="content-wrapper">
	<h1>MongoDB Insertion</h1>
		<div>
			<label>Choose a translation</label>
			<select id="encode_data">
				<option value="encodeBadgerFish" selected="selected">BadgerFish</option>
 				<option value="encodeGData">GData</option>
				<option value="encodeParker">Parker</option>
				<option value="encodeSpark">Spark</option>
			</select>
			<div class="icon legend encode data">Encode</div>
			<div class="icon legend save mongodb">Save to database</div>
		</div>
		
		<div id="result"></div>
	
	</body>
</html>