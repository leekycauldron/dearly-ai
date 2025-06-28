"""
Setup basic chatting with LLM, only need to provide OpenAI API Key.

Context handled by client, simply send input and it returns output.
"""

import dearly_ai
from dotenv import load_dotenv
import os

load_dotenv()

client = dearly_ai.Client(api_key=os.getenv("OPENAI_API_KEY"))

while True:
    user_input = input("User: ")
    print("Assistant: " + client.response(user_input))