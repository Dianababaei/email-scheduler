"""
Email Action Item Agent - Main Orchestration Module

This module orchestrates the complete email processing pipeline:
1. Load all .txt files from emails/ directory
2. Process each email: read → summarize → extract action items
3. Aggregate all tasks into single list
4. Apply prioritization and sorting
5. Generate final action_items.json output
"""

import os
import logging
from pathlib import Path

# Import dependent modules
from email_reader import read_email
from summarization import summarize_email
from action_extraction import extract_action_items
from prioritization import prioritize_tasks
from json_output import generate_json_output


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """
    Main entry point for email processing pipeline.
    
    Orchestrates the complete workflow:
    - Loads all email files from emails/ directory
    - Processes each email sequentially
    - Aggregates all extracted tasks
    - Applies prioritization
    - Generates JSON output
    """
    logger.info("Starting email processing pipeline...")
    
    # Define emails directory
    emails_dir = Path("emails")
    
    # Validate emails directory exists
    if not emails_dir.exists():
        logger.error(f"Emails directory not found: {emails_dir}")
        logger.info("Creating emails/ directory...")
        emails_dir.mkdir(parents=True, exist_ok=True)
        logger.warning("No emails to process. Please add .txt files to emails/ directory.")
        return
    
    # Load all .txt files from emails directory
    email_files = sorted(emails_dir.glob("*.txt"))
    
    if not email_files:
        logger.warning("No .txt files found in emails/ directory")
        return
    
    total_emails = len(email_files)
    logger.info(f"Found {total_emails} email(s) to process")
    
    # Master list to collect all tasks from all emails
    all_tasks = []
    processed_count = 0
    failed_count = 0
    
    # Process each email sequentially
    for idx, email_file in enumerate(email_files, start=1):
        filename = email_file.name
        logger.info(f"Processing email {idx}/{total_emails}: {filename}...")
        
        try:
            # Step 1: Read email content
            email_content = read_email(str(email_file))
            
            if not email_content:
                logger.warning(f"Empty email content for {filename}, skipping...")
                failed_count += 1
                continue
            
            # Step 2: Summarize email
            logger.debug(f"Summarizing {filename}...")
            summary = summarize_email(email_content)
            
            # Step 3: Extract action items
            logger.debug(f"Extracting action items from {filename}...")
            action_items = extract_action_items(email_content, summary)
            
            # Step 4: Collect tasks from this email
            if action_items:
                # Add source email information to each task
                for task in action_items:
                    if isinstance(task, dict):
                        task['source_email'] = filename
                
                all_tasks.extend(action_items)
                logger.info(f"Extracted {len(action_items)} task(s) from {filename}")
            else:
                logger.info(f"No action items found in {filename}")
            
            processed_count += 1
            
        except FileNotFoundError as e:
            logger.error(f"File not found error for {filename}: {e}")
            failed_count += 1
            continue
            
        except Exception as e:
            logger.error(f"Error processing {filename}: {e}")
            failed_count += 1
            continue
    
    # Log processing summary
    total_tasks = len(all_tasks)
    logger.info(f"Processed {processed_count} email(s), extracted {total_tasks} task(s)")
    
    if failed_count > 0:
        logger.warning(f"Failed to process {failed_count} email(s)")
    
    # Step 5: Apply prioritization and sorting to all collected tasks
    if all_tasks:
        logger.info("Applying prioritization and sorting to tasks...")
        try:
            prioritized_tasks = prioritize_tasks(all_tasks)
            logger.info(f"Successfully prioritized {len(prioritized_tasks)} task(s)")
        except Exception as e:
            logger.error(f"Error during prioritization: {e}")
            logger.info("Using unprioritized task list as fallback")
            prioritized_tasks = all_tasks
    else:
        logger.warning("No tasks to prioritize")
        prioritized_tasks = []
    
    # Step 6: Generate final JSON output
    output_file = "action_items.json"
    logger.info(f"Generating output file: {output_file}...")
    
    try:
        generate_json_output(prioritized_tasks, output_file)
        logger.info(f"Successfully generated {output_file}")
    except Exception as e:
        logger.error(f"Error generating JSON output: {e}")
        return
    
    # Final summary
    logger.info("=" * 50)
    logger.info("Email processing pipeline completed successfully!")
    logger.info(f"Summary:")
    logger.info(f"  - Total emails found: {total_emails}")
    logger.info(f"  - Successfully processed: {processed_count}")
    logger.info(f"  - Failed: {failed_count}")
    logger.info(f"  - Total tasks extracted: {total_tasks}")
    logger.info(f"  - Output file: {output_file}")
    logger.info("=" * 50)


if __name__ == "__main__":
    main()
