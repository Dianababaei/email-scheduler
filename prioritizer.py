"""
Task Prioritization Module

This module provides functionality to prioritize extracted action items based on:
- Urgency keywords in task descriptions
- Deadline proximity
- Explicit priority mentions

Tasks are assigned priority levels: critical, high, medium, or low.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import re


# Priority level constants
PRIORITY_CRITICAL = "critical"
PRIORITY_HIGH = "high"
PRIORITY_MEDIUM = "medium"
PRIORITY_LOW = "low"

# Urgency keywords with their respective weights
URGENCY_KEYWORDS = {
    "critical": 100,
    "asap": 90,
    "urgent": 85,
    "immediately": 85,
    "emergency": 95,
    "today": 80,
    "important": 70,
    "priority": 60,
    "soon": 50,
    "time-sensitive": 80,
    "time sensitive": 80,
}

# Explicit priority patterns
EXPLICIT_PRIORITY_PATTERNS = {
    r"\b(critical|p0)\s*priority\b": 100,
    r"\bhigh\s*priority\b": 75,
    r"\bmedium\s*priority\b": 50,
    r"\blow\s*priority\b": 25,
    r"\bp0\b": 100,
    r"\bp1\b": 75,
    r"\bp2\b": 50,
    r"\bp3\b": 25,
}


def detect_urgency_keywords(description: str) -> float:
    """
    Detect urgency keywords in task description and return urgency score.
    
    Args:
        description: The task description text
        
    Returns:
        Urgency score (0-100), where higher values indicate greater urgency
    """
    if not description:
        return 0.0
    
    description_lower = description.lower()
    max_score = 0.0
    
    for keyword, score in URGENCY_KEYWORDS.items():
        if keyword in description_lower:
            max_score = max(max_score, score)
    
    return max_score


def parse_explicit_priority(description: str) -> Optional[float]:
    """
    Parse explicit priority mentions from task description.
    
    Args:
        description: The task description text
        
    Returns:
        Priority score (0-100) if found, None otherwise
    """
    if not description:
        return None
    
    description_lower = description.lower()
    
    for pattern, score in EXPLICIT_PRIORITY_PATTERNS.items():
        if re.search(pattern, description_lower, re.IGNORECASE):
            return float(score)
    
    return None


def calculate_deadline_proximity_score(deadline: Optional[Any]) -> float:
    """
    Calculate priority score based on how soon the deadline is.
    
    Args:
        deadline: Task deadline (can be string, datetime, or None)
        
    Returns:
        Proximity score (0-100), where higher values indicate closer deadlines
    """
    if deadline is None:
        return 0.0
    
    try:
        # If deadline is already a datetime object
        if isinstance(deadline, datetime):
            deadline_dt = deadline
        # If deadline is a string, try to parse it
        elif isinstance(deadline, str):
            deadline_dt = parse_deadline_string(deadline)
            if deadline_dt is None:
                return 0.0
        else:
            return 0.0
        
        # Calculate days until deadline
        now = datetime.now()
        days_until = (deadline_dt - now).total_seconds() / 86400  # Convert to days
        
        # Score based on proximity
        if days_until < 0:
            # Overdue tasks get maximum score
            return 100.0
        elif days_until <= 1:
            # Due today or tomorrow
            return 95.0
        elif days_until <= 3:
            # Due within 3 days
            return 85.0
        elif days_until <= 7:
            # Due within a week
            return 70.0
        elif days_until <= 14:
            # Due within 2 weeks
            return 50.0
        elif days_until <= 30:
            # Due within a month
            return 30.0
        else:
            # Due more than a month away
            return 10.0
            
    except Exception:
        # If any parsing error occurs, return 0
        return 0.0


def parse_deadline_string(deadline_str: str) -> Optional[datetime]:
    """
    Parse a deadline string into a datetime object.
    
    Supports various formats:
    - ISO format: "2024-01-15", "2024-01-15T10:00:00"
    - Common formats: "Jan 15, 2024", "15/01/2024", "01/15/2024"
    - Relative: "today", "tomorrow"
    
    Args:
        deadline_str: The deadline string to parse
        
    Returns:
        datetime object if parsing succeeds, None otherwise
    """
    if not deadline_str:
        return None
    
    deadline_lower = deadline_str.lower().strip()
    now = datetime.now()
    
    # Handle relative dates
    if deadline_lower == "today":
        return now
    elif deadline_lower == "tomorrow":
        return now + timedelta(days=1)
    
    # Try common date formats
    formats = [
        "%Y-%m-%d",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%m/%d/%Y",
        "%d/%m/%Y",
        "%B %d, %Y",
        "%b %d, %Y",
        "%d %B %Y",
        "%d %b %Y",
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(deadline_str.strip(), fmt)
        except ValueError:
            continue
    
    return None


def calculate_importance_score(
    task: Dict[str, Any],
    urgency_weight: float = 0.3,
    deadline_weight: float = 0.4,
    explicit_weight: float = 0.3
) -> float:
    """
    Calculate overall importance score for a task.
    
    Combines urgency keywords, deadline proximity, and explicit priority mentions
    into a single score.
    
    Args:
        task: Task dictionary containing 'description', 'deadline', etc.
        urgency_weight: Weight for urgency keyword score (default 0.3)
        deadline_weight: Weight for deadline proximity score (default 0.4)
        explicit_weight: Weight for explicit priority score (default 0.3)
        
    Returns:
        Overall importance score (0-100)
    """
    description = task.get("description", "")
    deadline = task.get("deadline")
    
    # Calculate component scores
    urgency_score = detect_urgency_keywords(description)
    deadline_score = calculate_deadline_proximity_score(deadline)
    explicit_score = parse_explicit_priority(description)
    
    # If explicit priority is found, give it strong weight
    if explicit_score is not None:
        total_score = (
            urgency_score * urgency_weight +
            deadline_score * deadline_weight +
            explicit_score * explicit_weight
        )
    else:
        # Redistribute explicit weight if no explicit priority found
        # Give more weight to deadline and urgency
        adjusted_urgency_weight = urgency_weight + explicit_weight * 0.4
        adjusted_deadline_weight = deadline_weight + explicit_weight * 0.6
        
        total_score = (
            urgency_score * adjusted_urgency_weight +
            deadline_score * adjusted_deadline_weight
        )
    
    # If no indicators found at all, return default medium score
    if total_score == 0 and urgency_score == 0 and deadline_score == 0 and explicit_score is None:
        return 50.0
    
    return min(100.0, max(0.0, total_score))


def map_score_to_priority_level(score: float) -> str:
    """
    Map numeric importance score to priority level.
    
    Args:
        score: Importance score (0-100)
        
    Returns:
        Priority level: "critical", "high", "medium", or "low"
    """
    if score >= 80:
        return PRIORITY_CRITICAL
    elif score >= 60:
        return PRIORITY_HIGH
    elif score >= 30:
        return PRIORITY_MEDIUM
    else:
        return PRIORITY_LOW


def prioritize_tasks(tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Prioritize and sort a list of extracted action items.
    
    This is the main entry point for task prioritization. It:
    1. Calculates importance score for each task
    2. Assigns priority level (critical/high/medium/low)
    3. Sorts tasks by importance score (highest first)
    
    Args:
        tasks: List of task dictionaries. Each task should have at least:
               - 'description' (str): The task description
               - 'deadline' (str/datetime, optional): Task deadline
               Additional fields are preserved in the output.
               
    Returns:
        Sorted list of tasks with added fields:
        - 'importance_score' (float): Calculated importance score (0-100)
        - 'priority' (str): Priority level (critical/high/medium/low)
        
    Example:
        >>> tasks = [
        ...     {"description": "Review urgent report", "responsible": "Alice"},
        ...     {"description": "Update documentation", "deadline": "2024-02-01"},
        ...     {"description": "Critical bug fix needed ASAP", "responsible": "Bob"}
        ... ]
        >>> prioritized = prioritize_tasks(tasks)
        >>> print(prioritized[0]['priority'])
        critical
    """
    if not tasks:
        return []
    
    # Calculate scores and assign priority levels
    for task in tasks:
        score = calculate_importance_score(task)
        task["importance_score"] = score
        task["priority"] = map_score_to_priority_level(score)
    
    # Sort by importance score (descending - highest priority first)
    sorted_tasks = sorted(tasks, key=lambda t: t.get("importance_score", 0), reverse=True)
    
    return sorted_tasks


def get_tasks_by_priority(tasks: List[Dict[str, Any]], priority_level: str) -> List[Dict[str, Any]]:
    """
    Filter tasks by priority level.
    
    Args:
        tasks: List of prioritized tasks
        priority_level: Priority level to filter by ("critical", "high", "medium", "low")
        
    Returns:
        List of tasks matching the specified priority level
    """
    return [task for task in tasks if task.get("priority") == priority_level]
