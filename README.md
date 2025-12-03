# Gemini RAG Multi-Store Chat Application

A powerful Retrieval-Augmented Generation (RAG) chat application demonstrating the capabilities of Google's Gemini File Search API with multiple specialized knowledge stores.

---

## 📖 Table of Contents

1. [Understanding Gemini File Search](#-understanding-gemini-file-search)
2. [Advanced Capabilities](#-advanced-capabilities)
3. [Cost Analysis](#-cost-analysis)
4. [About This Project](#-about-this-project)
5. [Getting Started](#-getting-started)
6. [Usage](#-usage)
7. [API Documentation](#-api-documentation)
8. [Project Structure](#-project-structure)
9. [Configuration](#-configuration)

---

## 🧠 Understanding Gemini File Search

### What is Gemini File Search?

**Gemini File Search** is a powerful feature of Google's Gemini AI that enables intelligent document search and retrieval. It allows you to upload documents (PDFs, text files, etc.) and then ask questions about their content using natural language.

### How Does It Work?

![Gemini File Search Architecture](File-search%20(2).png)

As illustrated above, the workflow involves:

1.  **User Query**: The user asks a question via the frontend.
2.  **File Search Tool**: The query is sent to the Gemini API, which utilizes the File Search tool.
3.  **Vector Store**: Gemini searches the relevant vector store (e.g., Business, Science) where documents are indexed.
4.  **Retrieval**: Relevant chunks of text are retrieved based on semantic similarity.
5.  **Generation**: The Gemini model generates a response using the retrieved chunks as context.

### Why Use File Search?

| Feature | Traditional RAG | Gemini File Search |
| :--- | :--- | :--- |
| **Chunking** | Manual strategy required (fixed size, semantic, etc.) | ✅ **Automatic & Intelligent** (or Custom) |
| **Embeddings** | Must choose and manage embedding models | ✅ **Built-in & Managed** |
| **Vector DB** | Requires setup (Pinecone, Milvus, etc.) | ✅ **Fully Managed Storage** |
| **Retrieval** | Complex logic to implement | ✅ **Integrated & Optimized** |
| **Scalability** | Hard to scale infrastructure | ✅ **Google-scale Infrastructure** |
| **Cost** | Pay for DB + Compute + Embeddings | ✅ **Pay only for Indexing & Generation** |

---

## 🚀 Advanced Capabilities

### Custom Chunking

While Gemini handles chunking automatically, you can fine-tune it for specific needs. This is crucial for optimizing retrieval accuracy.

**How it works:**
- **Max Tokens per Chunk**: Controls the size of each text segment.
- **Overlap**: Ensures context isn't lost between chunks.

**Example Configuration:**
```python
chunking_config = {
    "chunk_size": 500,  # Max tokens per chunk (100-500)
    "chunk_overlap": 100 # Tokens of overlap
}
```

**Advantages:**
- **Precision**: Smaller chunks for precise fact retrieval.
- **Context**: Larger chunks for broader thematic understanding.

### Large Document Handling

Gemini File Search is designed for scale:
- **High Capacity**: Supports millions of tokens per store.
- **Parallel Processing**: Upload and index multiple files simultaneously.
- **Smart Filtering**: Filter search results by metadata (e.g., file name, date).

---

## 💰 Cost Analysis

Gemini File Search offers a highly competitive pricing model, especially for read-heavy applications.

| Component | Cost | Notes |
| :--- | :--- | :--- |
| **Storage** | **FREE** | Up to 1GB of vector storage is free. |
| **Indexing** | **$0.15 / 1M tokens** | One-time cost when you upload/index a file. |
| **Querying** | **Standard Model Rates** | You pay for the input/output tokens of the model (e.g., Gemini 1.5 Flash). |
| **Cache** | **FREE** | Context caching for frequently used files is automatic and free. |

**Why this is cheaper:**
- No monthly vector database fees.
- No separate cost for embedding generation during queries.
- You only pay once to index your knowledge base.

---

## 🚀 About This Project

This project is a **practical demonstration** of Gemini File Search capabilities, implementing a multi-store RAG system with a modern web interface.

### 🌟 Features

- **Multi-Store Architecture**: Three specialized knowledge bases (Business, Science, Story)
- **Unified Search**: Query all stores simultaneously or search individual domains
- **Real-time Chat**: Interactive chat interface with markdown-formatted responses
- **Pre-indexed Knowledge**: Uses pre-configured Gemini File Search stores for instant queries
- **Modern UI**: Beautiful, responsive React frontend with glassmorphism design
- **RESTful API**: Clean FastAPI backend with CORS support

### 🏗️ System Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────────────┐
│   React     │─────▶│   FastAPI    │─────▶│   Gemini File       │
│   Frontend  │      │   Backend    │      │   Search Stores     │
│             │◀─────│              │◀─────│                     │
│  (Vite)     │      │  (Python)    │      │  - Business Store   │
│             │      │              │      │  - Science Store    │
│             │      │              │      │  - Story Store      │
└─────────────┘      └──────────────┘      └─────────────────────┘
```

### 📚 Tech Stack

**Backend**
- FastAPI - Modern Python web framework
- Google Generative AI - Gemini 2.5 Flash model
- Python-dotenv - Environment variable management
- Uvicorn - ASGI server

**Frontend**
- React 19 - UI library
- Vite - Build tool and dev server
- Axios - HTTP client
- React Markdown - Markdown rendering

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+**
- **Node.js 18+** and npm
- **Google AI API Key** ([Get it here](https://makersuite.google.com/app/apikey))
- **Pre-created Gemini File Search Stores** with indexed documents

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Freecodecamp-Gemini-Rag.git
   cd Freecodecamp-Gemini-Rag
   ```

2. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   GOOGLE_API_KEY="your-google-api-key-here"
   businessstore="fileSearchStores/business-XXXXXXXXXX"
   sciencestore="fileSearchStores/science-XXXXXXXXXX"
   storystore="fileSearchStores/story-XXXXXXXXXX"
   ```

3. **Install backend dependencies**
   ```bash
   cd backend
   pip install fastapi google-generativeai python-dotenv uvicorn
   ```

4. **Install frontend dependencies**
   ```bash
   cd ../frontend
   npm install
   ```

### Setting Up Your File Search Stores

If you need to create your own stores (instead of using pre-created ones):

```python
from google import genai
import os

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# Upload documents
business_file = client.files.upload(file='businesszerotoone.pdf')
science_file = client.files.upload(file='sciencebook.pdf')
story_file = client.files.upload(file='storyharry.pdf')

# Create stores
business_store = client.file_search_stores.create(
    config={'display_name': 'Business Store'}
)
science_store = client.file_search_stores.create(
    config={'display_name': 'Science Store'}
)
story_store = client.file_search_stores.create(
    config={'display_name': 'Story Store'}
)

# Import files into stores
client.file_search_stores.import_file(
    file_search_store_name=business_store.name,
    file_name=business_file.name
)
# ... repeat for other stores

# Copy the store IDs to your .env file
print(f"businessstore=\"{business_store.name}\"")
print(f"sciencestore=\"{science_store.name}\"")
print(f"storystore=\"{story_store.name}\"")
```

---

## 🎯 Usage

### Starting the Backend

```bash
cd backend
python main.py
```

The API server will start on `http://localhost:8000`

### Starting the Frontend

```bash
cd frontend
npm run dev
```

The frontend will start on `http://localhost:5173`

### Using the Application

1. Open your browser and navigate to `http://localhost:5173`
2. Select a knowledge store tab:
   - **Business** - Ask about business strategies, entrepreneurship
   - **Science** - Query scientific concepts and facts
   - **Story** - Questions about story plots and characters
   - **All Stores** - Search across all domains simultaneously
3. Type your question in the chat input
4. Receive AI-generated responses grounded in the indexed documents

---

## 📡 API Documentation

### Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/chat/business` | POST | Chat with Business knowledge store |
| `/chat/science` | POST | Chat with Science knowledge store |
| `/chat/story` | POST | Chat with Story knowledge store |
| `/chat/all` | POST | Chat with all stores simultaneously |

### Request Format

```json
{
  "message": "What is the key idea in Zero to One?"
}
```

### Response Format

```json
{
  "response": "According to the document, the key idea is..."
}
```

### Example cURL Request

```bash
curl -X POST http://localhost:8000/chat/business \
  -H "Content-Type: application/json" \
  -d '{"message": "What is a monopoly business?"}'
```

---

## 📂 Project Structure

```
Freecodecamp-Gemini-Rag/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── notebook.ipynb          # Gemini File Search exploration
│   ├── businesszerotoone.pdf   # Business knowledge document
│   ├── sciencebook.pdf         # Science knowledge document
│   └── storyharry.pdf          # Story knowledge document
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChatWindow.jsx  # Chat interface component
│   │   │   └── ChatWindow.css  # Chat styling
│   │   ├── App.jsx             # Main application
│   │   ├── App.css             # Main styling
│   │   ├── api.js              # API client
│   │   ├── index.css           # Global styles
│   │   └── main.jsx            # Entry point
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
├── .env                        # Environment variables
└── README.md
```

---

## 🔧 Configuration

### Backend Configuration

The backend uses static store IDs from environment variables for instant startup.

**Key Points:**
- Model: `gemini-2.5-flash`
- System Instruction: Always use file_search tool for document-grounded answers
- CORS: Enabled for all origins (configure for production)
- Port: 8000

### Frontend Configuration

**Key Points:**
- API Base URL: `http://localhost:8000`
- Dev Server Port: 5173
- Build Output: `dist/`

---

## 🐛 Troubleshooting

### Frontend Build Errors

```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Backend Issues

- Verify `.env` file exists in root directory
- Ensure store IDs are valid and accessible
- Check Google API key permissions

### CORS Errors

Update API base URL in `frontend/src/api.js` if needed.

---

## 📝 License

MIT License - free to use for learning and development

## 🤝 Contributing

Contributions welcome! Please submit a Pull Request.

---

**Built with ❤️ using Google Gemini File Search API**
