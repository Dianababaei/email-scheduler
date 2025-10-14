# Email Action Item Agent

## Goal

Develop an intelligent agent that reads email content, summarizes messages, extracts actionable tasks, and prioritizes them for follow-up. The agent uses AI reasoning to detect context, deadlines, and implied tasks beyond simple keyword-based rules.

## Description

This demo project showcases a lightweight prototype for processing emails stored as .txt files. The agent performs:

* Summarization of email contents.
* Action item extraction: identifies tasks, responsible person, and deadlines.
* Task prioritization based on urgency or deadlines.

The system is designed for API-driven or local LLM integration, such as Ollama, for fast experimentation with agent workflows.

## Organisation of Concerns

### Data Layer

* Input Parsing: Reads email files from a folder (emails/) and converts them into structured text inputs.
* Storage Layer: Uses in-memory data structures to store summaries, tasks, and priorities for immediate processing.

### Agent & Reasoning Layer

* Summarization: Generates concise overviews of email content.
* Task Extraction: Identifies actionable items, responsible owners, deadlines, and dependencies.
* Prioritization: Ranks tasks based on urgency, deadlines, and importance.

### Integration Layer

* Exposes outputs via JSON or local API.
* Enables interactive queries such as:

  * “Show tasks due this week”
  * “Generate a follow-up email draft for all assigned tasks.”

## Demo Workflow

1. Place email .txt files in the emails/ folder.
2. Run the demo agent script.
3. Agent reads each email, summarizes content, and extracts tasks.
4. Agent outputs structured JSON or Markdown with:

   * Task description
   * Responsible owner
   * Deadline (if detected)
   * Priority
5. Optional: Query tasks via API or print to console.

## Recommendation Aims

Using Ollama or local LLM, this demo aims to:

* Demonstrate basic agent setup and prompt chaining.
* Show contextual reasoning on unstructured email text.
* Provide a starting point for integrating agent logic into productivity pipelines.

## Acceptance Criteria

* Email content is correctly read and parsed.
* Tasks are extracted with responsible owners and deadlines.
* Summaries reflect the core content of emails.
* Agent outputs are accessible in JSON or Markdown format.
* Demo workflow is fully reproducible with sample email files.
