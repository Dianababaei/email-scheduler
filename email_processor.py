"""
Email Processing Pipeline Module.

This module orchestrates the email processing workflow including:
- Reading email files
- Summarizing email content
- Extracting action items
- Prioritizing tasks
- Outputting structured JSON results
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

from summarizer import create_summarizer, EmailSummarizer


class EmailProcessor:
    """
    Main email processing pipeline that coordinates all processing steps.
    
    Integrates:
    - Email reading and parsing
    - Content summarization
    - Action item extraction
    - Task prioritization
    """
    
    def __init__(self, emails_dir: str = "emails", output_file: str = "action_items.json"):
        """
        Initialize the EmailProcessor.
        
        Args:
            emails_dir: Directory containing email .txt files
            output_file: Path to output JSON file for results
        """
        self.emails_dir = Path(emails_dir)
        self.output_file = Path(output_file)
        self.summarizer = create_summarizer()
        
        # Create emails directory if it doesn't exist
        self.emails_dir.mkdir(exist_ok=True)
    
    def read_email_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Read an email file and extract basic metadata.
        
        Args:
            file_path: Path to the email .txt file
            
        Returns:
            Dictionary with email content and metadata
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return {
            'filename': file_path.name,
            'content': content,
            'timestamp': datetime.now().isoformat()
        }
    
    def process_email(self, email_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a single email through the pipeline.
        
        Args:
            email_data: Dictionary containing email content and metadata
            
        Returns:
            Dictionary with processed email data including summary
        """
        email_content = email_data['content']
        
        # Generate summary using the summarization chain
        summary = self.summarizer.summarize(email_content)
        
        # Build processed email structure
        processed = {
            'email_id': email_data['filename'].replace('.txt', ''),
            'filename': email_data['filename'],
            'timestamp': email_data['timestamp'],
            'summary': summary,
            'content_length': len(email_content),
            'raw_content': email_content
        }
        
        return processed
    
    def process_all_emails(self) -> List[Dict[str, Any]]:
        """
        Process all email files in the emails directory.
        
        Returns:
            List of processed email dictionaries with summaries
        """
        processed_emails = []
        
        # Get all .txt files in the emails directory
        email_files = sorted(self.emails_dir.glob("*.txt"))
        
        if not email_files:
            print(f"No email files found in {self.emails_dir}")
            return processed_emails
        
        print(f"Processing {len(email_files)} email(s)...")
        
        for email_file in email_files:
            try:
                print(f"  - Processing: {email_file.name}")
                
                # Read email file
                email_data = self.read_email_file(email_file)
                
                # Process email (including summarization)
                processed = self.process_email(email_data)
                
                processed_emails.append(processed)
                
                print(f"    ✓ Summary: {processed['summary'][:100]}...")
                
            except Exception as e:
                print(f"    ✗ Error processing {email_file.name}: {str(e)}")
                continue
        
        return processed_emails
    
    def save_results(self, processed_emails: List[Dict[str, Any]]) -> None:
        """
        Save processed emails with summaries to JSON output file.
        
        Args:
            processed_emails: List of processed email dictionaries
        """
        output_data = {
            'processed_at': datetime.now().isoformat(),
            'total_emails': len(processed_emails),
            'emails': processed_emails
        }
        
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"\nResults saved to: {self.output_file}")
    
    def run(self) -> Dict[str, Any]:
        """
        Execute the complete email processing pipeline.
        
        Returns:
            Dictionary containing all processed emails with summaries
        """
        print("=" * 80)
        print("EMAIL PROCESSING PIPELINE")
        print("=" * 80)
        print()
        
        # Process all emails
        processed_emails = self.process_all_emails()
        
        if processed_emails:
            # Save results to JSON
            self.save_results(processed_emails)
            
            print()
            print("=" * 80)
            print(f"COMPLETE: Processed {len(processed_emails)} email(s)")
            print("=" * 80)
        else:
            print("\nNo emails processed.")
        
        return {
            'total_emails': len(processed_emails),
            'emails': processed_emails
        }


def main():
    """
    Main entry point for the email processing pipeline.
    """
    # Create and run the processor
    processor = EmailProcessor()
    results = processor.run()
    
    # Display summary statistics
    if results['emails']:
        print("\n" + "=" * 80)
        print("SUMMARY STATISTICS")
        print("=" * 80)
        for email in results['emails']:
            print(f"\n📧 {email['email_id']}")
            print(f"   Summary: {email['summary']}")
            print(f"   Content Length: {email['content_length']} characters")


if __name__ == "__main__":
    main()
