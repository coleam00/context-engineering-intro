"""
OpenAI-compatible LLM client with retry logic and error handling.
"""

import asyncio
import logging
from typing import List, Dict, Optional
import httpx
from pydantic import BaseModel

from config.settings import Settings, get_settings

logger = logging.getLogger(__name__)


class LLMMessage(BaseModel):
    """
    Message format for LLM API.
    """

    role: str
    content: str


class LLMResponse(BaseModel):
    """
    Response from LLM API.
    """

    content: str
    usage: Optional[Dict[str, int]] = None


class RateLimitError(Exception):
    """Raised when API rate limit is hit."""

    pass


class LLMClient:
    """
    Client for OpenAI-compatible LLM APIs with retry logic.
    """

    def __init__(self, settings: Optional[Settings] = None):
        """
        Initialize LLM client.

        Args:
            settings: Application settings
        """
        self.settings = settings or get_settings()
        self.api_key = self.settings.llm_api_key
        self.model = self.settings.llm_model
        self.base_url = self.settings.llm_base_url
        self.max_retries = self.settings.max_retries
        self.retry_delay = self.settings.retry_delay

    async def generate(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs,
    ) -> LLMResponse:
        """
        Generate response from LLM with retry logic.

        Args:
            messages: List of message dictionaries
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response
            **kwargs: Additional API parameters

        Returns:
            LLMResponse: Generated text and usage info

        Raises:
            Exception: If all retries fail
        """
        for attempt in range(self.max_retries):
            try:
                response = await self._make_request(
                    messages, temperature, max_tokens, **kwargs
                )
                return response
            except RateLimitError:
                wait_time = self.retry_delay * (2**attempt)
                logger.warning(
                    f"Rate limit hit, retrying in {wait_time}s (attempt {attempt + 1}/{self.max_retries})"
                )
                await asyncio.sleep(wait_time)
            except Exception as e:
                logger.error(f"API request failed: {e}")
                if attempt == self.max_retries - 1:
                    raise
                await asyncio.sleep(self.retry_delay)

        raise Exception(f"All {self.max_retries} retry attempts failed")

    async def _make_request(
        self,
        messages: List[Dict[str, str]],
        temperature: float,
        max_tokens: Optional[int],
        **kwargs,
    ) -> LLMResponse:
        """
        Make actual API request.

        Args:
            messages: List of message dictionaries
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response
            **kwargs: Additional API parameters

        Returns:
            LLMResponse: API response

        Raises:
            RateLimitError: If rate limit is hit
            Exception: For other API errors
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        data = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            **kwargs,
        }

        if max_tokens:
            data["max_tokens"] = max_tokens

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=60.0,
            )

            if response.status_code == 429:
                raise RateLimitError("Rate limit exceeded")

            response.raise_for_status()

            result = response.json()
            return LLMResponse(
                content=result["choices"][0]["message"]["content"],
                usage=result.get("usage"),
            )

    def create_message(self, role: str, content: str) -> Dict[str, str]:
        """
        Create properly formatted message.

        Args:
            role: Message role (system, user, assistant)
            content: Message content

        Returns:
            Dict[str, str]: Formatted message
        """
        return {"role": role, "content": content}
