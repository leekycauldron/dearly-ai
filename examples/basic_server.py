"""
Run a web server to allow chat/image generation requests from any machine.

A web interface is also provided at the server's "/" for testing.
"""
import dearly_ai
from dotenv import load_dotenv
import os

load_dotenv()


if __name__ == "__main__":
    dearly_ai.serve(os.getenv("OPENAI_API_KEY"))