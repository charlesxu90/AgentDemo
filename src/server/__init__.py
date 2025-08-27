"""
FastAPI Server Package for Deep Research System

This package provides the complete FastAPI server implementation for the Deep Research
AI-powered research and analysis platform. It exposes RESTful APIs and streaming
endpoints for AI conversations, research workflows, and system management.

Package Exports:
    app: FastAPI application instance ready for deployment
        - Pre-configured with all routes, middleware, and documentation
        - Includes CORS settings for cross-origin requests
        - Enhanced OpenAPI documentation with custom schemas
        - Comprehensive error handling and logging

Server Architecture:
    - FastAPI Framework: Modern, fast Python web framework
    - Async Support: Full asynchronous request handling
    - Server-Sent Events: Real-time streaming for chat responses
    - RESTful Design: Standard HTTP methods and status codes
    - OpenAPI Integration: Automatic API documentation generation

Core API Categories:
    Chat & Research:
        - Streaming AI conversations with research capabilities
        - Multi-step research workflow execution
        - Real-time response streaming via SSE
        
    Prompt Engineering:
        - AI-powered prompt enhancement and optimization
        - Context-aware prompt improvements
        - Style adaptation for different use cases
        
    MCP Integration:
        - Model Context Protocol server discovery
        - External tool and data source integration
        - Dynamic tool loading and metadata retrieval
        
    RAG System:
        - Retrieval-Augmented Generation configuration
        - Knowledge base resource discovery
        - Document search and retrieval capabilities
        
    System Configuration:
        - Model configuration and status reporting
        - Health checks and monitoring endpoints
        - Feature flag and capability discovery

Middleware and Security:
    - CORS middleware for cross-origin support
    - Request validation and sanitization
    - Error handling with appropriate HTTP status codes
    - Optional authentication support (configurable)

Deployment Features:
    - Environment-based configuration
    - Database checkpoint support (PostgreSQL/MongoDB)
    - Scalable async architecture
    - Production-ready logging and monitoring

Usage:
    from src.server import app
    
    # Run with uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
    # Or import for ASGI deployment
    application = app

The server provides a complete API surface for AI-powered research workflows,
supporting both simple chat interactions and complex multi-step research processes
with external tool integration and knowledge base access.
"""

from .app import app

__all__ = ["app"]
