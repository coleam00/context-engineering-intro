## FEATURE:

- Pydantic AI agent that has another Pydantic AI agent as a tool.
- Research Agent for the primary agent and then an email draft Agent for the subagent.
- CLI to interact with the agent.
- Gmail for the email draft agent, Brave API for the research agent.

## EXAMPLES:

Read `use-cases/pydantic-ai/README.md` for an overview of the Pydantic AI template and an example of how to structure your own README for the above feature.

- `use-cases/pydantic-ai/examples/main_agent_reference/cli.py` - use this as a reference for the CLI interaction pattern.
- `use-cases/pydantic-ai/examples/` - read the agent examples for patterns for configuring providers and LLMs, handling agent dependencies, and adding tools.

The root `examples/` folder is a placeholder for examples you add to your own project. The references above are under `use-cases/pydantic-ai/`.

Don't copy any of these examples directly, it is for a different project entirely. But use this as inspiration and for best practices.

## DOCUMENTATION:

Pydantic AI documentation: https://ai.pydantic.dev/

## OTHER CONSIDERATIONS:

- Include a .env.example, README with instructions for setup including how to configure Gmail and Brave.
- Include the project structure in the README.
- Virtual environment has already been set up with the necessary dependencies.
- Use python_dotenv and load_env() for environment variables
