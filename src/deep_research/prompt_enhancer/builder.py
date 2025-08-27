"""
Prompt Enhancement Workflow Builder

This module constructs the LangGraph workflow for prompt enhancement using a simple
single-node architecture. The workflow takes user prompts and enhances them using
AI models to improve clarity, specificity, and research effectiveness.

Key Functions:
    build_graph(): Creates and compiles the prompt enhancement workflow graph
        - Constructs StateGraph with PromptEnhancerState type
        - Adds single enhancer node for prompt processing
        - Sets entry and finish points for linear workflow
        - Compiles graph for execution

Workflow Architecture:
    - Single Node Design: Simplified workflow with one enhancement step
    - Linear Flow: Entry → Enhancer → Finish (no branching or loops)
    - State Management: Uses PromptEnhancerState for input/output handling
    - Compiled Execution: Returns ready-to-execute graph instance

Graph Structure:
    START → enhancer (prompt_enhancer_node) → END
    
    Input State:
        - prompt: Original user prompt
        - context: Optional additional context
        - report_style: Target report style preference
        
    Output State:
        - output: Enhanced prompt ready for research workflow

The workflow is designed for simplicity and reliability, focusing on a single
enhancement step rather than complex multi-stage processing. This ensures
fast execution and predictable results while maintaining high enhancement quality.

Integration:
    - Used by main research workflow for prompt preprocessing
    - Can be called independently for prompt improvement
    - Integrates with LLM management system for model selection
    - Compatible with different report styles and contexts
""" 

from langgraph.graph import StateGraph

from src.deep_research.prompt_enhancer.enhancer_node import prompt_enhancer_node
from src.deep_research.prompt_enhancer.state import PromptEnhancerState


def build_graph():
    """Build and return the prompt enhancer workflow graph."""
    # Build state graph
    builder = StateGraph(PromptEnhancerState)

    # Add the enhancer node
    builder.add_node("enhancer", prompt_enhancer_node)

    # Set entry point
    builder.set_entry_point("enhancer")

    # Set finish point
    builder.set_finish_point("enhancer")

    # Compile and return the graph
    return builder.compile()
