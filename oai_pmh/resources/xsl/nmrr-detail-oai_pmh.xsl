<?xml version="1.0" encoding="UTF-8"?>
<!--
################################################################################
#
# File Name: nmrr-detail-oai_pmh.xsl
# Purpose: 	Renders an XML document in HTML  
#
# Author: Guillaume SOUSA AMARAL
#         guillaume.sousa@nist.gov
#
# Sponsor: National Institute of Standards and Technology (NIST)
#
################################################################################ 
 -->
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"
	xmlns:nr="urn:nist.gov/nmrr.res/1.0wd">
	<xsl:output method="html" indent="yes" encoding="UTF-8" />	
	
	<xsl:template match="/">		
		<div style="background-color:#fafafa">
			<table>
				<tr style="background-color:#f0f0f0">
					<td style="width:180px" colspan="2">
						<xsl:variable name="url" select="//nr:Resource/nr:content/nr:referenceURL" />
						<xsl:choose>
							<xsl:when test="//nr:Resource/nr:content/nr:referenceURL!=''">
								<a target="_blank" href="{$url}"><xsl:value-of select="//nr:Resource/nr:identity/nr:title"/></a>	
							</xsl:when>
							<xsl:otherwise>
								<xsl:value-of select="//nr:Resource/nr:identity/nr:title"/>
							</xsl:otherwise>
						</xsl:choose>
					</td>
				</tr>
				<xsl:apply-templates select="/*" />
				<xsl:apply-templates select="//*[not(*)]" />
				<tr style="background-color:#f0f0f0">
					<td style="width:180px" colspan="2">
						{% if template_name %}
						<span class="alert alert-error" style="float: left;padding:0.3em 0.5em 0em 0.5em;margin: 0em 0.5em 0em 0em;height: 1.8em;">
							<strong>{{template_name}}</strong>
						</span>
						{% endif %}
						{% if oai_pmh %}
						<span class="alert alert-info" style="float: left;padding:0.3em 0.5em 0em 0.5em;margin: 0em 0.5em 0em 0em;height: 1.8em;">
							<strong>OAI-PMH</strong>
						</span>
						<span class="alert alert-success" style="float: left;padding:0.3em 0.5em 0em 0.5em;margin: 0em 0.5em 0em 0em;height: 1.8em;">
							<text>{{registry_name}}</text>
						</span>
						{% endif %}
					</td>
				</tr>
			</table>
		</div>
	</xsl:template>
	
	<xsl:template match="/*">
		<xsl:apply-templates select="@*"/>
	</xsl:template>
	
	<xsl:template match="//*[not(*)]">
		
		<xsl:variable name="name" select="name(.)" />
		<xsl:variable name="value" select="." />		
		
		<xsl:choose>
			<xsl:when test="following-sibling::node()[name()=$name] or preceding-sibling::node()[name()=$name]">
				<xsl:choose>
					<xsl:when test="preceding-sibling::node()[name()=$name]" >
					</xsl:when>
					<xsl:otherwise>
						<tr class="nmrr_line line_{$name}">
							<td width="180">
								<xsl:value-of select="$name" />
							</td>
							<td>
								<span class='value'>
									<xsl:call-template name="join">
										<xsl:with-param name="current" select="$value" />
										<xsl:with-param name="list" select="following-sibling::node()[name()=$name]" />
										<xsl:with-param name="separator" select="', '" />
									</xsl:call-template>
								</span>
							</td>
						</tr>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:when>
			
			<xsl:otherwise>
				<tr class="nmrr_line line_{$name}">
					<td width="180">
						<xsl:value-of select="$name" />
					</td>
					<td>
						<span class='value'>
							<xsl:choose>
								<xsl:when test="contains($name, 'URL')">
									<a target="_blank" href="{$value}"><xsl:value-of select="$value"/></a>							
								</xsl:when>
								<xsl:otherwise>
									<xsl:value-of select="$value"/>
								</xsl:otherwise>
							</xsl:choose>
						</span>
					</td>
				</tr>
			</xsl:otherwise>
		</xsl:choose>
		<xsl:apply-templates select="@*" />
	</xsl:template>
	
	<xsl:template name="join">
		<xsl:param name="current" />
		<xsl:param name="list" />
		<xsl:param name="separator"/>
		
		<xsl:value-of select="$current" />
		<xsl:value-of select="$separator" />
		
		<xsl:for-each select="$list">
			<xsl:value-of select="." />
			<xsl:if test="position() != last()">
				<xsl:value-of select="$separator" />
			</xsl:if>
		</xsl:for-each>
	</xsl:template>
	
	<xsl:template match="@*">
		<xsl:variable name="name" select="name(.)" />
		<xsl:variable name="value" select="." />		
		
		<tr class="nmrr_line line_{$name}">
			<td width="180">
				<xsl:value-of select="$name" />
			</td>
			<td>
				<span class='value'>
					<xsl:choose>
						<xsl:when test="contains($name, 'URL')">
							<a target="_blank" href="{$value}"><xsl:value-of select="$value"/></a>							
						</xsl:when>
						<xsl:otherwise>
							<xsl:value-of select="$value"/>
						</xsl:otherwise>
					</xsl:choose>
				</span>
			</td>
		</tr>
	</xsl:template>
</xsl:stylesheet>