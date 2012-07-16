<?xml version="1.0" encoding="ISO-8859-1"?>

<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<!-- LEVEL 0 -->
<!-- Display the title then call the required templates -->
<xsl:template match="/">
	<html>
	<body>
	<h2>Experiment description</h2>
	<xsl:apply-templates select="experiment/datas"/>
	<xsl:apply-templates select="experiment/materials"/>
	<xsl:apply-templates select="experiment/preparation"/>
	<xsl:apply-templates select="experiment/temperature"/>
	<xsl:apply-templates select="experiment/pressure"/>
	<xsl:apply-templates select="experiment/duration"/>
	<xsl:apply-templates select="experiment/properties"/>
	</body>
	</html>
</xsl:template>

<!-- LEVEL 1 -->
<!-- Display the data title then call the required templates -->
<xsl:template match="experiment/datas">
	<h3>Experiment</h3>
	<p>
	<xsl:apply-templates select="id"/>
	<xsl:apply-templates select="type"/>
	<xsl:apply-templates select="description"/>
	<xsl:apply-templates select="measuredParameters"/>
	</p>
</xsl:template>

<!-- Display the material title then call the required templates -->
<xsl:template match="experiment/materials">
	<h3>Material</h3>
	<p>
	<xsl:apply-templates select="constituents"/>
	<xsl:apply-templates select="diffusingSpecie"/>
	<xsl:apply-templates select="phases"/>
	<xsl:apply-templates select="bulkComposition"/>
	</p>
</xsl:template>

<!-- Display the preparation title then call the required templates -->
<xsl:template match="experiment/preparation">
	<h3>Preparations</h3>
	<p>
	<xsl:apply-templates select="preparationContainer"/>
	<xsl:apply-templates select="samplePreparationMethod"/>
	<xsl:apply-templates select="samplePreparationSteps"/>
	</p>
</xsl:template>

<!-- Display the experiment temperature title then display its value in the required format -->
<xsl:template match="experiment/temperature">
	<p>
	<h3>Experiment Temperature: </h3>
	temperature = <xsl:value-of select="value"/>, <xsl:value-of select="unit"/>
	<!-- Call the error template -->
	<xsl:apply-templates select="error"/>
	</p>
</xsl:template>

<!-- Display the experiment pressure title then display its value in the required format -->
<xsl:template match="experiment/pressure">
	<p>
	<h3>Experiment Pressure: </h3>
	pressure = <xsl:value-of select="value"/>, <xsl:value-of select="unit"/>
	<!-- Call the error template -->
	<xsl:apply-templates select="error"/>
	</p>
</xsl:template>

<!-- Display the experiment duration title then display its value in the required format -->
<xsl:template match="experiment/duration">
	<p>
	<h3>Experiment Duration: </h3>
	duration = <xsl:value-of select="value"/>, <xsl:value-of select="unit"/>
	<!-- Call the error template -->
	<xsl:apply-templates select="error"/>
	</p>
</xsl:template>

<!-- Display the experiment properties title then display its value -->
<xsl:template match="experiment/properties">
	<p>
	<h3>Measurement Properties: </h3>
	<xsl:value-of select="."/>
	</p>
</xsl:template>

<!-- LEVEL 2  Datas-->
<!-- Display the id value -->
<xsl:template match="id">
	Experiment id: <xsl:value-of select="."/>
	<br />
</xsl:template>

<!-- Display the type value -->
<xsl:template match="type">
	Experiment Type: <xsl:value-of select="."/>
	<br />
</xsl:template>

<!-- Display the description value -->
<xsl:template match="description">
	Comment: <xsl:value-of select="."/>
	<br />
</xsl:template>

<!-- Display the measuredParameters value -->
<xsl:template match="measuredParameters">
	Measured Parameters: <xsl:value-of select="."/>
	<br />
</xsl:template>

<!-- LEVEL 2  Material-->
<!-- Display the constituent value in the required format -->
<xsl:template match="constituents">
	Constituents: <xsl:for-each select="constituent"><xsl:value-of select="."/></xsl:for-each>
	<br />
</xsl:template>

<!-- Display the diffusingSpecie value -->
<xsl:template match="diffusingSpecie">
	Diffusing Specie: <xsl:value-of select="."/>
	<br />
</xsl:template>

<!-- Display the phases value in the required format then call the crystalStructure template-->
<xsl:template match="phases">
	Phases: 	
		<!-- For each phase tag -->
		<xsl:for-each select="phase">Phase of {<xsl:value-of select="name"/>, <xsl:value-of select="bulkFraction"/>, <xsl:apply-templates select="crystalStructure"/>}</xsl:for-each>
	<br />
</xsl:template>

<!-- Display the bulkComposition value in the required format -->
<xsl:template match="bulkComposition">
	Bulk Composition: {<xsl:value-of select="constituent"/>, <xsl:value-of select="bulkFraction"/>, <xsl:value-of select="materialPurity"/>, <xsl:value-of select="materialForm"/>}
	<br />
</xsl:template>

<!-- ./Phases/Phase/crystalStructure -->
<!-- Display the crystalStructure value in the required format -->
<xsl:template match="crystalStructure">
	(<xsl:value-of select="spaceGroup"/>, <xsl:value-of select="wyckoffSequence"/>)
</xsl:template>

<!-- LEVEL 2  Preparations-->
<!-- Display the preparationContainer value -->
<xsl:template match="preparationContainer">
	Container: <xsl:value-of select="."/>
	<br />
</xsl:template>

<!-- Display the samplePreparationMethod value -->
<xsl:template match="samplePreparationMethod">
	Sample Preparation Method: <xsl:value-of select="."/>
	<br />
</xsl:template>

<!-- Display the samplePreparationSteps value in the required format -->
<xsl:template match="samplePreparationSteps">
	<!-- For each samplePreparationStep tag -->
	<xsl:for-each select="samplePreparationStep">
	<!-- Display the comment value then call the surround template -->
	<xsl:value-of select="comment"/> {<xsl:apply-templates select="surround"/>
	<!-- Test if the temperature tag is present. If yes, call its template. If not, display NA instead. -->
	<xsl:choose>
		<xsl:when test="not(temperature)">
			; NA
		</xsl:when>
		<xsl:otherwise>
          <xsl:apply-templates select="temperature"/>
		</xsl:otherwise>
	</xsl:choose>
	<!-- Test if the pressure tag is present. If yes, call its template. If not, display NA instead. -->
	<xsl:choose>
		<xsl:when test="not(pressure)">
			; NA
		</xsl:when>
		<xsl:otherwise>
          <xsl:apply-templates select="pressure"/>
		</xsl:otherwise>
	</xsl:choose>
	<!-- Test if the duration tag is present. If yes, call its template. If not, display NA instead. -->
	<xsl:choose>
		<xsl:when test="not(duration)">
			; NA
		</xsl:when>
		<xsl:otherwise>
          <xsl:apply-templates select="duration"/>
		</xsl:otherwise>
	</xsl:choose>
	<!-- Test if the method tag is present. If yes, call its template. If not, display NA instead. -->
	<xsl:choose>
		<xsl:when test="not(method)">
			; NA
		</xsl:when>
		<xsl:otherwise>
          <xsl:apply-templates select="method"/>
		</xsl:otherwise>
	</xsl:choose>
	<!-- Test if the container tag is present. If yes, call its template. If not, display NA instead. -->
	<xsl:choose>
		<xsl:when test="not(container)">
			; NA
		</xsl:when>
		<xsl:otherwise>
          <xsl:apply-templates select="container"/>
		</xsl:otherwise>
	</xsl:choose>
	<!-- Test if the sampleGeometry tag is present. If yes, call its template. If not, display NA instead. -->
	<xsl:choose>
		<xsl:when test="not(sampleGeometry)">
			; NA
		</xsl:when>
		<xsl:otherwise>
          <xsl:apply-templates select="sampleGeometry"/>
		</xsl:otherwise>
	</xsl:choose>
	 }
	<br /></xsl:for-each>
</xsl:template>

<!-- ./samplePreparationStep/Surround -->
<!-- Display the surround value in the required format -->
<xsl:template match="surround">
	(<xsl:value-of select="constituent"/>, <xsl:value-of select="bulkFraction"/>, 
	<!-- Test if the materialPurity tag is present. If yes, display its value. If not, display NA instead. -->
	<xsl:choose>
		<xsl:when test="not(materialPurity)">
			NA
		</xsl:when>
		<xsl:otherwise>
          <xsl:value-of select="materialPurity"/>
		</xsl:otherwise>
	</xsl:choose>, <xsl:value-of select="materialForm"/>)
</xsl:template>

<!-- ./samplePreparationStep/Temperature -->
<!-- Display the temperature value in the required format -->
<xsl:template match="temperature">
	; (<xsl:value-of select="value"/>, <xsl:value-of select="unit"/><xsl:apply-templates select="error"/>)
</xsl:template>

<!-- ./samplePreparationStep/Pressure -->
<!-- Display the pressure value in the required format -->
<xsl:template match="pressure">
	; (<xsl:value-of select="value"/>, <xsl:value-of select="unit"/><xsl:apply-templates select="error"/>)
</xsl:template>

<!-- ./samplePreparationStep/Duration -->
<!-- Display the duration value in the required format -->
<xsl:template match="duration">
	; (<xsl:value-of select="value"/>, <xsl:value-of select="unit"/><xsl:apply-templates select="error"/>)
</xsl:template>

<!-- ./samplePreparationStep/Method -->
<xsl:template match="method">
	; <xsl:value-of select="."/>
</xsl:template>

<!-- ./samplePreparationStep/Container -->
<xsl:template match="container">
	; <xsl:value-of select="."/>
</xsl:template>

<!-- ./samplePreparationStep/sampleGeometry -->
<xsl:template match="sampleGeometry">
	; <xsl:value-of select="."/>
</xsl:template>

<!-- Error Template for Measurements -->
<!-- Display the error value in the required format -->
<xsl:template match="error">
	, +/- <xsl:value-of select="."/>
	<!-- Test either the attribute type equals 'percentage'. If yes, display its value with '%'.-->
	<xsl:if test=".[@type='percentage']">%</xsl:if>
</xsl:template>

</xsl:stylesheet>
