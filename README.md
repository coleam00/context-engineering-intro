# Novel Extractor

An AI-powered tool that extracts structural elements from existing novels using Large Language Models.

## Features

- **Automated Structure Extraction**: Analyzes novels to extract characters, plot, themes, and writing style
- **Context Management**: Intelligently handles LLM context windows with automatic compression
- **Multi-Provider Support**: Works with any OpenAI-compatible API
- **Settings Management**: Maintains structured settings files for novel generation
- **CLI Interface**: Simple command-line interface for all operations

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd context-engineering-intro
```

2. Create a virtual environment:
```bash
# Linux/Mac
python -m venv venv_linux
source venv_linux/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API key and configuration
```

## Usage

### Initialize Settings
```bash
python -m novel_extractor init
```

### Extract Novel Structure
```bash
python -m novel_extractor extract path/to/novel.txt
```

### Show Current Settings
```bash
python -m novel_extractor show
```

### Compress Settings Files
```bash
python -m novel_extractor compress --threshold 0.8
```

## Configuration

Configure the following in your `.env` file:

```env
LLM_API_KEY=your-api-key-here
LLM_PROVIDER=openai
LLM_MODEL=gpt-4
LLM_BASE_URL=https://api.openai.com/v1
MAX_CONTEXT_LENGTH=8192
COMPRESSION_THRESHOLD=0.8
```

## Project Structure

```
novel_extractor/      # Main extraction module
├── extractor.py      # Core extraction logic
├── llm_client.py     # LLM API interface
├── settings_manager.py # Settings file management
└── context_manager.py  # Context window management

settings/             # Novel settings files
├── global_settings.txt    # User-defined settings
├── novel_background.txt   # Extracted background
├── character_settings.txt # Character profiles
└── plot_settings.txt      # Plot structure

tests/                # Test suite
└── test_*.py         # Unit tests
```

## Development

### Running Tests
```bash
pytest tests/ -v --cov=novel_extractor
```

### Code Formatting
```bash
black novel_extractor/ tests/
```

### Linting
```bash
ruff check novel_extractor/ --fix
```

## License

[License information]