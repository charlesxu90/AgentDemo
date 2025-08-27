"""
Research Planning Data Models for Deep Research System

This module defines Pydantic models for structured research planning, providing
type-safe data structures for research plan creation, execution tracking, and
step management throughout the Deep Research workflow.

Key Classes:
    StepType: Enumeration defining research step categories
        - RESEARCH: Information gathering and data collection steps
            * Web searches, document analysis, data extraction
            * External API calls, database queries
            * Content crawling and information synthesis
            
        - PROCESSING: Data analysis and computation steps  
            * Mathematical calculations and statistical analysis
            * Code execution and algorithm processing
            * Data transformation and synthesis operations

    Step: Individual research step with comprehensive metadata
        - need_search: bool - Explicitly indicates if step requires web search
        - title: str - Descriptive name for the research step
        - description: str - Detailed specification of data collection requirements
        - step_type: StepType - Category of step (RESEARCH or PROCESSING)
        - execution_res: Optional[str] - Results from step execution (populated during workflow)

    Plan: Complete research plan structure with execution context
        - locale: str - Language/region identifier (e.g., 'en-US', 'zh-CN')
        - has_enough_context: bool - Indicates if sufficient information exists
        - thought: str - Planning rationale and strategic thinking
        - title: str - Descriptive title for the entire research plan
        - steps: List[Step] - Ordered sequence of research and processing steps

Data Validation:
    - Pydantic field validation ensures data integrity
    - Required fields prevent incomplete plan creation
    - Type enforcement maintains consistency across workflow
    - Optional fields support incremental plan development

Execution Tracking:
    - execution_res field captures step completion results
    - has_enough_context guides plan iteration decisions
    - step_type enables appropriate tool selection
    - need_search flag optimizes search resource usage

Example Schema:
    The Config class provides example JSON structures demonstrating
    proper plan formatting and expected data patterns for AI model training.

Integration:
    - Used by planner agent for structured plan generation
    - Supports LLM structured output for reliable parsing
    - Enables workflow state management and step tracking
    - Provides type safety for plan manipulation and validation

The models ensure consistent plan structure while supporting flexible
research strategies and execution patterns across different domains.
"""

# Copyright (c) 2025 charlesxu90
# SPDX-License-Identifier: MIT

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class StepType(str, Enum):
    RESEARCH = "research"
    PROCESSING = "processing"


class Step(BaseModel):
    need_search: bool = Field(..., description="Must be explicitly set for each step")
    title: str
    description: str = Field(..., description="Specify exactly what data to collect")
    step_type: StepType = Field(..., description="Indicates the nature of the step")
    execution_res: Optional[str] = Field(
        default=None, description="The Step execution result"
    )


class Plan(BaseModel):
    locale: str = Field(
        ..., description="e.g. 'en-US' or 'zh-CN', based on the user's language"
    )
    has_enough_context: bool
    thought: str
    title: str
    steps: List[Step] = Field(
        default_factory=list,
        description="Research & Processing steps to get more context",
    )

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "has_enough_context": False,
                    "thought": (
                        "To understand the current market trends in AI, we need to gather comprehensive information."
                    ),
                    "title": "AI Market Research Plan",
                    "steps": [
                        {
                            "need_search": True,
                            "title": "Current AI Market Analysis",
                            "description": (
                                "Collect data on market size, growth rates, major players, and investment trends in AI sector."
                            ),
                            "step_type": "research",
                        }
                    ],
                }
            ]
        }
