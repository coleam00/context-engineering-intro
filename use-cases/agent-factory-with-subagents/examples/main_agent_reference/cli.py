#!/usr/bin/env python3
"""Conversational CLI with real-time streaming and tool call visibility for Pydantic AI agents."""

import asyncio
import sys
import os
from typing import List

# Add parent directory to Python path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.live import Live
from rich.text import Text

from pydantic_ai import Agent
from agents.research_agent import research_agent
from agents.dependencies import ResearchAgentDependencies
from agents.settings import settings

console = Console()


async def stream_agent_interaction(user_input: str, conversation_history: List[str]) -> tuple[str, str]:
    """Stream agent interaction with real-time tool call display."""
    
    try:
        # Set up dependencies
        research_deps = ResearchAgentDependencies(brave_api_key=settings.brave_api_key)
        
        # Build context with conversation history
        context = "\n".join(conversation_history[-6:]) if conversation_history else ""
        
        prompt = f"""Previous conversation:
{context}

User: {user_input}

Respond naturally and helpfully."""

        # Stream the agent execution
        async with research_agent.iter(prompt, deps=research_deps) as run:
            
            async for node in run:
                
                # Handle user prompt node
                if Agent.is_user_prompt_node(node):
                    pass  # Clean start - no processing messages
                
                # Handle model request node - stream the thinking process
                elif Agent.is_model_request_node(node):
                    # Show assistant prefix at the start
                    console.print("[bold blue]Assistant:[/bold blue] ", end="")
                    
                    # Stream model request events for real-time text
                    response_text = ""
                    async with node.stream(run.ctx) as request_stream:
                        async for event in request_stream:
                            # Handle different event types based on their type
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
                
                # Handle tool calls - this is the key part
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
                                
                                # Debug: print part attributes to understand structure
                                if tool_name == "Unknown Tool" and hasattr(event, 'part'):
                                    part_attrs = [attr for attr in dir(event.part) if not attr.startswith('_')]
                                    console.print(f"    [dim red]Debug - Part attributes: {part_attrs}[/dim red]")
                                    
                                    # Try to get more details about the part
                                    if hasattr(event.part, '__dict__'):
                                        console.print(f"    [dim red]Part dict: {event.part.__dict__}[/dim red]")
                                
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
                                # Display tool result
                                result = str(event.tool_return) if hasattr(event, 'tool_return') else "No result"
                                if len(result) > 100:
                                    result = result[:97] + "..."
                                console.print(f"  ✅ [green]Tool result:[/green] [dim]{result}[/dim]")
                
                # Handle end node  
                elif Agent.is_end_node(node):
                    # Don't show "Processing complete" - keep it clean
                    pass
        
        # Get final result
        final_result = run.result
        final_output = final_result.output if hasattr(final_result, 'output') else str(final_result)
        
        # Return both streamed and final content
        return (response_text.strip(), final_output)
        
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        return ("", f"Error: {e}")


async def main():
    """Main conversation loop."""
    
    # Show welcome
    welcome = Panel(
        "[bold blue]🤖 Pydantic AI Research Assistant[/bold blue]\n\n"
        "[green]Real-time tool execution visibility[/green]\n"
        "[dim]Type 'exit' to quit[/dim]",
        style="blue",
        padding=(1, 2)
    )
    console.print(welcome)
    console.print()
    
    conversation_history = []
    
    while True:
        try:
            # Get user input
            user_input = Prompt.ask("[bold green]You").strip()
            
            # Handle exit
            if user_input.lower() in ['exit', 'quit']:
                console.print("\n[yellow]👋 Goodbye![/yellow]")
                break
                
            if not user_input:
                continue
            
            # Add to history
            conversation_history.append(f"User: {user_input}")
            
            # Stream the interaction and get response
            streamed_text, final_response = await stream_agent_interaction(user_input, conversation_history)
            
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
            else:
                # No response
                console.print()
            
        except KeyboardInterrupt:
            console.print("\n[yellow]Use 'exit' to quit[/yellow]")
            continue
            
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            continue


if __name__ == "__main__":
    asyncio.run(main())