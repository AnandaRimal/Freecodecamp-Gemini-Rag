# Gemini RAG Multi-Store Chat Application

A comprehensive guide to building a Retrieval-Augmented Generation (RAG) system using Google's Gemini File Search API, featuring a practical multi-store implementation.

---

## 📖 Table of Contents

1. [Understanding the Architecture](#-understanding-the-architecture)
2. [Implementation Guide (Code)](#-implementation-guide-code)
3. [Cost Analysis & Comparison](#-cost-analysis--comparison)
4. [The Project: Multi-Store RAG System](#-the-project-multi-store-rag-system)
5. [Getting Started](#-getting-started)
6. [API Documentation](#-api-documentation)

---

## 🏗️ Understanding the Architecture

### How Gemini File Search Works

![Gemini File Search Architecture](File-search%20(2).png)

The Gemini File Search system operates in two distinct phases: **Indexing** (preparing your documents) and **Querying** (retrieving information).

### Phase 1: Indexing (Preparation)

Before you can query your documents, they must be indexed. This is a one-time setup process:

1. **Document Upload**: You upload your files (PDFs, text files, etc.) to Google's infrastructure using the Gemini API.
2. **Automatic Chunking**: Gemini intelligently splits your documents into smaller chunks (segments of text). You can customize the chunk size (100-500 tokens) and overlap.
3. **Embedding Generation**: Each chunk is converted into a vector embedding (a mathematical representation of the text's meaning).
4. **Store Creation**: These embeddings are stored in a **File Search Store** - a managed vector database that enables semantic search.

**Key Point**: This indexing process happens once per document. You pay a one-time fee ($0.15 per 1M tokens) and then the indexed data is stored for free.

### Phase 2: Querying (Retrieval & Generation)

When a user asks a question, the system performs the following steps:

1. **User Query**: The user submits a question through your application interface.
2. **File Search Tool Invocation**: Your application sends the query to the Gemini API with the `file_search` tool enabled, pointing to specific File Search Stores.
3. **Vector Store Lookup**: Gemini identifies the relevant store(s) (e.g., "Business Store" or "Science Store").
4. **Semantic Retrieval**: The system performs a semantic search to find the most relevant chunks based on meaning (not just keywords).
5. **Context-Aware Generation**: The retrieved chunks are passed to the Gemini model (e.g., Gemini 2.5 Flash) as context, and the model generates a precise, grounded answer based *only* on the provided information.

**Key Point**: During querying, you only pay for the model's input/output tokens. The embedding generation and vector search are free.

---

## 💻 Implementation Guide (Code)

This section provides step-by-step code examples for implementing Gemini File Search. You can find these examples in `backend/notebook.ipynb`.

### Step 1: Setup and Initialization

First, install the required package and initialize the Gemini client:

```bash
pip install google-generativeai python-dotenv
```

```python
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
```

### Step 2: Upload Documents

Upload your documents to Google's infrastructure:

```python
# Upload a PDF document
file = client.files.upload(
    file='businesszerotoone.pdf',
    config={'name': 'business_book'}
)
print(f"Uploaded: {file.name}")
# Output: Uploaded: files/business_book
```

### Step 3: Create a File Search Store

Create a logical container (store) for your documents:

```python
store = client.file_search_stores.create(
    config={'display_name': 'Business Knowledge Base'}
)
print(f"Store ID: {store.name}")
# Output: Store ID: fileSearchStores/business-abc123xyz
```

### Step 4: Import Files into Store

Link your uploaded file to the store. This triggers the indexing process:

```python
import time

# Import file into the store
import_operation = client.file_search_stores.import_file(
    file_search_store_name=store.name,
    file_name=file.name
)

# Wait for indexing to complete
while not import_operation.done:
    time.sleep(2)
    import_operation = client.operations.get(import_operation)

print("Indexing completed!")
```

### Step 5: Query the Store

Now you can ask questions about your documents:

```python
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="What is the main concept of Zero to One?",
    config={
        'system_instruction': 'You are a helpful assistant. Use the file_search tool to find relevant information.',
        'tools': [{
            'file_search': {
                'file_search_store_names': [store.name]
            }
        }]
    }
)

print(response.text)
# Output: According to the document, the main concept of "Zero to One" is...
```

### Custom Chunking (Optional)

For advanced use cases, you can customize how documents are chunked:

```python
# Note: Custom chunking configuration varies by API version
# Typical parameters:
# - max_tokens_per_chunk: 100-500 tokens
# - max_overlap_tokens: 20-100 tokens
```

---

## 💰 Cost Analysis & Comparison

### Gemini File Search Pricing

| Component | Cost | Details |
| :--- | :--- | :--- |
| **Storage** | **FREE** | Up to 1GB of vector storage included |
| **Indexing** | **$0.15 / 1M tokens** | One-time fee when processing documents |
| **Query Embeddings** | **FREE** | No cost for embedding generation during queries |
| **Model Usage** | **Standard Rates** | Gemini 2.5 Flash: ~$0.075/1M input tokens, ~$0.30/1M output tokens |
| **Context Caching** | **FREE** | Automatic caching for frequently accessed context |

### Traditional RAG vs. Gemini File Search

| Aspect | Traditional RAG | Gemini File Search | Winner |
| :--- | :--- | :--- | :--- |
| **Infrastructure** | Self-managed (Pinecone, Weaviate, Qdrant) | Fully managed by Google | ✅ Gemini |
| **Chunking** | Manual implementation required | Automatic + customizable | ✅ Gemini |
| **Embeddings** | Pay per generation (query + index) | Pay once (index only) | ✅ Gemini |
| **Vector DB Costs** | $70-200+/month | Free (up to 1GB) | ✅ Gemini |
| **Maintenance** | High (updates, scaling, monitoring) | Zero | ✅ Gemini |
| **Flexibility** | Full control over pipeline | Limited to Gemini's implementation | ✅ Traditional |
| **Custom Models** | Can use any embedding model | Locked to Gemini embeddings | ✅ Traditional |
| **Data Privacy** | Self-hosted options available | Data sent to Google | ✅ Traditional |

### Advantages of Gemini File Search

✅ **Serverless & Managed**: No infrastructure to maintain  
✅ **Cost-Effective**: Free storage, free query embeddings, pay-once indexing  
✅ **Fast Setup**: Production-ready in minutes  
✅ **Automatic Optimization**: Google handles chunking and embedding strategies  
✅ **Scalability**: Built on Google's infrastructure  
✅ **Integrated**: Works seamlessly with Gemini models  

### Disadvantages of Gemini File Search

❌ **Vendor Lock-in**: Tied to Google's ecosystem  
❌ **Limited Customization**: Cannot use custom embedding models  
❌ **Data Privacy**: Documents stored on Google's servers  
❌ **Pricing Uncertainty**: Future pricing changes possible  
❌ **API Limitations**: Subject to rate limits and quotas  
❌ **Black Box**: Less control over retrieval algorithms  

### Cost Example: 1000 Documents (500 pages each)

**Traditional RAG:**
- Vector DB: $100/month (Pinecone)
- Embeddings: $50/month (OpenAI)
- Compute: $30/month
- **Total: $180/month = $2,160/year**

**Gemini File Search:**
- Indexing: $75 (one-time)
- Storage: $0 (under 1GB)
- Queries: ~$20/month (model usage)
- **Total: $75 + $240/year = $315/year**

**Savings: ~$1,845/year (85% reduction)**

---

## 🚀 The Project: Multi-Store RAG System

This repository demonstrates a production-ready implementation of Gemini File Search with a modern full-stack architecture.

### Project Overview

We've built a **Multi-Store Chat Application** that allows users to query three different knowledge domains:
- **Business Store**: Contains business strategy documents (e.g., "Zero to One")
- **Science Store**: Contains scientific knowledge
- **Story Store**: Contains fiction/narrative content (e.g., Harry Potter)

Users can query individual stores or search across all stores simultaneously.

### Backend Architecture (`backend/`)

Built with **FastAPI**, the backend serves as the bridge between the frontend and Gemini API.

**File: `main.py`**

```python
# Key features:
# 1. Static Store IDs: Uses pre-configured stores from .env
# 2. Multiple Endpoints: Separate routes for each knowledge domain
# 3. Unified Search: /chat/all endpoint queries all stores
```

**How it works:**
1. **Initialization**: Loads store IDs from environment variables (no file uploads on startup)
2. **Request Handling**: Receives user queries via POST requests
3. **Gemini Integration**: Forwards queries to Gemini with the appropriate File Search store(s)
4. **Response Streaming**: Returns AI-generated responses to the frontend

**Endpoints:**
- `/chat/business` - Query business knowledge
- `/chat/science` - Query science knowledge  
- `/chat/story` - Query story knowledge
- `/chat/all` - Query all stores simultaneously

### Frontend Architecture (`frontend/`)

Built with **React 19** and **Vite**, featuring a premium glassmorphism UI.

**Key Components:**

1. **`App.jsx`**: Main application with tab-based store selection
2. **`ChatWindow.jsx`**: Real-time chat interface with markdown rendering
3. **`api.js`**: Axios-based API client for backend communication

**Features:**
- 🎨 **Glassmorphism Design**: Modern blur effects and gradients
- 💬 **Real-time Chat**: Instant responses with markdown formatting
- 📱 **Responsive**: Works on desktop, tablet, and mobile
- 🎯 **Store Switching**: Easy toggle between knowledge domains

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Node.js 18+
- Google API Key ([Get one here](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Freecodecamp-Gemini-Rag.git
   cd Freecodecamp-Gemini-Rag
   ```

2. **Backend Setup**
   ```bash
   cd backend
   pip install fastapi google-generativeai python-dotenv uvicorn
   
   # Create .env file
   echo 'GOOGLE_API_KEY="your-api-key"' > ../.env
   echo 'businessstore="fileSearchStores/business-xxx"' >> ../.env
   echo 'sciencestore="fileSearchStores/science-xxx"' >> ../.env
   echo 'storystore="fileSearchStores/story-xxx"' >> ../.env
   
   python main.py
   ```

3. **Frontend Setup**
   ```bash
   cd ../frontend
   npm install
   npm run dev
   ```

4. **Access the Application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000

---

## 📡 API Documentation

### Endpoints

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/chat/business` | POST | Query Business knowledge store |
| `/chat/science` | POST | Query Science knowledge store |
| `/chat/story` | POST | Query Story knowledge store |
| `/chat/all` | POST | Query all stores simultaneously |

### Request Format

```json
{
  "message": "What is a monopoly business?"
}
```

### Response Format

```json
{
  "response": "According to the document, a monopoly business is..."
}
```

### Example cURL Request

```bash
curl -X POST http://localhost:8000/chat/business \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the main idea of Zero to One?"}'
```

---

## 📝 License

MIT License - Free to use for learning and development

## 🤝 Contributing

Contributions welcome! Please submit a Pull Request.

---

**Built with ❤️ using Google Gemini File Search API**
