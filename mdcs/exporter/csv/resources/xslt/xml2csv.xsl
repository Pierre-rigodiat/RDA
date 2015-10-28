<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="text" omit-xml-declaration="yes" indent="no"/>

    <xsl:template match="/">
        <xsl:text>&#xa;</xsl:text><!--new line-->
        <xsl:for-each select="//profile/table">
            <xsl:apply-templates select="."/>
            <xsl:text>---END TABLE---</xsl:text>
            <xsl:text>&#xa;</xsl:text>
        </xsl:for-each>
    </xsl:template>

    <xsl:template match="//profile/table">
        <!-- TABLE VALUES -->
        <!--<xsl:text>TABLE VALUES</xsl:text>-->
        <!--Write Headers-->
        <xsl:for-each select="descendant::headers/column">
            <!--Write Header-->
            <xsl:value-of select="."/>
            <!--Write separator-->
            <xsl:text>,</xsl:text>
        </xsl:for-each>
        <xsl:text>&#xa;</xsl:text>
        <xsl:for-each select="descendant::rows/row">
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

