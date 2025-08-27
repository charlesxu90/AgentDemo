"""
Core RAG Abstractions and Data Models

This module defines the foundational abstractions for Retrieval-Augmented Generation
within the Deep Research system. It provides data models for documents, chunks, and
resources, along with the abstract interface that all RAG providers must implement.

Key Classes:
    Chunk: Individual content segment with relevance scoring
        - content: str - The actual text content of the chunk
        - similarity: float - Relevance score (0.0 to 1.0) for ranking
        - Used for fine-grained content retrieval and ranking
        
    Document: Complete document structure with metadata and content chunks
        - id: str - Unique document identifier within the provider
        - url: Optional[str] - Source URL if document is web-based
        - title: Optional[str] - Human-readable document title
        - chunks: List[Chunk] - Ordered list of content segments
        - to_dict(): Serialization method for workflow integration
        
    Resource: External knowledge base or dataset representation
        - uri: str - Unique resource identifier (custom URI schemes supported)
        - title: str - Human-readable resource name
        - description: Optional[str] - Resource description and metadata
        - Pydantic model with validation for API integration
        
    Retriever: Abstract base class defining RAG provider interface
        - list_resources(): Abstract method for resource discovery
        - query_relevant_documents(): Abstract method for document search

Data Flow:
    1. Resource Discovery: list_resources() finds available knowledge bases
    2. Query Processing: query_relevant_documents() searches within selected resources
    3. Document Assembly: Results returned as Document objects with ranked Chunks
    4. Integration: Documents converted to dict format for workflow consumption

Chunk Similarity Scoring:
    - Float values between 0.0 (irrelevant) and 1.0 (highly relevant)
    - Used for ranking and filtering search results
    - Provider-specific scoring algorithms (cosine similarity, BM25, etc.)

Document Structure:
    - Hierarchical organization: Document → Chunks → Content
    - Preserves source metadata (URL, title) for attribution
    - Supports chunked retrieval for large documents
    - Flexible chunk size and overlap based on provider capabilities

Resource URI Schemes:
    - Custom URI schemes for different provider types
    - Examples: "rag://dataset/123", "vikingdb://kb/456"
    - Enables provider-agnostic resource references
    - Supports nested resource hierarchies

Provider Interface:
    - Abstract methods ensure consistent behavior across providers
    - Standardized input/output formats for interoperability
    - Error handling delegated to concrete implementations
    - Extensible design for adding new RAG providers

The module provides a clean abstraction layer that allows the research workflow
to work with any RAG provider through a consistent interface.
"""

# 

import abc

from pydantic import BaseModel, Field


class Chunk:
    content: str
    similarity: float

    def __init__(self, content: str, similarity: float):
        self.content = content
        self.similarity = similarity


class Document:
    """
    Document is a class that represents a document.
    """

    id: str
    url: str | None = None
    title: str | None = None
    chunks: list[Chunk] = []

    def __init__(
        self,
        id: str,
        url: str | None = None,
        title: str | None = None,
        chunks: list[Chunk] = [],
    ):
        self.id = id
        self.url = url
        self.title = title
        self.chunks = chunks

    def to_dict(self) -> dict:
        d = {
            "id": self.id,
            "content": "\n\n".join([chunk.content for chunk in self.chunks]),
        }
        if self.url:
            d["url"] = self.url
        if self.title:
            d["title"] = self.title
        return d


class Resource(BaseModel):
    """
    Resource is a class that represents a resource.
    """

    uri: str = Field(..., description="The URI of the resource")
    title: str = Field(..., description="The title of the resource")
    description: str | None = Field("", description="The description of the resource")


class Retriever(abc.ABC):
    """
    Define a RAG provider, which can be used to query documents and resources.
    """

    @abc.abstractmethod
    def list_resources(self, query: str | None = None) -> list[Resource]:
        """
        List resources from the rag provider.
        """
        pass

    @abc.abstractmethod
    def query_relevant_documents(
        self, query: str, resources: list[Resource] = []
    ) -> list[Document]:
        """
        Query relevant documents from the resources.
        """
        pass
