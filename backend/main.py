import os
import time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()

# Global dictionary to hold Store IDs
store_ids = {
    "business": os.getenv("businessstore"),
    "science": os.getenv("sciencestore"),
    "story": os.getenv("storystore")
}

print("--- Initializing Static RAG ---")
print(f"Business Store ID: {store_ids['business']}")
print(f"Science Store ID: {store_ids['science']}")
print(f"Story Store ID: {store_ids['story']}")

print("--- Initialization Complete ---")

# Create FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

# Helper function
def chat_with_stores(prompt: str, store_names: list[str]):
    if not any(store_names):
        return {"response": "Stores not initialized."}

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction="You are a helpful assistant. You have access to a knowledge base of documents. Always use the file_search tool to find relevant information to answer the user's question. If the answer is not found in the documents, say no.",
                tools=[
                    types.Tool(
                        file_search=types.FileSearch(
                            file_search_store_names=store_names
                        )
                    )
                ]
            )
        )
        return {"response": response.text}
    except Exception as e:
        print(f"Error generating content: {e}")
        return {"response": f"Error generating response: {str(e)}"}

# Endpoints
@app.post("/chat/business")
async def chat_business(request: ChatRequest):
    return chat_with_stores(request.message, [store_ids["business"]])

@app.post("/chat/science")
async def chat_science(request: ChatRequest):
    return chat_with_stores(request.message, [store_ids["science"]])

@app.post("/chat/story")
async def chat_story(request: ChatRequest):
    return chat_with_stores(request.message, [store_ids["story"]])

@app.post("/chat/all")
async def chat_all(request: ChatRequest):
    return chat_with_stores(request.message, list(store_ids.values()))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
