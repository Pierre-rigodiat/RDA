<?xml version="1.0" encoding="UTF-8"?>
<!--
################################################################################
#
# File Name: xml2html.xsl
# Purpose: 	Renders an XML document in HTML  
#
# Author: Guillaume SOUSA AMARAL
#         guillaume.sousa@nist.gov
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################ 
 -->
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
	<xsl:output method="html" indent="yes" encoding="UTF-8" />	
	
	<xsl:preserve-space elements="*" />
	<xsl:template match="/">	
		<div style="background-color:#fafafa">
			<table>
				<tr style="background-color:#f0f0f0">
					<td style="width:180px" colspan="2">
						<div style="font-size: 25px; float: left; text-decoration: none; cursor: pointer; color: rgb(136, 136, 136);" 
							onmouseover="this.style.textDecoration='underline';this.style.cursor='pointer';this.style.color='blue';" 
							onmouseout="this.style.textDecoration='none';style.color='#888888'" 
							onclick="">
							<xsl:value-of select="//Resource/identity/title"/>
						</div>
						<div style="margin-top:5px;font-size:20px;float:right">
							<div style="float:right;margin:-10px 0px 0px 0px">
								<button class="btn" onclick="dialog_detail(res_utils_get_id(event));" title="Click to view this resource.">Resource Details</button>
								<xsl:variable name="url" select="//Resource/content/referenceURL" />
								<a href="{$url}"><button class="btn" title="Click to view this resource.">Go To</button></a>
							</div></div>
					</td>
				</tr>
				<xsl:apply-templates />
			</table>
		</div>
	</xsl:template>
	<xsl:template match="//*[not(*)]">
		<tr>
			<td width="180">
				<xsl:value-of select="name(.)" />
			</td>
			<td>
				<span class='value'>
					<xsl:value-of select="." />
				</span>
			</td>
		</tr>
	</xsl:template>

</xsl:stylesheet>