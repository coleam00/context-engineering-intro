"""
CLI entry point for the novel extractor.
"""

import click
import asyncio
import logging
import sys
from pathlib import Path

from .extractor import NovelExtractor
from .settings_manager import SettingsManager
from config.settings import get_settings

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@click.group()
@click.version_option(version="0.1.0", prog_name="novel-extractor")
def cli():
    """
    Novel Extractor - AI-powered novel structure extraction tool.
    """
    pass


@cli.command()
def init():
    """
    Initialize settings directory and global settings file.
    """
    click.echo("Initializing novel extractor settings...")

    try:
        settings_manager = SettingsManager()
        settings_manager.initialize_global_settings()

        click.echo(f"✓ Created settings directory: {settings_manager.settings_dir}")
        click.echo(f"✓ Created global settings file: {SettingsManager.GLOBAL_SETTINGS}")
        click.echo(
            "\nPlease edit settings/global_settings.txt to configure your preferences."
        )

    except Exception as e:
        click.echo(f"✗ Error during initialization: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("novel_path", type=click.Path(exists=True))
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
def extract(novel_path: str, verbose: bool):
    """
    Extract structure from a novel file.

    NOVEL_PATH: Path to the novel text file
    """
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    click.echo(f"Extracting structure from: {novel_path}")

    # Check if global settings exists
    settings_manager = SettingsManager()
    global_settings_path = (
        Path(settings_manager.settings_dir) / SettingsManager.GLOBAL_SETTINGS
    )

    if not global_settings_path.exists():
        click.echo("✗ Global settings not found. Please run 'init' first.", err=True)
        sys.exit(1)

    # Progress callback
    def progress_callback(status: str, progress: float):
        click.echo(f"{status} [{int(progress * 100)}%]")

    # Run extraction
    try:
        extractor = NovelExtractor()

        # Run async extraction
        result = asyncio.run(
            extractor.extract_novel_structure(novel_path, progress_callback)
        )

        click.echo("\n✓ Extraction completed successfully!")
        click.echo(f"  Title: {result.metadata.title}")
        click.echo(f"  Word count: {result.metadata.word_count:,}")
        click.echo(f"\nSettings files created in: {settings_manager.settings_dir}/")

    except FileNotFoundError as e:
        click.echo(f"✗ File error: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"✗ Extraction failed: {e}", err=True)
        if verbose:
            import traceback

            traceback.print_exc()
        sys.exit(1)


@cli.command()
def show():
    """
    Display current settings files.
    """
    settings_manager = SettingsManager()
    settings_dict = settings_manager.get_all_settings()

    if not settings_dict:
        click.echo("No settings files found.")
        return

    for filename, content in settings_dict.items():
        click.echo(f"\n=== {filename.upper()} ===")
        click.echo(content[:500] + "..." if len(content) > 500 else content)
        click.echo(f"\n[Full content: {len(content)} characters]")


@cli.command()
@click.option(
    "--threshold", "-t", type=float, default=0.8, help="Compression threshold (0-1)"
)
@click.option(
    "--file",
    "-f",
    type=click.Choice(["background", "character", "plot", "all"]),
    default="all",
    help="Which file(s) to compress",
)
def compress(threshold: float, file: str):
    """
    Compress settings files that exceed token threshold.
    """
    settings_manager = SettingsManager()

    # Update threshold if different from config
    if threshold != settings_manager.compression_threshold:
        settings_manager.compression_threshold = threshold

    click.echo(f"Checking files with threshold: {threshold}")

    async def run_compression():
        if file == "all":
            compressed = await settings_manager.check_and_compress_if_needed()
        else:
            filename = f"{file}_settings.txt"
            try:
                compressed_content = await settings_manager.compress_settings(filename)
                settings_manager.write_settings(filename, compressed_content)
                compressed = [filename]
            except FileNotFoundError:
                click.echo(f"✗ File not found: {filename}", err=True)
                return []

        return compressed

    try:
        compressed_files = asyncio.run(run_compression())

        if compressed_files:
            click.echo(f"✓ Compressed {len(compressed_files)} file(s):")
            for f in compressed_files:
                click.echo(f"  - {f}")
        else:
            click.echo("No files needed compression.")

    except Exception as e:
        click.echo(f"✗ Compression failed: {e}", err=True)
        sys.exit(1)


@cli.command()
def config():
    """
    Display current configuration.
    """
    try:
        settings = get_settings()

        click.echo("Current Configuration:")
        click.echo(f"  LLM Provider: {settings.llm_provider}")
        click.echo(f"  Model: {settings.llm_model}")
        click.echo(f"  Max Context: {settings.max_context_length} tokens")
        click.echo(f"  Compression Threshold: {settings.compression_threshold}")
        click.echo(f"  Settings Directory: {settings.settings_path}")

    except Exception as e:
        click.echo(f"✗ Could not load configuration: {e}", err=True)
        click.echo("Please ensure .env file is properly configured.")
        sys.exit(1)


if __name__ == "__main__":
    cli()
