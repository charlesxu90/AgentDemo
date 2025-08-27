"""
Article Data Model and Content Representation

This module defines the Article class, which serves as the primary data structure
for representing extracted web content. It provides methods for converting content
between different formats suitable for various consumption scenarios.

Key Classes:
    Article: Core data structure for web content representation
        - title: str - Extracted article title
        - html_content: str - Clean HTML content from readability extraction
        - url: str - Source URL (set by crawler after extraction)

Key Methods:
    to_markdown(including_title): Converts article content to markdown format
        - including_title: bool - Whether to include title as H1 header
        - Returns clean markdown suitable for text processing
        - Uses markdownify library for HTML to markdown conversion
        - Preserves important formatting while removing HTML complexity
        
    to_message(): Prepares content for LLM consumption with structured blocks
        - Parses markdown to identify text and image components
        - Returns list of message blocks with type annotations
        - Handles image URLs with proper resolution using urljoin
        - Creates structured format compatible with multimodal LLMs

Content Processing Features:
    Markdown Conversion:
        - HTML to markdown transformation using markdownify
        - Optional title inclusion as H1 header
        - Preserves text formatting (bold, italic, links)
        - Maintains list structures and code blocks
        - Removes complex HTML while keeping semantic meaning
        
    LLM Message Format:
        - Structured message blocks for multimodal processing
        - Text blocks for textual content
        - Image blocks with resolved URLs for visual content
        - Alternating pattern recognition using regex
        - Proper URL resolution for relative image paths

Image Handling:
    - Pattern Matching: Uses regex to identify markdown image syntax
    - URL Resolution: Converts relative URLs to absolute using urljoin
    - Content Splitting: Separates text and image content for structured processing
    - Multimodal Support: Prepares content for LLMs that support images

Text Processing:
    - Clean Text Extraction: Removes HTML artifacts and formatting noise
    - Structure Preservation: Maintains important document structure
    - Content Trimming: Strips whitespace and empty elements
    - Format Consistency: Ensures consistent output formatting

Integration Points:
    - Crawler Pipeline: Created by ReadabilityExtractor during content processing
    - Tool Integration: Used by crawl_tool for research workflow integration
    - LLM Processing: to_message() format compatible with multimodal models
    - Content Storage: Serializable structure for caching and persistence

The Article class provides a clean abstraction for web content that bridges
the gap between raw HTML extraction and structured content consumption by
research tools and LLM models.
"""

import re
from urllib.parse import urljoin

from markdownify import markdownify as md


class Article:
    url: str

    def __init__(self, title: str, html_content: str):
        self.title = title
        self.html_content = html_content

    def to_markdown(self, including_title: bool = True) -> str:
        markdown = ""
        if including_title:
            markdown += f"# {self.title}\n\n"
        markdown += md(self.html_content)
        return markdown

    def to_message(self) -> list[dict]:
        image_pattern = r"!\[.*?\]\((.*?)\)"

        content: list[dict[str, str]] = []
        parts = re.split(image_pattern, self.to_markdown())

        for i, part in enumerate(parts):
            if i % 2 == 1:
                image_url = urljoin(self.url, part.strip())
                content.append({"type": "image_url", "image_url": {"url": image_url}})
            else:
                content.append({"type": "text", "text": part.strip()})

        return content
