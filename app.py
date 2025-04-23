import streamlit as st
import validators
import requests
import subprocess
import os
import sys

# Page config
st.set_page_config(page_title="Groq Web Summarizer", layout="centered")

st.title("🌐 Groq Web Summarizer")
url = st.text_input("Enter a URL to summarize:")

if st.button("Summarize"):
    # Validate URL syntax
    if not validators.url(url):
        st.error("❌ That does not look like a valid URL. Try again!")
    else:
        st.info("🔍 Checking URL reachability...")
        try:
            resp = requests.head(url, timeout=5)
            resp.raise_for_status()
        except Exception as e:
            st.error(f"🚫 URL unreachable: {e}")
        else:
            st.info("⏳ Summarizing—this may take about a minute.")
            # Use the current Python interpreter to ensure venv correctness
            python_exec = sys.executable
            result = subprocess.run(
                [python_exec, "main.py", url],
                capture_output=True,
                text=True,
                env=os.environ
            )
            if result.returncode == 0 and result.stdout:
                st.success("✅ Summary:")
                st.write(result.stdout)
            else:
                error_msg = result.stderr.strip() if result.stderr else "Unknown error occurred."
                st.error(f"⚠️ Something went wrong:\n```\n{error_msg}\n```Check terminal logs for details.")
