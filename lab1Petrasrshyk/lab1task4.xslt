<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="html" encoding="utf-8" indent="yes"/>
    <xsl:template match="/">
        <xsl:text disable-output-escaping='yes'>&lt;!DOCTYPE html&gt;</xsl:text>
        <html>
            <head>
                <title>Price list</title>
            </head>
            <body>
                <h2>Price list</h2>
                <xsl:apply-templates/>
            </body>
        </html>
    </xsl:template>

    <xsl:template match="products">
        <table>
            <tr>
                <th>image</th>
                <th>description</th>
                <th>price</th>
            </tr>
            <xsl:apply-templates select="product"/>
        </table>
    </xsl:template>

    <xsl:template match="product">
        <tr>
            <td>
                <img>
                    <xsl:attribute name="src">
                        <xsl:value-of select="@image"/>
                    </xsl:attribute>
                </img>
            </td>
            <td>
                <xsl:value-of select="@description"/>
            </td>
            <td>
                <xsl:value-of select="@price"/>
            </td>
        </tr>
    </xsl:template>
</xsl:stylesheet>