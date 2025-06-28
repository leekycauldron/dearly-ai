from openai import OpenAI
import os


class Client:
    """
    OpenAI Client Instance

    - api_key = API Key from OpenAI
    - model = model name for LLM
    
    """
    def __init__(self, api_key: str, model: str = "gpt-4.1-nano-2025-04-14") -> None:
        self._key = api_key
        self._model = model
        self._client = OpenAI(api_key=api_key)
        self._context = []
        
        # Get the directory where this module is located
        module_dir = os.path.dirname(os.path.abspath(__file__))
        prompt_path = os.path.join(module_dir, 'prompt')
        
        with open(prompt_path, 'r') as f:
            self._context.append({"role": "developer", "content": f.read()})

    def response(self, message: str) -> str:
        self._context.append({"role": "user", "content": message})
        response = self._client.responses.create(
            model=self._model,
            input=self._context
        )
        self._context.append({"role": "assistant", "content": response.output_text})
        return response.output_text
    