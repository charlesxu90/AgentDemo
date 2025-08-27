"""
Prompt Enhancement Package for Deep Research System

This package provides AI-powered prompt enhancement capabilities to improve user queries
before they enter the main research workflow. The enhancement process analyzes user input
and transforms it into more effective, detailed, and research-oriented prompts.

Modules:
    builder.py: LangGraph workflow builder for prompt enhancement
        - build_graph(): Creates the prompt enhancement workflow graph
        - Single-node workflow with enhancer entry and finish points
        
    enhancer_node.py: Core prompt enhancement logic
        - prompt_enhancer_node(): Main enhancement function using AI models
        - XML tag parsing for structured enhancement output
        - Fallback parsing for unstructured responses
        - Error handling with graceful degradation
        
    state.py: State management for prompt enhancement workflow
        - PromptEnhancerState: TypedDict defining workflow state structure
        - Input/output state management for enhancement process

Key Features:
    - AI-Powered Enhancement: Uses configured LLM models to improve prompts
    - Context Integration: Incorporates additional context into enhancement
    - Report Style Awareness: Considers target report style in enhancement
    - Robust Parsing: Multiple parsing strategies for enhanced prompt extraction
    - Error Recovery: Graceful fallback to original prompt on enhancement failure

Workflow Process:
    1. Input: Original user prompt + optional context and report style
    2. Enhancement: AI model analyzes and improves the prompt
    3. Parsing: Extracts enhanced prompt from model response
    4. Output: Improved prompt ready for research workflow

The enhanced prompts typically include:
    - More specific research objectives
    - Better-defined scope and methodology
    - Relevant keywords and terminology
    - Structured research questions
    - Context-appropriate language

Usage:
    from src.deep_research.prompt_enhancer.builder import build_graph
    
    enhancer_graph = build_graph()
    result = enhancer_graph.invoke({
        "prompt": "Tell me about AI",
        "context": "For academic research",
        "report_style": ReportStyle.ACADEMIC
    })
    enhanced_prompt = result["output"]
""" 

"""Prompt enhancer module for improving user prompts."""
