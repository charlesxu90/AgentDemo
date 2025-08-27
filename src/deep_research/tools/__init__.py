"""
Research Tools Package for Deep Research System

This package provides a comprehensive suite of tools for automated research and data analysis
within the Deep Research workflow. Each tool is designed to handle specific aspects of the
research process, from web crawling to code execution to document retrieval.

Available Tools:
    crawl_tool: Web content extraction and processing
        - Crawls URLs and extracts readable content in markdown format
        - Handles various content types including articles, PDFs, and structured data
        - Returns formatted content suitable for further analysis
        
    python_repl_tool: Code execution and data analysis
        - Executes Python code in a secure sandboxed environment
        - Supports mathematical calculations, data processing, and visualization
        - Configurable through environment variables for security
        
    get_web_search_tool(): Web search engine integration
        - Factory function for creating configured search tools
        - Supports multiple search engines (Tavily, DuckDuckGo, Brave, ArXiv, Wikipedia)
        - Configurable result limits and filtering options
        
    get_retriever_tool(): Document retrieval from knowledge bases
        - Creates RAG-based document retrieval tools
        - Integrates with multiple RAG providers (RAGFlow, VikingDB)
        - Supports resource filtering and relevance ranking

Tool Categories:
    1. Content Extraction: Web crawling and content processing
    2. Search & Discovery: Multi-engine web search capabilities  
    3. Code Execution: Safe Python code execution for analysis
    4. Knowledge Retrieval: RAG-based document and knowledge access
    5. Utility Functions: Logging, decorators, and tool enhancement

Integration Features:
    - LangChain tool compatibility for seamless agent integration
    - Comprehensive logging and monitoring through decorators
    - Environment-based configuration for flexible deployment
    - Error handling and graceful degradation
    - Async support for non-blocking operations

Security & Safety:
    - Sandboxed code execution with configurable restrictions
    - Input validation and sanitization
    - Rate limiting and resource management
    - Secure credential handling through environment variables

The tools are designed to work together as part of the broader Deep Research
ecosystem, providing agents with the capabilities needed for comprehensive
automated research and analysis.
"""

from .crawl import crawl_tool
from .python_repl import python_repl_tool
from .retriever import get_retriever_tool
from .search import get_web_search_tool
# from .tts import VolcengineTTS  # Commented out as tts.py doesn't exist

__all__ = [
    "crawl_tool",
    "python_repl_tool",
    "get_web_search_tool",
    "get_retriever_tool",
]
