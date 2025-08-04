name: "Novel Structure Extractor - Phase 1 Implementation"
description: |

## Purpose
Implementation of an automated novel structure extraction system that analyzes existing novels to extract key structural elements, character information, and plot patterns using LLM technology with OpenAI-compatible APIs.

## Core Principles
1. **Context is King**: Manage LLM context windows effectively with dynamic loading
2. **Validation Loops**: Implement comprehensive testing for extraction accuracy
3. **Information Dense**: Extract maximum structural information from novels
4. **Progressive Success**: Start with basic extraction, validate, then enhance
5. **Global rules**: Follow all rules in CLAUDE.md for modularity and testing

---

## Goal
Build a robust novel structure extraction system (Phase 1) that:
- Reads existing novels and extracts structural information using LLMs
- Manages multiple settings files (global, background, characters, plot)
- Handles context length limitations intelligently
- Automatically compresses settings when they exceed thresholds
- Provides a clean CLI interface for all operations

## Why
- **Enables automated novel generation**: Extracted structures serve as templates for new novels
- **Preserves writing patterns**: Captures author style and narrative structures
- **Scalable analysis**: Can process multiple novels to build a knowledge base
- **Foundation for AI writing**: Provides structured data for AI novel generation

## What
A Python-based CLI tool that:
- Extracts novel structure using OpenAI-compatible LLM APIs
- Manages settings files with automatic compression
- Handles large novels with intelligent context management
- Provides progress tracking and error recovery

### Success Criteria
- [ ] Successfully extracts structure from a sample novel
- [ ] Settings files are generated and properly formatted
- [ ] Context length limits are respected
- [ ] Automatic compression works when thresholds exceeded
- [ ] All tests pass with >90% coverage
- [ ] CLI provides intuitive user experience

## All Needed Context

### Documentation & References
```yaml
# MUST READ - Include these in your context window
- url: https://platform.openai.com/docs/api-reference/chat/create
  why: OpenAI API format for LLM calls
  
- url: https://docs.pydantic.dev/latest/concepts/pydantic_settings/
  why: Configuration management with environment variables
  
- url: https://github.com/openai/tiktoken
  why: Token counting for OpenAI models
  
- file: use-cases/pydantic-ai/examples/main_agent_reference/settings.py
  why: Pattern for pydantic-settings with dotenv

- doc: https://click.palletsprojects.com/en/8.1.x/
  section: Commands and Groups
  critical: CLI structure and command organization
```

### Current Codebase tree
```bash
context-engineering-intro/
├── CLAUDE.md
├── INITIAL.md
├── PRPs/
│   └── novel_extractor_phase1.md
└── use-cases/
    └── pydantic-ai/
        └── examples/
```

### Desired Codebase tree with files
```bash
context-engineering-intro/
├── CLAUDE.md
├── INITIAL.md
├── PLANNING.md (project architecture overview)
├── TASK.md (task tracking)
├── README.md (setup and usage instructions)
├── .env.example (environment variables template)
├── requirements.txt (project dependencies)
├── novel_extractor/
│   ├── __init__.py
│   ├── __main__.py (CLI entry point)
│   ├── extractor.py (main extraction logic)
│   ├── llm_client.py (OpenAI-compatible LLM interface)
│   ├── settings_manager.py (manages settings files)
│   ├── context_manager.py (handles token counting and truncation)
│   └── prompts.py (system prompts for extraction)
├── config/
│   ├── __init__.py
│   └── settings.py (pydantic settings with env vars)
├── settings/ (directory for novel settings files)
│   ├── .gitkeep
│   └── global_settings.txt.example
├── tests/
│   ├── __init__.py
│   ├── conftest.py (pytest fixtures)
│   ├── test_extractor.py
│   ├── test_llm_client.py
│   ├── test_settings_manager.py
│   └── test_context_manager.py
├── novel_generator/ (placeholder for phase 2)
│   └── __init__.py
└── novel_writer/ (placeholder for phase 3)
    └── __init__.py
```

### Known Gotchas & Library Quirks
```python
# CRITICAL: tiktoken requires specific encoding for each model
# Example: gpt-4 uses "cl100k_base" encoding
# Example: Must handle tiktoken.model.UnsupportedModelError

# CRITICAL: OpenAI API has rate limits
# Example: Implement exponential backoff for retries
# Example: Handle openai.RateLimitError explicitly

# CRITICAL: File encoding issues with novels
# Example: Always use encoding='utf-8' when reading text files
# Example: Handle BOM (Byte Order Mark) in files

# CRITICAL: Context window management
# Example: GPT-4 has 8k tokens, GPT-4-32k has 32k tokens
# Example: Reserve tokens for response (typically 1000-2000)
```

## Implementation Blueprint

### Data models and structure

```python
# config/settings.py - Environment configuration
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator
from typing import Optional

class Settings(BaseSettings):
    # LLM Configuration
    llm_api_key: str = Field(..., description="API key for LLM provider")
    llm_provider: str = Field(default="openai", description="LLM provider name")
    llm_model: str = Field(default="gpt-4", description="Model to use")
    llm_base_url: str = Field(default="https://api.openai.com/v1")
    
    # Context Configuration
    max_context_length: int = Field(default=8192, description="Maximum context tokens")
    compression_threshold: float = Field(default=0.8, description="Compression trigger")
    reserved_response_tokens: int = Field(default=2000)
    
    # Retry Configuration
    max_retries: int = Field(default=3)
    retry_delay: float = Field(default=1.0)
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# novel_extractor/models.py - Data structures
from pydantic import BaseModel
from typing import List, Dict, Optional

class NovelMetadata(BaseModel):
    title: str
    author: Optional[str] = None
    word_count: int
    file_path: str

class Character(BaseModel):
    name: str
    description: str
    role: str  # protagonist, antagonist, supporting
    relationships: Dict[str, str]  # character_name -> relationship_type

class PlotPoint(BaseModel):
    chapter: int
    event: str
    significance: str
    characters_involved: List[str]

class NovelStructure(BaseModel):
    metadata: NovelMetadata
    theme: str
    setting: str
    timeline: str
    narrative_style: str
    point_of_view: str
```

### List of tasks to be completed

```yaml
Task 1:
CREATE config/settings.py:
  - IMPLEMENT pydantic-settings configuration
  - LOAD environment variables with python-dotenv
  - VALIDATE API keys and configuration values

Task 2:
CREATE novel_extractor/llm_client.py:
  - IMPLEMENT OpenAI-compatible client
  - ADD retry logic with exponential backoff
  - HANDLE rate limits and API errors gracefully

Task 3:
CREATE novel_extractor/context_manager.py:
  - IMPLEMENT token counting with tiktoken
  - ADD context window management
  - CREATE truncation strategies for long content

Task 4:
CREATE novel_extractor/settings_manager.py:
  - IMPLEMENT file I/O for settings files
  - ADD automatic backup before modifications
  - CREATE compression logic for long settings

Task 5:
CREATE novel_extractor/prompts.py:
  - DEFINE system prompts for extraction
  - CREATE task-specific prompts (background, characters, plot)
  - ADD prompt templates with placeholders

Task 6:
CREATE novel_extractor/extractor.py:
  - IMPLEMENT main extraction workflow
  - COORDINATE between components
  - ADD progress tracking and logging

Task 7:
CREATE novel_extractor/__main__.py:
  - IMPLEMENT CLI using click
  - ADD commands: init, extract, show, compress
  - HANDLE user input validation

Task 8:
CREATE tests for all modules:
  - WRITE unit tests with pytest
  - ADD integration tests
  - MOCK LLM API calls for testing
```

### Per task pseudocode

```python
# Task 2 - LLM Client
class LLMClient:
    def __init__(self, settings: Settings):
        self.api_key = settings.llm_api_key
        self.model = settings.llm_model
        self.base_url = settings.llm_base_url
        self.max_retries = settings.max_retries
        
    async def generate(self, messages: List[Dict], **kwargs) -> str:
        # PATTERN: Retry with exponential backoff
        for attempt in range(self.max_retries):
            try:
                # CRITICAL: Use httpx for async requests
                response = await self._make_request(messages, **kwargs)
                return response.choices[0].message.content
            except RateLimitError:
                # GOTCHA: OpenAI rate limits need exponential backoff
                await asyncio.sleep(2 ** attempt)
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise
                    
# Task 3 - Context Manager
class ContextManager:
    def __init__(self, model: str, max_tokens: int):
        # PATTERN: Model-specific tokenizer
        self.encoding = tiktoken.encoding_for_model(model)
        self.max_tokens = max_tokens
        self.reserved_tokens = 2000  # For response
        
    def fit_content(self, settings: Dict[str, str], novel_text: str) -> str:
        # CRITICAL: Always include settings first
        settings_tokens = self._count_tokens(settings)
        available = self.max_tokens - settings_tokens - self.reserved_tokens
        
        # PATTERN: Truncate novel from end if needed
        novel_tokens = self._count_tokens(novel_text)
        if novel_tokens > available:
            # Keep last N tokens (most recent content)
            truncated = self._truncate_to_tokens(novel_text, available)
            return f"{settings}\n\n{truncated}"
            
# Task 4 - Settings Manager  
class SettingsManager:
    def compress_settings(self, file_path: str, target_ratio: float = 0.7):
        # PATTERN: Backup before modification
        backup_path = f"{file_path}.backup"
        shutil.copy(file_path, backup_path)
        
        # CRITICAL: Use LLM to compress while preserving key info
        content = self.read_settings(file_path)
        compressed = await self.llm_client.generate([
            {"role": "system", "content": COMPRESSION_PROMPT},
            {"role": "user", "content": f"Compress to {target_ratio*100}% while keeping key information:\n{content}"}
        ])
        
        self.write_settings(file_path, compressed)
```

### Integration Points
```yaml
CLI:
  - entry point: novel_extractor/__main__.py
  - pattern: "if __name__ == '__main__': cli()"
  
SETTINGS:
  - location: settings/ directory
  - pattern: "Plain text files for LLM context"
  
CONFIG:
  - add to: .env file
  - pattern: "LLM_API_KEY=sk-..."
  
LOGGING:
  - use: Python logging module
  - pattern: "logger = logging.getLogger(__name__)"
```

## Validation Loop

### Level 1: Syntax & Style
```bash
# Run these FIRST - fix any errors before proceeding
python -m py_compile novel_extractor/*.py  # Syntax check
black novel_extractor/ tests/              # Format code
ruff check novel_extractor/ --fix          # Linting

# Expected: No errors. If errors, READ and fix.
```

### Level 2: Unit Tests
```python
# test_context_manager.py
def test_token_counting():
    """Correctly counts tokens"""
    manager = ContextManager("gpt-4", 8192)
    count = manager.count_tokens("Hello world")
    assert count == 2

def test_content_truncation():
    """Truncates content to fit context"""
    manager = ContextManager("gpt-4", 100)
    result = manager.fit_content(
        {"settings": "short"}, 
        "very " * 1000 + "long text"
    )
    assert manager.count_tokens(result) <= 100

def test_settings_compression():
    """Compresses settings files correctly"""
    manager = SettingsManager()
    original = "A" * 1000
    compressed = manager.compress_content(original, 0.5)
    assert len(compressed) < len(original) * 0.6
```

```bash
# Run and iterate until passing:
pytest tests/ -v --cov=novel_extractor --cov-report=term-missing
# Target: >90% coverage
```

### Level 3: Integration Test
```bash
# Create sample novel
echo "Chapter 1: The Beginning..." > sample_novel.txt

# Initialize settings
python -m novel_extractor init

# Extract structure
python -m novel_extractor extract sample_novel.txt --verbose

# Check generated files
ls -la settings/
cat settings/novel_background.txt

# Expected: All settings files created with content
```

## Final Validation Checklist
- [ ] All tests pass: `pytest tests/ -v`
- [ ] No linting errors: `ruff check novel_extractor/`
- [ ] No type errors: `mypy novel_extractor/`
- [ ] CLI works: `python -m novel_extractor --help`
- [ ] Extraction successful on sample novel
- [ ] Settings compression works when triggered
- [ ] Error messages are helpful and clear
- [ ] README.md includes setup instructions

---

## Anti-Patterns to Avoid
- ❌ Don't hardcode API keys - use environment variables
- ❌ Don't ignore token limits - always validate context size
- ❌ Don't skip error handling for API calls
- ❌ Don't load entire novel into memory at once for large files
- ❌ Don't modify settings files without backups
- ❌ Don't use synchronous I/O in async functions
- ❌ Don't forget to handle encoding issues in text files