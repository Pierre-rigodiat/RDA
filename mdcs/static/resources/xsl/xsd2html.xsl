<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
	version="1.0">
	<xsl:output method="html" indent="yes" encoding="UTF-8" />
	<xsl:preserve-space elements="*" />
	<xsl:template match="/">	 	
		<ul class="tree">
			<xsl:apply-templates />
		</ul>
	</xsl:template>
	<xsl:template match="*">
		<li>
		<div class="element-wrapper">
			<!-- no left indent for root element -->
			<xsl:if test="not(ancestor::*)">
				<xsl:attribute name="style">left:0</xsl:attribute>
			</xsl:if>	
			<span class="path">
				<xsl:value-of select="name(.)"/>
		        <xsl:variable name="vnumPrecSiblings" select="count(preceding-sibling::*[name()=name(current())])"/>
		        <xsl:if test="$vnumPrecSiblings">
		            <xsl:value-of select="concat('[', $vnumPrecSiblings +1, ']')"/>
		        </xsl:if>
			</span>
			<xsl:choose>
				<!-- Element with children -->
				<xsl:when test="*">
					<span class="collapse" style="cursor:pointer;" onclick="showhide(event);"></span>
					<span class="category">	
						<xsl:choose>
							<xsl:when test="contains(name(.),'sequence')">																		
								<span onclick="showMenuSequence(event)" style="cursor:pointer;">																								
									<xsl:value-of select="name(.)" />
								</span>
							</xsl:when>
							<xsl:otherwise>
								<span>
									<xsl:value-of select="name(.)" />
								</span>
							</xsl:otherwise>						
						</xsl:choose>						
						<xsl:choose>
							<xsl:when test="./@name">
							<span class="type">
								<xsl:value-of select="@name" />
							</span>
							</xsl:when>
						</xsl:choose>
					</span>
				</xsl:when>
				<!-- Element without children -->					
				<xsl:otherwise>
					<span class="element">
						<xsl:choose>
							<xsl:when test="contains(name(.),'sequence')">
								<span onclick="showMenuSequence(event)" style="cursor:pointer;">
									<xsl:value-of select="name(.)" />
								</span>
							</xsl:when>
							<xsl:otherwise>
								<span>
									<xsl:value-of select="name(.)" />
									<xsl:text> : </xsl:text>
								</span>
							</xsl:otherwise>						
						</xsl:choose>						
					</span>
				</xsl:otherwise>
			</xsl:choose>
			<xsl:choose>
				<xsl:when test="not(*)">					
					<xsl:choose>
						<xsl:when test="./@name">
						<span class="name">
							<xsl:value-of select="@name" />
						</span>
						</xsl:when>
					</xsl:choose>
					<xsl:choose>
						<xsl:when test="./@type">
						<span class="type">
							<xsl:value-of select="@type" />
						</span>
						</xsl:when>
					</xsl:choose>
				</xsl:when>
				<xsl:otherwise>
					<ul>
						<xsl:apply-templates />
					</ul>
				</xsl:otherwise>				
			</xsl:choose>
		</div>
		</li>		
	</xsl:template>
</xsl:stylesheet>

