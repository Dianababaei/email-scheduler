"""
Action Item Extractor Module

This module provides functionality to extract structured action items from email content
using LangChain and Ollama LLM integration. It identifies tasks, responsible owners,
deadlines, priorities, and categories from unstructured email text.
"""

import json
from typing import List, Dict, Any, Optional
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain


# Valid categories for action items
VALID_CATEGORIES = ['meeting', 'deadline', 'follow-up', 'approval', 'review']

# Default values for missing fields
DEFAULT_PRIORITY = 'medium'
DEFAULT_CATEGORY = 'follow-up'


def create_extraction_prompt() -> PromptTemplate:
    """
    Create a prompt template for extracting action items from email content.
    
    Returns:
        PromptTemplate: Configured prompt template for action item extraction
    """
    template = """You are an AI assistant that extracts action items from email content.

Your task is to analyze the email text and identify all actionable tasks, then return them in a structured JSON format.

For each action item found, extract the following information:
- task: A clear description of what needs to be done (REQUIRED)
- owner: The person responsible for completing the task (extract from email if mentioned, otherwise null)
- deadline: The due date or deadline in ISO format YYYY-MM-DD (extract if mentioned, otherwise null)
- priority: The urgency level - must be one of: "high", "medium", "low" (infer from context, default to "medium")
- category: The type of action - must be one of: "meeting", "deadline", "follow-up", "approval", "review" (infer from context)

Important instructions:
1. Only extract actual actionable items that require someone to do something
2. If no action items exist in the email, return an empty array
3. You may extract multiple action items from a single email
4. Use null for missing information (owner, deadline) - do not make up information
5. Infer priority and category from context when possible
6. Return ONLY valid JSON, no additional text or explanation

Email content:
{email_content}

Return your response as a JSON object with this exact structure:
{{
  "action_items": [
    {{
      "task": "string describing the task",
      "owner": "person's name or null",
      "deadline": "YYYY-MM-DD or null",
      "priority": "high/medium/low",
      "category": "meeting/deadline/follow-up/approval/review"
    }}
  ]
}}

JSON Response:"""
    
    return PromptTemplate(
        input_variables=["email_content"],
        template=template
    )


def parse_llm_response(response: str) -> Dict[str, Any]:
    """
    Parse the LLM's JSON response into a Python dictionary.
    
    Args:
        response: Raw string response from the LLM
        
    Returns:
        Dict containing parsed action items or error information
    """
    try:
        # Clean up the response - remove any markdown code blocks if present
        cleaned_response = response.strip()
        if cleaned_response.startswith('```json'):
            cleaned_response = cleaned_response[7:]
        if cleaned_response.startswith('```'):
            cleaned_response = cleaned_response[3:]
        if cleaned_response.endswith('```'):
            cleaned_response = cleaned_response[:-3]
        cleaned_response = cleaned_response.strip()
        
        # Parse JSON
        parsed = json.loads(cleaned_response)
        return parsed
    except json.JSONDecodeError as e:
        # If JSON parsing fails, return empty structure
        return {"action_items": [], "error": f"JSON parsing error: {str(e)}"}
    except Exception as e:
        return {"action_items": [], "error": f"Unexpected error: {str(e)}"}


def validate_action_item(item: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and normalize a single action item.
    
    Args:
        item: Raw action item dictionary from LLM
        
    Returns:
        Validated and normalized action item dictionary
    """
    validated = {}
    
    # Task description is required
    validated['task'] = item.get('task', '').strip()
    if not validated['task']:
        return None  # Invalid item without task description
    
    # Owner can be null or a string
    owner = item.get('owner')
    validated['owner'] = owner if owner and str(owner).strip().lower() != 'null' else None
    
    # Deadline can be null or a date string
    deadline = item.get('deadline')
    validated['deadline'] = deadline if deadline and str(deadline).strip().lower() != 'null' else None
    
    # Priority must be one of the valid values, default to medium
    priority = item.get('priority', DEFAULT_PRIORITY).lower()
    if priority not in ['high', 'medium', 'low']:
        priority = DEFAULT_PRIORITY
    validated['priority'] = priority
    
    # Category must be one of the valid categories
    category = item.get('category', DEFAULT_CATEGORY).lower()
    if category not in VALID_CATEGORIES:
        # Try to infer category based on keywords in task
        task_lower = validated['task'].lower()
        if any(word in task_lower for word in ['meet', 'call', 'discussion', 'sync']):
            category = 'meeting'
        elif any(word in task_lower for word in ['due', 'deadline', 'submit', 'deliver']):
            category = 'deadline'
        elif any(word in task_lower for word in ['approve', 'authorization', 'sign off']):
            category = 'approval'
        elif any(word in task_lower for word in ['review', 'feedback', 'check']):
            category = 'review'
        else:
            category = DEFAULT_CATEGORY
    validated['category'] = category
    
    return validated


def validate_and_normalize(parsed_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Validate and normalize the complete parsed response.
    
    Args:
        parsed_data: Parsed JSON data from LLM
        
    Returns:
        List of validated action item dictionaries
    """
    if 'error' in parsed_data:
        # Return empty list if there was a parsing error
        return []
    
    action_items = parsed_data.get('action_items', [])
    if not isinstance(action_items, list):
        return []
    
    validated_items = []
    for item in action_items:
        if isinstance(item, dict):
            validated = validate_action_item(item)
            if validated:  # Only add valid items
                validated_items.append(validated)
    
    return validated_items


def extract_action_items(email_content: str, model_name: str = "llama3.1", 
                        base_url: str = "http://localhost:11434") -> List[Dict[str, Any]]:
    """
    Extract action items from email content using LangChain and Ollama.
    
    This is the main function that orchestrates the extraction process:
    1. Connects to Ollama LLM
    2. Creates the extraction prompt
    3. Processes the email content
    4. Parses and validates the results
    
    Args:
        email_content: The raw email text to analyze
        model_name: Name of the Ollama model to use (default: llama3.1)
        base_url: Base URL for Ollama API (default: http://localhost:11434)
        
    Returns:
        List of dictionaries, each containing:
            - task (str): Description of the action item
            - owner (str or None): Responsible person
            - deadline (str or None): Due date in YYYY-MM-DD format
            - priority (str): 'high', 'medium', or 'low'
            - category (str): 'meeting', 'deadline', 'follow-up', 'approval', or 'review'
        
        Returns empty list if no action items found or if processing fails.
    
    Example:
        >>> email = "Hi team, please submit your reports by Friday. John, can you review the proposal?"
        >>> items = extract_action_items(email)
        >>> print(items)
        [
            {
                'task': 'Submit reports',
                'owner': None,
                'deadline': None,
                'priority': 'medium',
                'category': 'deadline'
            },
            {
                'task': 'Review the proposal',
                'owner': 'John',
                'deadline': None,
                'priority': 'medium',
                'category': 'review'
            }
        ]
    """
    # Validate input
    if not email_content or not isinstance(email_content, str):
        return []
    
    if not email_content.strip():
        return []
    
    try:
        # Initialize Ollama LLM with JSON format
        llm = Ollama(
            model=model_name,
            base_url=base_url,
            format="json",  # Enable JSON mode for structured output
            temperature=0.1  # Low temperature for more consistent output
        )
        
        # Create prompt template
        prompt = create_extraction_prompt()
        
        # Create LangChain chain
        chain = LLMChain(llm=llm, prompt=prompt)
        
        # Run the chain
        response = chain.run(email_content=email_content)
        
        # Parse the response
        parsed_data = parse_llm_response(response)
        
        # Validate and normalize
        validated_items = validate_and_normalize(parsed_data)
        
        return validated_items
        
    except Exception as e:
        # Log error and return empty list
        print(f"Error during action item extraction: {str(e)}")
        return []


def extract_action_items_batch(emails: List[str], model_name: str = "llama3.1",
                               base_url: str = "http://localhost:11434") -> List[List[Dict[str, Any]]]:
    """
    Extract action items from multiple emails in batch.
    
    Args:
        emails: List of email content strings
        model_name: Name of the Ollama model to use
        base_url: Base URL for Ollama API
        
    Returns:
        List of lists, where each inner list contains action items for one email
    """
    results = []
    for email_content in emails:
        items = extract_action_items(email_content, model_name, base_url)
        results.append(items)
    return results


if __name__ == "__main__":
    # Example usage for testing
    sample_email = """
    Subject: Project Update and Next Steps
    
    Hi Team,
    
    Thank you all for the great work on the Q4 project. Here are the next steps:
    
    1. Sarah, please finalize the budget report by Friday, December 15th.
    2. We need to schedule a review meeting next week to discuss the findings.
    3. John, can you get approval from the director on the new proposal?
    4. Everyone should submit their timesheets by end of week.
    
    Best regards,
    Manager
    """
    
    print("Extracting action items from sample email...\n")
    action_items = extract_action_items(sample_email)
    
    print(f"Found {len(action_items)} action item(s):\n")
    for i, item in enumerate(action_items, 1):
        print(f"{i}. Task: {item['task']}")
        print(f"   Owner: {item['owner']}")
        print(f"   Deadline: {item['deadline']}")
        print(f"   Priority: {item['priority']}")
        print(f"   Category: {item['category']}")
        print()
