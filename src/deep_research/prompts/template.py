"""
Prompt Template Engine for Deep Research System

This module provides a Jinja2-based template engine for managing and processing
prompt templates used throughout the Deep Research workflow. It handles dynamic
prompt generation with variable substitution and message formatting.

Key Functions:
    get_prompt_template(prompt_name): Loads and renders basic prompt templates
        - Loads .md template files from the prompts directory
        - Uses Jinja2 for template processing and rendering
        - Returns rendered template string without variable substitution
        - Handles template loading errors with descriptive messages
        
    apply_prompt_template(prompt_name, state, configurable): Full template processing
        - Loads template and applies state variables for dynamic content
        - Integrates current timestamp (CURRENT_TIME) automatically
        - Merges agent state and configuration parameters
        - Returns formatted message list with system prompt and conversation history
        - Handles template rendering errors with comprehensive error reporting

Template Processing Features:
    - Jinja2 Environment: Configured with autoescaping for security
    - Trim Settings: Removes unnecessary whitespace (trim_blocks, lstrip_blocks)
    - File Loading: FileSystemLoader for .md template files
    - Variable Injection: Automatic state and configuration merging
    - Time Stamping: Current timestamp injection for time-aware prompts

Template Variables Available:
    - CURRENT_TIME: Formatted current timestamp for temporal context
    - Agent State: All variables from the current agent workflow state
    - Configuration: All fields from the Configuration dataclass
    - Custom Variables: Any additional variables passed in state

Message Format:
    Returns a list with:
    1. System message containing the rendered prompt template
    2. Conversation history from state["messages"]

Error Handling:
    - Template loading failures with specific error messages
    - Rendering failures with context about missing variables
    - Graceful degradation with informative error messages

The template engine enables consistent, maintainable prompt management across
all agents while supporting dynamic content generation based on workflow state.
"""

# Copyright (c) 2025 charlesxu90
# SPDX-License-Identifier: MIT

import dataclasses
import os
from datetime import datetime

from jinja2 import Environment, FileSystemLoader, select_autoescape
from langgraph.prebuilt.chat_agent_executor import AgentState

from src.deep_research.config.configuration import Configuration

# Initialize Jinja2 environment
env = Environment(
    loader=FileSystemLoader(os.path.dirname(__file__)),
    autoescape=select_autoescape(),
    trim_blocks=True,
    lstrip_blocks=True,
)


def get_prompt_template(prompt_name: str) -> str:
    """
    Load and return a prompt template using Jinja2.

    Args:
        prompt_name: Name of the prompt template file (without .md extension)

    Returns:
        The template string with proper variable substitution syntax
    """
    try:
        template = env.get_template(f"{prompt_name}.md")
        return template.render()
    except Exception as e:
        raise ValueError(f"Error loading template {prompt_name}: {e}")


def apply_prompt_template(
    prompt_name: str, state: AgentState, configurable: Configuration = None
) -> list:
    """
    Apply template variables to a prompt template and return formatted messages.

    Args:
        prompt_name: Name of the prompt template to use
        state: Current agent state containing variables to substitute

    Returns:
        List of messages with the system prompt as the first message
    """
    # Convert state to dict for template rendering
    state_vars = {
        "CURRENT_TIME": datetime.now().strftime("%a %b %d %Y %H:%M:%S %z"),
        **state,
    }

    # Add configurable variables
    if configurable:
        state_vars.update(dataclasses.asdict(configurable))

    try:
        template = env.get_template(f"{prompt_name}.md")
        system_prompt = template.render(**state_vars)
        return [{"role": "system", "content": system_prompt}] + state["messages"]
    except Exception as e:
        raise ValueError(f"Error applying template {prompt_name}: {e}")
