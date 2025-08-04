"""
Tests for settings manager module.
"""

import pytest
import os
from unittest.mock import patch

from novel_extractor.settings_manager import SettingsManager
from novel_extractor.llm_client import LLMResponse


class TestSettingsManager:
    """
    Test settings manager functionality.
    """

    def test_read_settings(self, settings_manager_with_temp_dir):
        """
        Test reading settings files.
        """
        manager = settings_manager_with_temp_dir

        # Create a test file
        test_content = "Test settings content"
        test_file = "test_settings.txt"

        file_path = os.path.join(manager.settings_dir, test_file)
        with open(file_path, "w") as f:
            f.write(test_content)

        # Read the file
        content = manager.read_settings(test_file)
        assert content == test_content

    def test_read_nonexistent_file(self, settings_manager_with_temp_dir):
        """
        Test reading non-existent file raises error.
        """
        manager = settings_manager_with_temp_dir

        with pytest.raises(FileNotFoundError):
            manager.read_settings("nonexistent.txt")

    def test_write_settings(self, settings_manager_with_temp_dir):
        """
        Test writing settings files.
        """
        manager = settings_manager_with_temp_dir

        test_content = "New settings content"
        test_file = "new_settings.txt"

        # Write file
        manager.write_settings(test_file, test_content, backup=False)

        # Verify file exists and has correct content
        file_path = os.path.join(manager.settings_dir, test_file)
        assert os.path.exists(file_path)

        with open(file_path, "r") as f:
            assert f.read() == test_content

    def test_write_with_backup(self, settings_manager_with_temp_dir):
        """
        Test writing settings with backup creation.
        """
        manager = settings_manager_with_temp_dir

        # Create initial file
        test_file = "backup_test.txt"
        original_content = "Original content"
        manager.write_settings(test_file, original_content, backup=False)

        # Write new content with backup
        new_content = "Updated content"
        manager.write_settings(test_file, new_content, backup=True)

        # Check that backup exists
        backup_files = [
            f
            for f in os.listdir(manager.settings_dir)
            if f.startswith(f"{test_file}.backup_")
        ]
        assert len(backup_files) == 1

        # Verify backup has original content
        backup_path = os.path.join(manager.settings_dir, backup_files[0])
        with open(backup_path, "r") as f:
            assert f.read() == original_content

    def test_get_all_settings(self, settings_manager_with_temp_dir):
        """
        Test reading all settings files.
        """
        manager = settings_manager_with_temp_dir

        # Create some settings files
        files_content = {
            SettingsManager.GLOBAL_SETTINGS: "Global content",
            SettingsManager.NOVEL_BACKGROUND: "Background content",
            SettingsManager.CHARACTER_SETTINGS: "Character content",
        }

        for filename, content in files_content.items():
            manager.write_settings(filename, content, backup=False)

        # Get all settings
        all_settings = manager.get_all_settings()

        assert len(all_settings) == 3
        assert all_settings["global_settings"] == "Global content"
        assert all_settings["novel_background"] == "Background content"
        assert all_settings["character_settings"] == "Character content"

    def test_initialize_global_settings(self, settings_manager_with_temp_dir):
        """
        Test global settings initialization.
        """
        manager = settings_manager_with_temp_dir

        # Initialize settings
        manager.initialize_global_settings()

        # Check file exists
        file_path = os.path.join(manager.settings_dir, SettingsManager.GLOBAL_SETTINGS)
        assert os.path.exists(file_path)

        # Check content includes expected sections
        content = manager.read_settings(SettingsManager.GLOBAL_SETTINGS)
        assert "## Genre" in content
        assert "## Target Audience" in content
        assert "## Tone and Style" in content

    def test_initialize_global_settings_already_exists(
        self, settings_manager_with_temp_dir
    ):
        """
        Test that existing global settings are not overwritten.
        """
        manager = settings_manager_with_temp_dir

        # Create existing file
        existing_content = "Existing settings"
        manager.write_settings(
            SettingsManager.GLOBAL_SETTINGS, existing_content, backup=False
        )

        # Try to initialize again
        manager.initialize_global_settings()

        # Content should remain unchanged
        content = manager.read_settings(SettingsManager.GLOBAL_SETTINGS)
        assert content == existing_content

    @pytest.mark.asyncio
    async def test_compress_settings(self, settings_manager_with_temp_dir):
        """
        Test settings compression using LLM.
        """
        manager = settings_manager_with_temp_dir

        # Create a file to compress
        long_content = "This is a very long content. " * 100
        test_file = "test_compress.txt"
        manager.write_settings(test_file, long_content, backup=False)

        # Mock LLM response
        mock_response = LLMResponse(
            content="Compressed content", usage={"total_tokens": 50}
        )

        with patch.object(
            manager.llm_client, "generate", return_value=mock_response
        ) as mock_generate:
            compressed = await manager.compress_settings(test_file, target_ratio=0.5)

            assert compressed == "Compressed content"
            assert mock_generate.called

    @pytest.mark.asyncio
    async def test_check_and_compress_if_needed(self, settings_manager_with_temp_dir):
        """
        Test automatic compression check.
        """
        manager = settings_manager_with_temp_dir
        manager.compression_threshold = 0.8

        # Create a large file that needs compression
        large_content = "x" * 10000  # Will exceed threshold
        manager.write_settings(
            SettingsManager.NOVEL_BACKGROUND, large_content, backup=False
        )

        # Create a small file that doesn't need compression
        small_content = "Small content"
        manager.write_settings(
            SettingsManager.CHARACTER_SETTINGS, small_content, backup=False
        )

        # Mock compression
        async def mock_compress(filename):
            return "Compressed version"

        with patch.object(manager, "compress_settings", side_effect=mock_compress):
            compressed_files = await manager.check_and_compress_if_needed()

            # Only the large file should be compressed
            assert SettingsManager.NOVEL_BACKGROUND in compressed_files
            assert SettingsManager.CHARACTER_SETTINGS not in compressed_files

    def test_settings_directory_creation(self, temp_settings_dir):
        """
        Test that settings directory is created if it doesn't exist.
        """
        # Use a non-existent subdirectory
        new_dir = os.path.join(temp_settings_dir, "new_settings_dir")
        assert not os.path.exists(new_dir)

        # Create manager with new directory
        SettingsManager(settings_dir=new_dir)

        # Directory should now exist
        assert os.path.exists(new_dir)
