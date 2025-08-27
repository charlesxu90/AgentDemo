"""
Tool Configuration and Provider Selection

This module defines available tool providers and manages their selection through
environment variables. It provides enums for different categories of external tools
used throughout the Deep Research workflow.

Key Classes:
    SearchEngine: Enum defining available web search providers
        - TAVILY: Primary web search API (default)
        - DUCKDUCKGO: Alternative search engine
        - BRAVE_SEARCH: Privacy-focused search
        - ARXIV: Academic paper search
        - WIKIPEDIA: Encyclopedia search
        
    RAGProvider: Enum defining Retrieval-Augmented Generation providers
        - RAGFLOW: Document processing and retrieval system
        - VIKINGDB_KNOWLEDGE_BASE: Vector database knowledge base

Configuration Variables:
    SELECTED_SEARCH_ENGINE: Current search engine (from SEARCH_API env var)
    SELECTED_RAG_PROVIDER: Current RAG provider (from RAG_PROVIDER env var)

Environment Variables:
    - SEARCH_API: Selects the search engine provider (default: "tavily")
    - RAG_PROVIDER: Selects the RAG system provider (optional)

The module enables flexible switching between different tool providers without
code changes, supporting different deployment scenarios and provider preferences.
Research workflows can adapt to available services through environment configuration.
"""

# 

import enum
import os

from dotenv import load_dotenv

load_dotenv()

# Tavily search
class SearchEngine(enum.Enum):
    TAVILY = "tavily"
    DUCKDUCKGO = "duckduckgo"
    BRAVE_SEARCH = "brave_search"
    ARXIV = "arxiv"
    WIKIPEDIA = "wikipedia"


# Tool configuration
SELECTED_SEARCH_ENGINE = os.getenv("SEARCH_API", SearchEngine.TAVILY.value)


# RAG
class RAGProvider(enum.Enum):
    RAGFLOW = "ragflow"
    VIKINGDB_KNOWLEDGE_BASE = "vikingdb_knowledge_base"


SELECTED_RAG_PROVIDER = os.getenv("RAG_PROVIDER")
