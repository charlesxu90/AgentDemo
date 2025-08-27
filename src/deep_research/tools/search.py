"""
Multi-Engine Web Search Tool for Deep Research System

This module provides a unified interface for multiple web search engines, enabling
flexible search capabilities across different information sources. It supports
various search providers with configurable parameters and logging integration.

Key Functions:
    get_search_config(): Configuration loader for search engine settings
        - Loads search configuration from conf.yaml
        - Returns search engine specific settings
        - Supports domain filtering and language preferences
        
    get_web_search_tool(max_search_results): Search tool factory function
        - Creates configured search tool based on SELECTED_SEARCH_ENGINE
        - Applies result limits and provider-specific configurations
        - Returns LangChain-compatible search tool with logging

Supported Search Engines:
    1. Tavily Search (SearchEngine.TAVILY):
        - Advanced web search with content analysis
        - Support for include/exclude domain filtering
        - Image search and description capabilities
        - Raw content extraction for detailed analysis
        
    2. DuckDuckGo (SearchEngine.DUCKDUCKGO):
        - Privacy-focused search engine
        - No tracking or personalization
        - Good for general web search
        
    3. Brave Search (SearchEngine.BRAVE_SEARCH):
        - Independent search index
        - Privacy-focused alternative
        - Requires API key configuration
        
    4. ArXiv (SearchEngine.ARXIV):
        - Academic paper search
        - Scholarly publications and preprints
        - Metadata and full-text search
        
    5. Wikipedia (SearchEngine.WIKIPEDIA):
        - Encyclopedia search
        - Multilingual support
        - Structured knowledge base

Configuration Features:
    - Domain Filtering: Include/exclude specific domains (Tavily)
    - Language Support: Configurable language for Wikipedia
    - Content Limits: Character limits for content extraction
    - Result Limits: Configurable maximum results per query
    - API Keys: Secure API key management through environment variables

Logging Integration:
    - Enhanced Logging: All search tools wrapped with logging decorators
    - Operation Tracking: Input/output logging for monitoring
    - Performance Monitoring: Search timing and result metrics
    - Error Tracking: Search failures and API errors

Tool Creation:
    - Factory Pattern: Centralized tool creation based on configuration
    - LangChain Compatibility: All tools compatible with LangChain agents
    - Consistent Interface: Uniform interface across different providers
    - Error Handling: Graceful handling of unsupported engines

Search Capabilities:
    - Web Content: General web search across various sources
    - Academic Content: Scholarly articles and research papers
    - Reference Material: Encyclopedia and reference sources
    - Image Search: Visual content discovery (Tavily)
    - Domain-Specific: Filtered searches within specific domains

The module enables agents to access diverse information sources through
a unified interface, supporting comprehensive research across different
types of content and sources while maintaining consistent behavior.
"""

import logging
import os
from typing import List, Optional

from langchain_community.tools import (
    BraveSearch,
    DuckDuckGoSearchResults,
    WikipediaQueryRun,
)
from langchain_community.tools.arxiv import ArxivQueryRun
from langchain_community.utilities import (
    ArxivAPIWrapper,
    BraveSearchWrapper,
    WikipediaAPIWrapper,
)

from src.deep_research.config import SELECTED_SEARCH_ENGINE, SearchEngine, load_yaml_config
from src.deep_research.tools.decorators import create_logged_tool
from src.deep_research.tools.tavily_search.tavily_search_results_with_images import (
    TavilySearchWithImages,
)

logger = logging.getLogger(__name__)

# Create logged versions of the search tools
LoggedTavilySearch = create_logged_tool(TavilySearchWithImages)
LoggedDuckDuckGoSearch = create_logged_tool(DuckDuckGoSearchResults)
LoggedBraveSearch = create_logged_tool(BraveSearch)
LoggedArxivSearch = create_logged_tool(ArxivQueryRun)
LoggedWikipediaSearch = create_logged_tool(WikipediaQueryRun)


def get_search_config():
    config = load_yaml_config("conf.yaml")
    search_config = config.get("SEARCH_ENGINE", {})
    return search_config


# Get the selected search tool
def get_web_search_tool(max_search_results: int):
    search_config = get_search_config()

    if SELECTED_SEARCH_ENGINE == SearchEngine.TAVILY.value:
        # Only get and apply include/exclude domains for Tavily
        include_domains: Optional[List[str]] = search_config.get("include_domains", [])
        exclude_domains: Optional[List[str]] = search_config.get("exclude_domains", [])

        logger.info(
            f"Tavily search configuration loaded: include_domains={include_domains}, exclude_domains={exclude_domains}"
        )

        return LoggedTavilySearch(
            name="web_search",
            max_results=max_search_results,
            include_raw_content=True,
            include_images=True,
            include_image_descriptions=True,
            include_domains=include_domains,
            exclude_domains=exclude_domains,
        )
    elif SELECTED_SEARCH_ENGINE == SearchEngine.DUCKDUCKGO.value:
        return LoggedDuckDuckGoSearch(
            name="web_search",
            num_results=max_search_results,
        )
    elif SELECTED_SEARCH_ENGINE == SearchEngine.BRAVE_SEARCH.value:
        return LoggedBraveSearch(
            name="web_search",
            search_wrapper=BraveSearchWrapper(
                api_key=os.getenv("BRAVE_SEARCH_API_KEY", ""),
                search_kwargs={"count": max_search_results},
            ),
        )
    elif SELECTED_SEARCH_ENGINE == SearchEngine.ARXIV.value:
        return LoggedArxivSearch(
            name="web_search",
            api_wrapper=ArxivAPIWrapper(
                top_k_results=max_search_results,
                load_max_docs=max_search_results,
                load_all_available_meta=True,
            ),
        )
    elif SELECTED_SEARCH_ENGINE == SearchEngine.WIKIPEDIA.value:
        wiki_lang = search_config.get("wikipedia_lang", "en")
        wiki_doc_content_chars_max = search_config.get(
            "wikipedia_doc_content_chars_max", 4000
        )
        return LoggedWikipediaSearch(
            name="web_search",
            api_wrapper=WikipediaAPIWrapper(
                lang=wiki_lang,
                top_k_results=max_search_results,
                load_all_available_meta=True,
                doc_content_chars_max=wiki_doc_content_chars_max,
            ),
        )
    else:
        raise ValueError(f"Unsupported search engine: {SELECTED_SEARCH_ENGINE}")
