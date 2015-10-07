<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="xml" indent="yes" omit-xml-declaration="yes"/>
    
    <xsl:template match="/root">
        <results>
            <xsl:for-each select="experiment">
                <xsl:apply-templates select="."/>
            </xsl:for-each>
        </results>
    </xsl:template>
    
    <xsl:template match="experiment">
        <result>
            <xsl:copy-of select="."/>       
        </result>
    </xsl:template>       
</xsl:stylesheet>