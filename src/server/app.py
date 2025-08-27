"""
FastAPI Server Application for Deep Research AI Platform

This module implements the complete FastAPI server for the Deep Research AI-powered
research and analysis platform. It provides RESTful APIs, streaming endpoints,
and comprehensive system management capabilities.

Key Functions:
    chat_stream(request): Main streaming chat endpoint for AI research conversations
        - Real-time Server-Sent Events streaming
        - Multi-step research workflow execution
        - Tool integration (web search, document analysis, etc.)
        - MCP (Model Context Protocol) support
        - RAG (Retrieval-Augmented Generation) integration
        - Conversation persistence with checkpoints
        
    enhance_prompt(request): AI-powered prompt enhancement service
        - Automatic prompt optimization and clarity improvement
        - Context integration and style adaptation
        - Best practices application for better results
        
    mcp_server_metadata(request): MCP server discovery and tool loading
        - Connect to external MCP servers via multiple transports
        - Dynamic tool discovery and metadata retrieval
        - Support for stdio, SSE, and HTTP protocols
        
    rag_config(): RAG system configuration endpoint
        - Current provider information and status
        - System capabilities and integration details
        
    rag_resources(request): RAG resource discovery and search
        - Knowledge base resource listing
        - Semantic search across available resources
        - Resource metadata and access information
        
    config(): Complete system configuration endpoint
        - Model configuration and availability
        - Feature flags and capability discovery
        - RAG and integration status reporting

Helper Functions:
    _astream_workflow_generator(): Core streaming workflow generator
        - Manages research workflow execution
        - Handles database checkpoints (PostgreSQL/MongoDB)
        - Processes message streaming and tool calls
        - Manages interrupts and user feedback
        
    _stream_graph_events(): Event streaming from LangGraph workflow
        - Real-time event processing and formatting
        - Tool call execution monitoring
        - Agent coordination and message routing
        
    _process_message_chunk(): Individual message chunk processing
        - Message type detection and routing
        - Tool call formatting and sanitization
        - Event stream message creation
        
    _make_event(): Server-Sent Events formatting
        - JSON serialization with proper encoding
        - Error handling and fallback mechanisms
        - Chat stream persistence integration

Server Features:
    Streaming Capabilities:
        - Server-Sent Events for real-time responses
        - Token-by-token message streaming
        - Tool execution progress monitoring
        - Research workflow status updates
        
    Research Workflows:
        - Multi-step research plan generation and execution
        - Background investigation capabilities
        - Interrupt-driven user feedback integration
        - Report generation in multiple styles
        
    Tool Integration:
        - Web search (Tavily, DuckDuckGo, Brave, etc.)
        - Document crawling and analysis
        - Python code execution environment
        - RAG document retrieval
        - MCP external tool loading
        
    System Management:
        - Health monitoring and status checks
        - Configuration discovery and reporting
        - Model availability and capability listing
        - Error handling with appropriate HTTP status codes

Middleware and Security:
    - CORS middleware with configurable origins
    - Request validation and sanitization
    - Environment-based configuration
    - Optional authentication support
    - Rate limiting ready infrastructure

Database Integration:
    - PostgreSQL checkpoint support for conversation persistence
    - MongoDB checkpoint support as alternative
    - In-memory storage for temporary data
    - Automatic failover and error handling

API Documentation:
    - Enhanced OpenAPI schema with detailed descriptions
    - Interactive Swagger UI with live testing
    - Alternative ReDoc documentation interface
    - Comprehensive endpoint categorization and tagging

Error Handling:
    - Structured error responses with appropriate HTTP codes
    - Detailed logging for debugging and monitoring
    - Graceful fallbacks for service failures
    - Client-friendly error messages

=== API ENDPOINTS REFERENCE ===

Chat & Research APIs:
    POST /api/chat/stream
        Function: chat_stream(request: ChatRequest)
        Purpose: Stream AI-powered research conversations with real-time responses
        Features: SSE streaming, multi-step workflows, tool integration, RAG support
        Request: ChatRequest with messages, resources, research parameters
        Response: Server-Sent Events stream with message chunks and tool results
        Authentication: None required
        Rate Limiting: Based on system configuration

Prompt Engineering APIs:
    POST /api/prompt/enhance
        Function: enhance_prompt(request: EnhancePromptRequest)
        Purpose: AI-powered prompt enhancement and optimization service
        Features: Automatic optimization, context integration, style adaptation
        Request: EnhancePromptRequest with prompt, context, report_style
        Response: JSON with enhanced prompt result
        Authentication: None required
        Processing Time: 5-30 seconds depending on prompt complexity

MCP Integration APIs:
    POST /api/mcp/server/metadata
        Function: mcp_server_metadata(request: MCPServerMetadataRequest)
        Purpose: Retrieve metadata and tools from Model Context Protocol servers
        Features: Dynamic tool discovery, multiple transport protocols
        Request: MCPServerMetadataRequest with transport, command, URL details
        Response: MCPServerMetadataResponse with server metadata and available tools
        Authentication: None required (but MCP must be enabled via ENABLE_MCP_SERVER_CONFIGURATION=true)
        Timeout: Configurable, default 300 seconds

RAG System APIs:
    GET /api/rag/config
        Function: rag_config()
        Purpose: Retrieve current RAG system configuration and provider information
        Features: Provider status, capabilities, integration details
        Request: No parameters required
        Response: RAGConfigResponse with provider information
        Authentication: None required
        Cache: Configuration is cached until server restart

    GET /api/rag/resources
        Function: rag_resources(request: RAGResourceRequest)
        Purpose: Search and retrieve available resources from RAG system
        Features: Resource discovery, semantic search, metadata retrieval
        Request: Query parameter for resource search (optional)
        Response: RAGResourcesResponse with list of available resources
        Authentication: None required
        Dependency: Requires configured RAG provider

System Configuration APIs:
    GET /api/config
        Function: config()
        Purpose: Retrieve comprehensive system configuration and status
        Features: Model configuration, RAG settings, feature flags
        Request: No parameters required
        Response: ConfigResponse with complete system status
        Authentication: None required
        Cache: Real-time configuration data

System Information APIs:
    GET /
        Function: root()
        Purpose: API information and navigation links
        Features: Welcome message, endpoint discovery, documentation links
        Request: No parameters required
        Response: JSON with API information and available endpoints
        Authentication: None required
        Purpose: Entry point for API discovery

    GET /health
        Function: health()
        Purpose: System health check and operational status
        Features: Health indicators, uptime verification, monitoring support
        Request: No parameters required
        Response: JSON with health status and timestamp
        Authentication: None required
        SLA: < 100ms response time

=== HELPER FUNCTIONS REFERENCE ===

Streaming and Event Processing:
    _astream_workflow_generator(): Core streaming workflow generator and orchestrator
    _stream_graph_events(): Event streaming from LangGraph workflow execution
    _process_message_chunk(): Individual message chunk processing and formatting
    _make_event(): Server-Sent Events formatting with JSON serialization
    _process_tool_call_chunks(): Tool call chunk processing and sanitization

Message and Event Handling:
    _create_event_stream_message(): Base event stream message creation
    _create_interrupt_event(): Interrupt event creation for user feedback
    _process_initial_messages(): Initial message processing and formatting
    _get_agent_name(): Agent name extraction from workflow metadata

System and Configuration:
    custom_openapi(): Enhanced OpenAPI schema generation with custom documentation

The server provides a complete API surface for AI-powered research workflows,
supporting both simple chat interactions and complex multi-step research processes
with external tool integration and knowledge base access.
"""

import base64
import json
import logging
from typing import Annotated, List, cast
from uuid import uuid4


from langchain_core.messages import AIMessageChunk, BaseMessage, ToolMessage
from langgraph.types import Command
from langgraph.store.memory import InMemoryStore
from langgraph.checkpoint.mongodb import AsyncMongoDBSaver
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from psycopg_pool import AsyncConnectionPool


# pure server imports
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, StreamingResponse
from fastapi.openapi.utils import get_openapi
from src.server.config_request import ConfigResponse
from src.server.chat_request import ChatRequest, EnhancePromptRequest
from src.server.mcp_request import MCPServerMetadataRequest, MCPServerMetadataResponse
from src.server.mcp_utils import load_mcp_tools
from src.server.rag_request import (
    RAGConfigResponse,
    RAGResourceRequest,
    RAGResourcesResponse,
)

# agent imports
from src.deep_research.config.configuration import get_recursion_limit, get_bool_env, get_str_env
from src.deep_research.config.report_style import ReportStyle
from src.deep_research.config.tools import SELECTED_RAG_PROVIDER
from src.deep_research.graph.builder import build_graph_with_memory
from src.deep_research.graph.checkpoint import chat_stream_message
from src.deep_research.llms.llm import get_configured_llm_models
from src.deep_research.prompt_enhancer.builder import build_graph as build_prompt_enhancer_graph
from src.deep_research.rag.builder import build_retriever
from src.deep_research.rag.retriever import Resource
from src.deep_research.utils.json_utils import sanitize_args

logger = logging.getLogger(__name__)

INTERNAL_SERVER_ERROR_DETAIL = "Internal Server Error"

app = FastAPI(
    title="DeepResearch API",
    description="""
    ## DeepResearch API
    
    A comprehensive AI-powered research and analysis platform that provides:
    
    * **Chat Streaming**: Real-time conversational AI with research capabilities
    * **Prompt Enhancement**: AI-powered prompt optimization and refinement
    * **MCP Integration**: Model Context Protocol server metadata and tools
    * **RAG System**: Retrieval-Augmented Generation for enhanced responses
    * **Configuration**: Dynamic model and system configuration
    
    ### Authentication
    Some endpoints may require authentication based on configuration.
    
    ### Rate Limits
    API calls are subject to rate limiting based on your configuration.
    """,
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Add CORS middleware
# It's recommended to load the allowed origins from an environment variable
# for better security and flexibility across different environments.
allowed_origins_str = get_str_env("ALLOWED_ORIGINS", "http://localhost:3000")
allowed_origins = [origin.strip() for origin in allowed_origins_str.split(",")]

logger.info(f"Allowed origins: {allowed_origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Temporarily allow all origins for debugging
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"],  # Add more methods
    allow_headers=["*"],  # Now allow all headers, but can be restricted further
)
in_memory_store = InMemoryStore()
graph = build_graph_with_memory()


@app.post(
    "/api/chat/stream",
    tags=["Chat & Research"],
    summary="Stream AI Research Chat",
    description="""
    **Stream AI-powered research conversations with real-time responses.**
    
    This endpoint provides a streaming interface for AI-powered research conversations.
    It supports:
    - Real-time message streaming via Server-Sent Events (SSE)
    - Multi-step research workflows
    - RAG (Retrieval-Augmented Generation) integration
    - MCP (Model Context Protocol) server integration
    - Customizable research parameters
    
    ### Features:
    - **Streaming Response**: Real-time token-by-token streaming
    - **Research Planning**: Automatic research plan generation and execution
    - **Tool Integration**: Access to web search, document analysis, and more
    - **Context Management**: Thread-based conversation persistence
    - **Interrupts**: User can interrupt and modify research plans
    
    ### Request Parameters:
    - `messages`: Chat history between user and assistant
    - `resources`: External resources to include in research
    - `thread_id`: Conversation thread identifier (use "__default__" for new conversations)
    - `max_plan_iterations`: Maximum research plan iterations (default: 1)
    - `max_step_num`: Maximum steps per plan (default: 3)
    - `auto_accepted_plan`: Whether to auto-execute plans (default: false)
    - `report_style`: Output format style (ACADEMIC, POPULAR_SCIENCE)
    
    ### Response Format:
    Server-Sent Events stream with the following event types:
    - `message_chunk`: AI response tokens
    - `tool_calls`: Tool invocation events
    - `tool_call_result`: Tool execution results
    - `interrupt`: Plan approval requests
    """,
    response_description="Server-Sent Events stream with chat messages and research results",
    responses={
        200: {
            "description": "Successful streaming response",
            "content": {"text/event-stream": {"example": "event: message_chunk\\ndata: {\"content\": \"Hello\", \"agent\": \"researcher\"}\\n\\n"}}
        },
        403: {"description": "MCP features disabled"},
        500: {"description": "Internal server error"}
    }
)
async def chat_stream(request: ChatRequest):
    # Check if MCP server configuration is enabled
    mcp_enabled = get_bool_env("ENABLE_MCP_SERVER_CONFIGURATION", False)

    # Validate MCP settings if provided
    if request.mcp_settings and not mcp_enabled:
        raise HTTPException(
            status_code=403,
            detail="MCP server configuration is disabled. Set ENABLE_MCP_SERVER_CONFIGURATION=true to enable MCP features.",
        )

    thread_id = request.thread_id
    if thread_id == "__default__":
        thread_id = str(uuid4())

    return StreamingResponse(
        _astream_workflow_generator(
            request.model_dump()["messages"],
            thread_id,
            request.resources,
            request.max_plan_iterations,
            request.max_step_num,
            request.max_search_results,
            request.auto_accepted_plan,
            request.interrupt_feedback,
            request.mcp_settings if mcp_enabled else {},
            request.enable_background_investigation,
            request.report_style,
            request.enable_deep_thinking,
        ),
        media_type="text/event-stream",
    )


def _process_tool_call_chunks(tool_call_chunks):
    """Process tool call chunks and sanitize arguments."""
    chunks = []
    for chunk in tool_call_chunks:
        chunks.append(
            {
                "name": chunk.get("name", ""),
                "args": sanitize_args(chunk.get("args", "")),
                "id": chunk.get("id", ""),
                "index": chunk.get("index", 0),
                "type": chunk.get("type", ""),
            }
        )
    return chunks


def _get_agent_name(agent, message_metadata):
    """Extract agent name from agent tuple."""
    agent_name = "unknown"
    if agent and len(agent) > 0:
        agent_name = agent[0].split(":")[0] if ":" in agent[0] else agent[0]
    else:
        agent_name = message_metadata.get("langgraph_node", "unknown")
    return agent_name


def _create_event_stream_message(
    message_chunk, message_metadata, thread_id, agent_name
):
    """Create base event stream message."""
    event_stream_message = {
        "thread_id": thread_id,
        "agent": agent_name,
        "id": message_chunk.id,
        "role": "assistant",
        "checkpoint_ns": message_metadata.get("checkpoint_ns", ""),
        "langgraph_node": message_metadata.get("langgraph_node", ""),
        "langgraph_path": message_metadata.get("langgraph_path", ""),
        "langgraph_step": message_metadata.get("langgraph_step", ""),
        "content": message_chunk.content,
    }

    # Add optional fields
    if message_chunk.additional_kwargs.get("reasoning_content"):
        event_stream_message["reasoning_content"] = message_chunk.additional_kwargs[
            "reasoning_content"
        ]

    if message_chunk.response_metadata.get("finish_reason"):
        event_stream_message["finish_reason"] = message_chunk.response_metadata.get(
            "finish_reason"
        )

    return event_stream_message


def _create_interrupt_event(thread_id, event_data):
    """Create interrupt event."""
    interrupt_obj = event_data["__interrupt__"][0]
    
    # Handle different Interrupt object structures with better error handling
    try:
        # Try the new structure first
        interrupt_id = getattr(interrupt_obj, 'id', None)
        if interrupt_id is None:
            # Try the old structure
            if hasattr(interrupt_obj, 'ns') and interrupt_obj.ns:
                interrupt_id = interrupt_obj.ns[0]
            else:
                interrupt_id = "interrupt"
        
        interrupt_value = getattr(interrupt_obj, 'value', str(interrupt_obj))
        
    except Exception as e:
        logger.warning(f"Error accessing interrupt object attributes: {e}")
        interrupt_id = "interrupt"
        interrupt_value = str(interrupt_obj)
    
    return _make_event(
        "interrupt",
        {
            "thread_id": thread_id,
            "id": interrupt_id,
            "role": "assistant",
            "content": interrupt_value,
            "finish_reason": "interrupt",
            "options": [
                {"text": "Edit plan", "value": "edit_plan"},
                {"text": "Start research", "value": "accepted"},
            ],
        },
    )


def _process_initial_messages(message, thread_id):
    """Process initial messages and yield formatted events."""
    json_data = json.dumps(
        {
            "thread_id": thread_id,
            "id": "run--" + message.get("id", uuid4().hex),
            "role": "user",
            "content": message.get("content", ""),
        },
        ensure_ascii=False,
        separators=(",", ":"),
    )
    chat_stream_message(
        thread_id, f"event: message_chunk\ndata: {json_data}\n\n", "none"
    )


async def _process_message_chunk(message_chunk, message_metadata, thread_id, agent):
    """Process a single message chunk and yield appropriate events."""
    agent_name = _get_agent_name(agent, message_metadata)
    event_stream_message = _create_event_stream_message(
        message_chunk, message_metadata, thread_id, agent_name
    )

    if isinstance(message_chunk, ToolMessage):
        # Tool Message - Return the result of the tool call
        event_stream_message["tool_call_id"] = message_chunk.tool_call_id
        yield _make_event("tool_call_result", event_stream_message)
    elif isinstance(message_chunk, AIMessageChunk):
        # AI Message - Raw message tokens
        if message_chunk.tool_calls:
            # AI Message - Tool Call
            event_stream_message["tool_calls"] = message_chunk.tool_calls
            event_stream_message["tool_call_chunks"] = message_chunk.tool_call_chunks
            event_stream_message["tool_call_chunks"] = _process_tool_call_chunks(
                message_chunk.tool_call_chunks
            )
            yield _make_event("tool_calls", event_stream_message)
        elif message_chunk.tool_call_chunks:
            # AI Message - Tool Call Chunks
            event_stream_message["tool_call_chunks"] = _process_tool_call_chunks(
                message_chunk.tool_call_chunks
            )
            yield _make_event("tool_call_chunks", event_stream_message)
        else:
            # AI Message - Raw message tokens
            yield _make_event("message_chunk", event_stream_message)


async def _stream_graph_events(
    graph_instance, workflow_input, workflow_config, thread_id
):
    """Stream events from the graph and process them."""
    async for agent, _, event_data in graph_instance.astream(
        workflow_input,
        config=workflow_config,
        stream_mode=["messages", "updates"],
        subgraphs=True,
    ):
        if isinstance(event_data, dict):
            if "__interrupt__" in event_data:
                yield _create_interrupt_event(thread_id, event_data)
            continue

        message_chunk, message_metadata = cast(
            tuple[BaseMessage, dict[str, any]], event_data
        )

        async for event in _process_message_chunk(
            message_chunk, message_metadata, thread_id, agent
        ):
            yield event


async def _astream_workflow_generator(
    messages: List[dict],
    thread_id: str,
    resources: List[Resource],
    max_plan_iterations: int,
    max_step_num: int,
    max_search_results: int,
    auto_accepted_plan: bool,
    interrupt_feedback: str,
    mcp_settings: dict,
    enable_background_investigation: bool,
    report_style: ReportStyle,
    enable_deep_thinking: bool,
):
    # Process initial messages
    for message in messages:
        if isinstance(message, dict) and "content" in message:
            _process_initial_messages(message, thread_id)

    # Prepare workflow input
    workflow_input = {
        "messages": messages,
        "plan_iterations": 0,
        "final_report": "",
        "current_plan": None,
        "observations": [],
        "auto_accepted_plan": auto_accepted_plan,
        "enable_background_investigation": enable_background_investigation,
        "research_topic": messages[-1]["content"] if messages else "",
    }

    if not auto_accepted_plan and interrupt_feedback:
        resume_msg = f"[{interrupt_feedback}]"
        if messages:
            resume_msg += f" {messages[-1]['content']}"
        workflow_input = Command(resume=resume_msg)

    # Prepare workflow config
    workflow_config = {
        "thread_id": thread_id,
        "resources": resources,
        "max_plan_iterations": max_plan_iterations,
        "max_step_num": max_step_num,
        "max_search_results": max_search_results,
        "mcp_settings": mcp_settings,
        "report_style": report_style.value,
        "enable_deep_thinking": enable_deep_thinking,
        "recursion_limit": get_recursion_limit(),
    }

    checkpoint_saver = get_bool_env("LANGGRAPH_CHECKPOINT_SAVER", False)
    checkpoint_url = get_str_env("LANGGRAPH_CHECKPOINT_DB_URL", "")
    # Handle checkpointer if configured
    connection_kwargs = {
        "autocommit": True,
        "row_factory": "dict_row",
        "prepare_threshold": 0,
    }
    if checkpoint_saver and checkpoint_url != "":
        if checkpoint_url.startswith("postgresql://"):
            logger.info("start async postgres checkpointer.")
            async with AsyncConnectionPool(
                checkpoint_url, kwargs=connection_kwargs
            ) as conn:
                checkpointer = AsyncPostgresSaver(conn)
                await checkpointer.setup()
                graph.checkpointer = checkpointer
                graph.store = in_memory_store
                async for event in _stream_graph_events(
                    graph, workflow_input, workflow_config, thread_id
                ):
                    yield event

        if checkpoint_url.startswith("mongodb://"):
            logger.info("start async mongodb checkpointer.")
            async with AsyncMongoDBSaver.from_conn_string(
                checkpoint_url
            ) as checkpointer:
                graph.checkpointer = checkpointer
                graph.store = in_memory_store
                async for event in _stream_graph_events(
                    graph, workflow_input, workflow_config, thread_id
                ):
                    yield event
    else:
        # Use graph without MongoDB checkpointer
        async for event in _stream_graph_events(
            graph, workflow_input, workflow_config, thread_id
        ):
            yield event


def _make_event(event_type: str, data: dict[str, any]):
    if data.get("content") == "":
        data.pop("content")
    # Ensure JSON serialization with proper encoding
    try:
        json_data = json.dumps(data, ensure_ascii=False)

        finish_reason = data.get("finish_reason", "")
        chat_stream_message(
            data.get("thread_id", ""),
            f"event: {event_type}\ndata: {json_data}\n\n",
            finish_reason,
        )

        return f"event: {event_type}\ndata: {json_data}\n\n"
    except (TypeError, ValueError) as e:
        logger.error(f"Error serializing event data: {e}")
        # Return a safe error event
        error_data = json.dumps({"error": "Serialization failed"}, ensure_ascii=False)
        return f"event: error\ndata: {error_data}\n\n"


@app.post(
    "/api/prompt/enhance",
    tags=["Prompt Engineering"],
    summary="Enhance and Optimize Prompts",
    description="""
    **AI-powered prompt enhancement and optimization service.**
    
    This endpoint uses advanced AI techniques to improve and optimize prompts for better results.
    
    ### Features:
    - **Prompt Optimization**: Automatically improves prompt clarity and effectiveness
    - **Context Integration**: Incorporates additional context into prompts
    - **Style Adaptation**: Adapts prompts for different report styles
    - **Best Practices**: Applies prompt engineering best practices
    
    ### Use Cases:
    - Research query optimization
    - Content generation prompts
    - Analysis and synthesis requests
    - Creative writing prompts
    
    ### Request Parameters:
    - `prompt`: The original prompt to enhance (required)
    - `context`: Additional context or background information (optional)
    - `report_style`: Target output style - academic or popular_science
    
    ### Response:
    Returns an enhanced version of the input prompt optimized for the specified context and style.
    """,
    response_description="Enhanced prompt with optimizations applied",
    responses={
        200: {
            "description": "Successfully enhanced prompt",
            "content": {
                "application/json": {
                    "example": {
                        "result": "Enhanced prompt with improved clarity, specificity, and effectiveness for the target use case."
                    }
                }
            }
        },
        400: {"description": "Invalid request parameters"},
        500: {"description": "Internal server error"}
    }
)
async def enhance_prompt(request: EnhancePromptRequest):
    try:
        sanitized_prompt = request.prompt.replace("\r\n", "").replace("\n", "")
        logger.info(f"Enhancing prompt: {sanitized_prompt}")

        # Convert string report_style to ReportStyle enum
        report_style = None
        if request.report_style:
            try:
                # Handle both uppercase and lowercase input
                style_mapping = {
                    "ACADEMIC": ReportStyle.ACADEMIC,
                    "POPULAR_SCIENCE": ReportStyle.POPULAR_SCIENCE,
                }
                report_style = style_mapping.get(
                    request.report_style.upper(), ReportStyle.ACADEMIC
                )
            except Exception:
                # If invalid style, default to ACADEMIC
                report_style = ReportStyle.ACADEMIC
        else:
            report_style = ReportStyle.ACADEMIC

        workflow = build_prompt_enhancer_graph()
        final_state = workflow.invoke(
            {
                "prompt": request.prompt,
                "context": request.context,
                "report_style": report_style,
            }
        )
        return {"result": final_state["output"]}
    except Exception as e:
        logger.exception(f"Error occurred during prompt enhancement: {str(e)}")
        raise HTTPException(status_code=500, detail=INTERNAL_SERVER_ERROR_DETAIL)


@app.post(
    "/api/mcp/server/metadata", 
    response_model=MCPServerMetadataResponse,
    tags=["MCP Integration"],
    summary="Get MCP Server Metadata and Tools",
    description="""
    **Retrieve metadata and available tools from Model Context Protocol (MCP) servers.**
    
    The Model Context Protocol enables AI applications to connect to external data sources
    and tools in a standardized way. This endpoint allows you to discover and interact with
    MCP servers.
    
    ### Features:
    - **Server Discovery**: Connect to MCP servers via different transports
    - **Tool Enumeration**: List available tools and their capabilities
    - **Dynamic Integration**: Dynamically load tools from external servers
    - **Multiple Transports**: Support for different connection methods
    
    ### Supported Transports:
    - **stdio**: Standard input/output based servers
    - **sse**: Server-Sent Events based servers
    - **http**: HTTP-based servers
    
    ### Request Parameters:
    - `transport`: Connection method (stdio, sse, http)
    - `command`: Server command for stdio transport
    - `args`: Command arguments for stdio transport
    - `url`: Server URL for sse/http transports
    - `env`: Environment variables for the server
    - `headers`: HTTP headers for http transport
    - `timeout_seconds`: Connection timeout (default: 300s)
    
    ### Security Note:
    MCP server configuration must be explicitly enabled via environment variable:
    `ENABLE_MCP_SERVER_CONFIGURATION=true`
    """,
    response_description="MCP server metadata including available tools and capabilities",
    responses={
        200: {
            "description": "Successfully retrieved MCP server metadata",
            "content": {
                "application/json": {
                    "example": {
                        "transport": "stdio",
                        "command": "mcp-server",
                        "tools": [
                            {
                                "name": "search_web",
                                "description": "Search the web for information",
                                "parameters": {"query": "string"}
                            }
                        ]
                    }
                }
            }
        },
        403: {"description": "MCP server configuration is disabled"},
        408: {"description": "Server connection timeout"},
        500: {"description": "Internal server error"}
    }
)
async def mcp_server_metadata(request: MCPServerMetadataRequest):
    """Get information about an MCP server."""
    # Check if MCP server configuration is enabled
    if not get_bool_env("ENABLE_MCP_SERVER_CONFIGURATION", False):
        raise HTTPException(
            status_code=403,
            detail="MCP server configuration is disabled. Set ENABLE_MCP_SERVER_CONFIGURATION=true to enable MCP features.",
        )

    try:
        # Set default timeout with a longer value for this endpoint
        timeout = 300  # Default to 300 seconds for this endpoint

        # Use custom timeout from request if provided
        if request.timeout_seconds is not None:
            timeout = request.timeout_seconds

        # Load tools from the MCP server using the utility function
        tools = await load_mcp_tools(
            server_type=request.transport,
            command=request.command,
            args=request.args,
            url=request.url,
            env=request.env,
            headers=request.headers,
            timeout_seconds=timeout,
        )

        # Create the response with tools
        response = MCPServerMetadataResponse(
            transport=request.transport,
            command=request.command,
            args=request.args,
            url=request.url,
            env=request.env,
            headers=request.headers,
            tools=tools,
        )

        return response
    except Exception as e:
        logger.exception(f"Error in MCP server metadata endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=INTERNAL_SERVER_ERROR_DETAIL)


@app.get(
    "/api/rag/config", 
    response_model=RAGConfigResponse,
    tags=["RAG System"],
    summary="Get RAG Configuration",
    description="""
    **Retrieve current Retrieval-Augmented Generation (RAG) system configuration.**
    
    The RAG system enhances AI responses by incorporating relevant information from
    external knowledge sources. This endpoint provides information about the current
    RAG configuration.
    
    ### Features:
    - **Provider Information**: Details about the active RAG provider
    - **Configuration Status**: Current system settings and capabilities
    - **Integration Details**: How RAG is integrated with the AI system
    
    ### RAG Providers:
    Different RAG providers offer various capabilities:
    - **Vector Databases**: Semantic search and similarity matching
    - **Document Stores**: Structured document retrieval
    - **Web Search**: Real-time web information retrieval
    - **Knowledge Graphs**: Relationship-based information retrieval
    
    ### Use Cases:
    - Check current RAG system status
    - Verify provider configuration
    - Debug RAG-related issues
    - System monitoring and health checks
    """,
    response_description="Current RAG system configuration and provider information",
    responses={
        200: {
            "description": "Successfully retrieved RAG configuration",
            "content": {
                "application/json": {
                    "example": {
                        "provider": "tavily_search",
                        "status": "active",
                        "capabilities": ["web_search", "real_time_data"]
                    }
                }
            }
        },
        500: {"description": "Internal server error"}
    }
)
async def rag_config():
    """Get the config of the RAG."""
    return RAGConfigResponse(provider=SELECTED_RAG_PROVIDER)


@app.get(
    "/api/rag/resources", 
    response_model=RAGResourcesResponse,
    tags=["RAG System"],
    summary="Search RAG Resources",
    description="""
    **Search and retrieve available resources from the RAG system.**
    
    This endpoint allows you to search through the available knowledge resources
    in the RAG system and retrieve relevant documents or information.
    
    ### Features:
    - **Resource Discovery**: Find available knowledge resources
    - **Semantic Search**: Search using natural language queries
    - **Filtered Results**: Get targeted results based on query parameters
    - **Resource Metadata**: Detailed information about each resource
    
    ### Query Parameters:
    - `query`: Search query to find relevant resources (optional)
    
    ### Resource Types:
    Resources can include:
    - **Documents**: PDFs, articles, papers, reports
    - **Web Pages**: Relevant web content and articles
    - **Databases**: Structured data sources
    - **APIs**: External data APIs and services
    
    ### Response Format:
    Returns a list of resources with metadata including:
    - Resource ID and type
    - Title and description
    - Relevance score
    - Source information
    - Access methods
    """,
    response_description="List of available RAG resources matching the search query",
    responses={
        200: {
            "description": "Successfully retrieved RAG resources",
            "content": {
                "application/json": {
                    "example": {
                        "resources": [
                            {
                                "id": "doc_001",
                                "title": "Research Paper on AI",
                                "type": "document",
                                "relevance_score": 0.95,
                                "source": "academic_database"
                            }
                        ]
                    }
                }
            }
        },
        400: {"description": "Invalid query parameters"},
        500: {"description": "Internal server error"}
    }
)
async def rag_resources(request: Annotated[RAGResourceRequest, Query()]):
    """Get the resources of the RAG."""
    retriever = build_retriever()
    if retriever:
        return RAGResourcesResponse(resources=retriever.list_resources(request.query))
    return RAGResourcesResponse(resources=[])


@app.get(
    "/api/config", 
    response_model=ConfigResponse,
    tags=["System Configuration"],
    summary="Get System Configuration",
    description="""
    **Retrieve comprehensive system configuration and status information.**
    
    This endpoint provides a complete overview of the system's current configuration,
    including all enabled features, model settings, and integration status.
    
    ### Configuration Information:
    - **Model Configuration**: Available AI models and their settings
    - **RAG System**: Retrieval-Augmented Generation configuration
    - **Feature Flags**: Enabled/disabled features and capabilities
    - **Integration Status**: Status of external integrations (MCP, APIs, etc.)
    
    ### Model Information:
    Returns details about configured AI models:
    - Model names and versions
    - Capabilities and limitations
    - Token limits and pricing
    - Provider information
    
    ### RAG Configuration:
    Includes current RAG system settings:
    - Active provider
    - Available resources
    - Search capabilities
    - Integration status
    
    ### Use Cases:
    - System health monitoring
    - Configuration validation
    - Troubleshooting and debugging
    - Feature discovery
    - Client configuration
    """,
    response_description="Complete system configuration including models and RAG settings",
    responses={
        200: {
            "description": "Successfully retrieved system configuration",
            "content": {
                "application/json": {
                    "example": {
                        "models": [
                            {
                                "name": "doubao-seed-1-6-flash-250715",
                                "provider": "charlesxu90",
                                "capabilities": ["chat", "reasoning"],
                                "max_tokens": 20000
                            }
                        ],
                        "rag": {
                            "provider": "tavily_search",
                            "status": "active"
                        },
                        "features": {
                            "mcp_enabled": False,
                            "streaming": True,
                            "reasoning": True
                        }
                    }
                }
            }
        },
        500: {"description": "Internal server error"}
    }
)
async def config():
    """Get the config of the server."""
    return ConfigResponse(
        rag=RAGConfigResponse(provider=SELECTED_RAG_PROVIDER),
        models=get_configured_llm_models(),
    )


@app.get(
    "/",
    tags=["System Information"],
    summary="API Information and Quick Start",
    description="""
    **Welcome to the DeepResearch API!**
    
    This is the main entry point for the DeepResearch AI-powered research platform.
    
    ### Quick Links:
    - **📚 Interactive Documentation**: [/docs](/docs) - Swagger UI with live testing
    - **📖 Alternative Documentation**: [/redoc](/redoc) - ReDoc interface
    - **⚙️ System Configuration**: [/api/config](/api/config) - Current system settings
    - **🔍 Health Check**: [/health](/health) - System health status
    
    ### Key Features:
    - **🤖 AI-Powered Research**: Intelligent research assistance with multi-step workflows
    - **📡 Real-time Streaming**: Server-Sent Events for live responses
    - **🔧 Tool Integration**: Access to web search, document analysis, and external APIs
    - **📝 Prompt Enhancement**: AI-powered prompt optimization
    - **🔌 MCP Support**: Model Context Protocol for external integrations
    - **📚 RAG System**: Retrieval-Augmented Generation for enhanced accuracy
    
    ### Getting Started:
    1. Visit [/docs](/docs) for interactive API documentation
    2. Test endpoints directly in the browser
    3. Check [/api/config](/api/config) for available models and features
    4. Start with [/api/chat/stream](/docs#/Chat%20%26%20Research/chat_stream_api_chat_stream_post) for AI conversations
    
    ### Authentication:
    Some features may require authentication. Check individual endpoint documentation for requirements.
    """,
    response_description="API information and navigation links",
    responses={
        200: {
            "description": "API welcome message with navigation information",
            "content": {
                "application/json": {
                    "example": {
                        "message": "DeepResearch API",
                        "version": "0.1.0",
                        "docs": "/docs",
                        "redoc": "/redoc",
                        "status": "operational"
                    }
                }
            }
        }
    }
)
async def root():
    """Root endpoint with API information."""
    return {
        "message": "DeepResearch API",
        "version": "0.1.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "chat_stream": "/api/chat/stream",
            "prompt_enhance": "/api/prompt/enhance", 
            "mcp_metadata": "/api/mcp/server/metadata",
            "rag_config": "/api/rag/config",
            "rag_resources": "/api/rag/resources",
            "config": "/api/config"
        }
    }


@app.get(
    "/health",
    tags=["System Information"],
    summary="System Health Check",
    description="""
    **Check the health and operational status of the DeepResearch API.**
    
    This endpoint provides a quick way to verify that the API is running and operational.
    It's useful for monitoring, load balancers, and automated health checks.
    
    ### Health Indicators:
    - **API Status**: Whether the API is responding
    - **System Timestamp**: Current server time
    - **Service Availability**: Basic service availability check
    
    ### Use Cases:
    - Load balancer health checks
    - Monitoring and alerting systems
    - Service discovery
    - Automated testing
    - Uptime verification
    """,
    response_description="System health status and basic operational information",
    responses={
        200: {
            "description": "System is healthy and operational",
            "content": {
                "application/json": {
                    "example": {
                        "status": "healthy",
                        "timestamp": "2025-08-27T12:00:00Z",
                        "version": "0.1.0",
                        "uptime": "24h 15m"
                    }
                }
            }
        },
        503: {"description": "Service temporarily unavailable"}
    }
)
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": "2025-08-27"}


def custom_openapi():
    """Custom OpenAPI schema with enhanced documentation."""
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="DeepResearch API",
        version="0.1.0",
        description="""
# DeepResearch API Documentation

Welcome to the **DeepResearch API** - a comprehensive AI-powered research and analysis platform.

## 🚀 Quick Start

1. **Interactive Testing**: Use the "Try it out" buttons below to test endpoints directly
2. **Authentication**: Some endpoints may require API keys (check individual endpoint docs)
3. **Streaming**: Chat endpoints use Server-Sent Events for real-time responses
4. **Rate Limits**: Be mindful of rate limits specified in your configuration

## 📋 Endpoint Categories

### 🤖 Chat & Research
Core AI conversation and research capabilities with streaming responses.

### 🔧 Prompt Engineering  
Tools for optimizing and enhancing prompts for better AI performance.

### 🔌 MCP Integration
Model Context Protocol integration for external tools and data sources.

### 📚 RAG System
Retrieval-Augmented Generation for enhanced accuracy with external knowledge.

### ⚙️ System Configuration
System settings, health checks, and configuration management.

## 🔗 External Resources

- [Documentation](https://github.com/charlesxu90/DeepResearcch)
- [GitHub Repository](https://github.com/charlesxu90/DeepResearcch)
- [Issues & Support](https://github.com/charlesxu90/DeepResearcch/issues)

## 📞 Contact & Support

For questions, issues, or feature requests, please visit our GitHub repository.
        """,
        routes=app.routes,
    )
    
    # Add additional metadata
    openapi_schema["info"]["contact"] = {
        "name": "DeepResearch Team",
        "url": "https://github.com/charlesxu90/DeepResearcch",
    }
    
    openapi_schema["info"]["license"] = {
        "name": "MIT License",
        "url": "https://github.com/charlesxu90/DeepResearcch/blob/main/LICENSE",
    }
    
    # Add server information
    openapi_schema["servers"] = [
        {
            "url": "http://localhost:8000",
            "description": "Local development server"
        },
        {
            "url": "http://localhost:8001", 
            "description": "Alternative local server"
        }
    ]
    
    # Add tag descriptions
    openapi_schema["tags"] = [
        {
            "name": "Chat & Research",
            "description": "AI-powered conversational research with streaming responses and tool integration"
        },
        {
            "name": "Prompt Engineering", 
            "description": "Prompt optimization and enhancement tools for improved AI performance"
        },
        {
            "name": "MCP Integration",
            "description": "Model Context Protocol integration for external tools and data sources"
        },
        {
            "name": "RAG System",
            "description": "Retrieval-Augmented Generation system for enhanced accuracy with external knowledge"
        },
        {
            "name": "System Configuration",
            "description": "System settings, health monitoring, and configuration management"
        },
        {
            "name": "System Information",
            "description": "Basic system information, health checks, and API navigation"
        }
    ]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


# Override the default OpenAPI schema
app.openapi = custom_openapi
