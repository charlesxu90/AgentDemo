
"""
Configuration Management for Deep Research System

This module provides centralized configuration management for the Deep Research workflow system.
It handles environment variable parsing, configuration validation, and provides a unified 
Configuration dataclass for workflow parameters.

Key Functions:
    get_bool_env(name, default): Parses boolean environment variables with truthy value detection
    get_str_env(name, default): Retrieves string environment variables with fallback defaults
    get_int_env(name, default): Parses integer environment variables with error handling
    get_recursion_limit(default): Gets workflow recursion limit with validation

Key Classes:
    Configuration: Dataclass holding all configurable workflow parameters
        - resources: List of external resources for research context
        - max_plan_iterations: Maximum number of research plan refinements
        - max_step_num: Maximum steps per research plan
        - max_search_results: Limit for search result count
        - mcp_settings: Model Context Protocol tool configurations
        - report_style: Output format style (academic/popular_science)
        - enable_deep_thinking: Flag for reasoning model deep thinking mode

Configuration Sources:
    1. Environment variables (highest precedence)
    2. RunnableConfig from LangGraph workflow
    3. Default values (lowest precedence)

Environment Variable Parsing:
    - Boolean: Supports "1", "true", "yes", "y", "on" as truthy values (case-insensitive)
    - Integer: Validates numeric values with error logging for invalid inputs
    - String: Direct string extraction with whitespace trimming
    - Recursion Limit: Special handling for workflow execution limits

The Configuration class integrates with LangGraph's RunnableConfig system to provide
seamless parameter passing throughout the research workflow execution.
"""

import logging
import os
from dataclasses import dataclass, field, fields
from typing import Any, Optional

from langchain_core.runnables import RunnableConfig

from src.deep_research.config.report_style import ReportStyle
from src.deep_research.rag.retriever import Resource

logger = logging.getLogger(__name__)

_TRUTHY = {"1", "true", "yes", "y", "on"}


def get_bool_env(name: str, default: bool = False) -> bool:
    val = os.getenv(name)
    if val is None:
        return default
    return str(val).strip().lower() in _TRUTHY


def get_str_env(name: str, default: str = "") -> str:
    val = os.getenv(name)
    return default if val is None else str(val).strip()


def get_int_env(name: str, default: int = 0) -> int:
    val = os.getenv(name)
    if val is None:
        return default
    try:
        return int(val.strip())
    except ValueError:
        logger.warning(
            f"Invalid integer value for {name}: {val}. Using default {default}."
        )
        return default


def get_recursion_limit(default: int = 25) -> int:
    """Get the recursion limit from environment variable or use default.

    Args:
        default: Default recursion limit if environment variable is not set or invalid

    Returns:
        int: The recursion limit to use
    """
    env_value_str = get_str_env("AGENT_RECURSION_LIMIT", str(default))
    parsed_limit = get_int_env("AGENT_RECURSION_LIMIT", default)

    if parsed_limit > 0:
        logger.info(f"Recursion limit set to: {parsed_limit}")
        return parsed_limit
    else:
        logger.warning(
            f"AGENT_RECURSION_LIMIT value '{env_value_str}' (parsed as {parsed_limit}) is not positive. "
            f"Using default value {default}."
        )
        return default


@dataclass(kw_only=True)
class Configuration:
    """The configurable fields."""

    resources: list[Resource] = field(
        default_factory=list
    )  # Resources to be used for the research
    max_plan_iterations: int = 1  # Maximum number of plan iterations
    max_step_num: int = 3  # Maximum number of steps in a plan
    max_search_results: int = 3  # Maximum number of search results
    mcp_settings: dict = None  # MCP settings, including dynamic loaded tools
    report_style: str = ReportStyle.ACADEMIC.value  # Report style
    enable_deep_thinking: bool = False  # Whether to enable deep thinking

    @classmethod
    def from_runnable_config(
        cls, config: Optional[RunnableConfig] = None
    ) -> "Configuration":
        """Create a Configuration instance from a RunnableConfig."""
        configurable = (
            config["configurable"] if config and "configurable" in config else {}
        )
        values: dict[str, Any] = {
            f.name: os.environ.get(f.name.upper(), configurable.get(f.name))
            for f in fields(cls)
            if f.init
        }
        return cls(**{k: v for k, v in values.items() if v})
