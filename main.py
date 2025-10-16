"""
Email Action Item Agent - Main Entry Point

This module initializes the LangChain + Ollama LLM configuration for 
processing email content, extracting action items, and generating summaries.

Configuration:
- Model: llama3.1 (via Ollama)
- Temperature: 0.2 (low for consistent, deterministic extraction)
- Base URL: http://localhost:11434 (default Ollama endpoint)
"""

import sys
from typing import Optional
from langchain_community.chat_models import ChatOllama


def initialize_llm(
    model: str = "llama3.1",
    temperature: float = 0.2,
    base_url: str = "http://localhost:11434"
) -> Optional[ChatOllama]:
    """
    Initialize ChatOllama LLM with appropriate configuration for extraction tasks.
    
    Args:
        model: Name of the Ollama model to use (default: llama3.1)
        temperature: Sampling temperature (0.1-0.3 recommended for extraction, default: 0.2)
        base_url: Ollama service endpoint (default: http://localhost:11434)
    
    Returns:
        ChatOllama instance if successful, None if initialization fails
    
    Error Handling:
        - Connection errors: Ollama service not running
        - Model not found: llama3.1 model not pulled
        - Other exceptions: Generic error handling
    """
    try:
        print(f"Initializing LLM with model: {model}")
        print(f"Temperature: {temperature}")
        print(f"Base URL: {base_url}")
        
        # Initialize ChatOllama with specified parameters
        llm = ChatOllama(
            model=model,
            temperature=temperature,
            base_url=base_url
        )
        
        print("✓ LLM initialized successfully")
        return llm
        
    except ConnectionError as e:
        print("\n❌ ERROR: Could not connect to Ollama service", file=sys.stderr)
        print("→ Make sure Ollama is running:", file=sys.stderr)
        print("  Run: ollama serve", file=sys.stderr)
        print(f"  Expected endpoint: {base_url}", file=sys.stderr)
        print(f"\nDetails: {e}", file=sys.stderr)
        return None
        
    except Exception as e:
        # Check if error message indicates model not found
        error_msg = str(e).lower()
        if "not found" in error_msg or "pull" in error_msg or "404" in error_msg:
            print(f"\n❌ ERROR: Model '{model}' not found", file=sys.stderr)
            print("→ Pull the model first:", file=sys.stderr)
            print(f"  Run: ollama pull {model}", file=sys.stderr)
            print(f"\nDetails: {e}", file=sys.stderr)
        else:
            print("\n❌ ERROR: Failed to initialize LLM", file=sys.stderr)
            print(f"Details: {e}", file=sys.stderr)
        return None


def test_llm_connection(llm: ChatOllama) -> bool:
    """
    Test the LLM connection with a simple prompt to verify setup.
    
    Args:
        llm: ChatOllama instance to test
    
    Returns:
        True if test succeeds, False otherwise
    """
    try:
        print("\nTesting LLM connection...")
        response = llm.invoke("Respond with exactly: OK")
        
        if hasattr(response, 'content'):
            content = response.content
        else:
            content = str(response)
        
        if "OK" in content:
            print(f"✓ Connection test passed: {content.strip()}")
            return True
        else:
            print(f"⚠ Unexpected response: {content}", file=sys.stderr)
            return False
            
    except ConnectionError as e:
        print("\n❌ ERROR: Lost connection to Ollama service during test", file=sys.stderr)
        print("→ Ensure Ollama service is still running", file=sys.stderr)
        print(f"Details: {e}", file=sys.stderr)
        return False
        
    except Exception as e:
        error_msg = str(e).lower()
        if "not found" in error_msg or "pull" in error_msg or "404" in error_msg:
            print("\n❌ ERROR: Model not available during test", file=sys.stderr)
            print("→ Pull the model:", file=sys.stderr)
            print("  Run: ollama pull llama3.1", file=sys.stderr)
            print(f"Details: {e}", file=sys.stderr)
        else:
            print(f"\n❌ ERROR: Connection test failed: {e}", file=sys.stderr)
        return False


def main():
    """
    Main entry point for the Email Action Item Agent.
    Initializes and tests the LLM configuration.
    """
    print("=" * 60)
    print("Email Action Item Agent - LLM Setup")
    print("=" * 60)
    
    # Initialize the LLM with recommended parameters for extraction tasks
    llm = initialize_llm(
        model="llama3.1",
        temperature=0.2,  # Low temperature for consistent extraction
        base_url="http://localhost:11434"
    )
    
    if llm is None:
        print("\n⚠ LLM initialization failed. Exiting.", file=sys.stderr)
        sys.exit(1)
    
    # Test the connection
    if not test_llm_connection(llm):
        print("\n⚠ LLM connection test failed. Exiting.", file=sys.stderr)
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✓ LLM Setup Complete - Ready for email processing")
    print("=" * 60)
    
    # Store LLM instance for use by other modules
    return llm


if __name__ == "__main__":
    main()
