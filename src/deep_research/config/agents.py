"""
Agent Configuration and LLM Type Mappings

This module defines the agent-to-LLM type mappings used throughout the system.
It specifies which type of language model should be used for different agent roles
in the research workflow, enabling optimal model selection for specific tasks.

Types:
    LLMType: Literal type defining available LLM categories
    
Constants:
    AGENT_LLM_MAP: Dictionary mapping agent names to their optimal LLM types

Agent categories include:
- Planner: Strategic research planning (uses reasoning models)
- Researcher: Information gathering and analysis (uses basic models)  
- Reporter: Final report generation (uses basic models)
- Coder: Code analysis and generation (uses code-optimized models)
"""

from typing import Literal

# Define available LLM types
LLMType = Literal["basic", "reasoning", "vision", "code"]

# Define agent-LLM mapping
AGENT_LLM_MAP: dict[str, LLMType] = {
    "coordinator": "basic",
    "planner": "basic",
    "researcher": "basic",
    "coder": "basic",
    "reporter": "basic",
    "podcast_script_writer": "basic",
    "ppt_composer": "basic",
    "prose_writer": "basic",
    "prompt_enhancer": "basic",
}
