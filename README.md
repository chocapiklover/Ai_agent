# AI Agent

This project is an AI-powered agent that can process natural language prompts, use available tools to gather information, and iterate on results until it reaches a final answer.

## Features
- Uses the Google Gemini API to generate and iterate on responses.
- Supports function calling to run custom tools.
- Verbose mode for debugging and inspection.
- Iterative execution loop (up to 20 iterations).
- Handles both text responses and function call outputs.

## Requirements
- Python 3.9+
- Google Gemini API key

## Installation
1. Clone this repository:
   ```bash
   git clone <your-repo-url>
   cd Ai_agent
   ```

2. (Optional but recommended) Create and activate a uv virtual environment:
   ```bash
    uv venv
    source .venv/bin/activate   # On macOS/Linux
    .venv\Scripts\activate      # On Windows
   ```

3. Install dependencies:
   ```bash
   uv pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root directory and add your Google Gemini API key:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```


## Usage
To run the AI agent, use the following command:
```bash
python main.py "Your prompt here"
 or
uv run python main.py "Your prompt here"
```

To enable verbose mode for debugging and detailed output:
```bash
python main.py "Your prompt here" --verbose
```


## Project Structure
- `main.py`  
  The entry point of the project. Handles parsing command-line arguments, loading environment variables, and running the AI agent with the provided prompt.
- `agent.py`  
  Contains the core logic for the AI agent, including the execution loop, interaction with the Gemini API, and tool function calling.
- `tools.py`  
  Defines custom tools/functions that the agent can use to gather information or perform tasks during its reasoning process.
- `requirements.txt`  
  Lists all Python dependencies required to run the project.
- `.env`  
  Environment file (not committed to version control) where you store your Google Gemini API key as `GEMINI_API_KEY`.