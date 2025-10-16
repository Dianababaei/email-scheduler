"""
JSON Generation and File Writing Module

This module handles the generation of JSON output from sorted action items
and writes them to a file in the project root directory.
"""

import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path


def format_date_iso8601(date_value: Any) -> Optional[str]:
    """
    Format a date value to ISO 8601 format (YYYY-MM-DD).
    
    Args:
        date_value: Date in various formats (string, datetime, None)
        
    Returns:
        ISO 8601 formatted date string or None if date is invalid/missing
    """
    if date_value is None or date_value == "":
        return None
    
    # If already a datetime object
    if isinstance(date_value, datetime):
        return date_value.strftime("%Y-%m-%d")
    
    # If it's a string, try to parse common formats
    if isinstance(date_value, str):
        # Try ISO format first
        try:
            parsed_date = datetime.fromisoformat(date_value.replace('Z', '+00:00'))
            return parsed_date.strftime("%Y-%m-%d")
        except (ValueError, AttributeError):
            pass
        
        # Try common date formats
        date_formats = [
            "%Y-%m-%d",
            "%m/%d/%Y",
            "%d/%m/%Y",
            "%Y/%m/%d",
            "%B %d, %Y",
            "%b %d, %Y",
            "%d %B %Y",
            "%d %b %Y",
        ]
        
        for fmt in date_formats:
            try:
                parsed_date = datetime.strptime(date_value.strip(), fmt)
                return parsed_date.strftime("%Y-%m-%d")
            except (ValueError, AttributeError):
                continue
    
    # If we couldn't parse it, return the original value as string
    return str(date_value) if date_value else None


def validate_task_structure(task: Dict[str, Any]) -> bool:
    """
    Validate that a task has all required fields.
    
    Args:
        task: Dictionary representing a task
        
    Returns:
        True if task has all required fields, False otherwise
    """
    required_fields = ['task', 'owner', 'deadline', 'priority', 'category', 'source_email', 'summary']
    
    for field in required_fields:
        if field not in task:
            return False
    
    return True


def build_json_structure(sorted_tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Build JSON structure from sorted task list with proper formatting.
    
    Args:
        sorted_tasks: List of task dictionaries with extracted fields
        
    Returns:
        List of properly formatted task dictionaries
    """
    formatted_tasks = []
    
    for task in sorted_tasks:
        # Validate task structure
        if not validate_task_structure(task):
            # Log warning but continue processing
            print(f"Warning: Task missing required fields: {task}")
            continue
        
        # Format the task with proper date handling
        formatted_task = {
            'task': task.get('task', ''),
            'owner': task.get('owner', ''),
            'deadline': format_date_iso8601(task.get('deadline')),
            'priority': task.get('priority', ''),
            'category': task.get('category', ''),
            'source_email': task.get('source_email', ''),
            'summary': task.get('summary', '')
        }
        
        formatted_tasks.append(formatted_task)
    
    return formatted_tasks


def write_action_items_to_json(sorted_tasks: List[Dict[str, Any]], 
                                output_file: str = "action_items.json",
                                indent: int = 2) -> bool:
    """
    Write sorted action items to JSON file in project root.
    
    Args:
        sorted_tasks: List of task dictionaries with all required fields
        output_file: Output filename (default: action_items.json)
        indent: JSON indentation level (default: 2)
        
    Returns:
        True if successful, False otherwise
        
    Raises:
        IOError: If file writing fails
        ValueError: If task list is invalid
    """
    if not sorted_tasks:
        print("Warning: Empty task list provided")
        sorted_tasks = []
    
    try:
        # Build JSON structure with formatted dates
        formatted_tasks = build_json_structure(sorted_tasks)
        
        # Create output path in project root
        output_path = Path(output_file)
        
        # Write JSON to file with UTF-8 encoding
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(formatted_tasks, f, indent=indent, ensure_ascii=False)
        
        print(f"Successfully wrote {len(formatted_tasks)} action items to {output_file}")
        return True
        
    except IOError as e:
        print(f"Error: Failed to write to file {output_file}: {e}")
        print("Possible causes: insufficient permissions, disk space, or invalid path")
        raise
        
    except (TypeError, ValueError) as e:
        print(f"Error: Invalid task data structure: {e}")
        raise ValueError(f"Task list contains invalid data: {e}")
        
    except Exception as e:
        print(f"Unexpected error writing JSON file: {e}")
        raise


def generate_action_items_json(sorted_tasks: List[Dict[str, Any]], 
                               output_file: str = "action_items.json") -> None:
    """
    Main entry point for generating action items JSON file.
    
    This function accepts a sorted list of action items and writes them
    to a JSON file with proper formatting and error handling.
    
    Args:
        sorted_tasks: List of task dictionaries with fields:
                     - task: Task description
                     - owner: Person responsible
                     - deadline: Due date (will be formatted to ISO 8601)
                     - priority: Priority level
                     - category: Task category
                     - source_email: Source email identifier
                     - summary: Task summary
        output_file: Output filename in project root (default: action_items.json)
        
    Example:
        >>> tasks = [
        ...     {
        ...         'task': 'Review proposal',
        ...         'owner': 'John Doe',
        ...         'deadline': '2024-01-15',
        ...         'priority': 'high',
        ...         'category': 'review',
        ...         'source_email': 'email_001.txt',
        ...         'summary': 'Review Q1 proposal document'
        ...     }
        ... ]
        >>> generate_action_items_json(tasks)
    """
    try:
        write_action_items_to_json(sorted_tasks, output_file)
    except Exception as e:
        print(f"Failed to generate action items JSON: {e}")
        raise
