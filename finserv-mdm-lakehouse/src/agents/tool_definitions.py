#!/usr/bin/env python3
"""
Tool Definitions — Enterprise Data Platform Tools
===================================================
Tools available to Claude Opus 4.6 agents for building the MDM Lakehouse.
"""

TOOLS = [
    {
        "name": "profile_data_source",
        "description": "Profile a data source to understand schema, volumes, data types, nullability, cardinality, and statistical patterns.",
        "input_schema": {
            "type": "object",
            "properties": {
                "source_name": {"type": "string", "description": "Name of the source system (e.g., 'core_banking', 'salesforce')"},
                "table_name": {"type": "string", "description": "Specific table or object to profile"},
                "sample_size": {"type": "integer", "description": "Number of rows to sample", "default": 1000},
            },
            "required": ["source_name", "table_name"],
        },
    },
    {
        "name": "write_pipeline_code",
        "description": "Generate PySpark/SQL pipeline code and write to the repository.",
        "input_schema": {
            "type": "object",
            "properties": {
                "pipeline_name": {"type": "string"},
                "layer": {"type": "string", "enum": ["bronze", "silver", "mdm", "gold"]},
                "code": {"type": "string", "description": "Python or SQL code to write"},
                "file_path": {"type": "string"},
            },
            "required": ["pipeline_name", "layer", "code", "file_path"],
        },
    },
    {
        "name": "query_database",
        "description": "Execute a SQL query against the data lake (Athena/Snowflake).",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "database": {"type": "string", "enum": ["bronze", "silver", "mdm", "gold"]},
                "limit": {"type": "integer", "default": 100},
            },
            "required": ["query", "database"],
        },
    },
    {
        "name": "run_tests",
        "description": "Execute data quality tests and return results.",
        "input_schema": {
            "type": "object",
            "properties": {
                "test_suite": {"type": "string", "description": "Name of test suite to run"},
                "layer": {"type": "string", "enum": ["bronze", "silver", "mdm", "gold"]},
            },
            "required": ["test_suite"],
        },
    },
    {
        "name": "delta_lake_operation",
        "description": "Perform Delta Lake operations (MERGE, OPTIMIZE, VACUUM, TIME TRAVEL).",
        "input_schema": {
            "type": "object",
            "properties": {
                "operation": {"type": "string", "enum": ["merge", "optimize", "vacuum", "history", "restore"]},
                "table_path": {"type": "string"},
                "parameters": {"type": "object"},
            },
            "required": ["operation", "table_path"],
        },
    },
]
