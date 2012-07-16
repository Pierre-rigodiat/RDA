<?xml version="1.0" encoding="ISO-8859-1"?>

<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

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

<xsl:template match="experiment/datas">
	<h3>Experiment</h3>
	<p>
	<xsl:apply-templates select="id"/>
	<xsl:apply-templates select="type"/>
	<xsl:apply-templates select="description"/>
	<xsl:apply-templates select="measuredParameters"/>
	</p>
</xsl:template>

<xsl:template match="id">
	Experiment id: <xsl:value-of select="."/>
	<br />
</xsl:template>

<xsl:template match="type">
	Experiment Type: <xsl:value-of select="."/>
	<br />
</xsl:template>

<xsl:template match="description">
	Comment: <xsl:value-of select="."/>
	<br />
</xsl:template>

<xsl:template match="measuredParameters">
	Measured Parameters: <xsl:value-of select="."/>
	<br />
</xsl:template>

<xsl:template match="experiment/materials">
	<h3>Material</h3>
	<p>
	<xsl:apply-templates select="constituents"/>
	<xsl:apply-templates select="diffusingSpecie"/>
	<xsl:apply-templates select="phases"/>
	<xsl:apply-templates select="bulkComposition"/>
	</p>
</xsl:template>

<xsl:template match="constituents">
	Constituents: <xsl:for-each select="constituent"><xsl:value-of select="."/></xsl:for-each>
	<br />
</xsl:template>

<xsl:template match="diffusingSpecie">
	Diffusing Specie: <xsl:value-of select="."/>
	<br />
</xsl:template>

<xsl:template match="phases">
	Phases: <xsl:for-each select="phase">Phase of {<xsl:value-of select="name"/>, <xsl:value-of select="bulkFraction"/>, <xsl:apply-templates select="crystalStructure"/>}</xsl:for-each>
	<br />
</xsl:template>

<xsl:template match="crystalStructure">
	(<xsl:value-of select="spaceGroup"/>, <xsl:value-of select="wyckoffSequence"/>)
</xsl:template>

<xsl:template match="bulkComposition">
	Bulk Composition: {<xsl:value-of select="constituent"/>, <xsl:value-of select="bulkFraction"/>, <xsl:value-of select="materialPurity"/>, <xsl:value-of select="materialForm"/>}
	<br />
</xsl:template>

<xsl:template match="experiment/preparation">
	<h3>Preparations</h3>
	<p>
	<xsl:apply-templates select="preparationContainer"/>
	<xsl:apply-templates select="samplePreparationMethod"/>
	<xsl:apply-templates select="samplePreparationSteps"/>
	</p>
</xsl:template>

<xsl:template match="preparationContainer">
	Container: <xsl:value-of select="."/>
	<br />
</xsl:template>

<xsl:template match="samplePreparationMethod">
	Sample Preparation Method: <xsl:value-of select="."/>
	<br />
</xsl:template>

<xsl:template match="samplePreparationSteps">
	<xsl:for-each select="samplePreparationStep">
	<xsl:value-of select="comment"/> {<xsl:apply-templates select="surround"/>
	<xsl:choose>
		<xsl:when test="not(temperature)">
			; NA
		</xsl:when>
		<xsl:otherwise>
          <xsl:apply-templates select="temperature"/>
		</xsl:otherwise>
	</xsl:choose>
	<xsl:choose>
		<xsl:when test="not(pressure)">
			; NA
		</xsl:when>
		<xsl:otherwise>
          <xsl:apply-templates select="pressure"/>
		</xsl:otherwise>
	</xsl:choose>
	<xsl:choose>
		<xsl:when test="not(duration)">
			; NA
		</xsl:when>
		<xsl:otherwise>
          <xsl:apply-templates select="duration"/>
		</xsl:otherwise>
	</xsl:choose>
	<xsl:choose>
		<xsl:when test="not(method)">
			; NA
		</xsl:when>
		<xsl:otherwise>
          <xsl:apply-templates select="method"/>
		</xsl:otherwise>
	</xsl:choose>
	<xsl:choose>
		<xsl:when test="not(container)">
			; NA
		</xsl:when>
		<xsl:otherwise>
          <xsl:apply-templates select="container"/>
		</xsl:otherwise>
	</xsl:choose>
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

<xsl:template match="surround">
	(<xsl:value-of select="constituent"/>, <xsl:value-of select="bulkFraction"/>, 
	<xsl:choose>
		<xsl:when test="not(materialPurity)">
			NA
		</xsl:when>
		<xsl:otherwise>
          <xsl:value-of select="materialPurity"/>
		</xsl:otherwise>
	</xsl:choose>, <xsl:value-of select="materialForm"/>)
</xsl:template>

<xsl:template match="temperature">
	; (<xsl:value-of select="value"/>, <xsl:value-of select="unit"/><xsl:apply-templates select="error"/>)
</xsl:template>

<xsl:template match="pressure">
	; (<xsl:value-of select="value"/>, <xsl:value-of select="unit"/><xsl:apply-templates select="error"/>)
</xsl:template>

<xsl:template match="duration">
	; (<xsl:value-of select="value"/>, <xsl:value-of select="unit"/><xsl:apply-templates select="error"/>)
</xsl:template>

<xsl:template match="method">
	; <xsl:value-of select="."/>
</xsl:template>

<xsl:template match="container">
	; <xsl:value-of select="."/>
</xsl:template>

<xsl:template match="sampleGeometry">
	; <xsl:value-of select="."/>
</xsl:template>

<xsl:template match="experiment/temperature">
	<p>
	<h3>Experiment Temperature: </h3>
	temperature = <xsl:value-of select="value"/>, <xsl:value-of select="unit"/><xsl:apply-templates select="error"/>
	</p>
</xsl:template>

<xsl:template match="experiment/pressure">
	<p>
	<h3>Experiment Pressure: </h3>
	pressure = <xsl:value-of select="value"/>, <xsl:value-of select="unit"/><xsl:apply-templates select="error"/>
	</p>
</xsl:template>

<xsl:template match="experiment/duration">
	<p>
	<h3>Experiment Duration: </h3>
	duration = <xsl:value-of select="value"/>, <xsl:value-of select="unit"/><xsl:apply-templates select="error"/>
	</p>
</xsl:template>

<xsl:template match="experiment/properties">
	<p>
	<h3>Measurement Properties: </h3>
	<xsl:value-of select="."/>
	</p>
</xsl:template>

<xsl:template match="error">
	, +/- <xsl:value-of select="."/>
	<xsl:if test=".[@type='percentage']">%</xsl:if>
</xsl:template>

</xsl:stylesheet>
