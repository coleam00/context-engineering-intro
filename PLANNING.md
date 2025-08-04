# Novel Generation System - Project Architecture

## Overview
A three-phase AI-powered novel generation system that learns from existing novels to create new ones.

## Architecture Principles
1. **Modular Design**: Each phase (extraction, generation, writing) is a separate module
2. **Context-Aware**: Intelligent management of LLM context windows
3. **Settings-Driven**: Configuration and novel settings stored as plain text for LLM consumption
4. **API Agnostic**: Uses OpenAI-compatible APIs for flexibility across providers

## Project Structure
```
novel_extractor/     - Phase 1: Extracts structure from existing novels
novel_generator/     - Phase 2: Generates new novel structures
novel_writer/        - Phase 3: Writes novels based on structures
config/              - Global configuration and environment settings
settings/            - Novel-specific settings files
tests/               - Comprehensive test coverage
```

## Technology Stack
- **Language**: Python 3.8+
- **LLM Integration**: OpenAI-compatible APIs
- **Configuration**: pydantic-settings with dotenv
- **CLI**: Click framework
- **Testing**: Pytest with mocking
- **Context Management**: tiktoken for token counting

## Coding Standards
- PEP8 compliance with black formatting
- Type hints for all functions
- Google-style docstrings
- Maximum 500 lines per file
- Comprehensive error handling
- Unit tests for all features

## Phase 1: Novel Extractor
Analyzes existing novels to extract:
- Character profiles and relationships
- Plot structure and key events
- Writing style and narrative voice
- Themes and settings

## Phase 2: Novel Generator (Future)
Creates new novel structures by:
- Combining extracted patterns
- Generating unique character combinations
- Creating plot variations
- Maintaining stylistic consistency

## Phase 3: Novel Writer (Future)
Writes complete novels by:
- Following generated structures
- Maintaining character consistency
- Implementing plot progression
- Applying learned writing styles