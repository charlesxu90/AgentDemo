"""
Prompt Management Package for Deep Research System

This package provides comprehensive prompt template management and processing capabilities
for the Deep Research workflow. It handles prompt loading, template rendering, and
structured data models for research planning.

Modules:
    template.py: Core prompt template engine using Jinja2
        - get_prompt_template(): Loads and renders prompt templates from .md files
        - apply_prompt_template(): Applies state variables to templates and formats messages
        - Jinja2 environment configuration with autoescaping and trim settings
        
    planner_model.py: Pydantic models for research planning structures
        - StepType: Enum defining research step categories (RESEARCH, PROCESSING)
        - Step: Individual research step with metadata and execution tracking
        - Plan: Complete research plan with locale, context, and step sequences

Template Files (.md):
    - coordinator.md: System prompts for coordination agent
    - planner.md: System prompts for research planning agent
    - researcher.md: System prompts for research execution agent
    - reporter.md: System prompts for report generation agent
    - coder.md: System prompts for code analysis and execution agent
    - prompt_enhancer/prompt_enhancer.md: Enhancement instructions
    - ppt/ppt_composer.md: PowerPoint composition instructions

Key Features:
    - Jinja2 Template Engine: Dynamic prompt generation with variable substitution
    - Markdown Templates: Human-readable prompt definitions in .md files
    - State Integration: Seamless integration with LangGraph agent states
    - Configuration Support: Automatic inclusion of configuration parameters
    - Structured Planning: Pydantic models for type-safe research planning
    - Multilingual Support: Locale-aware prompt generation

Template Variables:
    - CURRENT_TIME: Automatically injected current timestamp
    - State Variables: All agent state variables available in templates
    - Configuration: All Configuration dataclass fields accessible
    - Custom Variables: Additional context-specific variables

The package enables consistent, maintainable, and flexible prompt management
across all agents in the Deep Research system.
"""

# Copyright (c) 2025 charlesxu90
# SPDX-License-Identifier: MIT

from .template import apply_prompt_template, get_prompt_template

__all__ = [
    "apply_prompt_template",
    "get_prompt_template",
]
