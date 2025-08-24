## FEATURE:

- Create a Pydantic-based AI agent that uses another Pydantic agent as a tool.
- The primary agent is a Research Agent; the sub-agent is responsible for drafting emails.
- Provide a CLI interface to interact with the agents.
- Use Gmail integration for the email draft agent, and the Brave API for the research agent.

## EXAMPLES:

The `examples/` folder includes a `README.md` that explains the context of the provided examples and offers a template for structuring your own documentation.

- `examples/cli.py` – use this as a reference for implementing the CLI.
- `examples/agent/` – review all files in this directory to understand best practices for building Pydantic AI agents that support multiple providers and LLMs, manage agent dependencies, and register tools.

Note: These examples belong to a different project. Do not reuse them directly, but use them as inspiration and to guide best practices.

## DOCUMENTATION:

- [Pydantic AI Documentation](https://ai.pydantic.dev/)

## OTHER CONSIDERATIONS:

- Provide a `.env.example` file and a `README.md` with setup instructions, including configuration for Gmail and Brave.
- Document the project structure in the `README.md`.
- The virtual environment has already been configured with the necessary dependencies.
- Use the `python-dotenv` library and `load_env()` to manage environment variables.
