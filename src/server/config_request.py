"""
System Configuration Response Models

This module defines Pydantic models for system configuration API responses.
It provides comprehensive information about the server's current configuration,
including model settings, RAG configuration, and available features.

Classes:
    ConfigResponse: Main configuration response containing models and RAG settings

Used by the /api/config endpoint to return complete system status and configuration
information for client applications and monitoring systems.
"""

from pydantic import BaseModel, Field

from src.server.rag_request import RAGConfigResponse


class ConfigResponse(BaseModel):
    """Response model for server config."""

    rag: RAGConfigResponse = Field(..., description="The config of the RAG")
    models: dict[str, list[str]] = Field(..., description="The configured models")
