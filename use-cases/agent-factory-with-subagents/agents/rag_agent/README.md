# 🔍 Semantic Search Agent

An intelligent knowledge base search system powered by Pydantic AI and PostgreSQL with PGVector. This agent provides both semantic and hybrid search capabilities with automatic strategy selection and result summarization.

## Features

- **Semantic Search**: Pure vector similarity search using embeddings
- **Hybrid Search**: Combined semantic and keyword matching for precise results
- **Intelligent Strategy Selection**: Agent automatically chooses the best search approach
- **Result Summarization**: Coherent insights generated from search results
- **Interactive CLI**: Rich command-line interface with real-time streaming
- **Multi-Provider Support**: Works with any OpenAI-compatible API (OpenAI, Gemini, Ollama, etc.)

## Prerequisites

- Python 3.10+
- PostgreSQL with PGVector extension
- LLM API key (OpenAI, Gemini, Ollama, Groq, or any OpenAI-compatible provider)
- Existing database with documents and chunks (schema provided)

## Installation

1. **Clone or copy the agent directory**:
```bash
cd agents/rag_agent
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up PostgreSQL with PGVector**:
```bash
# SIMPLEST: Run the SQL in your SQL editor if you are using a platform like Supabase/Postgres

# Or run the schema with psql
psql -d your_database -f sql/schema.sql
```

4. **Configure environment variables**:
```bash
cp .env.example .env
# Edit .env with your credentials
```

5. **Ingest documents into the database**:
```bash
# This step is required before running the agent
# It will process documents and generate embeddings
python -m ingestion.ingest --documents documents/
```

## Configuration

### Required Environment Variables

- `DATABASE_URL`: PostgreSQL connection string with PGVector
- `LLM_PROVIDER`: Provider name (openai, anthropic, ollama, etc.)
- `LLM_API_KEY`: Your LLM provider API key
- `LLM_MODEL`: Model to use (e.g., gpt-4.1-mini, gemini-2.5-flash)
- `LLM_BASE_URL`: API base URL (default: https://api.openai.com/v1)
- `EMBEDDING_MODEL`: Embedding model to use (e.g., text-embedding-3-small, text-embedding-3-large)

## Usage

### Command Line Interface

Run the interactive CLI:
```bash
python -m cli
```

The CLI provides:
- Real-time streaming responses
- Tool execution visibility
- Session persistence
- User preference management

### Available Commands

- `help` - Show available commands
- `info` - Display system configuration
- `clear` - Clear the screen
- `set <key>=<value>` - Set preferences (e.g., `set text_weight=0.5`)
- `exit/quit` - Exit the application

## Search Strategies

The agent intelligently selects between two search strategies:

### Semantic Search
Best for conceptual queries and finding related content:
- "concepts similar to machine learning"
- "ideas about artificial intelligence"
- "related to neural networks"

### Hybrid Search
Best for specific facts and technical terms:
- "OpenAI GPT-4 specifications"
- "NASDAQ:NVDA stock price"
- "specific quote from Sam Altman"

The agent automatically chooses the appropriate strategy based on your query, or you can explicitly request a specific search type in your prompt.

## Database Setup

### Schema Overview

- **documents**: Stores full documents with metadata
- **chunks**: Stores document chunks with embeddings
- **match_chunks()**: Function for semantic search
- **hybrid_search()**: Function for combined search

## Development

### Running Tests
```bash
pytest tests/
```

### Code Formatting
```bash
black .
ruff check .
```

### Project Structure
```
semantic_search_agent/
├── agent.py           # Main agent implementation
├── cli.py            # Command-line interface
├── dependencies.py   # Agent dependencies
├── providers.py      # Model providers
├── prompts.py        # System prompts
├── settings.py       # Configuration
├── tools.py          # Search tools
├── ingestion/        # Document ingestion pipeline
├── sql/              # Database schema
└── documents/        # Sample documents
```
