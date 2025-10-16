# Email Action Item Agent

An intelligent agent that reads email content, summarizes messages, extracts actionable tasks, and prioritizes them for follow-up. This demo project uses AI reasoning to detect context, deadlines, and implied tasks beyond simple keyword-based rules.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Expected Output](#expected-output)
- [Example Output](#example-output)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)

## Prerequisites

Before setting up the Email Action Item Agent, ensure you have the following installed:

### 1. Python

- **Python 3.8 or higher** is required
- Verify your installation:
  ```bash
  python --version
  ```

### 2. Ollama

Ollama is required to run the local LLM for email processing.

- **Install Ollama**: Follow the instructions at [https://ollama.ai](https://ollama.ai)
- **Verify installation**:
  ```bash
  ollama --version
  ```

### 3. llama3.1 Model

After installing Ollama, pull the llama3.1 model:

```bash
ollama pull llama3.1
```

**Note**: The first pull may take several minutes depending on your internet connection as the model is several gigabytes in size.

**Verify the model is available**:
```bash
ollama list
```

You should see `llama3.1` in the list of available models.

## Installation

1. **Clone or download the repository** to your local machine.

2. **Navigate to the project directory**:
   ```bash
   cd email-action-item-agent
   ```

3. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   ```

4. **Activate the virtual environment**:
   
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

5. **Install required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   The project requires the following key dependencies:
   - `ollama` - Python client for Ollama API
   - `python-dateutil` - For intelligent date parsing

## Usage

### Basic Workflow

1. **Ensure Ollama is running**:
   ```bash
   ollama serve
   ```
   
   Leave this terminal window open, or run Ollama as a background service.

2. **Prepare your emails**:
   
   Place email files (`.txt` format) in the `emails/` directory. Each file should contain:
   - Email subject (first line or clearly marked)
   - Email body with the message content
   - Sender and recipient information (optional but helpful)

   Example email structure:
   ```
   Subject: Q4 Budget Review Meeting
   From: john@company.com
   To: team@company.com
   
   Hi team,
   
   Please review the Q4 budget proposal by Friday...
   ```

3. **Run the agent**:
   ```bash
   python main.py
   ```

4. **View the results**:
   
   The agent will:
   - Read all email files from the `emails/` directory
   - Process each email using the llama3.1 model
   - Generate summaries and extract action items
   - Save results to `action_items.json`

### Workflow Description

The agent performs the following steps:

1. **Email Discovery**: Scans the `emails/` folder for `.txt` files
2. **Content Parsing**: Reads and structures email content
3. **AI Processing**: Sends email content to llama3.1 for analysis
4. **Summarization**: Generates concise email summaries
5. **Task Extraction**: Identifies actionable items, deadlines, and owners
6. **Prioritization**: Ranks tasks based on urgency and importance
7. **Output Generation**: Writes structured JSON with all extracted information

## Expected Output

The agent generates an `action_items.json` file containing structured task information.

### Output File Structure

**Location**: `action_items.json` (in the project root directory)

**Format**: JSON array of task objects

### Field Descriptions

Each task object in the output contains the following fields:

| Field | Type | Description |
|-------|------|-------------|
| `task` | string | Description of the action item to be completed |
| `owner` | string | Person responsible for the task (extracted from email) |
| `deadline` | string | Due date in ISO format (YYYY-MM-DD) or "Not specified" |
| `priority` | string | Task urgency level: "high", "medium", or "low" |
| `category` | string | Task type: "meeting", "review", "response", "deliverable", etc. |
| `source_email` | string | Filename of the email this task was extracted from |
| `summary` | string | Brief summary of the related email content |

## Example Output

Here's a realistic example of `action_items.json` with multiple tasks:

```json
[
  {
    "task": "Review Q4 budget proposal and provide feedback",
    "owner": "Sarah Chen",
    "deadline": "2024-01-26",
    "priority": "high",
    "category": "review",
    "source_email": "budget_review.txt",
    "summary": "John requests team review of Q4 budget proposal with focus on marketing and R&D allocations. Feedback needed before Friday's board meeting."
  },
  {
    "task": "Prepare slide deck for client presentation",
    "owner": "Mike Rodriguez",
    "deadline": "2024-01-29",
    "priority": "high",
    "category": "deliverable",
    "source_email": "client_meeting_prep.txt",
    "summary": "Client presentation scheduled for Monday. Need to prepare 15-slide deck covering project progress, timeline updates, and next quarter roadmap."
  },
  {
    "task": "Respond to vendor inquiry about contract renewal",
    "owner": "Team",
    "deadline": "Not specified",
    "priority": "medium",
    "category": "response",
    "source_email": "vendor_contract.txt",
    "summary": "Vendor asking about contract renewal terms for next fiscal year. No urgent deadline mentioned but response expected within reasonable timeframe."
  }
]
```

## Project Structure

```
email-action-item-agent/
├── main.py                 # Main entry point - orchestrates the agent workflow
├── requirements.txt        # Python dependencies
├── emails/                 # Input directory - place your .txt email files here
│   ├── email1.txt
│   ├── email2.txt
│   └── ...
├── action_items.json       # Output file - generated task list (created after first run)
├── description.md          # Project specification and design documentation
├── README.md              # This file
└── .gitignore             # Git ignore rules
```

### Key Files

- **`main.py`**: Core agent logic including email parsing, LLM interaction, task extraction, and JSON output generation
- **`requirements.txt`**: List of Python packages needed to run the agent
- **`emails/`**: Directory where you place email files to be processed
- **`action_items.json`**: Generated output containing all extracted tasks and summaries

## Troubleshooting

### Issue: "Ollama not running" or "Connection refused"

**Symptoms**: Error messages about connection failures or "localhost:11434" being unreachable

**Solution**:
1. Ensure Ollama is running:
   ```bash
   ollama serve
   ```
2. Verify Ollama is listening on the default port:
   ```bash
   curl http://localhost:11434/api/tags
   ```
3. If using a custom port, update the Ollama client configuration in `main.py`

**Alternative**: Check if another process is using port 11434:
```bash
# On macOS/Linux
lsof -i :11434

# On Windows
netstat -ano | findstr :11434
```

---

### Issue: "llama3.1 model not found"

**Symptoms**: Error messages like "model 'llama3.1' not found" or "pull model first"

**Solution**:
1. Pull the llama3.1 model:
   ```bash
   ollama pull llama3.1
   ```
2. Verify the model is available:
   ```bash
   ollama list
   ```
3. Ensure you're using the exact model name `llama3.1` (case-sensitive)

**Note**: If you prefer to use a different model (e.g., `llama2`, `mistral`), update the model name in `main.py` and ensure that model is pulled.

---

### Issue: "No emails found in emails/ folder"

**Symptoms**: Agent runs but reports "No emails to process" or generates empty output

**Solution**:
1. Verify the `emails/` directory exists in the project root
2. Check that your email files have the `.txt` extension
3. Ensure files contain actual content (not empty)
4. Verify file permissions allow reading:
   ```bash
   ls -la emails/
   ```

**Create test emails**:
```bash
mkdir -p emails
echo -e "Subject: Test Email\nFrom: test@example.com\n\nThis is a test email with an action item." > emails/test.txt
```

---

### Issue: Low-quality or incorrect task extraction

**Symptoms**: Tasks are vague, missing deadlines, or incorrect priorities

**Solution**:
1. **Improve email formatting**: Ensure emails have clear structure with subject lines, dates, and explicit action items
2. **Be explicit in email content**: Use phrases like "by Friday", "due Monday", "please review", "action required"
3. **Check model version**: Ensure you're using llama3.1 (newer models generally perform better)
4. **Verify Ollama resources**: Ensure sufficient RAM (8GB+ recommended) for optimal model performance

---

### Issue: Slow processing time

**Symptoms**: Agent takes several minutes to process a few emails

**Solution**:
1. **Hardware check**: LLMs require significant computational resources
   - Recommended: 8GB+ RAM, modern CPU
   - Optional: GPU acceleration (check Ollama GPU support)
2. **Reduce model size**: Consider using smaller models like `llama2:7b` instead of larger variants
3. **Process fewer emails**: Start with 2-3 emails to verify functionality before batch processing

---

### Issue: JSON output formatting errors

**Symptoms**: `action_items.json` is malformed or contains syntax errors

**Solution**:
1. Check the console output for error messages during processing
2. Verify that email content doesn't contain special characters that might break JSON encoding
3. Ensure the agent completed processing (didn't exit early due to errors)
4. Try deleting `action_items.json` and re-running the agent

---

### Getting Additional Help

If you encounter issues not covered here:

1. **Check Ollama logs**: Review Ollama's output in the terminal where you ran `ollama serve`
2. **Enable debug mode**: If available in `main.py`, enable verbose logging
3. **Verify Python environment**: Ensure all dependencies are correctly installed:
   ```bash
   pip list
   ```
4. **Test with minimal input**: Create a simple one-line email to isolate the issue

## Contributing

This is a demo project showcasing agent-based email processing. Feel free to extend functionality:

- Add support for different email formats (HTML, EML)
- Implement interactive querying ("Show tasks due this week")
- Add email draft generation for follow-ups
- Integrate with email APIs (Gmail, Outlook)
- Add web interface for task management

## License

This project is provided as-is for demonstration purposes.
