"""
Web Crawling and Content Extraction Package for Deep Research System

This package provides comprehensive web crawling capabilities for extracting clean,
readable content from web pages. It integrates multiple crawling technologies to
deliver high-quality content extraction for research purposes.

Modules:
    article.py: Article data model and content representation
        - Article: Core data structure for extracted web content
        - to_markdown(): Converts HTML content to clean markdown format
        - to_message(): Prepares content for LLM consumption with text/image blocks
        
    crawler.py: Main crawling orchestration and workflow
        - Crawler: High-level interface for web content extraction
        - crawl(): Complete crawling pipeline from URL to Article
        - Integrates Jina API and readability extraction
        
    jina_client.py: Jina AI API integration for content fetching
        - JinaClient: HTTP client for Jina Reader API
        - crawl(): Fetches web content with configurable output formats
        - Handles authentication and rate limiting
        
    readability_extractor.py: Content cleaning and readability enhancement
        - ReadabilityExtractor: Extracts main content using readability algorithms
        - extract_article(): Processes raw HTML to extract clean article content
        - Removes navigation, ads, and non-content elements

Key Classes:
    Article: Structured representation of web content
        - title: Extracted article title
        - html_content: Clean HTML content
        - url: Source URL for reference
        - Conversion methods for markdown and LLM message formats
        
    Crawler: Main orchestrator for the crawling pipeline
        - Coordinates Jina API fetching and readability extraction
        - Provides unified interface for web content extraction
        - Handles error cases and fallback scenarios
        
    JinaClient: Interface to Jina AI's web reader service
        - HTTP-based content fetching with multiple format options
        - API key management and authentication
        - Rate limiting and quota management
        
    ReadabilityExtractor: Content cleaning and extraction
        - Uses readabilipy library for content extraction
        - Removes boilerplate and extracts main article content
        - Preserves important formatting and structure

Crawling Pipeline:
    1. URL Input: Target web page URL
    2. Content Fetching: Jina API retrieves raw HTML content
    3. Content Extraction: Readability algorithms extract main content
    4. Article Creation: Structured Article object with metadata
    5. Format Conversion: Markdown or LLM message format output

Features:
    - Multi-Format Support: HTML, markdown, and LLM message formats
    - Content Cleaning: Removes ads, navigation, and boilerplate content
    - Image Handling: Preserves and processes embedded images
    - API Integration: Professional content fetching through Jina AI
    - Error Handling: Robust error handling and fallback mechanisms

Use Cases:
    - Research Content: Extract articles for research analysis
    - News Processing: Clean news articles for information extraction
    - Documentation: Process technical documentation and guides
    - Academic Papers: Extract content from scholarly publications
    - Web Archiving: Create clean copies of web content

The package enables reliable web content extraction with professional-grade
content cleaning and formatting suitable for automated research workflows.
"""

from .article import Article
from .crawler import Crawler
from .jina_client import JinaClient
from .readability_extractor import ReadabilityExtractor

__all__ = ["Article", "Crawler", "JinaClient", "ReadabilityExtractor"]
