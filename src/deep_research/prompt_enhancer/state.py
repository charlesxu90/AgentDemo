"""
Prompt Enhancement State Management

This module defines the state structure for the prompt enhancement workflow using
TypedDict for type safety and clear data contracts. The state manages input 
parameters and output results throughout the enhancement process.

Key Classes:
    PromptEnhancerState: TypedDict defining the workflow state structure
        - prompt: str - Original user prompt that needs enhancement
        - context: Optional[str] - Additional context to inform enhancement
        - report_style: Optional[ReportStyle] - Target report style for enhancement
        - output: Optional[str] - Enhanced prompt result from processing

State Fields:
    Input Fields:
        - prompt: The original user query or request requiring enhancement
            * Required field containing the raw user input
            * Should be a clear, coherent question or research request
            * Forms the basis for AI model enhancement
            
        - context: Optional additional information to guide enhancement
            * Can include background information, specific requirements
            * Helps tailor enhancement to specific use cases
            * Examples: "for academic research", "for business analysis"
            
        - report_style: Optional target style for the enhanced prompt
            * Influences enhancement direction (academic vs popular science)
            * Helps generate style-appropriate enhanced prompts
            * Used by enhancement templates and instructions

    Output Fields:
        - output: The enhanced version of the original prompt
            * Contains the AI-improved prompt ready for research workflow
            * Should be more specific, detailed, and research-oriented
            * Falls back to original prompt if enhancement fails

State Evolution:
    1. Initial State: {prompt: "user input", context: optional, report_style: optional}
    2. Processing: Enhancement node analyzes and improves the prompt
    3. Final State: {output: "enhanced prompt", ...original fields preserved}

The state structure ensures type safety and clear data flow throughout the
enhancement workflow, making it easy to understand and maintain the process.
""" 

from typing import Optional, TypedDict

from src.deep_research.config.report_style import ReportStyle


class PromptEnhancerState(TypedDict):
    """State for the prompt enhancer workflow."""

    prompt: str  # Original prompt to enhance
    context: Optional[str]  # Additional context
    report_style: Optional[ReportStyle]  # Report style preference
    output: Optional[str]  # Enhanced prompt result
