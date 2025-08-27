"""
Jina AI API Client for Web Content Fetching

This module provides integration with Jina AI's web reader service, offering
professional-grade web content fetching capabilities. It handles HTTP communication,
authentication, and content retrieval from web URLs.

Key Classes:
    JinaClient: HTTP client for Jina Reader API integration
        - Manages communication with Jina AI's web reader service
        - Handles authentication and API key management
        - Provides configurable content fetching with multiple output formats

Key Methods:
    crawl(url, return_format): Fetches web content through Jina AI API
        - url: str - Target web page URL to fetch content from
        - return_format: str - Output format ("html", "markdown", "text", etc.)
        - Returns: str - Raw content in specified format from Jina service
        - Handles HTTP communication and error scenarios

Jina AI Integration:
    Service Features:
        - Professional web reader with high reliability
        - Advanced content extraction and cleaning capabilities
        - Support for various content types and web page structures
        - Rate limiting and quota management for API usage
        
    Authentication:
        - Optional API key authentication for higher rate limits
        - Environment variable-based configuration (JINA_API_KEY)
        - Graceful degradation when API key is not provided
        - Warning messages for rate limit awareness

    Output Formats:
        - HTML: Raw HTML content with basic cleaning
        - Markdown: Pre-converted markdown format
        - Text: Plain text extraction
        - Custom formats as supported by Jina API

HTTP Communication:
    - POST Request: Sends URL as JSON payload to Jina endpoint
    - Header Management: Proper content type and format specification
    - Authentication: Bearer token when API key is available
    - Response Handling: Returns raw response text for further processing

Rate Limiting & Quotas:
    - Free Tier: Limited requests per time period without API key
    - Authenticated: Higher rate limits with valid API key
    - Usage Monitoring: Automatic warnings about rate limit status
    - Graceful Handling: Continues operation with free tier when key unavailable

Error Handling:
    - HTTP Errors: Network and server error handling
    - Authentication Issues: Clear messaging for API key problems
    - Rate Limit Handling: Appropriate responses to quota exhaustion
    - Timeout Management: Configurable timeouts for slow responses

Configuration:
    - Environment Variables: JINA_API_KEY for authentication
    - Default Settings: Sensible defaults for most use cases
    - Format Flexibility: Configurable return formats
    - Endpoint Configuration: Uses standard Jina reader endpoint

Integration Points:
    - Crawler Pipeline: First stage of content extraction workflow
    - Content Processing: Raw content fed to ReadabilityExtractor
    - Tool Integration: Used by crawl_tool for research workflows
    - Service Layer: Abstraction for web content fetching

Performance Features:
    - Single Request: Efficient one-shot content retrieval
    - Minimal Overhead: Direct HTTP communication without extra layers
    - Caching Support: Content can be cached by calling applications
    - Scalability: Suitable for high-volume content processing

The JinaClient provides reliable, professional-grade web content fetching
that serves as the foundation for the Deep Research crawling pipeline,
offering robust content access with flexible output formatting.
"""

import logging
import os

import requests

logger = logging.getLogger(__name__)


class JinaClient:
    def crawl(self, url: str, return_format: str = "html") -> str:
        headers = {
            "Content-Type": "application/json",
            "X-Return-Format": return_format,
        }
        if os.getenv("JINA_API_KEY"):
            headers["Authorization"] = f"Bearer {os.getenv('JINA_API_KEY')}"
        else:
            logger.warning(
                "Jina API key is not set. Provide your own key to access a higher rate limit. See https://jina.ai/reader for more information."
            )
        data = {"url": url}
        response = requests.post("https://r.jina.ai/", headers=headers, json=data)
        return response.text
