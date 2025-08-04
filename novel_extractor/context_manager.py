"""
Context window management with token counting and truncation.
"""

import logging
from typing import Dict, List, Optional, Tuple
import tiktoken

from config.settings import get_settings

logger = logging.getLogger(__name__)


class ContextManager:
    """
    Manages LLM context windows with token counting and intelligent truncation.
    """

    def __init__(self, model: Optional[str] = None, max_tokens: Optional[int] = None):
        """
        Initialize context manager.

        Args:
            model: Model name for tokenizer selection
            max_tokens: Maximum context window size
        """
        settings = get_settings()
        self.model = model or settings.llm_model
        self.max_tokens = max_tokens or settings.max_context_length
        self.reserved_tokens = settings.reserved_response_tokens

        # Initialize tokenizer based on model
        try:
            self.encoding = tiktoken.encoding_for_model(self.model)
        except KeyError:
            # Fallback to cl100k_base for unknown models
            logger.warning(f"Unknown model {self.model}, using cl100k_base encoding")
            self.encoding = tiktoken.get_encoding("cl100k_base")

    def count_tokens(self, text: str) -> int:
        """
        Count tokens in text.

        Args:
            text: Text to count tokens for

        Returns:
            int: Number of tokens
        """
        return len(self.encoding.encode(text))

    def fit_content(
        self,
        settings_dict: Dict[str, str],
        novel_text: str,
        system_prompt: Optional[str] = None,
    ) -> Tuple[str, bool]:
        """
        Fit content within context window, prioritizing settings.

        Args:
            settings_dict: Settings to include (high priority)
            novel_text: Novel content (may be truncated)
            system_prompt: Optional system prompt

        Returns:
            Tuple[str, bool]: Fitted content and whether truncation occurred
        """
        # Calculate token usage
        settings_text = self._format_settings(settings_dict)
        settings_tokens = self.count_tokens(settings_text)

        system_tokens = 0
        if system_prompt:
            system_tokens = self.count_tokens(system_prompt)

        # Available tokens for novel content
        available = (
            self.max_tokens - settings_tokens - system_tokens - self.reserved_tokens
        )

        if available <= 0:
            raise ValueError(
                f"Settings and system prompt exceed context window: "
                f"{settings_tokens + system_tokens} tokens used, "
                f"{self.max_tokens - self.reserved_tokens} available"
            )

        # Check if novel fits
        novel_tokens = self.count_tokens(novel_text)
        truncated = False

        if novel_tokens > available:
            # Truncate novel to fit
            truncated = True
            novel_text = self._truncate_to_tokens(novel_text, available)
            logger.info(f"Truncated novel from {novel_tokens} to {available} tokens")

        # Combine content
        parts = []
        if system_prompt:
            parts.append(system_prompt)
        parts.append(settings_text)
        parts.append(novel_text)

        final_content = "\n\n".join(parts)
        return final_content, truncated

    def _format_settings(self, settings_dict: Dict[str, str]) -> str:
        """
        Format settings dictionary as text.

        Args:
            settings_dict: Settings to format

        Returns:
            str: Formatted settings text
        """
        lines = ["=== SETTINGS ==="]
        for key, value in settings_dict.items():
            lines.append(f"\n{key.upper()}:\n{value}")
        lines.append("\n=== END SETTINGS ===")
        return "\n".join(lines)

    def _truncate_to_tokens(self, text: str, max_tokens: int) -> str:
        """
        Truncate text to fit within token limit.

        Args:
            text: Text to truncate
            max_tokens: Maximum allowed tokens

        Returns:
            str: Truncated text
        """
        tokens = self.encoding.encode(text)

        if len(tokens) <= max_tokens:
            return text

        # Keep last N tokens (most recent content)
        truncated_tokens = tokens[-max_tokens:]

        # Decode back to text
        truncated_text = self.encoding.decode(truncated_tokens)

        # Add truncation marker
        return f"[... content truncated ...]\n{truncated_text}"

    def estimate_compression_ratio(
        self, original_text: str, compressed_text: str
    ) -> float:
        """
        Calculate compression ratio based on token count.

        Args:
            original_text: Original text
            compressed_text: Compressed text

        Returns:
            float: Compression ratio (0-1)
        """
        original_tokens = self.count_tokens(original_text)
        compressed_tokens = self.count_tokens(compressed_text)

        if original_tokens == 0:
            return 0.0

        return compressed_tokens / original_tokens

    def split_into_chunks(
        self, text: str, chunk_size: Optional[int] = None
    ) -> List[str]:
        """
        Split text into chunks that fit within token limits.

        Args:
            text: Text to split
            chunk_size: Target chunk size in tokens

        Returns:
            List[str]: List of text chunks
        """
        if chunk_size is None:
            chunk_size = self.max_tokens - self.reserved_tokens

        tokens = self.encoding.encode(text)
        chunks = []

        for i in range(0, len(tokens), chunk_size):
            chunk_tokens = tokens[i : i + chunk_size]
            chunk_text = self.encoding.decode(chunk_tokens)
            chunks.append(chunk_text)

        return chunks
