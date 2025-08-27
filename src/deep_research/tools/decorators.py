"""
Tool Enhancement Decorators and Logging Utilities

This module provides decorators and mixins for enhancing tools with logging,
monitoring, and debugging capabilities. It enables consistent instrumentation
across all tools in the Deep Research system.

Key Functions:
    log_io(func): Function decorator for input/output logging
        - Logs function calls with parameters and return values
        - Preserves function metadata using functools.wraps
        - Provides comprehensive debugging information
        - Non-intrusive logging that doesn't affect function behavior
        
    create_logged_tool(base_tool_class): Factory for creating logged tool classes
        - Creates new classes that inherit from LoggedToolMixin and base tool
        - Adds logging capabilities to any existing tool class
        - Maintains original class functionality while adding instrumentation
        - Returns enhanced tool class with descriptive naming

Key Classes:
    LoggedToolMixin: Mixin class for adding logging to tool classes
        - Provides _log_operation() helper for consistent operation logging
        - Overrides _run() method to add automatic logging
        - Integrates with LangChain tool patterns
        - Maintains backward compatibility with existing tools

Logging Features:
    Input Parameter Logging:
        - Captures all positional and keyword arguments
        - Formats parameters in readable string format
        - Includes function name for context
        - Uses INFO level for visibility
        
    Output Result Logging:
        - Logs function return values
        - Truncates large outputs for readability
        - Provides execution context
        - Uses DEBUG level for detailed information
        
    Operation Tracking:
        - Method-level operation logging
        - Tool class identification with name cleaning
        - Parameter capture for all operations
        - Consistent logging format across tools

Decorator Implementation:
    - Preserves Function Metadata: Uses functools.wraps for proper decoration
    - Type Safety: Maintains original function signatures and types
    - Exception Handling: Logging doesn't interfere with exception propagation
    - Performance: Minimal overhead for production use

Mixin Pattern:
    - Multiple Inheritance: Combines with any base tool class
    - Method Override: Safely overrides _run method with super() calls
    - Flexible Integration: Works with various tool architectures
    - Name Management: Automatic class naming for logged variants

Factory Function:
    - Dynamic Class Creation: Creates new classes at runtime
    - Type Preservation: Maintains original class types and interfaces
    - Naming Convention: Consistent "Logged" prefix naming
    - Inheritance Chain: Proper inheritance hierarchy maintenance

Tool Enhancement Pipeline:
    1. Original Tool Class: Base functionality implementation
    2. Mixin Application: LoggedToolMixin adds logging capabilities
    3. Factory Creation: create_logged_tool() generates enhanced class
    4. Integration: Enhanced tools work seamlessly with LangChain

Usage Patterns:
    - Direct Decoration: @log_io for simple function logging
    - Class Enhancement: create_logged_tool() for complex tool classes
    - Monitoring: Comprehensive operation visibility
    - Debugging: Detailed execution tracing

Logging Output Examples:
    - Tool TavilySearch called with parameters: query=AI trends, max_results=5
    - Tool TavilySearch returned: [{'title': '...', 'content': '...'}]
    - Tool RAGRetriever._run called with parameters: keywords=machine learning

The module provides a standardized approach to tool instrumentation,
enabling comprehensive monitoring and debugging across the entire
Deep Research tool ecosystem.
"""

import functools
import logging
from typing import Any, Callable, Type, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")


def log_io(func: Callable) -> Callable:
    """
    A decorator that logs the input parameters and output of a tool function.

    Args:
        func: The tool function to be decorated

    Returns:
        The wrapped function with input/output logging
    """

    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        # Log input parameters
        func_name = func.__name__
        params = ", ".join(
            [*(str(arg) for arg in args), *(f"{k}={v}" for k, v in kwargs.items())]
        )
        logger.info(f"Tool {func_name} called with parameters: {params}")

        # Execute the function
        result = func(*args, **kwargs)

        # Log the output
        logger.info(f"Tool {func_name} returned: {result}")

        return result

    return wrapper


class LoggedToolMixin:
    """A mixin class that adds logging functionality to any tool."""

    def _log_operation(self, method_name: str, *args: Any, **kwargs: Any) -> None:
        """Helper method to log tool operations."""
        tool_name = self.__class__.__name__.replace("Logged", "")
        params = ", ".join(
            [*(str(arg) for arg in args), *(f"{k}={v}" for k, v in kwargs.items())]
        )
        logger.debug(f"Tool {tool_name}.{method_name} called with parameters: {params}")

    def _run(self, *args: Any, **kwargs: Any) -> Any:
        """Override _run method to add logging."""
        self._log_operation("_run", *args, **kwargs)
        result = super()._run(*args, **kwargs)
        logger.debug(
            f"Tool {self.__class__.__name__.replace('Logged', '')} returned: {result}"
        )
        return result


def create_logged_tool(base_tool_class: Type[T]) -> Type[T]:
    """
    Factory function to create a logged version of any tool class.

    Args:
        base_tool_class: The original tool class to be enhanced with logging

    Returns:
        A new class that inherits from both LoggedToolMixin and the base tool class
    """

    class LoggedTool(LoggedToolMixin, base_tool_class):
        pass

    # Set a more descriptive name for the class
    LoggedTool.__name__ = f"Logged{base_tool_class.__name__}"
    return LoggedTool
