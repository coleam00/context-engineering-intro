### 🔄 Project Awareness & Context
- **Always read `PLANNING.md`** at the start of a new conversation to understand the project's architecture, goals, style, and constraints.
- **Check `TASK.md`** before starting a new task. If the task isn't listed, add it with a brief description and today's date.
- **Use consistent naming conventions, file structure, and architecture patterns** as described in `PLANNING.md`.
- **Use venv_linux** (the virtual environment) whenever executing Python commands, including for unit tests.

### 🧱 Code Structure & Modularity
- **Never create a file longer than 500 lines of code.** If a file approaches this limit, refactor by splitting it into modules or helper files.
- **Organize code into clearly separated modules**, grouped by feature or responsibility.
  For the novel generation system:
    - `novel_extractor/` - Extracts structure from existing novels
      - `extractor.py` - Main extraction logic
      - `llm_client.py` - LLM interface with OpenAI-compatible API
      - `settings_manager.py` - Manages novel settings files
      - `context_manager.py` - Handles context length and compression
    - `novel_generator/` - Generates new novel structure (placeholder)
    - `novel_writer/` - Writes novel based on structure (placeholder)
    - `config/` - Global configuration and environment settings
    - `settings/` - Directory for novel setting files
- **Use clear, consistent imports** (prefer relative imports within packages).
- **Use python_dotenv and load_env()** for environment variables.

### 🧪 Testing & Reliability
- **Always create Pytest unit tests for new features** (functions, classes, routes, etc).
- **After updating any logic**, check whether existing unit tests need to be updated. If so, do it.
- **Tests should live in a `/tests` folder** mirroring the main app structure.
  - Include at least:
    - 1 test for expected use
    - 1 edge case
    - 1 failure case

### ✅ Task Completion
- **Mark completed tasks in `TASK.md`** immediately after finishing them.
- Add new sub-tasks or TODOs discovered during development to `TASK.md` under a "Discovered During Work" section.

### 📎 Style & Conventions
- **Use Python** as the primary language.
- **Follow PEP8**, use type hints, and format with `black`.
- **Use `pydantic` for data validation** - especially for configuration and settings models.
- **Use `pydantic-settings` for environment variable management**.
- Write **docstrings for every function** using the Google style:
  ```python
  def example():
      """
      Brief summary.

      Args:
          param1 (type): Description.

      Returns:
          type: Description.
      """
  ```

### 📚 Novel Generation Specific Conventions
- **Settings File Management**:
  - Global novel settings (read-only, user-filled): `settings/global_settings.txt`
  - Novel background (LLM-generated): `settings/novel_background.txt`
  - Character settings (LLM-generated): `settings/character_settings.txt`
  - Plot settings (LLM-generated): `settings/plot_settings.txt`
- **Context Management**:
  - Always check context length before adding content to LLM calls
  - Implement automatic compression when settings files exceed length limits
  - Prioritize global settings and most recent content when truncating
- **LLM Integration**:
  - Use OpenAI-compatible API format for flexibility
  - Support multiple providers through configuration
  - Implement proper error handling and retry logic

### 📚 Documentation & Explainability
- **Update `README.md`** when new features are added, dependencies change, or setup steps are modified.
- **Comment non-obvious code** and ensure everything is understandable to a mid-level developer.
- When writing complex logic, **add an inline `# Reason:` comment** explaining the why, not just the what.

### 🧠 AI Behavior Rules
- **Never assume missing context. Ask questions if uncertain.**
- **Never hallucinate libraries or functions** – only use known, verified Python packages.
- **Always confirm file paths and module names** exist before referencing them in code or tests.
- **Never delete or overwrite existing code** unless explicitly instructed to or if part of a task from `TASK.md`.

### 🔧 Important Libraries for Novel Generation
- **openai** - For LLM API calls (OpenAI-compatible)
- **pydantic** & **pydantic-settings** - For configuration and data validation
- **python-dotenv** - For environment variable management
- **tiktoken** or similar - For token counting and context management
- **rich** or **click** - For CLI interface
- **asyncio** - For asynchronous LLM calls when needed