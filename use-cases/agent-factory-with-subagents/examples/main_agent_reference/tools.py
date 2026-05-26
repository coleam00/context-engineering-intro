"""
Pure tool functions for multi-agent system.
These are standalone functions that can be imported and used by any agent.
"""

import os
import base64
import logging
import httpx
from typing import List, Dict, Any, Optional
from datetime import datetime

from agents.models import BraveSearchResult

logger = logging.getLogger(__name__)


# Brave Search Tool Function
async def search_web_tool(
    api_key: str,
    query: str,
    count: int = 10,
    offset: int = 0,
    country: Optional[str] = None,
    lang: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Pure function to search the web using Brave Search API.
    
    Args:
        api_key: Brave Search API key
        query: Search query
        count: Number of results to return (1-20)
        offset: Offset for pagination
        country: Country code for localized results
        lang: Language code for results
        
    Returns:
        List of search results as dictionaries
        
    Raises:
        ValueError: If query is empty or API key missing
        Exception: If API request fails
    """
    if not api_key or not api_key.strip():
        raise ValueError("Brave API key is required")
    
    if not query or not query.strip():
        raise ValueError("Query cannot be empty")
    
    # Ensure count is within valid range
    count = min(max(count, 1), 20)
    
    headers = {
        "X-Subscription-Token": api_key,
        "Accept": "application/json"
    }
    
    params = {
        "q": query,
        "count": count,
        "offset": offset
    }
    
    if country:
        params["country"] = country
    if lang:
        params["lang"] = lang
    
    logger.info(f"Searching Brave for: {query}")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                "https://api.search.brave.com/res/v1/web/search",
                headers=headers,
                params=params,
                timeout=30.0
            )
            
            # Handle rate limiting
            if response.status_code == 429:
                raise Exception("Rate limit exceeded. Check your Brave API quota.")
            
            # Handle authentication errors
            if response.status_code == 401:
                raise Exception("Invalid Brave API key")
            
            # Handle other errors
            if response.status_code != 200:
                raise Exception(f"Brave API returned {response.status_code}: {response.text}")
            
            data = response.json()
            
            # Extract web results
            web_results = data.get("web", {}).get("results", [])
            
            # Convert to our format
            results = []
            for idx, result in enumerate(web_results):
                # Calculate a simple relevance score based on position
                score = 1.0 - (idx * 0.05)  # Decrease by 0.05 for each position
                score = max(score, 0.1)  # Minimum score of 0.1
                
                results.append({
                    "title": result.get("title", ""),
                    "url": result.get("url", ""),
                    "description": result.get("description", ""),
                    "score": score
                })
            
            logger.info(f"Found {len(results)} results for query: {query}")
            return results
            
        except httpx.RequestError as e:
            logger.error(f"Request error during Brave search: {e}")
            raise Exception(f"Request failed: {str(e)}")
        except Exception as e:
            logger.error(f"Error during Brave search: {e}")
            raise
