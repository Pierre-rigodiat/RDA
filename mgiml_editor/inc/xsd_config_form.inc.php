<div>
	<p class="popup cancelButton">
		<a href="#"> <img src="resources/close.png" width="20px"
			height="20px" />
		</a>
	</p>
	<p class="popup title" id="popup_title"></p>
	
	<form action="main.php" method="post">
	<p>
		Min: <input type="number" min="0" value="1" id="min" name="min"/><br />
		Max unbounded? <input type="checkbox" id="unbounded" name="unbounded" onclick="changeEditionStatus('max')"/><br />
		Max: <input type="number" min="0" value="1" id="max" name="max"/><br />
		<!--Editable? <input type="checkbox" id="editable" name="editable" onclick="changeEditionStatus('type')"/><br /-->
		Type: 
		<select id="type" name="type" id="type">
			<option value="">Select type...</option>
			<option value="int">Integer</option>
			<option value="dbl">Double</option>
			<option value="str">String</option>
		</select><br /> 
		Auto-generate? <input type="checkbox" id="ai" name="ai"/><br />
		<input type="hidden" id="elementId" name="elementId" value=""/>
		
		<input type="button" value="Cancel" onclick="window.location='#'"/>
		<input type="submit" value="Validate" onclick="checkForm()"/>
	</p>
	</form>
</div>