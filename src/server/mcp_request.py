"""
Model Context Protocol (MCP) Request and Response Models

This module defines Pydantic models for MCP server integration API requests and responses.
The Model Context Protocol enables AI applications to connect to external data sources
and tools in a standardized way, supporting multiple transport methods and server types.

Classes:
    MCPServerMetadataRequest: Request model for connecting to MCP servers
    MCPTool: Individual tool definition from MCP server
    MCPServerMetadataResponse: Response model containing server metadata and tools

Supports multiple transport protocols:
- stdio: Standard input/output based servers
- sse: Server-Sent Events based servers  
- streamable_http: HTTP streaming based servers

Used for dynamic tool discovery and integration with external MCP-compatible services.
"""

from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class MCPServerMetadataRequest(BaseModel):
    """Request model for MCP server metadata."""

    transport: str = Field(
        ...,
        description=(
            "The type of MCP server connection (stdio or sse or streamable_http)"
        ),
    )
    command: Optional[str] = Field(
        None, description="The command to execute (for stdio type)"
    )
    args: Optional[List[str]] = Field(
        None, description="Command arguments (for stdio type)"
    )
    url: Optional[str] = Field(
        None, description="The URL of the SSE server (for sse type)"
    )
    env: Optional[Dict[str, str]] = Field(
        None, description="Environment variables (for stdio type)"
    )
    headers: Optional[Dict[str, str]] = Field(
        None, description="HTTP headers (for sse/streamable_http type)"
    )
    timeout_seconds: Optional[int] = Field(
        None, description="Optional custom timeout in seconds for the operation"
    )


class MCPServerMetadataResponse(BaseModel):
    """Response model for MCP server metadata."""

    transport: str = Field(
        ...,
        description=(
            "The type of MCP server connection (stdio or sse or streamable_http)"
        ),
    )
    command: Optional[str] = Field(
        None, description="The command to execute (for stdio type)"
    )
    args: Optional[List[str]] = Field(
        None, description="Command arguments (for stdio type)"
    )
    url: Optional[str] = Field(
        None, description="The URL of the SSE server (for sse type)"
    )
    env: Optional[Dict[str, str]] = Field(
        None, description="Environment variables (for stdio type)"
    )
    headers: Optional[Dict[str, str]] = Field(
        None, description="HTTP headers (for sse/streamable_http type)"
    )
    tools: List = Field(
        default_factory=list, description="Available tools from the MCP server"
    )
