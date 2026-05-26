#!/usr/bin/env python3
"""Command-line interface for Semantic Search Agent."""

import asyncio
import sys
import uuid
from typing import List

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markdown import Markdown

from pydantic_ai import Agent
from agent import search_agent
from dependencies import AgentDependencies
from settings import load_settings

console = Console()


async def stream_agent_interaction(user_input: str, conversation_history: List[str], deps: AgentDependencies) -> tuple[str, str]:
    """Stream agent interaction with real-time tool call display."""
    
    try:
        # Build context with conversation history
        context = "\n".join(conversation_history[-6:]) if conversation_history else ""
        
        prompt = f"""Previous conversation:
{context}

User: {user_input}

Search the knowledge base to answer the user's question. Choose the appropriate search strategy (semantic_search or hybrid_search) based on the query type. Provide a comprehensive summary of your findings."""

        # Stream the agent execution
        async with search_agent.iter(prompt, deps=deps) as run:
            
            response_text = ""
            
            async for node in run:
                
                # Handle user prompt node
                if Agent.is_user_prompt_node(node):
                    pass  # Clean start
                
                # Handle model request node - stream the thinking process
                elif Agent.is_model_request_node(node):
                    # Show assistant prefix at the start
                    console.print("[bold blue]Assistant:[/bold blue] ", end="")
                    
                    # Stream model request events for real-time text
                    async with node.stream(run.ctx) as request_stream:
                        async for event in request_stream:
                            event_type = type(event).__name__
                            
                            if event_type == "PartDeltaEvent":
                                # Extract content from delta
                                if hasattr(event, 'delta') and hasattr(event.delta, 'content_delta'):
                                    delta_text = event.delta.content_delta
                                    if delta_text:
                                        console.print(delta_text, end="")
                                        response_text += delta_text
                            elif event_type == "FinalResultEvent":
                                console.print()  # New line after streaming
                
                # Handle tool calls
                elif Agent.is_call_tools_node(node):
                    # Stream tool execution events
                    async with node.stream(run.ctx) as tool_stream:
                        async for event in tool_stream:
                            event_type = type(event).__name__
                            
                            if event_type == "FunctionToolCallEvent":
                                # Extract tool name from the part attribute
                                tool_name = "Unknown Tool"
                                args = None
                                
                                # Check if the part attribute contains the tool call
                                if hasattr(event, 'part'):
                                    part = event.part
                                    
                                    # Check if part has tool_name directly
                                    if hasattr(part, 'tool_name'):
                                        tool_name = part.tool_name
                                    elif hasattr(part, 'function_name'):
                                        tool_name = part.function_name
                                    elif hasattr(part, 'name'):
                                        tool_name = part.name
                                    
                                    # Check for arguments in part
                                    if hasattr(part, 'args'):
                                        args = part.args
                                    elif hasattr(part, 'arguments'):
                                        args = part.arguments
                                
                                console.print(f"  🔹 [cyan]Calling tool:[/cyan] [bold]{tool_name}[/bold]")
                                
                                # Show tool args if available
                                if args and isinstance(args, dict):
                                    # Show first few characters of each arg
                                    arg_preview = []
                                    for key, value in list(args.items())[:3]:
                                        val_str = str(value)
                                        if len(val_str) > 50:
                                            val_str = val_str[:47] + "..."
                                        arg_preview.append(f"{key}={val_str}")
                                    console.print(f"    [dim]Args: {', '.join(arg_preview)}[/dim]")
                                elif args:
                                    args_str = str(args)
                                    if len(args_str) > 100:
                                        args_str = args_str[:97] + "..."
                                    console.print(f"    [dim]Args: {args_str}[/dim]")
                            
                            elif event_type == "FunctionToolResultEvent":
                                # Display tool result - check different possible attributes
                                result = None
                                if hasattr(event, 'result'):
                                    result = str(event.result)
                                elif hasattr(event, 'return_value'):
                                    result = str(event.return_value)
                                elif hasattr(event, 'tool_return'):
                                    result = str(event.tool_return)
                                elif hasattr(event, 'part'):
                                    if hasattr(event.part, 'content'):
                                        result = str(event.part.content)
                                    else:
                                        result = str(event.part)
                                else:
                                    # Debug: show what attributes are available
                                    attrs = [attr for attr in dir(event) if not attr.startswith('_')]
                                    result = f"Unknown result structure. Attrs: {attrs[:5]}"
                                
                                if result and len(result) > 100:
                                    result = result[:97] + "..."
                                console.print(f"  ✅ [green]Tool result:[/green] [dim]{result}[/dim]")
                
                # Handle end node
                elif Agent.is_end_node(node):
                    pass  # Keep it clean
        
        # Get final result
        final_result = run.result
        final_output = final_result.output if hasattr(final_result, 'output') else str(final_result)
        
        # Return both streamed and final content
        return (response_text.strip(), final_output)
        
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        return ("", f"Error: {e}")


def display_welcome():
    """Display welcome message."""
    welcome = Panel(
        "[bold blue]Semantic Search Agent[/bold blue]\n\n"
        "[green]Intelligent knowledge base search with PGVector[/green]\n"
        "[dim]Type 'exit' to quit, 'help' for commands[/dim]",
        style="blue",
        padding=(1, 2)
    )
    console.print(welcome)
    console.print()


def display_help():
    """Display help information."""
    help_text = """
# Available Commands

- **exit/quit**: Exit the application
- **help**: Show this help message
- **clear**: Clear the screen
- **info**: Display system configuration
- **set <key>=<value>**: Set a preference (e.g., 'set text_weight=0.5')

# Search Tips

- For conceptual queries, the agent will use semantic search
- For specific facts or technical terms, the agent will use hybrid search
- You can explicitly request a search type in your query
    """
    console.print(Panel(Markdown(help_text), title="Help", border_style="cyan"))


async def main():
    """Main conversation loop."""
    
    # Show welcome
    display_welcome()
    
    # Initialize dependencies for the session
    deps = AgentDependencies()
    await deps.initialize()
    deps.session_id = str(uuid.uuid4())
    
    console.print("[bold green]✓[/bold green] Search system initialized\n")
    
    conversation_history = []
    
    try:
        while True:
            try:
                # Get user input
                user_input = Prompt.ask("[bold green]You").strip()
                
                # Handle special commands
                if user_input.lower() in ['exit', 'quit', 'q']:
                    console.print("\n[yellow]👋 Goodbye![/yellow]")
                    break
                    
                elif user_input.lower() == 'help':
                    display_help()
                    continue
                
                elif user_input.lower() == 'clear':
                    console.clear()
                    display_welcome()
                    continue
                
                elif user_input.lower() == 'info':
                    settings = load_settings()
                    console.print(Panel(
                        f"[cyan]LLM Provider:[/cyan] {settings.llm_provider}\n"
                        f"[cyan]LLM Model:[/cyan] {settings.llm_model}\n"
                        f"[cyan]Embedding Model:[/cyan] {settings.embedding_model}\n"
                        f"[cyan]Default Match Count:[/cyan] {settings.default_match_count}\n"
                        f"[cyan]Default Text Weight:[/cyan] {settings.default_text_weight}",
                        title="System Configuration",
                        border_style="magenta"
                    ))
                    continue
                
                elif user_input.lower().startswith('set '):
                    # Handle preference setting
                    parts = user_input[4:].split('=')
                    if len(parts) == 2:
                        key, value = parts[0].strip(), parts[1].strip()
                        # Try to convert value to appropriate type
                        try:
                            if '.' in value:
                                value = float(value)
                            elif value.isdigit():
                                value = int(value)
                        except:
                            pass  # Keep as string
                        deps.set_user_preference(key, value)
                        console.print(f"[green]✓[/green] Set {key} = {value}")
                    else:
                        console.print("[red]Invalid format. Use: set key=value[/red]")
                    continue
                
                if not user_input:
                    continue
                
                # Add to history
                conversation_history.append(f"User: {user_input}")
                
                # Stream the interaction and get response
                streamed_text, final_response = await stream_agent_interaction(
                    user_input, 
                    conversation_history, 
                    deps
                )
                
                # Handle the response display
                if streamed_text:
                    # Response was streamed, just add spacing
                    console.print()
                    conversation_history.append(f"Assistant: {streamed_text}")
                elif final_response and final_response.strip():
                    # Response wasn't streamed, display with proper formatting
                    console.print(f"[bold blue]Assistant:[/bold blue] {final_response}")
                    console.print()
                    conversation_history.append(f"Assistant: {final_response}")
                    
            except KeyboardInterrupt:
                console.print("\n[yellow]Use 'exit' to quit[/yellow]")
                continue
                
    finally:
        # Clean up
        await deps.cleanup()
        console.print("[dim]Session ended[/dim]")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted[/yellow]")
        sys.exit(0)