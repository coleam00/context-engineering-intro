"""
Tests for the main extractor module.
"""

import pytest
from unittest.mock import Mock, AsyncMock
from pathlib import Path

from novel_extractor.extractor import NovelExtractor
from novel_extractor.models import NovelMetadata, NovelStructure
from novel_extractor.llm_client import LLMResponse


class TestNovelExtractor:
    """
    Test novel extractor functionality.
    """

    @pytest.fixture
    def mock_extractor(
        self, mock_llm_client, settings_manager_with_temp_dir, context_manager
    ):
        """
        Create extractor with mocked dependencies.
        """
        return NovelExtractor(
            settings_manager=settings_manager_with_temp_dir,
            llm_client=mock_llm_client,
            context_manager=context_manager,
        )

    def test_read_novel(self, mock_extractor, sample_novel_file):
        """
        Test reading novel file with different encodings.
        """
        content = mock_extractor._read_novel(sample_novel_file)

        assert "Chapter 1: The Beginning" in content
        assert "Sarah walked through the empty streets" in content

    def test_read_novel_encoding_fallback(self, mock_extractor, temp_settings_dir):
        """
        Test that encoding fallback works.
        """
        # Create a file with latin-1 encoding
        novel_path = Path(temp_settings_dir) / "latin1_novel.txt"
        content = "Café façade résumé"
        novel_path.write_text(content, encoding="latin-1")

        # Should still read successfully
        read_content = mock_extractor._read_novel(str(novel_path))
        assert "Café" in read_content

    def test_create_metadata(
        self, mock_extractor, sample_novel_file, sample_novel_content
    ):
        """
        Test metadata creation from novel file.
        """
        metadata = mock_extractor._create_metadata(
            sample_novel_file, sample_novel_content
        )

        assert isinstance(metadata, NovelMetadata)
        assert metadata.title == "test_novel"
        assert metadata.word_count > 0
        assert metadata.file_path == str(Path(sample_novel_file).absolute())

    @pytest.mark.asyncio
    async def test_extract_background(self, mock_extractor, sample_novel_content):
        """
        Test background extraction.
        """
        # Setup
        settings_dict = {"global_settings": "Test settings"}

        # Mock the LLM response
        mock_extractor.llm_client.generate.return_value = LLMResponse(
            content="Extracted background information"
        )

        # Execute
        await mock_extractor._extract_background(sample_novel_content, settings_dict)

        # Verify
        assert mock_extractor.llm_client.generate.called

        # Check that settings were written
        written_content = mock_extractor.settings_manager.read_settings(
            mock_extractor.settings_manager.NOVEL_BACKGROUND
        )
        assert written_content == "Extracted background information"

    @pytest.mark.asyncio
    async def test_extract_characters(self, mock_extractor, sample_novel_content):
        """
        Test character extraction.
        """
        settings_dict = {"global_settings": "Test settings"}

        mock_extractor.llm_client.generate.return_value = LLMResponse(
            content="Character profiles:\n1. Sarah - protagonist\n2. Marcus - mysterious friend"
        )

        await mock_extractor._extract_characters(sample_novel_content, settings_dict)

        written_content = mock_extractor.settings_manager.read_settings(
            mock_extractor.settings_manager.CHARACTER_SETTINGS
        )
        assert "Sarah - protagonist" in written_content
        assert "Marcus - mysterious friend" in written_content

    @pytest.mark.asyncio
    async def test_extract_plot(self, mock_extractor, sample_novel_content):
        """
        Test plot extraction.
        """
        settings_dict = {"global_settings": "Test settings"}

        mock_extractor.llm_client.generate.return_value = LLMResponse(
            content="Plot structure: Mystery thriller with artifact subplot"
        )

        await mock_extractor._extract_plot(sample_novel_content, settings_dict)

        written_content = mock_extractor.settings_manager.read_settings(
            mock_extractor.settings_manager.PLOT_SETTINGS
        )
        assert "Mystery thriller" in written_content

    @pytest.mark.asyncio
    async def test_extract_style(self, mock_extractor, sample_novel_content):
        """
        Test style analysis.
        """
        settings_dict = {"global_settings": "Test settings"}

        # First create background file
        mock_extractor.settings_manager.write_settings(
            mock_extractor.settings_manager.NOVEL_BACKGROUND, "Initial background"
        )

        mock_extractor.llm_client.generate.return_value = LLMResponse(
            content="Third-person narrative with suspenseful tone"
        )

        await mock_extractor._extract_style(sample_novel_content, settings_dict)

        # Style should be appended to background
        written_content = mock_extractor.settings_manager.read_settings(
            mock_extractor.settings_manager.NOVEL_BACKGROUND
        )
        assert "Initial background" in written_content
        assert "Writing Style Analysis" in written_content
        assert "Third-person narrative" in written_content

    @pytest.mark.asyncio
    async def test_extract_novel_structure_full_flow(
        self, mock_extractor, sample_novel_file
    ):
        """
        Test complete extraction workflow.
        """
        # Initialize global settings
        mock_extractor.settings_manager.initialize_global_settings()

        # Mock all LLM responses
        mock_extractor.llm_client.generate.side_effect = [
            LLMResponse(content="Background extracted"),
            LLMResponse(content="Characters extracted"),
            LLMResponse(content="Plot extracted"),
            LLMResponse(content="Style extracted"),
        ]

        # Mock compression check
        mock_extractor.settings_manager.check_and_compress_if_needed = AsyncMock(
            return_value=[]
        )

        # Progress tracking
        progress_updates = []

        def progress_callback(status, progress):
            progress_updates.append((status, progress))

        # Execute
        result = await mock_extractor.extract_novel_structure(
            sample_novel_file, progress_callback
        )

        # Verify result
        assert isinstance(result, NovelStructure)
        assert result.metadata.title == "test_novel"

        # Verify progress updates
        assert len(progress_updates) > 0
        assert progress_updates[-1][1] == 1.0  # 100% complete

        # Verify all extractions were called
        assert mock_extractor.llm_client.generate.call_count == 4

    @pytest.mark.asyncio
    async def test_file_not_found_error(self, mock_extractor):
        """
        Test error handling for non-existent file.
        """
        with pytest.raises(FileNotFoundError):
            await mock_extractor.extract_novel_structure("nonexistent.txt")

    @pytest.mark.asyncio
    async def test_context_truncation_handling(
        self, mock_extractor, sample_novel_content
    ):
        """
        Test that truncation is handled properly.
        """
        # Create very small context manager
        mock_extractor.context_manager = Mock()
        mock_extractor.context_manager.fit_content.return_value = (
            "Truncated content",
            True,
        )

        settings_dict = {"test": "settings"}

        mock_extractor.llm_client.generate.return_value = LLMResponse(
            content="Response despite truncation"
        )

        # Should complete without error
        await mock_extractor._extract_background(sample_novel_content, settings_dict)

        # Verify truncation was logged (would need to check logs)
