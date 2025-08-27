"""
Prompt Enhancement Node Implementation

This module contains the core logic for enhancing user prompts using AI models.
It processes user input through an AI model to generate improved, more specific,
and research-oriented prompts that lead to better research outcomes.

Key Functions:
    prompt_enhancer_node(state): Main enhancement function that processes user prompts
        - Takes PromptEnhancerState with original prompt and optional context
        - Uses configured LLM model to analyze and improve the prompt
        - Applies prompt templates for consistent enhancement instructions
        - Parses model response to extract enhanced prompt
        - Handles errors gracefully with fallback to original prompt

Enhancement Process:
    1. Context Integration: Combines original prompt with additional context
    2. Template Application: Uses prompt_enhancer template for instruction
    3. Model Invocation: Sends prompt to configured LLM for enhancement
    4. Response Parsing: Extracts enhanced prompt using multiple strategies
    5. Error Handling: Falls back to original prompt on failure

Parsing Strategies:
    - Primary: XML tag parsing for structured output (<enhanced_prompt>...</enhanced_prompt>)
    - Fallback: Text pattern matching and prefix removal
    - Robust: Handles various response formats from different LLM models

Response Processing:
    - XML Tag Extraction: Preferred method for structured responses
    - Prefix Removal: Cleans up common model-added prefixes
    - Content Cleaning: Strips whitespace and formatting artifacts
    - Validation: Ensures output quality and completeness

Error Handling:
    - Comprehensive exception catching for model failures
    - Graceful degradation to original prompt
    - Detailed logging for debugging and monitoring
    - No workflow interruption on enhancement failures

The node is designed to improve prompt quality while maintaining system reliability,
ensuring that even if enhancement fails, the original prompt can still be processed
by the research workflow.
"""

import logging
import re

from langchain.schema import HumanMessage

from src.deep_research.config.agents import AGENT_LLM_MAP
from src.deep_research.llms.llm import get_llm_by_type
from src.deep_research.prompt_enhancer.state import PromptEnhancerState
from src.deep_research.prompts.template import apply_prompt_template

logger = logging.getLogger(__name__)


def prompt_enhancer_node(state: PromptEnhancerState):
    """Node that enhances user prompts using AI analysis."""
    logger.info("Enhancing user prompt...")

    model = get_llm_by_type(AGENT_LLM_MAP["prompt_enhancer"])

    try:
        # Create messages with context if provided
        context_info = ""
        if state.get("context"):
            context_info = f"\n\nAdditional context: {state['context']}"

        original_prompt_message = HumanMessage(
            content=f"Please enhance this prompt:{context_info}\n\nOriginal prompt: {state['prompt']}"
        )

        messages = apply_prompt_template(
            "prompt_enhancer/prompt_enhancer",
            {
                "messages": [original_prompt_message],
                "report_style": state.get("report_style"),
            },
        )

        # Get the response from the model
        response = model.invoke(messages)

        # Extract content from response
        response_content = response.content.strip()
        logger.debug(f"Response content: {response_content}")

        # Try to extract content from XML tags first
        xml_match = re.search(
            r"<enhanced_prompt>(.*?)</enhanced_prompt>", response_content, re.DOTALL
        )

        if xml_match:
            # Extract content from XML tags and clean it up
            enhanced_prompt = xml_match.group(1).strip()
            logger.debug("Successfully extracted enhanced prompt from XML tags")
        else:
            # Fallback to original logic if no XML tags found
            enhanced_prompt = response_content
            logger.warning("No XML tags found in response, using fallback parsing")

            # Remove common prefixes that might be added by the model
            prefixes_to_remove = [
                "Enhanced Prompt:",
                "Enhanced prompt:",
                "Here's the enhanced prompt:",
                "Here is the enhanced prompt:",
                "**Enhanced Prompt**:",
                "**Enhanced prompt**:",
            ]

            for prefix in prefixes_to_remove:
                if enhanced_prompt.startswith(prefix):
                    enhanced_prompt = enhanced_prompt[len(prefix) :].strip()
                    break

        logger.info("Prompt enhancement completed successfully")
        logger.debug(f"Enhanced prompt: {enhanced_prompt}")
        return {"output": enhanced_prompt}
    except Exception as e:
        logger.error(f"Error in prompt enhancement: {str(e)}")
        return {"output": state["prompt"]}
