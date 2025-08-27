"""
LangGraph State Types and Data Models

This module defines the state management types and data structures used throughout
the LangGraph workflow system. It extends the base MessagesState with custom fields
for research planning, resource management, and conversation tracking.

Classes:
    DeepResearcchState: Main state class extending MessagesState with research-specific fields
    
The state manages the complete research workflow including messages, plans, observations,
resources, and configuration parameters needed for multi-step AI research processes.
"""

from langgraph.graph import MessagesState

from src.deep_research.prompts.planner_model import Plan
from src.deep_research.rag import Resource


class State(MessagesState):
    """State for the agent system, extends MessagesState with next field."""

    # Runtime Variables
    locale: str = "en-US"
    research_topic: str = ""
    observations: list[str] = []
    resources: list[Resource] = []
    plan_iterations: int = 0
    current_plan: Plan | str = None
    final_report: str = ""
    auto_accepted_plan: bool = False
    enable_background_investigation: bool = True
    background_investigation_results: str = None
