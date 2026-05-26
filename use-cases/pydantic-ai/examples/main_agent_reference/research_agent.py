"""
Research Agent that uses Brave Search and can invoke Email Agent.
"""

import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

from pydantic_ai import Agent, RunContext

from .providers import get_llm_model
from .email_agent import email_agent, EmailAgentDependencies
from .tools import search_web_tool

logger = logging.getLogger(__name__)


SYSTEM_PROMPT = """
You are an expert research assistant with the ability to search the web and create email drafts. Your primary goal is to help users find relevant information and communicate findings effectively.

Your capabilities:
1. **Web Search**: Use Brave Search to find current, relevant information on any topic
2. **Email Creation**: Create professional email drafts through Gmail when requested

When conducting research:
- Use specific, targeted search queries
- Analyze search results for relevance and credibility
- Synthesize information from multiple sources
- Provide clear, well-organized summaries
- Include source URLs for reference

When creating emails:
- Use research findings to create informed, professional content
- Adapt tone and detail level to the intended recipient
- Include relevant sources and citations when appropriate
- Ensure emails are clear, concise, and actionable

Always strive to provide accurate, helpful, and actionable information.
"""


@dataclass
class ResearchAgentDependencies:
    """Dependencies for the research agent - only configuration, no tool instances."""
    brave_api_key: str
    gmail_credentials_path: str
    gmail_token_path: str
    session_id: Optional[str] = None


# Initialize the research agent
research_agent = Agent(
    get_llm_model(),
    deps_type=ResearchAgentDependencies,
    system_prompt=SYSTEM_PROMPT
)


@research_agent.tool
async def search_web(
    ctx: RunContext[ResearchAgentDependencies],
    query: str,
    max_results: int = 10
) -> List[Dict[str, Any]]:
    """
    Search the web using Brave Search API.
    
    Args:
        query: Search query
        max_results: Maximum number of results to return (1-20)
    
    Returns:
        List of search results with title, URL, description, and score
    """
    try:        
        # Ensure max_results is within valid range
        max_results = min(max(max_results, 1), 20)
        
        results = await search_web_tool(
            api_key=ctx.deps.brave_api_key,
            query=query,
            count=max_results
        )
        
        logger.info(f"Found {len(results)} results for query: {query}")
        return results
        
    except Exception as e:
        logger.error(f"Web search failed: {e}")
        return [{"error": f"Search failed: {str(e)}"}]


@research_agent.tool
async def create_email_draft(
    ctx: RunContext[ResearchAgentDependencies],
    recipient_email: str,
    subject: str,
    context: str,
    research_summary: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create an email draft based on research context using the Email Agent.
    
    Args:
        recipient_email: Email address of the recipient
        subject: Email subject line
        context: Context or purpose for the email
        research_summary: Optional research findings to include
    
    Returns:
        Dictionary with draft creation results
    """
    try:
        # Prepare the email content prompt
        if research_summary:
            email_prompt = f"""
Create a professional email to {recipient_email} with the subject "{subject}".

Context: {context}

Research Summary:
{research_summary}

Please create a well-structured email that:
1. Has an appropriate greeting
2. Provides clear context
3. Summarizes the key research findings professionally
4. Includes actionable next steps if appropriate
5. Ends with a professional closing

The email should be informative but concise, and maintain a professional yet friendly tone.
"""
        else:
            email_prompt = f"""
Create a professional email to {recipient_email} with the subject "{subject}".

Context: {context}

Please create a well-structured email that addresses the context provided.
"""
        
        # Create dependencies for email agent
        email_deps = EmailAgentDependencies(
            gmail_credentials_path=ctx.deps.gmail_credentials_path,
            gmail_token_path=ctx.deps.gmail_token_path,
            session_id=ctx.deps.session_id
        )
        
        # Run the email agent
        result = await email_agent.run(
            email_prompt,
            deps=email_deps,
            usage=ctx.usage  # Pass usage for token tracking
        )
        
        logger.info(f"Email agent invoked for recipient: {recipient_email}")
        
        return {
            "success": True,
            "agent_response": result.data,
            "recipient": recipient_email,
            "subject": subject,
            "context": context
        }
        
    except Exception as e:
        logger.error(f"Failed to create email draft via Email Agent: {e}")
        return {
            "success": False,
            "error": str(e),
            "recipient": recipient_email,
            "subject": subject
        }


@research_agent.tool
async def summarize_research(
    ctx: RunContext[ResearchAgentDependencies],
    search_results: List[Dict[str, Any]],
    topic: str,
    focus_areas: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a comprehensive summary of research findings.
    
    Args:
        search_results: List of search result dictionaries
        topic: Main research topic
        focus_areas: Optional specific areas to focus on
    
    Returns:
        Dictionary with research summary
    """
    try:
        if not search_results:
            return {
                "summary": "No search results provided for summarization.",
                "key_points": [],
                "sources": []
            }
        
        # Extract key information
        sources = []
        descriptions = []
        
        for result in search_results:
            if "title" in result and "url" in result:
                sources.append(f"- {result['title']}: {result['url']}")
                if "description" in result:
                    descriptions.append(result["description"])
        
        # Create summary content
        content_summary = "\n".join(descriptions[:5])  # Limit to top 5 descriptions
        sources_list = "\n".join(sources[:10])  # Limit to top 10 sources
        
        focus_text = f"\nSpecific focus areas: {focus_areas}" if focus_areas else ""
        
        summary = f"""
Research Summary: {topic}{focus_text}

Key Findings:
{content_summary}

Sources:
{sources_list}
"""
        
        return {
            "summary": summary,
            "topic": topic,
            "sources_count": len(sources),
            "key_points": descriptions[:5]
        }
        
    except Exception as e:
        logger.error(f"Failed to summarize research: {e}")
        return {
            "summary": f"Failed to summarize research: {str(e)}",
            "key_points": [],
            "sources": []
        }


# Convenience function to create research agent with dependencies
def create_research_agent(
    brave_api_key: str,
    gmail_credentials_path: str,
    gmail_token_path: str,
    session_id: Optional[str] = None
) -> Agent:
    """
    Create a research agent with specified dependencies.
    
    Args:
        brave_api_key: Brave Search API key
        gmail_credentials_path: Path to Gmail credentials.json
        gmail_token_path: Path to Gmail token.json
        session_id: Optional session identifier
        
    Returns:
        Configured research agent
    """
    return research_agent