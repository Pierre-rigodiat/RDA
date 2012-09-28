<html>
<head>
<title>Add Element</title>
<script type="text/javascript">
this.num = 1;
function addElement(){
	$top = document.getElementById('top');
	newId = document.createElement('div');
	id = 'my'+this.num;
	newId.setAttribute('id', id );
	newId.innerHTML = "<a href='javascript:void(0); ' onclick='removedThis("+id +")' >Added Element"+id+"</a>";
	$top.appendChild(newId);
	this.num++;
}

function removedThis( id ){
	var d = document.getElementById('top');
	d.removeChild(id);
}
</script>
</head>
<body>
<input type="button" name="button" value="Add Element" onclick="addElement()" />
<div id="top" ></div>
</body>
</html>