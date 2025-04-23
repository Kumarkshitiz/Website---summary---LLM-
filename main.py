import os
import asyncio
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio
from dotenv import load_dotenv
import sys


# --- Load Environment Variables ---
# Loads variables from the .env file into the environment
load_dotenv()

# Check if the Groq API key is actually available in the environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    print("ERROR: GROQ_API_KEY not found in environment variables.")
    sys.exit(1)

# --- 1. Define the MCP fetch server ---
# This server handles fetching web content when the agent needs it.
mcp_fetch_server = MCPServerStdio(
    command="python",
    args=["-m", "mcp_server_fetch"]
)

# --- 2. Configure and Create the AI Agent ---
# Ensure the model name is a valid identifier from Groq, prefixed with 'groq/'
# Find available models at https://console.groq.com/docs/models
# Example using Llama3 70b:
agent = Agent(
    model="groq:llama-3.3-70b-versatile",
    mcp_servers=[mcp_fetch_server]
)

# --- 3. Define the main asynchronous function ---
async def main():
    """Runs the agent to fetch and summarize website content."""
    print("Starting MCP fetch server...")
    # Start the MCP servers in the background using an async context manager
    async with agent.run_mcp_servers():
        print("MCP server running. Asking agent to summarize...")
        # Define the target URL to summarize
        target_url = "https://blogs.nvidia.com/blog/what-is-a-transformer-model/" # Example URL
        # target_url = "https://ollama.com/" # Try a different URL if desired

        prompt = f"Please fetch the content from the URL '{target_url}' and provide a concise summary of the main points."

        try:
            # Run the agent with the prompt.
            # It will use the configured MCP server to handle the fetching part implicitly.
            print(f"Running agent with prompt: {prompt}")
            result = await agent.run(prompt)

            # Extract the text output from the result object
            output = result.output
            print("\n--- Summary ---")
            return output
        except Exception as e:
            # Catch potential errors during the agent run
            print(f"\nAn error occurred during agent execution: {e}")
            # Optionally, log the full traceback here for debugging
            # import traceback
            # traceback.print_exc()
            return None # Indicate failure
        finally:
            print("\nAgent task finished. MCP server will stop.") # Exiting 'async with' stops servers

# --- 4. Run the main function ---
if __name__ == "__main__":
    print("Executing main function...")
    # Run the asynchronous main function and wait for it to complete
    summary_output = asyncio.run(main())

    # Print the final summary if successful
    if summary_output:
        print(summary_output)
    else:
        print("Could not generate summary due to an error.")
    print("\nScript finished.")