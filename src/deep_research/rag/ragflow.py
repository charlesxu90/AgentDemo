"""
RAGFlow Service Integration for Document Retrieval

This module provides integration with RAGFlow, a document processing and retrieval service,
implementing the Retriever interface for seamless RAG capabilities within the Deep Research
workflow. It handles authentication, API communication, and data transformation.

Key Classes:
    RAGFlowProvider: Concrete implementation of Retriever interface for RAGFlow
        - Inherits from Retriever abstract base class
        - Manages RAGFlow API authentication and communication
        - Handles document retrieval and resource listing operations
        
Key Functions:
    query_relevant_documents(query, resources): Main document search functionality
        - Accepts natural language query and optional resource filters
        - Constructs API payload with dataset/document filtering
        - Processes API response to extract documents and chunks
        - Returns ranked Document objects with similarity-scored chunks
        
    list_resources(query): Resource discovery and listing
        - Optional query parameter for filtering available datasets
        - Returns list of Resource objects representing available knowledge bases
        - Supports resource filtering by name or metadata
        
    parse_uri(uri): URI parsing utility for RAGFlow resource identifiers
        - Parses custom "rag://" scheme URIs
        - Extracts dataset and document identifiers
        - Validates URI format and structure

RAGFlow API Integration:
    - REST API communication with Bearer token authentication
    - Environment-based configuration (RAGFLOW_API_URL, RAGFLOW_API_KEY)
    - Configurable page size for result pagination
    - Optional cross-language search capabilities

Authentication:
    - Bearer token authentication using API key
    - API key sourced from RAGFLOW_API_KEY environment variable
    - Secure HTTP headers for all API communications

Configuration Parameters:
    - api_url: RAGFlow service endpoint URL
    - api_key: Authentication token for API access
    - page_size: Maximum results per query (default: 10)
    - cross_languages: Optional language list for cross-lingual search

Search Features:
    - Natural language query processing
    - Dataset and document-level filtering
    - Similarity-based result ranking
    - Cross-language search support (if configured)
    - Pagination support for large result sets

Data Transformation:
    - API response parsing and validation
    - Document aggregation by document ID
    - Chunk extraction with similarity scores
    - Resource metadata extraction and formatting

Error Handling:
    - Comprehensive HTTP error handling with descriptive messages
    - Configuration validation during initialization
    - Graceful handling of malformed API responses
    - Detailed error reporting for debugging

The provider enables seamless integration with RAGFlow services while maintaining
compatibility with the standard Retriever interface used throughout the Deep
Research system.
"""

# 

import os
from typing import List, Optional
from urllib.parse import urlparse

import requests

from src.deep_research.rag.retriever import Chunk, Document, Resource, Retriever


class RAGFlowProvider(Retriever):
    """
    RAGFlowProvider is a provider that uses RAGFlow to retrieve documents.
    """

    api_url: str
    api_key: str
    page_size: int = 10
    cross_languages: Optional[List[str]] = None

    def __init__(self):
        api_url = os.getenv("RAGFLOW_API_URL")
        if not api_url:
            raise ValueError("RAGFLOW_API_URL is not set")
        self.api_url = api_url

        api_key = os.getenv("RAGFLOW_API_KEY")
        if not api_key:
            raise ValueError("RAGFLOW_API_KEY is not set")
        self.api_key = api_key

        page_size = os.getenv("RAGFLOW_PAGE_SIZE")
        if page_size:
            self.page_size = int(page_size)

        self.cross_languages = None
        cross_languages = os.getenv("RAGFLOW_CROSS_LANGUAGES")
        if cross_languages:
            self.cross_languages = cross_languages.split(",")

    def query_relevant_documents(
        self, query: str, resources: list[Resource] = []
    ) -> list[Document]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        dataset_ids: list[str] = []
        document_ids: list[str] = []

        for resource in resources:
            dataset_id, document_id = parse_uri(resource.uri)
            dataset_ids.append(dataset_id)
            if document_id:
                document_ids.append(document_id)

        payload = {
            "question": query,
            "dataset_ids": dataset_ids,
            "document_ids": document_ids,
            "page_size": self.page_size,
        }

        if self.cross_languages:
            payload["cross_languages"] = self.cross_languages

        response = requests.post(
            f"{self.api_url}/api/v1/retrieval", headers=headers, json=payload
        )

        if response.status_code != 200:
            raise Exception(f"Failed to query documents: {response.text}")

        result = response.json()
        data = result.get("data", {})
        doc_aggs = data.get("doc_aggs", [])
        docs: dict[str, Document] = {
            doc.get("doc_id"): Document(
                id=doc.get("doc_id"),
                title=doc.get("doc_name"),
                chunks=[],
            )
            for doc in doc_aggs
        }

        for chunk in data.get("chunks", []):
            doc = docs.get(chunk.get("document_id"))
            if doc:
                doc.chunks.append(
                    Chunk(
                        content=chunk.get("content"),
                        similarity=chunk.get("similarity"),
                    )
                )

        return list(docs.values())

    def list_resources(self, query: str | None = None) -> list[Resource]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        params = {}
        if query:
            params["name"] = query

        response = requests.get(
            f"{self.api_url}/api/v1/datasets", headers=headers, params=params
        )

        if response.status_code != 200:
            raise Exception(f"Failed to list resources: {response.text}")

        result = response.json()
        resources = []

        for item in result.get("data", []):
            item = Resource(
                uri=f"rag://dataset/{item.get('id')}",
                title=item.get("name", ""),
                description=item.get("description", ""),
            )
            resources.append(item)

        return resources


def parse_uri(uri: str) -> tuple[str, str]:
    parsed = urlparse(uri)
    if parsed.scheme != "rag":
        raise ValueError(f"Invalid URI: {uri}")
    return parsed.path.split("/")[1], parsed.fragment
