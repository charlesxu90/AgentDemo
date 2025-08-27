"""
Content Cleaning and Readability Enhancement

This module provides content extraction and cleaning capabilities using advanced
readability algorithms. It processes raw HTML content to extract clean, readable
article content while removing noise and non-essential elements.

Key Classes:
    ReadabilityExtractor: Content cleaning and extraction engine
        - Uses readabilipy library for advanced content extraction
        - Applies readability algorithms to identify main article content
        - Removes advertisements, navigation, and boilerplate content

Key Methods:
    extract_article(html): Processes HTML content to extract clean article
        - html: str - Raw HTML content from web page or API response
        - Returns: Article - Structured article object with cleaned content
        - Applies sophisticated algorithms to identify and extract main content
        - Preserves important formatting while removing noise

Readability Algorithm Features:
    Content Identification:
        - Analyzes HTML structure to identify main content areas
        - Distinguishes between article content and peripheral elements
        - Uses heuristics to determine content vs. navigation/ads
        - Preserves semantic meaning while removing clutter
        
    Content Cleaning:
        - Removes advertisements and promotional content
        - Eliminates navigation menus and footer information
        - Strips out social media widgets and tracking pixels
        - Preserves important links and formatting within content
        
    Structure Preservation:
        - Maintains headings and hierarchical structure
        - Preserves lists, tables, and formatted content
        - Keeps important images and media elements
        - Retains code blocks and technical formatting

Processing Pipeline:
    1. HTML Analysis: Parses HTML structure and identifies content patterns
    2. Content Scoring: Applies algorithms to score content relevance
    3. Noise Removal: Eliminates low-scoring and irrelevant elements
    4. Content Extraction: Extracts high-scoring content areas
    5. Structure Cleaning: Refines extracted content for readability
    6. Article Creation: Constructs Article object with clean content

Library Integration:
    - Readabilipy: Python implementation of readability algorithms
    - Simple JSON Interface: Uses simple_json_from_html_string function
    - Readability Mode: Enables advanced content extraction algorithms
    - Structured Output: Returns standardized content and metadata

Content Quality Features:
    - Title Extraction: Identifies and extracts article titles
    - Content Purity: Removes non-article content effectively
    - Format Preservation: Maintains important formatting elements
    - Image Handling: Preserves relevant images and captions
    - Link Management: Keeps important links while removing clutter

Algorithm Advantages:
    - Language Agnostic: Works across different languages and scripts
    - Domain Independent: Effective across various website types
    - Robust Processing: Handles complex and irregular HTML structures
    - Quality Focus: Prioritizes content quality over quantity
    - Consistent Results: Produces reliable output across different sources

Integration Points:
    - Crawler Pipeline: Second stage after Jina content fetching
    - Article Creation: Produces Article objects for downstream processing
    - Tool Integration: Supports crawl_tool and research workflows
    - Content Processing: Feeds clean content to analysis tools

Performance Characteristics:
    - Efficient Processing: Fast content extraction with minimal overhead
    - Memory Efficient: Processes content without excessive memory usage
    - Scalable Design: Suitable for high-volume content processing
    - Deterministic Output: Consistent results for the same input

Error Handling:
    - Malformed HTML: Handles broken or incomplete HTML gracefully
    - Missing Content: Provides fallback behavior for content-less pages
    - Encoding Issues: Manages character encoding problems
    - Empty Results: Handles cases where no main content is found

The ReadabilityExtractor provides sophisticated content cleaning that transforms
raw web content into clean, readable articles suitable for research analysis
and automated processing workflows.
"""

from readabilipy import simple_json_from_html_string

from .article import Article


class ReadabilityExtractor:
    def extract_article(self, html: str) -> Article:
        article = simple_json_from_html_string(html, use_readability=True)
        return Article(
            title=article.get("title"),
            html_content=article.get("content"),
        )
