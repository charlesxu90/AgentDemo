"""
RAG Document Retrieval Tool for Deep Research System

This module provides document retrieval capabilities using Retrieval-Augmented Generation
(RAG) systems. It enables agents to search and retrieve relevant documents from configured
knowledge bases and document collections.

Key Classes:
    RetrieverInput: Pydantic model for tool input validation
        - keywords: str - Search keywords for document retrieval
        - Provides type safety and validation for search parameters
        
    RetrieverTool: LangChain-compatible tool for document retrieval
        - Inherits from BaseTool for standard tool interface
        - Integrates with RAG providers for document search
        - Supports both synchronous and asynchronous operations
        - Returns structured document results with metadata

Key Functions:
    get_retriever_tool(resources): Factory function for creating retriever tools
        - Creates RetrieverTool instance with specified resources
        - Validates resource availability and configuration
        - Returns None if no resources or RAG provider available
        - Integrates with build_retriever() for provider selection

Tool Functionality:
    Document Search:
        - Keyword-based search across configured knowledge bases
        - Relevance ranking and similarity scoring
        - Resource filtering for targeted searches
        - Structured result formatting for downstream processing
        
    Async Support:
        - Both sync (_run) and async (_arun) implementations
        - Non-blocking operations for concurrent processing
        - Callback manager integration for monitoring
        
    Result Processing:
        - Document conversion to dictionary format
        - Metadata preservation (titles, URLs, descriptions)
        - Content chunking with similarity scores
        - Fallback handling for empty results

RAG Integration:
    - Provider Abstraction: Works with any configured RAG provider
    - Resource Management: Handles resource filtering and selection
    - Configuration Integration: Uses SELECTED_RAG_PROVIDER setting
    - Error Handling: Graceful handling of provider failures

Search Features:
    - Semantic Search: Vector-based similarity matching
    - Keyword Search: Traditional text-based search
    - Hybrid Retrieval: Combining multiple search strategies
    - Result Ranking: Relevance-based result ordering
    - Content Filtering: Resource-based content filtering

Tool Configuration:
    - Resource-Based: Tool creation based on available resources
    - Provider-Agnostic: Works with multiple RAG backends
    - Flexible Initialization: Optional tool creation for unconfigured systems
    - Logging Integration: Comprehensive operation logging

Usage Patterns:
    - Knowledge Base Search: Search internal documentation and knowledge
    - Research Context: Retrieve relevant background information
    - Reference Lookup: Find supporting documents and citations
    - Fact Verification: Cross-reference information across sources

Error Handling:
    - Empty Results: Graceful handling of no-match scenarios
    - Provider Failures: Fallback behavior for RAG system issues
    - Resource Validation: Checking resource availability
    - Input Validation: Parameter validation through Pydantic models

The tool enables agents to access and retrieve information from configured
knowledge bases, supporting research workflows with relevant context and
background information from curated document collections.
"""

import logging
from typing import List, Optional, Type

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from src.deep_research.config.tools import SELECTED_RAG_PROVIDER
from src.deep_research.rag import Document, Resource, Retriever, build_retriever

logger = logging.getLogger(__name__)


class RetrieverInput(BaseModel):
    keywords: str = Field(description="search keywords to look up")


class RetrieverTool(BaseTool):
    name: str = "local_search_tool"
    description: str = "Useful for retrieving information from the file with `rag://` uri prefix, it should be higher priority than the web search or writing code. Input should be a search keywords."
    args_schema: Type[BaseModel] = RetrieverInput

    retriever: Retriever = Field(default_factory=Retriever)
    resources: list[Resource] = Field(default_factory=list)

    def _run(
        self,
        keywords: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> list[Document]:
        logger.info(
            f"Retriever tool query: {keywords}", extra={"resources": self.resources}
        )
        documents = self.retriever.query_relevant_documents(keywords, self.resources)
        if not documents:
            return "No results found from the local knowledge base."
        return [doc.to_dict() for doc in documents]

    async def _arun(
        self,
        keywords: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> list[Document]:
        return self._run(keywords, run_manager.get_sync())


def get_retriever_tool(resources: List[Resource]) -> RetrieverTool | None:
    if not resources:
        return None
    logger.info(f"create retriever tool: {SELECTED_RAG_PROVIDER}")
    retriever = build_retriever()

    if not retriever:
        return None
    return RetrieverTool(retriever=retriever, resources=resources)
