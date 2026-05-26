"""
Core data models for the multi-agent system.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class ResearchQuery(BaseModel):
    """Model for research query requests."""
    query: str = Field(..., description="Research topic to investigate")
    max_results: int = Field(10, ge=1, le=50, description="Maximum number of results to return")
    include_summary: bool = Field(True, description="Whether to include AI-generated summary")


class BraveSearchResult(BaseModel):
    """Model for individual Brave search results."""
    title: str = Field(..., description="Title of the search result")
    url: str = Field(..., description="URL of the search result")
    description: str = Field(..., description="Description/snippet from the search result")
    score: float = Field(0.0, ge=0.0, le=1.0, description="Relevance score")
    
    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "title": "Understanding AI Safety",
                "url": "https://example.com/ai-safety",
                "description": "A comprehensive guide to AI safety principles...",
                "score": 0.95
            }
        }


class EmailDraft(BaseModel):
    """Model for email draft creation."""
    to: List[str] = Field(..., min_length=1, description="List of recipient email addresses")
    subject: str = Field(..., min_length=1, description="Email subject line")
    body: str = Field(..., min_length=1, description="Email body content")
    cc: Optional[List[str]] = Field(None, description="List of CC recipients")
    bcc: Optional[List[str]] = Field(None, description="List of BCC recipients")
    
    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "to": ["john@example.com"],
                "subject": "AI Research Summary",
                "body": "Dear John,\n\nHere's the latest research on AI safety...",
                "cc": ["team@example.com"]
            }
        }


class EmailDraftResponse(BaseModel):
    """Response model for email draft creation."""
    draft_id: str = Field(..., description="Gmail draft ID")
    message_id: str = Field(..., description="Message ID")
    thread_id: Optional[str] = Field(None, description="Thread ID if part of a thread")
    created_at: datetime = Field(default_factory=datetime.now, description="Draft creation timestamp")


class ResearchEmailRequest(BaseModel):
    """Model for research + email draft request."""
    research_query: str = Field(..., description="Topic to research")
    email_context: str = Field(..., description="Context for email generation")
    recipient_email: str = Field(..., description="Email recipient")
    email_subject: Optional[str] = Field(None, description="Optional email subject")


class ResearchResponse(BaseModel):
    """Response model for research queries."""
    query: str = Field(..., description="Original research query")
    results: List[BraveSearchResult] = Field(..., description="Search results")
    summary: Optional[str] = Field(None, description="AI-generated summary of results")
    total_results: int = Field(..., description="Total number of results found")
    timestamp: datetime = Field(default_factory=datetime.now, description="Query timestamp")


class AgentResponse(BaseModel):
    """Generic agent response model."""
    success: bool = Field(..., description="Whether the operation was successful")
    data: Optional[Dict[str, Any]] = Field(None, description="Response data")
    error: Optional[str] = Field(None, description="Error message if failed")
    tools_used: List[str] = Field(default_factory=list, description="List of tools used")


class ChatMessage(BaseModel):
    """Model for chat messages in the CLI."""
    role: str = Field(..., description="Message role (user/assistant)")
    content: str = Field(..., description="Message content")
    timestamp: datetime = Field(default_factory=datetime.now, description="Message timestamp")
    tools_used: Optional[List[Dict[str, Any]]] = Field(None, description="Tools used in response")


class SessionState(BaseModel):
    """Model for maintaining session state."""
    session_id: str = Field(..., description="Unique session identifier")
    user_id: Optional[str] = Field(None, description="User identifier")
    messages: List[ChatMessage] = Field(default_factory=list, description="Conversation history")
    created_at: datetime = Field(default_factory=datetime.now, description="Session creation time")
    last_activity: datetime = Field(default_factory=datetime.now, description="Last activity timestamp")