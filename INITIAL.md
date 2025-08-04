## FEATURE:

Automated novel generation system with three-phase architecture:
1. **Extract existing novel structure and information** (Primary focus)
2. Generate new novel structure and information (Placeholder for future development)
3. Generate new novel based on structure (Placeholder for future development)

### Phase 1: Novel Structure Extraction Requirements

- **LLM Integration**: Use OpenAI-compatible API format for flexibility across providers
- **Global Environment Configuration**:
  - API source configuration (OpenAI, local models, etc.)
  - Model context length limits
  - Token counting and management
  - Retry logic and error handling
- **Settings File Management**:
  - Global novel settings (user-filled, read-only by LLM)
  - Novel background (LLM-generated/edited)
  - Character settings (LLM-generated/edited)
  - Plot settings (LLM-generated/edited)
  - All settings loaded as context for each LLM call
- **Context Management**:
  - Dynamic content loading based on model's context length
  - Load settings files first, then add existing novel content
  - Generate/update settings based on novel analysis
- **Automatic Compression**:
  - Monitor settings file lengths after each generation
  - Automatically compress content when exceeding thresholds
  - Preserve key information during compression

## EXAMPLES:

Example usage flow:
```bash
# Initialize project with global settings
python -m novel_extractor init

# Extract structure from existing novel
python -m novel_extractor extract path/to/novel.txt

# View extracted settings
python -m novel_extractor show settings

# Compress settings if needed
python -m novel_extractor compress --auto
```

Example settings structure:
- `settings/global_settings.txt` - User-defined novel parameters, themes, constraints
- `settings/novel_background.txt` - World-building, setting descriptions
- `settings/character_settings.txt` - Character profiles, relationships, development arcs
- `settings/plot_settings.txt` - Plot structure, key events, narrative threads

## DOCUMENTATION:

- OpenAI API Documentation: https://platform.openai.com/docs/api-reference
- Pydantic Settings: https://docs.pydantic.dev/latest/concepts/pydantic_settings/
- Token counting libraries:
  - tiktoken (OpenAI models): https://github.com/openai/tiktoken
  - transformers (for other models): https://huggingface.co/docs/transformers/
- Context management best practices for LLMs
- Prompt engineering for novel analysis

## OTHER CONSIDERATIONS:

- **Error Handling**: Robust error handling for API failures, rate limits, and token limits
- **Modularity**: Clean separation between extraction, generation, and writing phases
- **Extensibility**: Support for different LLM providers through configuration
- **Performance**: Asynchronous API calls when processing large novels
- **File Format Support**: Initially support .txt files, with future expansion to .epub, .pdf
- **Progress Tracking**: Show extraction progress for long novels
- **Validation**: Validate extracted settings for completeness and consistency
- **Backup**: Automatic backup of settings before compression
- **CLI Interface**: User-friendly command-line interface with rich formatting
- **.env Configuration**: Include .env.example with required variables:
  ```
  LLM_API_KEY=your_api_key_here
  LLM_PROVIDER=openai
  LLM_MODEL=gpt-4
  LLM_BASE_URL=https://api.openai.com/v1
  MAX_CONTEXT_LENGTH=8192
  COMPRESSION_THRESHOLD=0.8
  ```