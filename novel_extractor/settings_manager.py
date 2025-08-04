"""
Settings file management with automatic backup and compression.
"""

import os
import shutil
import logging
from typing import Dict, Optional, List
from datetime import datetime

from config.settings import get_settings
from .llm_client import LLMClient
from .context_manager import ContextManager

logger = logging.getLogger(__name__)


class SettingsManager:
    """
    Manages novel settings files with backup and compression capabilities.
    """

    # Settings file types
    GLOBAL_SETTINGS = "global_settings.txt"
    NOVEL_BACKGROUND = "novel_background.txt"
    CHARACTER_SETTINGS = "character_settings.txt"
    PLOT_SETTINGS = "plot_settings.txt"

    def __init__(self, settings_dir: Optional[str] = None):
        """
        Initialize settings manager.

        Args:
            settings_dir: Directory for settings files
        """
        config = get_settings()
        self.settings_dir = settings_dir or config.settings_dir
        self.compression_threshold = config.compression_threshold

        # Create settings directory if it doesn't exist
        os.makedirs(self.settings_dir, exist_ok=True)

        self.llm_client = LLMClient()
        self.context_manager = ContextManager()

    def read_settings(self, filename: str) -> str:
        """
        Read settings file content.

        Args:
            filename: Settings file name

        Returns:
            str: File content

        Raises:
            FileNotFoundError: If file doesn't exist
        """
        file_path = os.path.join(self.settings_dir, filename)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Settings file not found: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        return content

    def write_settings(self, filename: str, content: str, backup: bool = True) -> None:
        """
        Write content to settings file with optional backup.

        Args:
            filename: Settings file name
            content: Content to write
            backup: Whether to create backup
        """
        file_path = os.path.join(self.settings_dir, filename)

        # Create backup if requested and file exists
        if backup and os.path.exists(file_path):
            self._create_backup(file_path)

        # Write new content
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        logger.info(f"Updated settings file: {filename}")

    def _create_backup(self, file_path: str) -> str:
        """
        Create backup of settings file.

        Args:
            file_path: Path to file to backup

        Returns:
            str: Path to backup file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{file_path}.backup_{timestamp}"

        shutil.copy2(file_path, backup_path)
        logger.info(f"Created backup: {backup_path}")

        return backup_path

    async def compress_settings(self, filename: str, target_ratio: float = 0.7) -> str:
        """
        Compress settings file using LLM while preserving key information.

        Args:
            filename: Settings file to compress
            target_ratio: Target compression ratio

        Returns:
            str: Compressed content
        """
        content = self.read_settings(filename)
        original_tokens = self.context_manager.count_tokens(content)

        compression_prompt = f"""You are compressing a novel settings file. 
Your task is to reduce the content to approximately {int(target_ratio * 100)}% of its original size 
while preserving ALL critical information.

Guidelines:
- Keep all character names, relationships, and key traits
- Preserve all plot points and their sequence
- Maintain setting details and world-building elements
- Remove redundant descriptions and verbose explanations
- Use concise language while keeping meaning intact
- Do NOT add new information or interpretations

Original content:
{content}

Provide the compressed version below:"""

        messages = [
            self.llm_client.create_message(
                "system", "You are a precise text compression assistant."
            ),
            self.llm_client.create_message("user", compression_prompt),
        ]

        response = await self.llm_client.generate(messages, temperature=0.3)
        compressed_content = response.content

        # Verify compression ratio
        compressed_tokens = self.context_manager.count_tokens(compressed_content)
        actual_ratio = compressed_tokens / original_tokens

        logger.info(
            f"Compressed {filename}: {original_tokens} -> {compressed_tokens} tokens "
            f"(ratio: {actual_ratio:.2f})"
        )

        return compressed_content

    def get_all_settings(self) -> Dict[str, str]:
        """
        Read all settings files into a dictionary.

        Returns:
            Dict[str, str]: Settings file contents
        """
        settings_dict = {}

        for filename in [
            self.GLOBAL_SETTINGS,
            self.NOVEL_BACKGROUND,
            self.CHARACTER_SETTINGS,
            self.PLOT_SETTINGS,
        ]:
            try:
                content = self.read_settings(filename)
                settings_dict[filename.replace(".txt", "")] = content
            except FileNotFoundError:
                logger.debug(f"Settings file not found: {filename}")

        return settings_dict

    async def check_and_compress_if_needed(self) -> List[str]:
        """
        Check all settings files and compress if they exceed threshold.

        Returns:
            List[str]: Files that were compressed
        """
        compressed_files = []
        settings = get_settings()
        max_tokens = int(settings.max_context_length * self.compression_threshold)

        for filename in [
            self.NOVEL_BACKGROUND,
            self.CHARACTER_SETTINGS,
            self.PLOT_SETTINGS,
        ]:
            try:
                content = self.read_settings(filename)
                tokens = self.context_manager.count_tokens(content)

                if tokens > max_tokens:
                    logger.info(
                        f"{filename} exceeds threshold ({tokens} > {max_tokens}), compressing..."
                    )
                    compressed = await self.compress_settings(filename)
                    self.write_settings(filename, compressed)
                    compressed_files.append(filename)

            except FileNotFoundError:
                continue

        return compressed_files

    def initialize_global_settings(
        self, template_content: Optional[str] = None
    ) -> None:
        """
        Initialize global settings file with template.

        Args:
            template_content: Optional template content
        """
        if os.path.exists(os.path.join(self.settings_dir, self.GLOBAL_SETTINGS)):
            logger.info("Global settings already exists")
            return

        default_template = """# Global Novel Settings
# This file contains user-defined settings for novel generation

## Genre
[Specify the genre: fantasy, sci-fi, mystery, romance, etc.]

## Target Audience
[Age group and reader preferences]

## Tone and Style
[Writing style preferences: formal, casual, humorous, dark, etc.]

## Length
[Target word count or chapter count]

## Additional Requirements
[Any specific requirements or constraints]
"""

        content = template_content or default_template
        self.write_settings(self.GLOBAL_SETTINGS, content, backup=False)
        logger.info("Initialized global settings file")
