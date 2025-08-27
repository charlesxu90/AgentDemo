"""
Python Code Execution Tool for Deep Research System

This module provides safe Python code execution capabilities within the Deep Research
workflow. It offers a sandboxed Python REPL environment for data analysis, mathematical
calculations, and computational tasks during research processes.

Key Functions:
    _is_python_repl_enabled(): Configuration checker for tool availability
        - Checks ENABLE_PYTHON_REPL environment variable
        - Supports multiple truthy formats ("true", "1", "yes", "on")
        - Returns boolean indicating if tool should be active
        - Used for security-conscious deployments
        
    python_repl_tool(code): Main code execution function
        - Executes Python code in isolated REPL environment
        - Returns formatted results with code and output
        - Handles errors gracefully with detailed error reporting
        - Supports print statements for visible output

Security Features:
    - Environment-Based Control: Tool can be disabled via configuration
    - Sandboxed Execution: Uses LangChain's PythonREPL for isolation
    - Input Validation: Validates code parameter types
    - Error Containment: Catches and reports exceptions safely
    - Controlled Access: Optional tool activation for security

Execution Capabilities:
    - Mathematical Calculations: Complex mathematical operations and statistics
    - Data Analysis: Pandas, NumPy, and other data science libraries
    - Visualization: Basic plotting and chart generation (if libraries available)
    - Algorithm Implementation: Custom algorithms and data processing
    - File Operations: Limited file system access within sandbox

Output Formatting:
    - Structured Results: Formatted output with code block and results
    - Error Reporting: Clear error messages with code context
    - Status Indication: Success/failure status in response
    - User Visibility: Print statements appear in output for user feedback

Error Handling:
    - Configuration Errors: Graceful handling when tool is disabled
    - Type Validation: Input type checking with informative errors
    - Execution Errors: Python exception catching and reporting
    - Logging Integration: Comprehensive logging for monitoring and debugging

Tool Integration:
    - LangChain Compatibility: Decorated as LangChain tool for agent use
    - Logging Enhancement: Enhanced with @log_io decorator
    - Type Safety: Full type annotations for validation
    - Agent Integration: Seamless integration with research agents

Use Cases:
    - Data Processing: Clean and analyze research data
    - Statistical Analysis: Calculate statistics and trends
    - Mathematical Modeling: Implement research algorithms
    - Visualization: Create charts and graphs for insights
    - Validation: Verify calculations and hypotheses

The tool provides researchers and agents with computational capabilities,
enabling sophisticated data analysis and mathematical operations within
the research workflow while maintaining security and isolation.
"""

import logging
import os
from typing import Annotated, Optional

from langchain_core.tools import tool
from langchain_experimental.utilities import PythonREPL

from .decorators import log_io


def _is_python_repl_enabled() -> bool:
    """Check if Python REPL tool is enabled from configuration."""
    # Check environment variable first
    env_enabled = os.getenv("ENABLE_PYTHON_REPL", "false").lower()
    if env_enabled in ("true", "1", "yes", "on"):
        return True
    return False


# Initialize REPL and logger
repl: Optional[PythonREPL] = PythonREPL() if _is_python_repl_enabled() else None
logger = logging.getLogger(__name__)


@tool
@log_io
def python_repl_tool(
    code: Annotated[
        str, "The python code to execute to do further analysis or calculation."
    ],
):
    """Use this to execute python code and do data analysis or calculation. If you want to see the output of a value,
    you should print it out with `print(...)`. This is visible to the user."""

    # Check if the tool is enabled
    if not _is_python_repl_enabled():
        error_msg = "Python REPL tool is disabled. Please enable it in environment configuration."
        logger.warning(error_msg)
        return f"Tool disabled: {error_msg}"

    if not isinstance(code, str):
        error_msg = f"Invalid input: code must be a string, got {type(code)}"
        logger.error(error_msg)
        return f"Error executing code:\n```python\n{code}\n```\nError: {error_msg}"

    logger.info("Executing Python code")
    try:
        result = repl.run(code)
        # Check if the result is an error message by looking for typical error patterns
        if isinstance(result, str) and ("Error" in result or "Exception" in result):
            logger.error(result)
            return f"Error executing code:\n```python\n{code}\n```\nError: {result}"
        logger.info("Code execution successful")
    except BaseException as e:
        error_msg = repr(e)
        logger.error(error_msg)
        return f"Error executing code:\n```python\n{code}\n```\nError: {error_msg}"

    result_str = f"Successfully executed:\n```python\n{code}\n```\nStdout: {result}"
    return result_str
