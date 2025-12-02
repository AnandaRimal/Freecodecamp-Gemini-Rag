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
    "business": None,
    "science": None,
    "story": None
}

print("--- Initializing Static RAG ---")

# Upload files (check existing first)
print("Uploading files...")

# Get list of existing files
existing_files = {}
for file in client.files.list():
    existing_files[file.name] = file

# Business file
if 'files/businessbook' in existing_files:
    business_file = existing_files['files/businessbook']
    print(f"Found existing Business Book: {business_file.name}")
else:
    business_file = client.files.upload(file='businesszerotoone.pdf', config={'name':'businessbook'})
    print(f"Uploaded Business Book: {business_file.name}")

# Science file
if 'files/sciencebook' in existing_files:
    science_file = existing_files['files/sciencebook']
    print(f"Found existing Science Book: {science_file.name}")
else:
    science_file = client.files.upload(file='sciencebook.pdf', config={'name':'sciencebook'})
    print(f"Uploaded Science Book: {science_file.name}")

# Story file
if 'files/storybook' in existing_files:
    story_file = existing_files['files/storybook']
    print(f"Found existing Story Book: {story_file.name}")
else:
    story_file = client.files.upload(file='storyharry.pdf', config={'name':'storybook'})
    print(f"Uploaded Story Book: {story_file.name}")

# Create File Search Stores (with error handling for existing stores)
print("Creating file search stores...")

# List existing stores first
existing_stores = {}
for store in client.file_search_stores.list():
    existing_stores[store.display_name] = store

# Business Store
if 'Business Store' in existing_stores:
    business_store = existing_stores['Business Store']
    print(f"Found existing Business Store: {business_store.name}")
else:
    business_store = client.file_search_stores.create(config={'display_name': 'Business Store'})
    print(f"Created Business Store: {business_store.name}")

# Science Store
if 'Science Store' in existing_stores:
    science_store = existing_stores['Science Store']
    print(f"Found existing Science Store: {science_store.name}")
else:
    science_store = client.file_search_stores.create(config={'display_name': 'Science Store'})
    print(f"Created Science Store: {science_store.name}")

# Story Store
if 'Story Store' in existing_stores:
    story_store = existing_stores['Story Store']
    print(f"Found existing Story Store: {story_store.name}")
else:
    story_store = client.file_search_stores.create(config={'display_name': 'Story Store'})
    print(f"Created Story Store: {story_store.name}")

# Store IDs for chat endpoints
store_ids["business"] = business_store.name
store_ids["science"] = science_store.name
store_ids["story"] = story_store.name

# Import files into stores
print("Importing files into stores...")
op1 = client.file_search_stores.import_file(
    file_search_store_name=business_store.name,
    file_name=business_file.name
)

op2 = client.file_search_stores.import_file(
    file_search_store_name=science_store.name,
    file_name=science_file.name
)

op3 = client.file_search_stores.import_file(
    file_search_store_name=story_store.name,
    file_name=story_file.name
)

# Wait for all imports to complete
print("Waiting for imports to complete...")
operations = [op1, op2, op3]

for operation in operations:
    while not operation.done:
        time.sleep(2)
        operation = client.operations.get(operation)
    print(f"Import completed: {operation.name}")

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
                system_instruction="You are a helpful assistant. You have access to a knowledge base of documents. Always use the file_search tool to find relevant information to answer the user's question. If the answer is not found in the documents, say so.",
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
