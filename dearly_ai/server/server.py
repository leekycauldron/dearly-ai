from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dearly_ai import Client
import uvicorn
import os


class ServerClient():
    def __init__(self) -> None:
        self.client = None


app = FastAPI()
client = ServerClient()


class UserMessage(BaseModel):
            message: str


class AIResponse(BaseModel):
    response: str


@app.get("/")
def read_root():
    # Get the directory where this module is located
    module_dir = os.path.dirname(os.path.abspath(__file__))
    public_dir = os.path.join(module_dir, "public")
    index_path = os.path.join(public_dir, "index.html")
    
    return FileResponse(index_path)

@app.post("/chat", response_model=AIResponse)
def chat_with_ai(user_message: UserMessage):
    """
    Endpoint to chat with the AI art designer.
    Takes a user message and returns an AI response.
    """
    try:
        # Get response from the AI
        ai_response = client.client.response(user_message.message)
        
        return AIResponse(response=ai_response)
    
    except Exception as e:
        return AIResponse(response=f"Error: {str(e)}")


def serve(key):
    client.client = Client(key)
    # Run the server (no reload with class approach)
    uvicorn.run("dearly_ai.server.server:app", host="127.0.0.1", port=8000, reload=False)


