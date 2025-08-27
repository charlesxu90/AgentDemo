"""
Utility Functions Package for Deep Research System

This package provides essential utility functions and helper modules that support
various operations throughout the Deep Research workflow. These utilities handle
common tasks like data processing, validation, and format conversion.

Modules:
    json_utils.py: JSON processing and validation utilities
        - sanitize_args(): Sanitizes tool call arguments for safe processing
        - repair_json_output(): Repairs malformed JSON strings and validates structure
        - Handles special character escaping and JSON format validation

Key Features:
    Data Sanitization:
        - Tool argument sanitization for security and compatibility
        - Special character handling to prevent parsing issues
        - Input validation and type checking
        
    JSON Processing:
        - Automatic JSON repair for malformed strings
        - Format validation and structure verification
        - Error handling with graceful fallbacks
        - Ensure ASCII and encoding management

    Error Handling:
        - Comprehensive logging for debugging and monitoring
        - Graceful degradation when utilities fail
        - Clear error messages and fallback behaviors
        - Non-breaking utility functions

Integration Points:
    - Tool System: Used by tools for argument processing and output formatting
    - API Layer: JSON validation and repair for API responses
    - Workflow Processing: Data sanitization throughout research pipeline
    - LLM Integration: Safe handling of model outputs and tool calls

The utilities provide foundational support for data processing and validation
across the Deep Research system, ensuring robust operation and data integrity.
"""
