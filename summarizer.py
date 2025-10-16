"""
Email Summarization Module using LangChain and Ollama.

This module provides functionality to generate concise summaries of email content,
focusing on key points and action items using the llama3.1 model via ChatOllama.
"""

from langchain_community.chat_models import ChatOllama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from typing import Optional


class EmailSummarizer:
    """
    Handles email summarization using LangChain with ChatOllama LLM.
    
    Generates 2-3 sentence summaries that capture:
    - Main topics and key points
    - Action items and deadlines
    - Essential context for quick understanding
    """
    
    def __init__(self, model_name: str = "llama3.1", temperature: float = 0.4):
        """
        Initialize the EmailSummarizer with ChatOllama LLM.
        
        Args:
            model_name: Ollama model to use (default: llama3.1)
            temperature: LLM temperature for consistency (0.3-0.5 recommended)
        """
        self.llm = ChatOllama(
            model=model_name,
            temperature=temperature
        )
        
        # Design prompt template for concise summarization
        self.prompt_template = PromptTemplate(
            input_variables=["email_text"],
            template="""You are an expert email analyst. Your task is to create a concise summary of the email below.

IMPORTANT INSTRUCTIONS:
- Summarize in exactly 2-3 sentences maximum
- Focus on the main topic and key points
- Highlight any action items, tasks, or deadlines if present
- Be specific and actionable
- If the email is very short, provide a clear one-sentence summary
- If there are no clear action items, focus on the main purpose and key information

EMAIL TEXT:
{email_text}

CONCISE SUMMARY (2-3 sentences):"""
        )
        
        # Create the summarization chain
        self.chain = LLMChain(
            llm=self.llm,
            prompt=self.prompt_template
        )
    
    def summarize(self, email_text: str) -> str:
        """
        Generate a concise summary of the given email text.
        
        Args:
            email_text: Raw email content as a string
            
        Returns:
            Concise summary string (2-3 sentences) highlighting key points and actions
            
        Raises:
            ValueError: If email_text is empty or None
            Exception: If LLM processing fails
        """
        # Handle edge case: empty or None input
        if not email_text or not email_text.strip():
            return "Empty email with no content."
        
        # Handle edge case: very short email
        if len(email_text.strip()) < 20:
            return f"Brief message: {email_text.strip()}"
        
        try:
            # Run the chain to generate summary
            result = self.chain.run(email_text=email_text)
            
            # Clean up the output
            summary = result.strip()
            
            # Handle edge case: ensure summary isn't too long
            # Split into sentences and take first 3 at most
            sentences = [s.strip() for s in summary.split('.') if s.strip()]
            if len(sentences) > 3:
                summary = '. '.join(sentences[:3]) + '.'
            elif not summary.endswith('.'):
                summary += '.'
            
            return summary
            
        except Exception as e:
            # Log error and return fallback summary
            print(f"Error generating summary: {str(e)}")
            # Provide a basic fallback
            words = email_text.split()[:30]
            fallback = ' '.join(words)
            if len(words) >= 30:
                fallback += "..."
            return f"Summary unavailable. Preview: {fallback}"


def create_summarizer(model_name: str = "llama3.1", temperature: float = 0.4) -> EmailSummarizer:
    """
    Factory function to create an EmailSummarizer instance.
    
    Args:
        model_name: Ollama model to use (default: llama3.1)
        temperature: LLM temperature for consistency (default: 0.4)
        
    Returns:
        Configured EmailSummarizer instance
    """
    return EmailSummarizer(model_name=model_name, temperature=temperature)


# Example usage and testing
if __name__ == "__main__":
    # Create summarizer instance
    summarizer = create_summarizer()
    
    # Test with sample emails
    test_emails = [
        """Subject: Project Deadline Update
        
Hi Team,

I wanted to remind everyone that the Q4 project deliverables are due by December 15th. 
Please ensure all your reports are submitted to the shared drive by EOD December 14th.

If you have any blockers, please reach out to me immediately.

Thanks,
John""",
        
        """Quick update: Meeting moved to 3pm tomorrow.""",
        
        """Subject: Budget Approval Needed

The marketing budget proposal needs final approval. The proposal includes:
- $50K for digital advertising
- $30K for content creation
- $20K for analytics tools

Please review and approve by Friday so we can start Q1 initiatives on time.

Best regards,
Sarah"""
    ]
    
    print("=== Email Summarization Tests ===\n")
    for i, email in enumerate(test_emails, 1):
        print(f"Test Email {i}:")
        print(f"Original length: {len(email)} characters")
        summary = summarizer.summarize(email)
        print(f"Summary: {summary}")
        print("-" * 80)
        print()
