<div id="featured-wrapper"><div id="featured">
	<h1>Data entering [DEMO]</h1>
	<p>
		In this step, you have to fill in the form. During the process you can save your work in order to complete it later.<br/>
		Once you have fill every field, you can view the XML.
	</p>
</div></div>

<div id="main">
<div class="left-side">
	<span class="ctx_menu"><div class="icon begin"></div></span>
	<span class="ctx_menu"><div class="icon previous"></div></span>
	<span class="ctx_menu button">1</span>
	<span class="ctx_menu selected">2</span>
	<span class="ctx_menu button">3</span>
	<span class="ctx_menu button">4</span>
	<span class="ctx_menu button">5</span>
	<span class="ctx_menu"><div class="icon next"></div></span>
	<span class="ctx_menu"><div class="icon end"></div></span>
</div>
	
<div class="right-side">
	<span class="ctx_menu">
		<div class="icon legend long blank">Clear all fields</div>
		<div class="icon legend save">Save</div>
	</span>
</div>
<h5>Experiment</h5>
<form method="post" action="validation.php">
	
	<ul><li id="0"><span class="elementName">experiment</span> 
	<ul><li id="3"><span class="elementName">experimentType</span> <span class="icon add"></span>
	
	<ul><li id="6"><span class="elementName">name</span> <input type="text" class="text"/></li></ul></li>
	<li id="7"><span class="elementName">data</span> <span class="icon add"></span>
	<ul><li id="10"><span class="elementName">id</span> <input type="text" class="text"/></li>
	<li id="11"><span class="elementName">type</span> <input type="text" class="text"/></li>
	<li id="12"><span class="elementName">description</span> <input type="text" class="text"/></li>
	<li id="13"><span class="elementName">properties</span> <input type="text" class="text"/></li>
	<li id="14"><span class="elementName">comment</span> <input type="text" class="text"/><span class="icon add"></span><span class="icon remove"></span></li>
	<li id="15"><span class="elementName">measuredParameters</span> 
	<ul><li id="18"><span class="elementName">name</span> <input type="text" class="text"/></li></ul></li>
	<li id="19"><span class="elementName">value</span> <span class="icon add"></span>
	<ul><li id="22"><span class="elementName">value</span> <input type="text" class="text"/></li>
	<li id="23"><span class="elementName">uncertainty</span> <span class="icon remove"></span>
	<ul><li id="26"><span class="elementName">type</span> <select><option value="amount">amount</option><option value="fraction">fraction</option></select></li>
	<li id="31"><span class="elementName">value</span> <input type="text" class="text"/></li></ul></li>
	<li id="32"><span class="elementName">unit</span> 
	<ul><li id="35"><span class="elementName">name</span> <input type="text" class="text"/></li>
	<li id="36"><span class="elementName">unitOfMeasureType</span> 
	<ul><li id="39"><span class="elementName">name</span> <input type="text" class="text"/></li></ul></li></ul></li></ul></li></ul></li>
	<li id="40"><span class="elementName">materials</span> 
	<ul><li id="43"><span class="elementName">material</span> <span class="icon add"></span>
	<ul><li id="46"><span class="elementName">phases</span> 
	<ul><li id="49"><span class="elementName">temperature</span> <span class="icon remove"></span>
	<ul><li id="52"><span class="elementName">value</span> <input type="text" class="text"/></li>
	<li id="53"><span class="elementName">uncertainty</span> <span class="icon remove"></span>
	<ul><li id="56"><span class="elementName">type</span> <select><option value="amount">amount</option><option value="fraction">fraction</option></select></li>
	<li id="61"><span class="elementName">value</span> <input type="text" class="text"/></li></ul></li>
	<li id="62"><span class="elementName">unit</span> 
	<ul><li id="65"><span class="elementName">name</span> <input type="text" class="text"/></li>
	<li id="66"><span class="elementName">unitOfMeasureType</span> 
	<ul><li id="69"><span class="elementName">name</span> <input type="text" class="text"/></li></ul></li></ul></li></ul></li>
	<li id="70"><span class="elementName">phase</span> <span class="icon add"></span>
	<ul><li id="73"><span class="elementName">name</span> <input type="text" class="text"/></li>
	<li id="74"><span class="elementName">crystalStructure</span> 
	<ul><li id="77"><span class="elementName">spaceGroup</span> <span class="icon remove"></span>
	<ul><li id="80"><span class="elementName">name</span> <input type="text" class="text"/></li></ul></li>
	<li id="81"><span class="elementName">wyckoffSequence</span> <span class="icon remove"></span>
	<ul><li id="84"><span class="elementName">name</span> <input type="text" class="text"/></li></ul></li>
	<li id="85"><span class="elementName">name</span> <input type="text" class="text"/></li></ul></li></ul></li></ul></li>
	<li id="86"><span class="elementName">materialName</span> <input type="text" class="text"/></li>
	<li id="87"><span class="elementName">bulkComposition</span> 
	<ul><li id="90"><span class="elementName">constituents</span> <span class="icon add"></span>
	<ul><li id="93"><span class="elementName">materialPurity</span> <input type="text" class="text"/><span class="icon remove"></span></li>
	<li id="94"><span class="elementName">chemicalSubstance</span> 
	<ul><li id="97"><span class="elementName">chemicalFormula</span> <input type="text" class="text"/></li>
	<li id="98"><span class="elementName">name</span> <input type="text" class="text"/></li>
	<li id="99"><span class="elementName">catalogNumber</span> <span class="icon add"></span><span class="icon remove"></span>
	<ul><li id="102"><span class="elementName">id</span> <input type="text" class="text"/></li>
	<li id="103"><span class="elementName">catalogTitle</span> 
	<ul><li id="106"><span class="elementName">name</span> <input type="text" class="text"/></li></ul></li></ul></li>
	<li id="107"><span class="elementName">elements</span> <span class="icon add"></span>
	<ul><li id="110"><span class="elementName">chemicalSymbol</span> <input type="text" class="text"/></li></ul></li></ul></li></ul></li>
	<li id="111"><span class="elementName">bulkFraction</span> 
	<ul><li id="114"><span class="elementName">value</span> <input type="text" class="text"/></li>
	<li id="115"><span class="elementName">uncertainty</span> <span class="icon remove"></span>
	<ul><li id="118"><span class="elementName">type</span> <select><option value="amount">amount</value><option value="fraction">fraction</value></select></li>
	<li id="123"><span class="elementName">value</span> <input type="text" class="text"/></li></ul></li>
	<li id="124"><span class="elementName">unit</span> 
	<ul><li id="127"><span class="elementName">name</span> <input type="text" class="text"/></li>
	<li id="128"><span class="elementName">unitOfMeasureType</span> 
	<ul><li id="131"><span class="elementName">name</span> <input type="text" class="text"/></li></ul></li></ul></li></ul></li>
	<li id="132"><span class="elementName">materialForm</span> 
	<ul><li id="135"><span class="elementName">name</span> <input type="text" class="text"/></li></ul></li></ul></li></ul></li></ul></li>
	<li id="136"><span class="elementName">id</span> <input type="text" class="text"/></li>
	<li id="137"><span class="elementName">table</span> <span class="icon add"></span><span class="icon remove"></span>
	<ul><li id="140"><span class="elementName">hDF5-File</span> </li>
	<li id="141"><span class="elementName">columnUnit</span> <span class="icon add"></span>
	<ul><li id="144"><span class="elementName">unitOfMeasureType</span> 
	<ul><li id="147"><span class="elementName">name</span> <input type="text" class="text"/></li></ul></li>
	<li id="148"><span class="elementName">field</span> </li></ul></li></ul></li></ul></li></ul>


	<input type="button" class="button" value="Go back"> <input
		type="submit" class="button" value="Download">
</form>

<div class="left-side">
	<span class="ctx_menu"><div class="icon begin"></div></span>
	<span class="ctx_menu"><div class="icon previous"></div></span>
	<span class="ctx_menu button">1</span>
	<span class="ctx_menu selected">2</span>
	<span class="ctx_menu button">3</span>
	<span class="ctx_menu button">4</span>
	<span class="ctx_menu button">5</span>
	<span class="ctx_menu"><div class="icon next"></div></span>
	<span class="ctx_menu"><div class="icon end"></div></span>
</div>
	
<div class="right-side">
	<span class="ctx_menu">
		<div class="icon legend long blank">Clear all fields</div>
		<div class="icon legend save">Save</div>
	</span>
</div>
</div>