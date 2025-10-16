# Email Action Item Agent - Summarization Module

This module implements intelligent email summarization using LangChain and Ollama (llama3.1 model).

## Features

- **Concise Summaries**: Generates 2-3 sentence summaries of email content
- **Action-Focused**: Highlights key points, action items, and deadlines
- **LangChain Integration**: Uses ChatOllama with llama3.1 model
- **Edge Case Handling**: Properly handles short emails, empty content, and emails without action items
- **Pipeline Integration**: Outputs summaries as part of the email processing pipeline in JSON format

## Prerequisites

1. **Ollama**: Install Ollama and pull the llama3.1 model
   ```bash
   # Install Ollama from https://ollama.ai
   ollama pull llama3.1
   ```

2. **Python Dependencies**: Install required packages
   ```bash
   pip install -r requirements.txt
   ```

## Project Structure

```
.
├── summarizer.py           # Email summarization module with LangChain
├── email_processor.py      # Main processing pipeline
├── emails/                 # Directory for email .txt files
│   ├── sample_email_1.txt
│   ├── sample_email_2.txt
│   └── sample_email_3.txt
├── action_items.json       # Output file with processed emails and summaries
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Usage

### Basic Usage

1. Place your email files (as .txt) in the `emails/` directory
2. Run the email processor:
   ```bash
   python email_processor.py
   ```
3. Check `action_items.json` for results with summaries

### Using the Summarizer Module Directly

```python
from summarizer import create_summarizer

# Create summarizer instance
summarizer = create_summarizer(
    model_name="llama3.1",
    temperature=0.4  # 0.3-0.5 for consistency
)

# Summarize email content
email_text = """
Subject: Project Update
...
"""
summary = summarizer.summarize(email_text)
print(summary)
```

### Using the Email Processor

```python
from email_processor import EmailProcessor

# Create processor
processor = EmailProcessor(
    emails_dir="emails",
    output_file="action_items.json"
)

# Process all emails
results = processor.run()
```

## Configuration

### LLM Parameters

The summarizer is configured with optimal parameters for email summarization:

- **Model**: llama3.1 (via Ollama)
- **Temperature**: 0.4 (range: 0.3-0.5 for consistency)
- **Output Length**: 2-3 sentences maximum

You can adjust these in `summarizer.py`:

```python
summarizer = EmailSummarizer(
    model_name="llama3.1",
    temperature=0.4  # Adjust for more/less variation
)
```

## Output Format

The `action_items.json` file contains:

```json
{
  "processed_at": "2024-01-01T10:00:00",
  "total_emails": 3,
  "emails": [
    {
      "email_id": "sample_email_1",
      "filename": "sample_email_1.txt",
      "timestamp": "2024-01-01T10:00:00",
      "summary": "Q4 project deliverables are due December 15th, including final reports, budget documents, and performance metrics. Team members must submit to shared drive by December 14th and report any blockers immediately. A final review meeting is scheduled for December 13th.",
      "content_length": 542,
      "raw_content": "..."
    }
  ]
}
```

## Edge Cases Handled

1. **Empty emails**: Returns "Empty email with no content."
2. **Very short emails** (<20 chars): Returns "Brief message: [content]"
3. **No action items**: Focuses on main purpose and key information
4. **LLM failures**: Provides fallback summary with content preview
5. **Long summaries**: Automatically truncates to first 3 sentences

## Performance

- **Processing time**: Typically <5 seconds per email on standard hardware
- **Concurrency**: Processes emails sequentially for reliability
- **Memory**: Minimal footprint, suitable for batch processing

## Testing

Run the summarizer module directly to test with built-in examples:

```bash
python summarizer.py
```

This will process three test emails and display their summaries.

## Integration with Pipeline

The summarization module is designed to integrate seamlessly with the email action item extraction pipeline:

1. Email content is read by `EmailProcessor`
2. Content is passed to `EmailSummarizer.summarize()`
3. Summary is included in the processed email data
4. Results are saved to `action_items.json`

## Next Steps

This module is part of a larger email processing pipeline. Future enhancements may include:

- Action item extraction and prioritization
- Deadline detection and calendar integration
- Task assignment and tracking
- Interactive querying capabilities

## Troubleshooting

### Ollama Connection Issues

If you get connection errors:
```bash
# Check Ollama is running
ollama list

# Verify llama3.1 is available
ollama pull llama3.1
```

### Import Errors

If you get LangChain import errors:
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### Slow Processing

If summarization is slow:
- Ensure Ollama is using GPU acceleration (if available)
- Reduce temperature slightly (e.g., 0.3)
- Check system resources

## License

This is a demo project for educational purposes.
