import os
import sys
import argparse
import asyncio
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio
from dotenv import load_dotenv

# ── UTF-8 stdout on Windows ───────────────────────────────────────────────
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        import io
        sys.stdout = io.TextIOWrapper(
            sys.stdout.buffer, encoding="utf-8", errors="replace"
        )

# ── Load Environment Variables ────────────────────────────────────────────
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    print("ERROR: GROQ_API_KEY not found in environment variables.")
    sys.exit(1)

# ── Parse URL argument ───────────────────────────────────────────────────
parser = argparse.ArgumentParser(description="Summarize a web page via Groq LLM")
parser.add_argument("url", help="The URL to fetch and summarize")
args = parser.parse_args()
target_url = args.url

# ── Define the MCP fetch server ───────────────────────────────────────────
mcp_fetch_server = MCPServerStdio(
    command="python",
    args=["-m", "mcp_server_fetch"]
)

# ── Configure and Create the AI Agent ────────────────────────────────────
agent = Agent(
    model="groq:llama-3.3-70b-versatile",
    mcp_servers=[mcp_fetch_server]
)

async def main():
    print("Starting MCP fetch server...")
    async with agent.run_mcp_servers():
        print("MCP server running. Asking agent to summarize...")
        prompt = (
            f"Please fetch the content from the URL '{target_url}' "
            "and provide a concise summary of the main points."
        )
        try:
            print(f"Running agent with prompt: {prompt}")
            result = await agent.run(prompt)
            output = result.output
            print("\n--- Summary ---")
            return output
        except Exception as e:
            print(f"\nAn error occurred during agent execution: {e}")
            return None
        finally:
            print("\nAgent task finished. MCP server will stop.\n")

if __name__ == "__main__":
    print("Executing main function...")
    summary_output = asyncio.run(main())

    if summary_output:
        print(summary_output)
    else:
        print("Could not generate summary due to an error.")
    print("\nScript finished.")
