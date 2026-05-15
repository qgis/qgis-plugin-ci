<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="html" encoding="UTF-8" doctype-public="-//W3C//DTD HTML 4.01//EN"/>

    <xsl:template match="/">
        <html lang="en">
            <head>
                <meta charset="UTF-8"/>
                <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
                <title>QGIS Plugin Repository</title>
                <style>
                    * { box-sizing: border-box; margin: 0; padding: 0; }

                    body {
                        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                        background: #f5f5f5;
                        color: #333;
                        padding: 2rem;
                    }

                    header {
                        margin-bottom: 2rem;
                    }

                    header h1 {
                        font-size: 1.75rem;
                        font-weight: 600;
                        color: #1a1a2e;
                    }

                    header p {
                        margin-top: 0.4rem;
                        color: #666;
                        font-size: 0.9rem;
                    }

                    .plugin-grid {
                        display: grid;
                        grid-template-columns: repeat(auto-fill, minmax(420px, 1fr));
                        gap: 1.25rem;
                    }

                    .plugin-card {
                        background: #fff;
                        border: 1px solid #e0e0e0;
                        border-radius: 8px;
                        padding: 1.25rem 1.5rem;
                        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
                    }

                    .plugin-header {
                        display: flex;
                        align-items: flex-start;
                        gap: 1rem;
                        margin-bottom: 0.75rem;
                    }

                    .plugin-icon {
                        width: 48px;
                        height: 48px;
                        object-fit: contain;
                        border-radius: 6px;
                        flex-shrink: 0;
                        background: #f0f0f0;
                    }

                    .plugin-title { flex: 1; }

                    .plugin-title h2 {
                        font-size: 1.05rem;
                        font-weight: 600;
                        color: #1a1a2e;
                        line-height: 1.3;
                    }

                    .plugin-title .version {
                        display: inline-block;
                        margin-top: 0.25rem;
                        font-size: 0.78rem;
                        color: #555;
                        background: #f0f0f0;
                        padding: 0.1rem 0.5rem;
                        border-radius: 12px;
                    }

                    .badge {
                        display: inline-block;
                        font-size: 0.72rem;
                        font-weight: 600;
                        padding: 0.15rem 0.55rem;
                        border-radius: 12px;
                        margin-left: 0.35rem;
                        text-transform: uppercase;
                        letter-spacing: 0.03em;
                    }

                    .badge-experimental {
                        background: #fff3cd;
                        color: #856404;
                        border: 1px solid #ffc107;
                    }

                    .badge-deprecated {
                        background: #f8d7da;
                        color: #842029;
                        border: 1px solid #f5c2c7;
                    }

                    .plugin-description {
                        font-size: 0.875rem;
                        color: #555;
                        line-height: 1.5;
                        margin-bottom: 1rem;
                    }

                    .plugin-meta {
                        display: flex;
                        flex-wrap: wrap;
                        gap: 0.5rem 1.25rem;
                        font-size: 0.8rem;
                        color: #666;
                        border-top: 1px solid #f0f0f0;
                        padding-top: 0.85rem;
                    }

                    .plugin-meta span { white-space: nowrap; }

                    .plugin-meta .label {
                        font-weight: 600;
                        color: #444;
                    }

                    .plugin-actions {
                        margin-top: 1rem;
                        display: flex;
                        flex-wrap: wrap;
                        gap: 0.5rem;
                    }

                    .btn {
                        display: inline-block;
                        font-size: 0.8rem;
                        font-weight: 500;
                        padding: 0.35rem 0.85rem;
                        border-radius: 6px;
                        text-decoration: none;
                        border: 1px solid transparent;
                    }

                    .btn-primary {
                        background: #1a73e8;
                        color: #fff;
                    }

                    .btn-primary:hover { background: #1558b0; }

                    .btn-secondary {
                        background: #fff;
                        color: #444;
                        border-color: #ccc;
                    }

                    .btn-secondary:hover { background: #f5f5f5; }

                    .tags {
                        margin-top: 0.6rem;
                        display: flex;
                        flex-wrap: wrap;
                        gap: 0.35rem;
                    }

                    .tag {
                        font-size: 0.72rem;
                        background: #e8f0fe;
                        color: #1a73e8;
                        padding: 0.15rem 0.55rem;
                        border-radius: 12px;
                    }

                    footer {
                        margin-top: 2.5rem;
                        text-align: center;
                        font-size: 0.8rem;
                        color: #999;
                    }
                </style>
            </head>
            <body>
                <header>
                    <h1>QGIS Plugin Repository</h1>
                    <p>
                        <xsl:value-of select="count(/plugins/pyqgis_plugin)"/>
                        <xsl:text> plugin(s) available</xsl:text>
                    </p>
                </header>

                <div class="plugin-grid">
                    <xsl:apply-templates select="/plugins/pyqgis_plugin"/>
                </div>

                <footer>
                    Generated by <a href="https://github.com/opengisch/qgis-plugin-ci">qgis-plugin-ci</a>
                </footer>
            </body>
        </html>
    </xsl:template>

    <xsl:template match="pyqgis_plugin">
        <div class="plugin-card">
            <div class="plugin-header">
                <xsl:if test="string-length(icon) &gt; 0">
                    <img class="plugin-icon" alt="Plugin icon">
                        <xsl:attribute name="src">
                            <xsl:value-of select="icon"/>
                        </xsl:attribute>
                    </img>
                </xsl:if>
                <div class="plugin-title">
                    <h2>
                        <xsl:value-of select="@name"/>
                        <xsl:if test="experimental = 'True'">
                            <span class="badge badge-experimental">Experimental</span>
                        </xsl:if>
                        <xsl:if test="deprecated = 'True'">
                            <span class="badge badge-deprecated">Deprecated</span>
                        </xsl:if>
                    </h2>
                    <span class="version">v<xsl:value-of select="version"/></span>
                </div>
            </div>

            <p class="plugin-description">
                <xsl:value-of select="description"/>
            </p>

            <xsl:if test="string-length(tags) &gt; 0">
                <div class="tags">
                    <!-- Split tags by comma and render each as a badge.
                         XSL 1.0 has no tokenize(), so we rely on a named template. -->
                    <xsl:call-template name="render-tags">
                        <xsl:with-param name="tags" select="normalize-space(tags)"/>
                    </xsl:call-template>
                </div>
            </xsl:if>

            <div class="plugin-meta">
                <span><span class="label">Author: </span><xsl:value-of select="author_name"/></span>
                <span><span class="label">QGIS: </span>
                    <xsl:value-of select="qgis_minimum_version"/>
                    <xsl:if test="string-length(qgis_maximum_version) &gt; 0">
                        <xsl:text> – </xsl:text>
                        <xsl:value-of select="qgis_maximum_version"/>
                    </xsl:if>
                </span>
                <span><span class="label">Updated: </span><xsl:value-of select="update_date"/></span>
                <xsl:if test="string-length(uploaded_by) &gt; 0">
                    <span><span class="label">By: </span><xsl:value-of select="uploaded_by"/></span>
                </xsl:if>
            </div>

            <div class="plugin-actions">
                <a class="btn btn-primary">
                    <xsl:attribute name="href"><xsl:value-of select="download_url"/></xsl:attribute>
                    Download ZIP
                </a>
                <xsl:if test="string-length(homepage) &gt; 0">
                    <a class="btn btn-secondary" target="_blank" rel="noopener">
                        <xsl:attribute name="href"><xsl:value-of select="homepage"/></xsl:attribute>
                        Homepage
                    </a>
                </xsl:if>
                <xsl:if test="string-length(tracker) &gt; 0">
                    <a class="btn btn-secondary" target="_blank" rel="noopener">
                        <xsl:attribute name="href"><xsl:value-of select="tracker"/></xsl:attribute>
                        Issue Tracker
                    </a>
                </xsl:if>
                <xsl:if test="string-length(repository) &gt; 0">
                    <a class="btn btn-secondary" target="_blank" rel="noopener">
                        <xsl:attribute name="href"><xsl:value-of select="repository"/></xsl:attribute>
                        Source
                    </a>
                </xsl:if>
            </div>
        </div>
    </xsl:template>

    <!-- Recursively split a comma-separated tag string and emit .tag spans -->
    <xsl:template name="render-tags">
        <xsl:param name="tags"/>
        <xsl:choose>
            <xsl:when test="contains($tags, ',')">
                <xsl:variable name="head" select="normalize-space(substring-before($tags, ','))"/>
                <xsl:variable name="tail" select="normalize-space(substring-after($tags, ','))"/>
                <xsl:if test="string-length($head) &gt; 0">
                    <span class="tag"><xsl:value-of select="$head"/></span>
                </xsl:if>
                <xsl:call-template name="render-tags">
                    <xsl:with-param name="tags" select="$tail"/>
                </xsl:call-template>
            </xsl:when>
            <xsl:otherwise>
                <xsl:if test="string-length($tags) &gt; 0">
                    <span class="tag"><xsl:value-of select="$tags"/></span>
                </xsl:if>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

</xsl:stylesheet>
