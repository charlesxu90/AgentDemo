"""
Report Style Configuration

This module defines the available report output styles for the Deep Research system.
It provides an enumeration of supported writing styles that influence how research
findings are presented in the final output.

Key Classes:
    ReportStyle: Enum defining available report writing styles
        - ACADEMIC: Formal, structured academic writing style
            * Uses technical terminology and formal language
            * Includes citations and references
            * Structured with clear sections and methodology
            * Suitable for research papers and academic publications
            
        - POPULAR_SCIENCE: Accessible, engaging writing for general audiences
            * Uses plain language and explanations for technical concepts
            * Engaging narrative style with analogies and examples
            * Less formal structure, more conversational tone
            * Suitable for blogs, articles, and public communication

Usage:
    The report style is configurable through the Configuration system and influences
    how the reporter agent formats the final research output. Different styles use
    different prompt templates and writing guidelines to match the intended audience.

Integration:
    - Used in Configuration dataclass for workflow parameters
    - Applied in reporter agent for output formatting
    - Configurable through environment variables and user settings
"""

import enum


class ReportStyle(enum.Enum):
    ACADEMIC = "academic"
    POPULAR_SCIENCE = "popular_science"
