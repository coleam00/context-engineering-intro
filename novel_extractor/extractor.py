"""
Main extraction logic for novel structure analysis.
"""

import os
import logging
from typing import Dict, Optional
from pathlib import Path

from .llm_client import LLMClient
from .context_manager import ContextManager
from .settings_manager import SettingsManager
from .prompts import EXTRACTION_SYSTEM_PROMPT, get_extraction_prompt
from .models import NovelMetadata, NovelStructure

logger = logging.getLogger(__name__)


class NovelExtractor:
    """
    Orchestrates the novel structure extraction process.
    """

    def __init__(
        self,
        settings_manager: Optional[SettingsManager] = None,
        llm_client: Optional[LLMClient] = None,
        context_manager: Optional[ContextManager] = None,
    ):
        """
        Initialize the extractor.

        Args:
            settings_manager: Settings file manager
            llm_client: LLM API client
            context_manager: Context window manager
        """
        self.settings_manager = settings_manager or SettingsManager()
        self.llm_client = llm_client or LLMClient()
        self.context_manager = context_manager or ContextManager()

    async def extract_novel_structure(
        self, novel_path: str, progress_callback: Optional[callable] = None
    ) -> NovelStructure:
        """
        Extract complete structure from a novel file.

        Args:
            novel_path: Path to novel text file
            progress_callback: Optional callback for progress updates

        Returns:
            NovelStructure: Extracted novel structure
        """
        # Validate novel file
        if not os.path.exists(novel_path):
            raise FileNotFoundError(f"Novel file not found: {novel_path}")

        # Read novel content
        novel_text = self._read_novel(novel_path)
        metadata = self._create_metadata(novel_path, novel_text)

        logger.info(f"Starting extraction for: {metadata.title}")

        # Read existing settings
        settings_dict = self.settings_manager.get_all_settings()

        # Extract components
        progress_steps = [
            ("Extracting background...", self._extract_background),
            ("Extracting characters...", self._extract_characters),
            ("Extracting plot structure...", self._extract_plot),
            ("Analyzing writing style...", self._extract_style),
        ]

        for i, (status, extract_func) in enumerate(progress_steps):
            if progress_callback:
                progress_callback(status, i / len(progress_steps))

            await extract_func(novel_text, settings_dict)

            # Check and compress if needed after each extraction
            compressed = await self.settings_manager.check_and_compress_if_needed()
            if compressed:
                logger.info(f"Compressed files: {', '.join(compressed)}")
                # Reload settings after compression
                settings_dict = self.settings_manager.get_all_settings()

        if progress_callback:
            progress_callback("Extraction complete!", 1.0)

        # Build final structure (simplified for now)
        return NovelStructure(
            metadata=metadata,
            theme="Extracted themes stored in settings files",
            setting="Extracted setting stored in settings files",
            timeline="Extracted timeline stored in settings files",
            narrative_style="Extracted style stored in settings files",
            point_of_view="Extracted POV stored in settings files",
            characters=[],  # Would be parsed from character_settings.txt
            plot_points=[],  # Would be parsed from plot_settings.txt
        )

    def _read_novel(self, novel_path: str) -> str:
        """
        Read novel file with proper encoding handling.

        Args:
            novel_path: Path to novel file

        Returns:
            str: Novel text content
        """
        # Try different encodings
        encodings = ["utf-8", "utf-8-sig", "latin-1", "cp1252"]

        for encoding in encodings:
            try:
                with open(novel_path, "r", encoding=encoding) as f:
                    content = f.read()
                logger.info(f"Successfully read novel with {encoding} encoding")
                return content
            except UnicodeDecodeError:
                continue

        raise ValueError("Could not read novel file with any supported encoding")

    def _create_metadata(self, novel_path: str, novel_text: str) -> NovelMetadata:
        """
        Create metadata for the novel.

        Args:
            novel_path: Path to novel file
            novel_text: Novel content

        Returns:
            NovelMetadata: Novel metadata
        """
        path = Path(novel_path)
        word_count = len(novel_text.split())

        return NovelMetadata(
            title=path.stem,
            author=None,  # Could be extracted from content
            word_count=word_count,
            file_path=str(path.absolute()),
        )

    async def _extract_background(
        self, novel_text: str, settings_dict: Dict[str, str]
    ) -> None:
        """
        Extract background information from the novel.

        Args:
            novel_text: Novel content
            settings_dict: Current settings
        """
        prompt = get_extraction_prompt("background")

        # Prepare content with context management
        content, truncated = self.context_manager.fit_content(
            settings_dict, novel_text, EXTRACTION_SYSTEM_PROMPT
        )

        if truncated:
            logger.warning("Novel was truncated for background extraction")

        messages = [
            self.llm_client.create_message("system", EXTRACTION_SYSTEM_PROMPT),
            self.llm_client.create_message("user", f"{prompt}\n\n{content}"),
        ]

        response = await self.llm_client.generate(messages, temperature=0.3)

        self.settings_manager.write_settings(
            SettingsManager.NOVEL_BACKGROUND, response.content
        )

        logger.info("Background extraction completed")

    async def _extract_characters(
        self, novel_text: str, settings_dict: Dict[str, str]
    ) -> None:
        """
        Extract character information from the novel.

        Args:
            novel_text: Novel content
            settings_dict: Current settings
        """
        prompt = get_extraction_prompt("character")

        content, truncated = self.context_manager.fit_content(
            settings_dict, novel_text, EXTRACTION_SYSTEM_PROMPT
        )

        if truncated:
            logger.warning("Novel was truncated for character extraction")

        messages = [
            self.llm_client.create_message("system", EXTRACTION_SYSTEM_PROMPT),
            self.llm_client.create_message("user", f"{prompt}\n\n{content}"),
        ]

        response = await self.llm_client.generate(messages, temperature=0.3)

        self.settings_manager.write_settings(
            SettingsManager.CHARACTER_SETTINGS, response.content
        )

        logger.info("Character extraction completed")

    async def _extract_plot(
        self, novel_text: str, settings_dict: Dict[str, str]
    ) -> None:
        """
        Extract plot structure from the novel.

        Args:
            novel_text: Novel content
            settings_dict: Current settings
        """
        prompt = get_extraction_prompt("plot")

        content, truncated = self.context_manager.fit_content(
            settings_dict, novel_text, EXTRACTION_SYSTEM_PROMPT
        )

        if truncated:
            logger.warning("Novel was truncated for plot extraction")

        messages = [
            self.llm_client.create_message("system", EXTRACTION_SYSTEM_PROMPT),
            self.llm_client.create_message("user", f"{prompt}\n\n{content}"),
        ]

        response = await self.llm_client.generate(messages, temperature=0.3)

        self.settings_manager.write_settings(
            SettingsManager.PLOT_SETTINGS, response.content
        )

        logger.info("Plot extraction completed")

    async def _extract_style(
        self, novel_text: str, settings_dict: Dict[str, str]
    ) -> None:
        """
        Extract writing style from the novel.

        Args:
            novel_text: Novel content
            settings_dict: Current settings
        """
        prompt = get_extraction_prompt("style")

        # For style analysis, we might want a sample rather than the whole text
        # Take first 10% of the novel for style analysis
        sample_size = len(novel_text) // 10
        style_sample = novel_text[:sample_size]

        content, truncated = self.context_manager.fit_content(
            settings_dict, style_sample, EXTRACTION_SYSTEM_PROMPT
        )

        messages = [
            self.llm_client.create_message("system", EXTRACTION_SYSTEM_PROMPT),
            self.llm_client.create_message("user", f"{prompt}\n\n{content}"),
        ]

        response = await self.llm_client.generate(messages, temperature=0.3)

        # Append style analysis to background
        current_background = self.settings_manager.read_settings(
            SettingsManager.NOVEL_BACKGROUND
        )
        updated_background = (
            f"{current_background}\n\n## Writing Style Analysis\n{response.content}"
        )

        self.settings_manager.write_settings(
            SettingsManager.NOVEL_BACKGROUND, updated_background
        )

        logger.info("Style analysis completed")
