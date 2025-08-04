"""
Tests for context manager module.
"""

import pytest
from novel_extractor.context_manager import ContextManager


class TestContextManager:
    """
    Test context manager functionality.
    """

    def test_token_counting(self):
        """
        Test that tokens are counted correctly.
        """
        manager = ContextManager("gpt-4", 8192)

        # Simple test
        count = manager.count_tokens("Hello world")
        assert count > 0
        assert count < 10  # Should be around 2-3 tokens

        # Longer text
        long_text = "The quick brown fox jumps over the lazy dog. " * 10
        long_count = manager.count_tokens(long_text)
        assert long_count > count

    def test_content_truncation(self):
        """
        Test that content is truncated when it exceeds limits.
        """
        manager = ContextManager("gpt-4", 100)  # Small context window

        # Create content that will definitely exceed 100 tokens
        settings = {"test": "short settings"}
        novel = "very " * 1000 + "long text"

        result, truncated = manager.fit_content(settings, novel)

        assert truncated is True
        assert "[... content truncated ...]" in result
        assert manager.count_tokens(result) <= 100

    def test_no_truncation_needed(self):
        """
        Test that content is not truncated when it fits.
        """
        manager = ContextManager("gpt-4", 8192)

        settings = {"test": "short settings"}
        novel = "This is a short novel."

        result, truncated = manager.fit_content(settings, novel)

        assert truncated is False
        assert "[... content truncated ...]" not in result
        assert "short novel" in result

    def test_settings_priority(self):
        """
        Test that settings are always included even with truncation.
        """
        manager = ContextManager("gpt-4", 200)

        settings = {"important": "These settings must be included"}
        novel = "x" * 10000  # Very long novel

        result, truncated = manager.fit_content(settings, novel)

        assert "These settings must be included" in result
        assert truncated is True

    def test_compression_ratio_calculation(self):
        """
        Test compression ratio calculation.
        """
        manager = ContextManager()

        original = "This is a long text that will be compressed."
        compressed = "Compressed text."

        ratio = manager.estimate_compression_ratio(original, compressed)

        assert 0 <= ratio <= 1
        assert ratio < 0.5  # Compressed should be less than half

    def test_split_into_chunks(self):
        """
        Test splitting text into chunks.
        """
        manager = ContextManager("gpt-4", 1000)

        # Create text that will need multiple chunks
        long_text = "word " * 1000

        chunks = manager.split_into_chunks(long_text, chunk_size=100)

        assert len(chunks) > 1
        assert all(manager.count_tokens(chunk) <= 100 for chunk in chunks)

        # Verify we can reconstruct the text (approximately)
        reconstructed = "".join(chunks)
        assert len(reconstructed) > 0

    def test_error_handling_for_too_large_settings(self):
        """
        Test error when settings alone exceed context window.
        """
        manager = ContextManager("gpt-4", 50)  # Very small window

        # Settings that exceed the window
        settings = {"huge": "x" * 10000}
        novel = "any text"

        with pytest.raises(ValueError, match="Settings and system prompt exceed"):
            manager.fit_content(settings, novel)

    def test_with_system_prompt(self):
        """
        Test content fitting with system prompt included.
        """
        manager = ContextManager("gpt-4", 500)

        system_prompt = "You are a helpful assistant."
        settings = {"test": "settings"}
        novel = "Novel content here."

        result, truncated = manager.fit_content(settings, novel, system_prompt)

        assert system_prompt in result
        assert "settings" in result
        assert "Novel content" in result
        assert not truncated
