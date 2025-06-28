from dearly_ai import Client
from dotenv import load_dotenv
import os

load_dotenv()

def test_dev_prompt():
    """
    Ensure that dev prompt loads properly.
    """
    c = Client(api_key=os.getenv("OPENAI_API_KEY"))
    expected = """You are a art designer. You help the user design art based on their needs.

Create beautiful and good art based on their prompt."""
    assert c._context[0]["content"] == expected, "Dev prompt broke."

def run():
    print("Test Dev Prompt...",end="")
    test_dev_prompt()
    print("Passed ✅")
    