# Email Action Item Agent

An intelligent agent that reads email content, summarizes messages, extracts actionable tasks, and prioritizes them for follow-up. The agent uses AI reasoning to detect context, deadlines, and implied tasks beyond simple keyword-based rules.

## Overview

This demo project showcases a lightweight prototype for processing emails stored as `.txt` files. The agent performs:

* **Summarization** of email contents
* **Action item extraction**: identifies tasks, responsible person, and deadlines
* **Task prioritization** based on urgency or deadlines

The system is designed for API-driven or local LLM integration using Ollama for fast experimentation with agent workflows.

## Prerequisites

Before running this project, ensure you have:

- **Python 3.8+** installed on your system
- **Ollama** installed with the `llama3.2` model available
  - Install Ollama: [https://ollama.ai](https://ollama.ai)
  - Pull the llama3.2 model: `ollama pull llama3.2`

## Installation

1. **Clone or download this repository**

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment** (optional):
   Create a `.env` file in the root directory if you need custom configuration:
   ```
   OLLAMA_HOST=http://localhost:11434
   ```

## Project Structure

```
.
├── emails/          # Input folder for email .txt files
├── output/          # Output folder for generated JSON/Markdown results
├── requirements.txt # Python dependencies
├── README.md        # This file
└── .gitignore       # Git exclusion rules
```

## Demo Workflow

1. **Place email `.txt` files** in the `emails/` folder
   - Each file should contain the raw email content
   - Files can be named descriptively (e.g., `meeting-request.txt`, `project-update.txt`)

2. **Run the demo agent script** (to be implemented in subsequent tasks)
   ```bash
   python agent.py
   ```

3. **Agent processes each email** and:
   - Reads and parses the email content
   - Generates a concise summary
   - Extracts actionable tasks with context

4. **Review the output** in the `output/` folder:
   - **JSON format**: Structured data with task descriptions, owners, deadlines, and priorities
   - **Markdown format**: Human-readable reports with formatted task lists

## Expected Outputs

The agent generates structured outputs containing:

- **Task description**: What needs to be done
- **Responsible owner**: Who should handle the task
- **Deadline**: When the task is due (if detected)
- **Priority**: Urgency level (High/Medium/Low)
- **Email summary**: Condensed overview of the original message

### Example Output Structure (JSON)

```json
{
  "email_file": "project-update.txt",
  "summary": "Project status update with Q4 deliverables...",
  "tasks": [
    {
      "description": "Review and approve Q4 budget proposal",
      "owner": "Sarah",
      "deadline": "2024-03-15",
      "priority": "High"
    }
  ]
}
```

## Features

- **Contextual reasoning**: Detects implied tasks and deadlines from natural language
- **Smart prioritization**: Ranks tasks based on urgency indicators
- **Flexible output**: Supports JSON and Markdown formats
- **Local processing**: Uses Ollama for privacy-focused LLM integration

## Use Cases

- Process daily email backlog and generate task lists
- Extract action items from meeting notes and team updates
- Prioritize follow-ups based on deadlines and importance
- Generate summaries for long email threads

## Next Steps

- Add sample email files to the `emails/` folder
- Implement the agent processing script
- Customize prompts for specific email domains
- Integrate with productivity tools (e.g., todo lists, calendars)

## Troubleshooting

**Issue**: `ollama` package not found
- **Solution**: Ensure you've activated your virtual environment and run `pip install -r requirements.txt`

**Issue**: Ollama connection errors
- **Solution**: Verify Ollama is running (`ollama serve`) and the `llama3.2` model is available (`ollama list`)

**Issue**: No output generated
- **Solution**: Check that email files are in the `emails/` folder and are readable `.txt` files

## License

This is a demo project for educational and experimental purposes.
