# Email Action Item Agent

An intelligent agent that reads email content, summarizes messages, extracts actionable tasks, and prioritizes them for follow-up. This demo project showcases a lightweight prototype for processing emails stored as .txt files using AI reasoning.

## Features

- **Summarization**: Generates concise overviews of email content
- **Action Item Extraction**: Identifies tasks, responsible persons, and deadlines
- **Task Prioritization**: Ranks tasks based on urgency or deadlines

The system uses local LLM integration via Ollama for fast experimentation with agent workflows.

## Prerequisites

Before running this project, ensure you have the following installed:

1. **Ollama**: Install Ollama on your system
   - Visit [https://ollama.ai](https://ollama.ai) to download and install Ollama
   - Follow the installation instructions for your operating system

2. **llama3.1 Model**: Pull the required model
   ```bash
   ollama pull llama3.1
   ```

3. **Python 3.8+**: Ensure you have Python installed on your system

## Installation

1. Clone or download this repository

2. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

*Usage instructions will be provided in a future update.*

## Project Structure

```
.
├── main.py              # Application entry point
├── emails/              # Directory for input email .txt files
├── requirements.txt     # Python dependencies
├── .gitignore          # Git ignore configuration
└── README.md           # This file
```

## Workflow

1. Place email .txt files in the `emails/` folder
2. Run the demo agent script
3. Agent reads each email, summarizes content, and extracts tasks
4. Agent outputs structured data with:
   - Task description
   - Responsible owner
   - Deadline (if detected)
   - Priority

## License

This is a demo project for educational purposes.
