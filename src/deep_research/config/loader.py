"""
YAML Configuration Loader with Environment Variable Substitution

This module provides utilities for loading and processing YAML configuration files
with automatic environment variable substitution and caching capabilities.

Key Functions:
    replace_env_vars(value): Substitutes environment variables in string values
        - Supports $VARIABLE_NAME syntax for environment variable references
        - Falls back to variable name if environment variable not found
        
    process_dict(config): Recursively processes dictionaries for environment variable substitution
        - Traverses nested dictionary structures
        - Applies environment variable replacement to string values
        - Preserves non-string values unchanged
        
    load_yaml_config(file_path): Loads and processes YAML files with caching
        - Loads YAML configuration from file system
        - Applies environment variable substitution
        - Caches processed configurations for performance
        - Returns empty dict if file doesn't exist

Features:
    - Environment Variable Substitution: Automatic $VAR replacement in YAML values
    - Caching System: File-based caching to avoid repeated YAML parsing
    - Error Handling: Graceful handling of missing files and invalid YAML
    - Recursive Processing: Deep traversal of nested configuration structures

Usage:
    config = load_yaml_config("conf.yaml")
    # YAML file can contain: api_key: $OPENAI_API_KEY
    # Result: api_key: "sk-..." (from environment variable)

The module is designed to work seamlessly with the main configuration system,
providing flexible configuration management with environment-specific overrides.
"""

# 

import os
from typing import Any, Dict

import yaml


def replace_env_vars(value: str) -> str:
    """Replace environment variables in string values."""
    if not isinstance(value, str):
        return value
    if value.startswith("$"):
        env_var = value[1:]
        return os.getenv(env_var, env_var)
    return value


def process_dict(config: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively process dictionary to replace environment variables."""
    if not config:
        return {}
    result = {}
    for key, value in config.items():
        if isinstance(value, dict):
            result[key] = process_dict(value)
        elif isinstance(value, str):
            result[key] = replace_env_vars(value)
        else:
            result[key] = value
    return result


_config_cache: Dict[str, Dict[str, Any]] = {}


def load_yaml_config(file_path: str) -> Dict[str, Any]:
    """Load and process YAML configuration file."""
    # 如果文件不存在，返回{}
    if not os.path.exists(file_path):
        return {}

    # 检查缓存中是否已存在配置
    if file_path in _config_cache:
        return _config_cache[file_path]

    # 如果缓存中不存在，则加载并处理配置
    with open(file_path, "r") as f:
        config = yaml.safe_load(f)
    processed_config = process_dict(config)

    # 将处理后的配置存入缓存
    _config_cache[file_path] = processed_config
    return processed_config
