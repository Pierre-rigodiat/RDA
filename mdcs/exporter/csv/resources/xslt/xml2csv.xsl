<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="text" omit-xml-declaration="yes" indent="no"/>

    <xsl:template match="/">
        
<!--        <xsl:text>$$  POP File
$$ CREATED </xsl:text><xsl:value-of select="$Date" />
        <xsl:text>
$$
$$</xsl:text>-->
        <xsl:text>&#xa;</xsl:text><!--new line-->
        <xsl:for-each select="experiment">
            <xsl:apply-templates select="."/>
            <xsl:text>&#xa;&#xa;</xsl:text>
        </xsl:for-each>
    </xsl:template>
    
    <xsl:template match="experiment">    
        <!-- TABLE VALUES -->
        <!--<xsl:text>TABLE VALUES</xsl:text>-->
        <xsl:text>&#xa;</xsl:text>
        <!--Write Headers-->
        <xsl:for-each select="descendant::profile/table/headers/column">
            <!--Write Header-->
            <xsl:value-of select="."/>
            <!--Write separator-->
            <xsl:text>,</xsl:text>
        </xsl:for-each>
        <xsl:text>&#xa;</xsl:text>
        <xsl:for-each select="descendant::profile/table/rows/row">
            <xsl:for-each select="column">
                <!--Write value-->
                <xsl:value-of select="."/>
                <!--Write separator-->
                <xsl:text>,</xsl:text>
            </xsl:for-each>
            <xsl:text>&#xa;</xsl:text>
        </xsl:for-each>
    </xsl:template>
    
    
</xsl:stylesheet>