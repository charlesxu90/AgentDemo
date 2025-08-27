"""
Configuration Package for Deep Research System

This package provides comprehensive configuration management for the Deep Research workflow,
including environment setup, tool selection, report styling, and team member definitions.

Modules:
    configuration.py: Core configuration management and environment variable parsing
        - Configuration dataclass for workflow parameters
        - Environment variable utilities (get_bool_env, get_str_env, get_int_env)
        - Recursion limit management for workflow execution
        
    loader.py: YAML configuration file loading with environment variable substitution
        - load_yaml_config(): Main configuration loading function
        - Environment variable replacement in YAML values
        - Configuration caching for performance
        
    tools.py: Tool provider selection and configuration
        - SearchEngine enum: Web search provider options
        - RAGProvider enum: Document retrieval system options
        - Environment-based provider selection
        
    report_style.py: Output formatting style definitions
        - ReportStyle enum: Academic vs Popular Science writing styles
        - Influences final report generation and presentation
        
    questions.py: Built-in research question templates
        - English and Chinese question examples
        - Covers multiple research domains and use cases
        
    agents.py: Agent-to-LLM type mapping configuration
        - AGENT_LLM_MAP: Maps agent roles to optimal LLM types
        - LLMType definitions for different model capabilities

Key Constants:
    TEAM_MEMBER_CONFIGURATIONS: Defines available research team members
        - researcher: Information gathering and analysis specialist
        - coder: Programming and mathematical computation specialist
        
    TEAM_MEMBERS: List of available team member types
    SELECTED_SEARCH_ENGINE: Currently configured search provider
    BUILT_IN_QUESTIONS: Predefined research questions in multiple languages

The package enables flexible configuration of the entire research workflow,
supporting different deployment scenarios, tool providers, and user preferences
through environment variables and configuration files.
"""

from dotenv import load_dotenv

from .loader import load_yaml_config
from .questions import BUILT_IN_QUESTIONS, BUILT_IN_QUESTIONS_ZH_CN
from .tools import SELECTED_SEARCH_ENGINE, SearchEngine

# Load environment variables
load_dotenv()

# Team configuration
TEAM_MEMBER_CONFIGURATIONS = {
    "researcher": {
        "name": "researcher",
        "desc": (
            "Responsible for searching and collecting relevant information, understanding user needs and conducting research analysis"
        ),
        "desc_for_llm": (
            "Uses search engines and web crawlers to gather information from the internet. "
            "Outputs a Markdown report summarizing findings. Researcher can not do math or programming."
        ),
        "is_optional": False,
    },
    "coder": {
        "name": "coder",
        "desc": (
            "Responsible for code implementation, debugging and optimization, handling technical programming tasks"
        ),
        "desc_for_llm": (
            "Executes Python or Bash commands, performs mathematical calculations, and outputs a Markdown report. "
            "Must be used for all mathematical computations."
        ),
        "is_optional": True,
    },
}

TEAM_MEMBERS = list(TEAM_MEMBER_CONFIGURATIONS.keys())

__all__ = [
    # Other configurations
    "TEAM_MEMBERS",
    "TEAM_MEMBER_CONFIGURATIONS",
    "SELECTED_SEARCH_ENGINE",
    "SearchEngine",
    "BUILT_IN_QUESTIONS",
    "BUILT_IN_QUESTIONS_ZH_CN",
    "load_yaml_config",
]
