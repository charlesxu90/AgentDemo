"""
RAG (Retrieval-Augmented Generation) Request and Response Models

This module defines Pydantic models for RAG system API requests and responses.
The RAG system enhances AI responses by incorporating relevant information from
external knowledge sources and databases.

Classes:
    RAGConfigResponse: Response model containing RAG provider configuration
    RAGResourceRequest: Request model for searching RAG resources  
    RAGResourcesResponse: Response model containing list of RAG resources

The RAG system supports multiple providers and enables semantic search across
various knowledge sources including documents, web pages, and databases.
"""

from pydantic import BaseModel, Field

from src.deep_research.rag.retriever import Resource


class RAGConfigResponse(BaseModel):
    """Response model for RAG config."""

    provider: str | None = Field(
        None, description="The provider of the RAG, default is ragflow"
    )


class RAGResourceRequest(BaseModel):
    """Request model for RAG resource."""

    query: str | None = Field(
        None, description="The query of the resource need to be searched"
    )


class RAGResourcesResponse(BaseModel):
    """Response model for RAG resources."""

    resources: list[Resource] = Field(..., description="The resources of the RAG")
