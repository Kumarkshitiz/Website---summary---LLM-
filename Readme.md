# Groq Web Summarizer

A dual-mode application that leverages Groq’s LLaMA-3 model to fetch and summarize web content. You can run it via CLI or with an interactive Streamlit frontend.

## Features

- **CLI Mode**: Summarize any URL directly from the command line.
- **Streamlit UI**: User-friendly interface for URL input, validation, and summarization.
- **URL Validation**: Checks syntax and reachability before summarizing.
- **Async Agent**: Uses an MCP server to fetch content and Groq’s LLM for summarization.
- **Docker Ready**: Includes a Dockerfile for containerized deployment.

## Getting Started

### Prerequisites

- Python 3.11+
- A Groq API key (set in `.env` as `GROQ_API_KEY`)
- Git (optional)

### Installation

1. **Clone the repository**  
   ```bash
   git clone <your-repo-url>
   cd <your-repo-directory>
2. **Create a virtual environment (recommended)**
    ```bash
    python -m venv venv
    source venv/bin/activate  # macOS/Linux
    venv\Scripts\activate    # Windows

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt

4. **Usage**
   ```bash
   python main.py <URL>
