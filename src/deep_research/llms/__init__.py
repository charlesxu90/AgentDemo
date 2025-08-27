"""
LLM Package Initialization

This package provides comprehensive Large Language Model (LLM) management for the Deep Research system.

Modules:
    llm.py: Core LLM factory and configuration management
        - LLM instance creation and caching
        - Configuration loading from YAML and environment variables
        - Support for multiple LLM types (reasoning, basic, vision, code)
        
    providers/: LLM provider-specific implementations
        dashscope.py: Alibaba Cloud Dashscope integration
            - Custom ChatDashscope class extending ChatOpenAI
            - Streaming support and tool calling capabilities
            - Reasoning model support with thinking tokens

The package abstracts away provider-specific details and provides a unified interface
for accessing different types of LLMs throughout the Deep Research workflow.

Usage:
    from src.deep_research.llms.llm import get_llm_by_type
    
    # Get a reasoning-capable LLM
    reasoning_llm = get_llm_by_type("reasoning")
    
    # Get a basic chat LLM  
    basic_llm = get_llm_by_type("basic")
"""

# 