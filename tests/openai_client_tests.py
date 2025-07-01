from dearly_ai import Client
from dotenv import load_dotenv
import os

load_dotenv()

def test_dev_prompt():
    """
    Ensure that dev prompt loads properly.
    """
    c = Client(api_key=os.getenv("OPENAI_API_KEY"))
    expected = """You are a visual designer specializing in AI-generated art for physical products.

Your goal is to help the user create beautiful, meaningful, and high-quality artwork that can be printed on items such as clothing, mugs, posters, and accessories.

The art should reflect the user's emotional intent or aesthetic vision, while being visually striking, balanced, and suitable for print.

When generating art ideas or prompts, consider composition, color harmony, emotion, and how the design will appear on real-world surfaces."""
    assert c._context[0]["content"] == expected, "Dev prompt broke."

def run():
    print("Test Dev Prompt...",end="")
    test_dev_prompt()
    print("Passed ✅")
    