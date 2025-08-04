"""
Tests for LLM client module.
"""

import pytest
from unittest.mock import Mock, patch
import httpx

from novel_extractor.llm_client import LLMClient, LLMResponse
from config.settings import Settings


class TestLLMClient:
    """
    Test LLM client functionality.
    """

    @pytest.fixture
    def mock_settings(self):
        """
        Create mock settings for LLM client.
        """
        return Settings(
            llm_api_key="test-key",
            llm_provider="openai",
            llm_model="gpt-4",
            llm_base_url="https://api.openai.com/v1",
            max_retries=3,
            retry_delay=0.1,  # Short delay for tests
        )

    @pytest.mark.asyncio
    async def test_successful_generation(self, mock_settings):
        """
        Test successful LLM generation.
        """
        client = LLMClient(mock_settings)

        # Mock the httpx response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Generated text"}}],
            "usage": {"total_tokens": 50},
        }

        with patch("httpx.AsyncClient.post", return_value=mock_response):
            messages = [{"role": "user", "content": "Test prompt"}]
            response = await client.generate(messages)

            assert isinstance(response, LLMResponse)
            assert response.content == "Generated text"
            assert response.usage["total_tokens"] == 50

    @pytest.mark.asyncio
    async def test_rate_limit_retry(self, mock_settings):
        """
        Test retry logic for rate limit errors.
        """
        client = LLMClient(mock_settings)

        # Mock responses: first two rate limits, then success
        mock_responses = [
            Mock(status_code=429),  # Rate limit
            Mock(status_code=429),  # Rate limit
            Mock(
                status_code=200,
                json=Mock(
                    return_value={
                        "choices": [{"message": {"content": "Success after retry"}}],
                        "usage": {"total_tokens": 30},
                    }
                ),
            ),
        ]

        call_count = 0

        async def mock_post(*args, **kwargs):
            nonlocal call_count
            response = mock_responses[call_count]
            call_count += 1
            if response.status_code == 429:
                response.raise_for_status = Mock(
                    side_effect=httpx.HTTPStatusError(
                        "Rate limit", request=Mock(), response=response
                    )
                )
            else:
                response.raise_for_status = Mock()
            return response

        with patch("httpx.AsyncClient.post", side_effect=mock_post):
            messages = [{"role": "user", "content": "Test"}]
            response = await client.generate(messages)

            assert response.content == "Success after retry"
            assert call_count == 3  # Should have tried 3 times

    @pytest.mark.asyncio
    async def test_max_retries_exceeded(self, mock_settings):
        """
        Test that exception is raised after max retries.
        """
        client = LLMClient(mock_settings)

        # Always return rate limit error
        mock_response = Mock(status_code=429)
        mock_response.raise_for_status = Mock(
            side_effect=httpx.HTTPStatusError(
                "Rate limit", request=Mock(), response=mock_response
            )
        )

        with patch("httpx.AsyncClient.post", return_value=mock_response):
            messages = [{"role": "user", "content": "Test"}]

            with pytest.raises(Exception, match="All 3 retry attempts failed"):
                await client.generate(messages)

    @pytest.mark.asyncio
    async def test_api_error_handling(self, mock_settings):
        """
        Test handling of non-rate-limit API errors.
        """
        client = LLMClient(mock_settings)

        # Mock a 500 error
        mock_response = Mock(status_code=500)
        mock_response.raise_for_status = Mock(
            side_effect=httpx.HTTPStatusError(
                "Server error", request=Mock(), response=mock_response
            )
        )

        with patch("httpx.AsyncClient.post", return_value=mock_response):
            messages = [{"role": "user", "content": "Test"}]

            # Should retry and eventually fail
            with pytest.raises(Exception):
                await client.generate(messages)

    def test_create_message(self, mock_settings):
        """
        Test message creation helper.
        """
        client = LLMClient(mock_settings)

        message = client.create_message("system", "You are helpful")
        assert message == {"role": "system", "content": "You are helpful"}

        message = client.create_message("user", "Hello")
        assert message == {"role": "user", "content": "Hello"}

    @pytest.mark.asyncio
    async def test_custom_parameters(self, mock_settings):
        """
        Test that custom parameters are passed to the API.
        """
        client = LLMClient(mock_settings)

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Response"}}]
        }

        with patch("httpx.AsyncClient.post", return_value=mock_response) as mock_post:
            messages = [{"role": "user", "content": "Test"}]
            await client.generate(messages, temperature=0.5, max_tokens=100, top_p=0.9)

            # Check that parameters were included in the request
            call_args = mock_post.call_args
            json_data = call_args.kwargs["json"]

            assert json_data["temperature"] == 0.5
            assert json_data["max_tokens"] == 100
            assert json_data["top_p"] == 0.9

    @pytest.mark.asyncio
    async def test_timeout_handling(self, mock_settings):
        """
        Test that timeouts are handled properly.
        """
        client = LLMClient(mock_settings)

        # Simulate timeout
        async def mock_post_timeout(*args, **kwargs):
            raise httpx.TimeoutException("Request timed out")

        with patch("httpx.AsyncClient.post", side_effect=mock_post_timeout):
            messages = [{"role": "user", "content": "Test"}]

            # Should retry and eventually fail
            with pytest.raises(Exception):
                await client.generate(messages)
