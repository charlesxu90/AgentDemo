"""
Web Content Crawling Tool for Deep Research System

This module provides web crawling capabilities for extracting and processing content
from URLs. It integrates with the Deep Research crawler system to provide clean,
readable content in markdown format for further analysis.

Key Functions:
    crawl_tool(url): Main web crawling function decorated as a LangChain tool
        - Accepts a URL parameter for content extraction
        - Uses the Deep Research Crawler for robust content processing
        - Returns structured data with URL and crawled content
        - Handles errors gracefully with detailed error reporting

Crawling Features:
    - URL Content Extraction: Retrieves and processes web page content
    - Markdown Conversion: Converts HTML content to clean markdown format
    - Content Truncation: Limits output to 1000 characters for efficiency
    - Error Handling: Comprehensive exception handling with logging
    - Structured Output: Returns JSON-like structure with URL and content

Technical Implementation:
    - LangChain Tool Integration: Decorated with @tool for agent compatibility
    - Logging Integration: Enhanced with @log_io decorator for monitoring
    - Type Annotations: Fully typed with Annotated types for validation
    - Crawler Integration: Uses src.deep_research.crawler.Crawler class

Content Processing:
    - HTML Parsing: Intelligent HTML content extraction
    - Text Cleaning: Removes noise and formatting artifacts
    - Markdown Generation: Structured markdown output for readability
    - Content Filtering: Focuses on main article content

Error Handling:
    - Exception Catching: Catches all BaseException types for robustness
    - Error Logging: Detailed error logging for debugging
    - Graceful Degradation: Returns error messages instead of crashing
    - User Feedback: Clear error messages for troubleshooting

Usage in Research Workflow:
    - Article Processing: Extracts content from news articles and blogs
    - Academic Papers: Processes research papers and documentation
    - Web Resources: Handles various web content types
    - Content Analysis: Provides clean text for further NLP processing

The tool enables agents to gather information from web sources by converting
raw HTML content into clean, structured markdown that can be easily processed
by downstream research tools and LLM models.
"""

import logging
from typing import Annotated

from langchain_core.tools import tool

from src.deep_research.crawler import Crawler

from .decorators import log_io

logger = logging.getLogger(__name__)


@tool
@log_io
def crawl_tool(
    url: Annotated[str, "The url to crawl."],
) -> str:
    """Use this to crawl a url and get a readable content in markdown format."""
    try:
        crawler = Crawler()
        article = crawler.crawl(url)
        return {"url": url, "crawled_content": article.to_markdown()[:1000]}
    except BaseException as e:
        error_msg = f"Failed to crawl. Error: {repr(e)}"
        logger.error(error_msg)
        return error_msg
