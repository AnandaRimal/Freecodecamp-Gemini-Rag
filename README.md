# Gemini RAG Multi-Store Chat Application

A comprehensive guide to building a Retrieval-Augmented Generation (RAG) system using Google's Gemini File Search API, featuring a practical multi-store implementation.

---

## 📖 Table of Contents

1. [Visualizing the Architecture](#-visualizing-the-architecture)
2. [Implementation Guide (Notebook)](#-implementation-guide-notebook)
3. [Cost Analysis & Comparison](#-cost-analysis--comparison)
4. [The Project: Multi-Store RAG](#-the-project-multi-store-rag)
5. [Getting Started](#-getting-started)
6. [API Documentation](#-api-documentation)

---

## 🧠 Visualizing the Architecture

### How Gemini File Search Works

The following diagram illustrates the core workflow of the Gemini File Search system used in this project.

![Gemini File Search Architecture](File-search%20(2).png)

**Step-by-Step Explanation:**

1.  **User Query**: The process begins when a user submits a question through the interface.
2.  **File Search Tool**: The application forwards this query to the Gemini API, specifically invoking the **File Search Tool**.
3.  **Vector Store Lookup**: Gemini identifies the appropriate **File Search Store** (e.g., a "Business" or "Science" store) which acts as a managed vector database containing your indexed documents.
4.  **Semantic Retrieval**: The system performs a semantic search within the store to find the most relevant document chunks (text segments) that match the user's intent.
5.  **Context-Aware Generation**: These retrieved chunks are passed to the Gemini model (e.g., Gemini 1.5 Flash) as context. The model then generates a precise, grounded answer based *only* on the provided information.

---

## 💻 Implementation Guide (Notebook)

This section explains the code implementation for Gemini File Search, corresponding to the steps found in `backend/notebook.ipynb`.

### 1. Setup and Initialization

First, we initialize the Gemini client using the Google GenAI SDK.

```python
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
```

### 2. Uploading Documents

Documents are uploaded to Google's infrastructure. Gemini supports various formats like PDF, CSV, and TXT.

```python
# Upload a PDF document
file = client.files.upload(
    file='businesszerotoone.pdf',
    config={'name': 'business_book'}
)
print(f"Uploaded: {file.name}")
```

### 3. Creating a File Search Store

A "Store" is a logical container for your documents. Think of it as a collection or a folder that you can query against.

```python
store = client.file_search_stores.create(
    config={'display_name': 'Business Knowledge Base'}
)
```

### 4. Importing Files & Custom Chunking

This is where the magic happens. You link your uploaded file to the store. You can also define **Custom Chunking** strategies here to optimize retrieval.

*   **Max Tokens**: The maximum size of each text chunk (e.g., 500 tokens).
*   **Overlap**: The number of tokens that overlap between chunks to preserve context (e.g., 100 tokens).

```python
# Import file into the store
client.file_search_stores.import_file(
    file_search_store_name=store.name,
    file_name=file.name
)
```

### 5. Querying the Store

Finally, we ask a question. We configure the model to use the `file_search` tool and point it to our specific store.

```python
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="What is the main concept of Zero to One?",
    config={
        'tools': [{
            'file_search': {
                'file_search_store_names': [store.name]
            }
        }]
    }
)
print(response.text)
```

---

## 💰 Cost Analysis & Comparison

### Traditional RAG vs. Gemini File Search

| Feature | Traditional RAG | Gemini File Search |
| :--- | :--- | :--- |
| **Infrastructure** | Requires managing Vector DBs (Pinecone, Weaviate) | ✅ **Serverless & Fully Managed** |
| **Chunking** | Manual implementation required | ✅ **Automatic or Configurable** |
| **Embeddings** | Pay per embedding generation | ✅ **Included in Indexing** |
| **Maintenance** | High (updates, scaling, security) | ✅ **Zero Maintenance** |
| **Cost Model** | Monthly fees + Compute + Storage | ✅ **Pay-per-use (Indexing/Gen)** |

### Gemini Pricing Breakdown

Gemini File Search is highly cost-effective, especially for applications with static knowledge bases.

| Component | Cost | Details |
| :--- | :--- | :--- |
| **Storage** | **FREE** | Up to 1GB of vector storage is included for free. |
| **Indexing** | **$0.15 / 1M tokens** | One-time fee when you process/index a document. |
| **Querying** | **Standard Rates** | You pay standard input/output token rates for the model (e.g., Gemini 1.5 Flash). |
| **Context Cache** | **FREE** | Automatic caching for frequently accessed context. |

**Verdict**: For most use cases, Gemini File Search is significantly cheaper because you eliminate the recurring monthly costs of dedicated vector databases and the compute costs of generating embeddings for every query.

---

## 🚀 The Project: Multi-Store RAG

This repository contains a full-stack application that demonstrates these concepts in a real-world scenario.

### Project Overview

We have built a **Multi-Store Chat Application** that allows users to switch between different knowledge domains (Business, Science, Story).

### Backend (`backend/`)

Built with **FastAPI**, the backend acts as the bridge between the frontend and Gemini.

*   **`main.py`**: The core application file.
    *   **Static Initialization**: Instead of uploading files on every restart, it uses pre-configured Store IDs from the `.env` file for instant startup.
    *   **Endpoints**: Exposes specific endpoints (`/chat/business`, `/chat/science`, etc.) that route queries to the correct Gemini Store.

### Frontend (`frontend/`)

Built with **React 19** and **Vite**, the frontend provides a modern, responsive interface.

*   **Glassmorphism Design**: Features a premium UI with blur effects and gradients.
*   **Chat Interface**: A real-time chat window that supports Markdown rendering for rich text responses.
*   **Store Switching**: Users can easily toggle between different knowledge bases using tabs.

---

## 🚀 Getting Started

### Prerequisites

*   **Python 3.8+**
*   **Node.js 18+**
*   **Google API Key**

### Installation

1.  **Clone the repo**:
    ```bash
    git clone https://github.com/yourusername/Freecodecamp-Gemini-Rag.git
    ```

2.  **Backend Setup**:
    ```bash
    cd backend
    pip install -r requirements.txt
    # Create .env file with GOOGLE_API_KEY and Store IDs
    python main.py
    ```

3.  **Frontend Setup**:
    ```bash
    cd frontend
    npm install
    npm run dev
    ```

4.  **Access**: Open `http://localhost:5173` in your browser.

---

## 📡 API Documentation

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/chat/business` | `POST` | Query the Business Knowledge Base |
| `/chat/science` | `POST` | Query the Science Knowledge Base |
| `/chat/story` | `POST` | Query the Story Knowledge Base |
| `/chat/all` | `POST` | Query all stores simultaneously |

**Request Body:**
```json
{
  "message": "Your question here"
}
```

---

**Built with ❤️ using Google Gemini AI**
