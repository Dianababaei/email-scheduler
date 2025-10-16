"""
Email Reader Module

This module provides functionality to read email .txt files from the emails/ directory
and return their contents in a structured format for downstream processing.
"""

import logging
from pathlib import Path
from typing import List, Dict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def read_emails(emails_dir: str = "emails") -> List[Dict[str, str]]:
    """
    Read all .txt files from the specified emails directory.
    
    Args:
        emails_dir (str): Path to the directory containing email .txt files.
                         Defaults to "emails".
    
    Returns:
        List[Dict[str, str]]: A list of dictionaries, each containing:
                              - 'filename': Name of the email file
                              - 'content': Full text content of the email
    
    Examples:
        >>> emails = read_emails()
        >>> print(emails[0]['filename'])
        'email_01.txt'
        >>> print(emails[0]['content'][:50])
        'Subject: Project Update...'
    """
    emails_path = Path(emails_dir)
    results = []
    
    # Handle missing directory
    if not emails_path.exists():
        logger.warning(f"Directory '{emails_dir}' does not exist. Creating it...")
        try:
            emails_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory '{emails_dir}'")
        except Exception as e:
            logger.error(f"Failed to create directory '{emails_dir}': {e}")
            return []
    
    if not emails_path.is_dir():
        logger.error(f"'{emails_dir}' exists but is not a directory")
        return []
    
    # Scan for .txt files
    txt_files = sorted(emails_path.glob("*.txt"))
    
    if not txt_files:
        logger.warning(f"No .txt files found in '{emails_dir}' directory")
        return []
    
    logger.info(f"Found {len(txt_files)} .txt file(s) in '{emails_dir}'")
    
    # Read each file with encoding fallbacks
    for file_path in txt_files:
        try:
            content = _read_file_with_fallback(file_path)
            results.append({
                "filename": file_path.name,
                "content": content
            })
            logger.info(f"Successfully read: {file_path.name}")
        except Exception as e:
            logger.error(f"Failed to read {file_path.name}: {e}")
            # Skip this file and continue with others
            continue
    
    logger.info(f"Successfully processed {len(results)} out of {len(txt_files)} files")
    return results


def _read_file_with_fallback(file_path: Path) -> str:
    """
    Read a file with multiple encoding attempts.
    
    Tries encodings in order:
    1. UTF-8 (most common)
    2. latin-1 (ISO-8859-1)
    3. cp1252 (Windows-1252)
    
    Args:
        file_path (Path): Path to the file to read
    
    Returns:
        str: File content as a string
    
    Raises:
        Exception: If all encoding attempts fail
    """
    encodings = ['utf-8', 'latin-1', 'cp1252']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            
            # Log warning if fallback encoding was used
            if encoding != 'utf-8':
                logger.warning(
                    f"File {file_path.name} read with fallback encoding: {encoding}"
                )
            
            return content
            
        except UnicodeDecodeError:
            if encoding == encodings[-1]:
                # Last encoding attempt failed
                raise Exception(
                    f"Failed to decode {file_path.name} with any supported encoding"
                )
            # Try next encoding
            continue
        except Exception as e:
            # Other errors (permissions, file not found, etc.)
            raise Exception(f"Error reading {file_path.name}: {e}")
    
    # Should never reach here, but for completeness
    raise Exception(f"Unexpected error reading {file_path.name}")


if __name__ == "__main__":
    # Test the email reader
    print("Testing email reader...")
    emails = read_emails()
    
    if emails:
        print(f"\nSuccessfully read {len(emails)} email(s):\n")
        for email in emails:
            print(f"Filename: {email['filename']}")
            print(f"Content preview: {email['content'][:100]}...")
            print("-" * 80)
    else:
        print("\nNo emails found or error occurred. Check logs for details.")
