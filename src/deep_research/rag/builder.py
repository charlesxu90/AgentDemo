"""
RAG Provider Factory and Configuration Builder

This module provides a factory function for creating and configuring RAG (Retrieval-Augmented
Generation) providers based on environment configuration. It serves as the central point
for RAG provider instantiation and management within the Deep Research system.

Key Functions:
    build_retriever(): Factory function for RAG provider creation
        - Reads SELECTED_RAG_PROVIDER from environment configuration
        - Instantiates appropriate provider based on configuration
        - Returns configured Retriever instance or None if not configured
        - Handles provider validation and error reporting

Supported Providers:
    1. RAGFlow (RAGProvider.RAGFLOW):
        - Document processing and retrieval service
        - Instantiates RAGFlowProvider with API configuration
        - Supports cross-language search and dataset management
        
    2. VikingDB Knowledge Base (RAGProvider.VIKINGDB_KNOWLEDGE_BASE):
        - ByteDance's enterprise knowledge base service
        - Instantiates VikingDBKnowledgeBaseProvider with authentication
        - High-performance vector search with security features

Provider Configuration:
    - Environment variable RAG_PROVIDER controls active provider
    - Each provider reads its own specific configuration variables
    - Automatic validation of required configuration parameters
    - Graceful handling of missing or invalid configurations

Factory Pattern Benefits:
    - Centralized provider instantiation and configuration
    - Loose coupling between workflow and specific providers
    - Easy addition of new RAG providers
    - Consistent error handling across provider types

Error Handling:
    - Returns None for unconfigured RAG (allowing workflows to continue)
    - Raises ValueError for unknown provider types
    - Provider-specific configuration errors bubble up from constructors
    - Clear error messages for debugging configuration issues

Integration:
    - Used by RAG tools to get configured retriever instances
    - Integrates with configuration system for environment management
    - Supports dynamic provider switching through configuration changes
    - Compatible with testing and development scenarios

The factory pattern ensures that RAG provider complexity is abstracted away
from the core research workflow, while maintaining flexibility for different
deployment scenarios and provider preferences.
"""

# 

from src.deep_research.config.tools import SELECTED_RAG_PROVIDER, RAGProvider
from src.deep_research.rag.ragflow import RAGFlowProvider
from src.deep_research.rag.retriever import Retriever
from src.deep_research.rag.vikingdb_knowledge_base import VikingDBKnowledgeBaseProvider


def build_retriever() -> Retriever | None:
    if SELECTED_RAG_PROVIDER == RAGProvider.RAGFLOW.value:
        return RAGFlowProvider()
    elif SELECTED_RAG_PROVIDER == RAGProvider.VIKINGDB_KNOWLEDGE_BASE.value:
        return VikingDBKnowledgeBaseProvider()
    elif SELECTED_RAG_PROVIDER:
        raise ValueError(f"Unsupported RAG provider: {SELECTED_RAG_PROVIDER}")
    return None
