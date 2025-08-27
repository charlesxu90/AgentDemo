"""
Retrieval-Augmented Generation (RAG) Package for Deep Research System

This package provides comprehensive RAG capabilities for document retrieval and knowledge
base integration within the Deep Research workflow. It supports multiple RAG providers
and offers a unified interface for document search and resource management.

Modules:
    retriever.py: Core RAG abstractions and data models
        - Retriever: Abstract base class defining RAG provider interface
        - Document: Document structure with chunks and metadata
        - Resource: External resource representation with URI and metadata
        - Chunk: Individual content chunk with similarity scores
        
    builder.py: RAG provider factory and configuration
        - build_retriever(): Factory function for creating configured RAG providers
        - Environment-based provider selection and initialization
        
    ragflow.py: RAGFlow service integration
        - RAGFlowProvider: Implementation for RAGFlow API integration
        - Document retrieval with cross-language support
        - Dataset and document management capabilities
        
    vikingdb_knowledge_base.py: VikingDB Knowledge Base integration
        - VikingDBKnowledgeBaseProvider: Implementation for VikingDB API
        - AWS-style signature authentication for secure API access
        - Knowledge base search and document retrieval

Key Classes:
    Retriever: Abstract interface for all RAG providers
        - list_resources(): Discover available knowledge bases and datasets
        - query_relevant_documents(): Search for relevant documents based on queries
        
    Document: Structured document representation
        - id, url, title: Document metadata
        - chunks: List of content chunks with similarity scores
        - to_dict(): Serialization for workflow integration
        
    Resource: External knowledge resource representation
        - uri: Unique resource identifier (with custom schemes)
        - title, description: Human-readable metadata
        - Used for resource selection and filtering

Supported Providers:
    1. RAGFlow: Document processing and retrieval service
        - REST API integration with bearer token authentication
        - Cross-language search capabilities
        - Dataset and document management
        
    2. VikingDB Knowledge Base: ByteDance's knowledge base service
        - AWS-style signature v4 authentication
        - High-performance vector search
        - Enterprise-grade security and scalability

Provider Selection:
    - Environment variable RAG_PROVIDER controls active provider
    - Automatic provider instantiation based on configuration
    - Graceful fallback when no provider is configured

Integration Features:
    - Unified interface across different RAG backends
    - Seamless integration with research workflow tools
    - Support for resource filtering and query optimization
    - Comprehensive error handling and logging

The package enables flexible document retrieval from various knowledge sources,
supporting the Deep Research system's need for comprehensive information gathering
and context-aware research assistance.
"""

from .builder import build_retriever
from .ragflow import RAGFlowProvider
from .retriever import Chunk, Document, Resource, Retriever
from .vikingdb_knowledge_base import VikingDBKnowledgeBaseProvider

__all__ = [
    "Retriever",
    "Document",
    "Resource",
    "RAGFlowProvider",
    "VikingDBKnowledgeBaseProvider",
    "Chunk",
    "build_retriever",
]
