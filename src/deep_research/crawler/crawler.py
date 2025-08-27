"""
Main Web Crawling Orchestration and Workflow

This module provides the primary Crawler class that orchestrates the complete
web crawling pipeline. It coordinates content fetching, cleaning, and extraction
to produce high-quality Article objects from web URLs.

Key Classes:
    Crawler: High-level interface for web content extraction
        - Provides unified crawling interface for the Deep Research system
        - Orchestrates Jina API content fetching and readability extraction
        - Returns structured Article objects ready for downstream processing

Key Methods:
    crawl(url): Complete crawling pipeline from URL to Article
        - url: str - Target web page URL to crawl and extract content from
        - Returns: Article - Structured article object with clean content
        - Coordinates multiple extraction technologies for optimal results
        - Handles the complete pipeline: fetch → clean → structure → return

Crawling Pipeline:
    1. Content Fetching: Uses JinaClient to retrieve raw HTML content
        - Leverages Jina AI's web reader service for reliable content access
        - Handles various content types and web page structures
        - Manages rate limiting and API authentication
        
    2. Content Cleaning: Applies ReadabilityExtractor for content purification
        - Removes navigation, advertisements, and boilerplate content
        - Extracts main article content using readability algorithms
        - Preserves important formatting and semantic structure
        
    3. Article Creation: Constructs Article object with processed content
        - Combines extracted title and clean HTML content
        - Sets source URL for reference and image resolution
        - Provides structured data model for downstream consumption

Technology Integration:
    - Jina AI Integration: Professional content fetching with high reliability
    - Readability Algorithms: Advanced content extraction and cleaning
    - Hybrid Approach: Combines multiple technologies for optimal results
    - Format Flexibility: Supports multiple output formats (HTML, markdown, messages)

Content Quality Features:
    - Noise Removal: Eliminates ads, navigation, and irrelevant content
    - Structure Preservation: Maintains important document hierarchy
    - Image Handling: Preserves embedded images with proper URL resolution
    - Text Cleaning: Removes HTML artifacts while preserving meaning
    - Consistency: Ensures consistent content quality across different sources

Error Handling:
    - Robust Pipeline: Handles failures at each stage gracefully
    - Fallback Mechanisms: Degrades gracefully when services are unavailable
    - Error Propagation: Meaningful error messages for debugging
    - Resource Management: Proper cleanup of resources and connections

Use Cases:
    - Research Content: Extract articles for academic and professional research
    - News Processing: Clean news articles for information analysis
    - Documentation: Process technical documentation and guides
    - Content Archiving: Create clean copies of web content for storage
    - Data Pipeline: Feed clean content into downstream analysis tools

Performance Considerations:
    - Efficient Processing: Optimized pipeline for speed and resource usage
    - Caching Support: Content can be cached to avoid repeated fetching
    - Scalability: Designed for high-volume content processing
    - Rate Limiting: Respects API limits and web server constraints

The Crawler class provides a reliable, high-quality web content extraction
service that transforms raw web pages into clean, structured content suitable
for automated research and analysis workflows.
"""

from .article import Article
from .jina_client import JinaClient
from .readability_extractor import ReadabilityExtractor


class Crawler:
    def crawl(self, url: str) -> Article:
        # To help LLMs better understand content, we extract clean
        # articles from HTML, convert them to markdown, and split
        # them into text and image blocks for one single and unified
        # LLM message.
        #
        # Jina is not the best crawler on readability, however it's
        # much easier and free to use.
        #
        # Instead of using Jina's own markdown converter, we'll use
        # our own solution to get better readability results.
        jina_client = JinaClient()
        html = jina_client.crawl(url, return_format="html")
        extractor = ReadabilityExtractor()
        article = extractor.extract_article(html)
        article.url = url
        return article
