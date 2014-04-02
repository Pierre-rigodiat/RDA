<!--
	Schema Configuration View
	Version 0.2 (12-13-2012)
-->
<div id="featured-wrapper"><div id="featured">
	<h1>Schema View Configuration [DEMO]</h1>
</div></div>

<div id="main">
<div id="schema_prop">
	<div id="main_prop">
		<div class="prop"><span class="fieldname">Filename:</span> test.xsd</div>
		<div class="menu">
			<div class="icon legend refresh">Reload</div>
			<div class="icon legend save">Save</div>	
		</div>
	</div>
	<div id="misc_prop">
		<div class="prop"><span class="fieldname">Last modification:</span> 12-04-2012 11:32am</div>
		<div class="prop"><span class="fieldname">Size:</span> 120 Mo</div>
	</div>
</div>
<div id="schema_content">
	<h3>Modules</h3>
	<div id="schema_modules">
		<div class="module"><span class="icon legend off">Pagination<span class="icon new"></span></span></div>
		<div class="module"><span class="icon legend off">HDF-5</span></div>
		<div class="module"><span class="icon legend disable">Images (Coming soon)</span></div>
		<div class="module"><span class="icon legend disable">Videos (Coming soon)</span></div>
	</div>
	
	<h3>Elements</h3>
	<div id="schema_elements">
		<ul>
			<li id="0"><span class="element_name">Experiment</span>
			<ul>
				<li id="3"><span class="element_name">ExperimentType</span><span class="attr">MAXOCCURS: unbounded</span><span class="icon edit"></span>
			<ul>
				<li id="6"><span class="element_name">Name</span><span class="attr">TYPE: string</span><span class="icon edit"></span></li></ul></li>
				<li id="7"><span class="element_name">Data</span><span class="attr">MAXOCCURS: unbounded</span><span class="icon edit"></span>
			<ul>
				<li id="10"><span class="element_name">Id</span><span class="attr">TYPE: integer</span><span class="icon edit"></span></li>
				<li id="11"><span class="element_name">Type</span><span class="attr">TYPE: string</span><span class="icon edit"></span></li>
				<li id="12"><span class="element_name">Description</span><span class="attr">TYPE: string</span><span class="icon edit"></span></li>
				<li id="13"><span class="element_name">Properties</span><span class="attr">TYPE: string</span><span class="icon edit"></span></li>
				<li id="14"><span class="element_name">Comment</span><span class="attr">MAXOCCURS: unbounded | MINOCCURS: 0 | TYPE: string</span><span class="icon edit"></span></li>
				<li id="15"><span class="element_name">MeasuredParameters</span><span class="icon edit"></span>
			<ul>
				<li id="18"><span class="element_name">Name</span><span class="attr">TYPE: string</span><span class="icon edit"></span></li></ul></li>
				<li id="19"><span class="element_name">Value</span><span class="attr">MAXOCCURS: unbounded</span><span class="icon edit"></span>
			<ul>
				<li id="22"><span class="element_name">Value</span><span class="attr">TYPE: double</span><span class="icon edit"></span></li>
				<li id="23"><span class="element_name">Uncertainty</span><span class="attr">MINOCCURS: 0</span><span class="icon edit"></span>
			<ul>
				<li id="26"><span class="element_name">Type</span><span class="attr">RESTRICTION: amount, fraction</span><span class="icon edit"></span></li>
				<li id="31"><span class="element_name">Value</span><span class="attr">TYPE: double</span><span class="icon edit"></span></li></ul></li>
				<li id="32"><span class="element_name">Unit</span><span class="icon edit"></span>
			<ul>
				<li id="35"><span class="element_name">Name</span><span class="attr">TYPE: string</span><span class="icon edit"></span></li>
				<li id="36"><span class="element_name">UnitOfMeasureType</span><span class="icon edit"></span>
			<ul>
				<li id="39"><span class="element_name">Name</span><span class="attr">TYPE: string</span><span class="icon edit"></span></li></ul></li></ul></li></ul></li></ul></li>
				<li id="40"><span class="element_name">Materials</span><span class="icon edit"></span>
			<ul>
				<li id="43"><span class="element_name">Material</span><span class="attr">MAXOCCURS: unbounded</span><span class="icon edit"></span>
			<ul>
				<li id="46"><span class="element_name">Phases</span><span class="icon edit"></span>
			<ul>
				<li id="49"><span class="element_name">Temperature</span><span class="attr">MINOCCURS: 0</span><span class="icon edit"></span>
			<ul>
				<li id="52"><span class="element_name">Value</span><span class="attr">TYPE: double</span><span class="icon edit"></span></li>
				<li id="53"><span class="element_name">Uncertainty</span><span class="attr">MINOCCURS: 0</span><span class="icon edit"></span>
			<ul>
				<li id="56"><span class="element_name">Type</span><span class="attr">RESTRICTION: amount, fraction</span><span class="icon edit"></span></li>
				<li id="61"><span class="element_name">Value</span><span class="attr">TYPE: double</span><span class="icon edit"></span></li></ul></li>
				<li id="62"><span class="element_name">Unit</span><span class="icon edit"></span>
			<ul>
				<li id="65"><span class="element_name">Name</span><span class="attr">TYPE: string</span><span class="icon edit"></span></li>
				<li id="66"><span class="element_name">UnitOfMeasureType</span><span class="icon edit"></span>
			<ul>
				<li id="69"><span class="element_name">Name</span><span class="attr">TYPE: string</span><span class="icon edit"></span></li></ul></li></ul></li></ul></li>
				<li id="70"><span class="element_name">Phase</span><span class="attr">MAXOCCURS: unbounded</span><span class="icon edit"></span>
			<ul>
				<li id="73"><span class="element_name">Name</span><span class="attr">TYPE: string</span><span class="icon edit"></span></li>
				<li id="74"><span class="element_name">CrystalStructure</span><span class="icon edit"></span>
			<ul>
				<li id="77"><span class="element_name">SpaceGroup</span><span class="attr">MINOCCURS: 0</span><span class="icon edit"></span>
			<ul>
				<li id="80"><span class="element_name">Name</span><span class="attr">TYPE: string</span><span class="icon edit"></span></li></ul></li>
				<li id="81"><span class="element_name">WyckoffSequence</span><span class="attr">MINOCCURS: 0</span><span class="icon edit"></span>
			<ul>
				<li id="84"><span class="element_name">Name</span><span class="attr">TYPE: string</span><span class="icon edit"></span></li></ul></li>
				<li id="85"><span class="element_name">Name</span><span class="attr">TYPE: string</span><span class="icon edit"></span></li></ul></li></ul></li></ul></li>
				<li id="86"><span class="element_name">MaterialName</span><span class="attr">TYPE: string</span><span class="icon edit"></span></li>
				<li id="87"><span class="element_name">BulkComposition</span><span class="icon edit"></span>
			<ul>
				<li id="90"><span class="element_name">Constituents</span><span class="attr">MAXOCCURS: unbounded</span><span class="icon edit"></span>
			<ul>
				<li id="93"><span class="element_name">MaterialPurity</span><span class="attr">MINOCCURS: 0 | TYPE: double</span><span class="icon edit"></span></li>
				<li id="94"><span class="element_name">ChemicalSubstance</span><span class="icon edit"></span>
			<ul>
				<li id="97"><span class="element_name">ChemicalFormula</span><span class="attr">TYPE: string</span><span class="icon edit"></span></li>
				<li id="98"><span class="element_name">Name</span><span class="attr">TYPE: string</span><span class="icon edit"></span></li>
				<li id="99"><span class="element_name">CatalogNumber</span><span class="attr">MAXOCCURS: unbounded | MINOCCURS: 0</span><span class="icon edit"></span>
			<ul>
				<li id="102"><span class="element_name">Id</span><span class="attr">TYPE: string</span><span class="icon edit"></span></li>
				<li id="103"><span class="element_name">CatalogTitle</span><span class="icon edit"></span>
			<ul>
				<li id="106"><span class="element_name">Name</span><span class="attr">TYPE: string</span><span class="icon edit"></span></li></ul></li></ul></li>
				<li id="107"><span class="element_name">Elements</span><span class="attr">MAXOCCURS: unbounded</span><span class="icon edit"></span>
			<ul>
				<li id="110"><span class="element_name">ChemicalSymbol</span><span class="attr">TYPE: string</span><span class="icon edit"></span></li></ul></li></ul></li></ul></li>
				<li id="111"><span class="element_name">BulkFraction</span><span class="icon edit"></span>
			<ul>
				<li id="114"><span class="element_name">Value</span><span class="attr">TYPE: double</span><span class="icon edit"></span></li>
				<li id="115"><span class="element_name">Uncertainty</span><span class="attr">MINOCCURS: 0</span><span class="icon edit"></span>
			<ul>
				<li id="118"><span class="element_name">Type</span><span class="attr">RESTRICTION: amount, fraction</span><span class="icon edit"></span></li>
				<li id="123"><span class="element_name">Value</span><span class="attr">TYPE: double</span><span class="icon edit"></span></li></ul></li>
				<li id="124"><span class="element_name">Unit</span><span class="icon edit"></span>
			<ul>
				<li id="127"><span class="element_name">Name</span><span class="attr">TYPE: string</span><span class="icon edit"></span></li>
				<li id="128"><span class="element_name">UnitOfMeasureType</span><span class="icon edit"></span>
			<ul>
				<li id="131"><span class="element_name">Name</span><span class="attr">TYPE: string</span><span class="icon edit"></span></li></ul></li></ul></li></ul></li>
				<li id="132"><span class="element_name">MaterialForm</span><span class="icon edit"></span>
			<ul>
				<li id="135"><span class="element_name">Name</span><span class="attr">TYPE: string</span><span class="icon edit"></span></li></ul></li></ul></li></ul></li></ul></li>
				<li id="136"><span class="element_name">Id</span><span class="attr">TYPE: integer</span><span class="icon edit"></span></li>
				<li id="137"><span class="element_name">Table</span><span class="attr">MAXOCCURS: unbounded | MINOCCURS: 0</span><span class="icon edit"></span>
			<ul>
				<li id="140"><span class="element_name">HDF5-File</span><span class="icon edit"></span></li>
				<li id="141"><span class="element_name">ColumnUnit</span><span class="attr">MAXOCCURS: unbounded</span><span class="icon edit"></span>
			<ul>
				<li id="144"><span class="element_name">UnitOfMeasureType</span><span class="icon edit"></span>
			<ul>
				<li id="147"><span class="element_name">Name</span><span class="attr">TYPE: string</span><span class="icon edit"></span></li></ul></li>
				<li id="148"><span class="element_name">Field</span><span class="icon edit"></span></li></ul></li></ul></li></ul></li>
		</ul>
	</div>
</div>
</div>

