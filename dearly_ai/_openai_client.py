from openai import OpenAI
import base64
import os
import json


TOOLS = [
    {
        "type": "function",
        "name": "_generate_image",
        "description": "Generates an image based on your prompt",
        "parameters": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "Text prompt to guide image generation"
                }
            },
            "required": ["prompt"],
            "additionalProperties": False
        }
    }
]


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

    def _generate_image(self, prompt: str):
        img = self._client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            n=1,
            size="1024x1024",
            quality="low"
        )

        image_bytes = base64.b64decode(img.data[0].b64_json)
        with open("output.png", "wb") as f:
            f.write(image_bytes)
        return "output.png"

    def response(self, message: str = None, debug=False) -> str:
        if message:
            self._context.append({"role": "user", "content": message})
            if debug:
                print(f"[User]: {message}")
        response = self._client.responses.create(
            model=self._model,
            input=self._context,
            tools=TOOLS,
        )
        # Check for tool/function call in the response
        for tool_call in response.output:
            if tool_call.type == "function_call":
                if debug:
                    print(f"[Tool Call]: {tool_call}")
                self._context.append(tool_call)
                if tool_call.name == "_generate_image":
                    args = json.loads(tool_call.arguments)
                    prompt = args["prompt"]
                    image_path = self._generate_image(prompt)
                    # Add the image result to the context as an assistant message
                    result_message = f"[Image generated: {image_path}]"
                    if debug:
                        print(f"[Tool Call Output]: {result_message}")
                    self._context.append({
                        "type": "function_call_output",
                        "call_id": tool_call.call_id,
                        "output": result_message
                    })
                return self.response(debug=True)

        # Default: add the assistant's text response
        self._context.append({"role": "assistant", "content": response.output_text})
        if debug:
            print(f"[Assistant]: {response.output_text}")
        return response.output_text
    