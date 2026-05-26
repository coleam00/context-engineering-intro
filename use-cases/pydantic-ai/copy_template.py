#!/usr/bin/env python3
"""
PydanticAI Template Copy Script

Copies the complete PydanticAI context engineering template to a target directory
for starting new PydanticAI agent development projects.

Usage:
    python copy_template.py <target_directory>

Example:
    python copy_template.py my-agent-project
    python copy_template.py /path/to/my-new-agent
"""

import os
import sys
import shutil
import argparse
from pathlib import Path
from typing import List, Tuple


def get_template_files() -> List[Tuple[str, str]]:
    """
    Get list of template files to copy with their relative paths.
    
    Returns:
        List of (source_path, relative_path) tuples
    """
    template_root = Path(__file__).parent
    files_to_copy = []
    
    # Core template files
    core_files = [
        "CLAUDE.md",
        "README.md",
    ]
    
    for file in core_files:
        source_path = template_root / file
        if source_path.exists():
            # Rename README.md to readme_template.md in target
            target_name = "README_TEMPLATE.md" if file == "README.md" else file
            files_to_copy.append((str(source_path), target_name))
    
    # Claude commands directory
    commands_dir = template_root / ".claude" / "commands"
    if commands_dir.exists():
        for file in commands_dir.glob("*.md"):
            rel_path = f".claude/commands/{file.name}"
            files_to_copy.append((str(file), rel_path))
    
    # PRPs directory
    prps_dir = template_root / "PRPs"
    if prps_dir.exists():
        # Copy templates subdirectory
        templates_dir = prps_dir / "templates"
        if templates_dir.exists():
            for file in templates_dir.glob("*.md"):
                rel_path = f"PRPs/templates/{file.name}"
                files_to_copy.append((str(file), rel_path))
        
        # Copy INITIAL.md example
        initial_file = prps_dir / "INITIAL.md"
        if initial_file.exists():
            files_to_copy.append((str(initial_file), "PRPs/INITIAL.md"))
    
    # Examples directory - copy all examples
    examples_dir = template_root / "examples"
    if examples_dir.exists():
        for example_dir in examples_dir.iterdir():
            if example_dir.is_dir():
                # Copy all files in each example directory
                for file in example_dir.rglob("*"):
                    if file.is_file():
                        rel_path = file.relative_to(template_root)
                        files_to_copy.append((str(file), str(rel_path)))
    
    return files_to_copy


def create_directory_structure(target_dir: Path, files: List[Tuple[str, str]]) -> None:
    """
    Create directory structure for all files.
    
    Args:
        target_dir: Target directory path
        files: List of (source_path, relative_path) tuples
    """
    directories = set()
    
    for _, rel_path in files:
        dir_path = target_dir / Path(rel_path).parent
        directories.add(dir_path)
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


def copy_template_files(target_dir: Path, files: List[Tuple[str, str]]) -> int:
    """
    Copy all template files to target directory.
    
    Args:
        target_dir: Target directory path
        files: List of (source_path, relative_path) tuples
    
    Returns:
        Number of files copied successfully
    """
    copied_count = 0
    
    for source_path, rel_path in files:
        target_path = target_dir / rel_path
        
        try:
            shutil.copy2(source_path, target_path)
            copied_count += 1
            print(f"  ✓ {rel_path}")
        except Exception as e:
            print(f"  ✗ {rel_path} - Error: {e}")
    
    return copied_count


def validate_template_integrity(target_dir: Path) -> bool:
    """
    Validate that essential template files were copied correctly.
    
    Args:
        target_dir: Target directory path
    
    Returns:
        True if template appears complete, False otherwise
    """
    essential_files = [
        "CLAUDE.md",
        "README_TEMPLATE.md",
        ".claude/commands/generate-pydantic-ai-prp.md",
        ".claude/commands/execute-pydantic-ai-prp.md",
        "PRPs/templates/prp_pydantic_ai_base.md",
        "PRPs/INITIAL.md",
        "examples/basic_chat_agent/agent.py",
        "examples/testing_examples/test_agent_patterns.py"
    ]
    
    missing_files = []
    for file_path in essential_files:
        if not (target_dir / file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n⚠️  Warning: Some essential files are missing:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    return True


def print_next_steps(target_dir: Path) -> None:
    """
    Print helpful next steps for using the template.
    
    Args:
        target_dir: Target directory path
    """
    print(f"""
🎉 PydanticAI template successfully copied to: {target_dir}

📋 Next Steps:

1. Navigate to your new project:
   cd {target_dir}

2. Set up your environment:
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate

   # Install packages ahead of time or let your AI coding assistant handle taht

3. Start building your agent:
   # 1. Edit PRPs/INITIAL.md with your agent requirements
   # 2. Generate PRP: /generate-pydantic-ai-prp PRPs/INITIAL.md
   # 3. Execute PRP: /execute-pydantic-ai-prp PRPs/generated_prp.md

5. Read the documentation:
   # Check README.md for complete usage guide
   # Check CLAUDE.md for PydanticAI development rules

🔗 Useful Resources:
   - PydanticAI Docs: https://ai.pydantic.dev/
   - Examples: See examples/ directory
   - Testing: See examples/testing_examples/

Happy agent building! 🤖
""")


def main():
    """Main function for the copy template script."""
    parser = argparse.ArgumentParser(
        description="Copy PydanticAI context engineering template to a new project directory",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python copy_template.py my-agent-project
  python copy_template.py /path/to/my-new-agent
  python copy_template.py ../customer-support-agent
        """
    )
    
    parser.add_argument(
        "target_directory",
        help="Target directory for the new PydanticAI project"
    )
    
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite target directory if it exists"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be copied without actually copying"
    )
    
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    args = parser.parse_args()
    
    # Convert target directory to Path object
    target_dir = Path(args.target_directory).resolve()
    
    # Check if target directory exists
    if target_dir.exists():
        if target_dir.is_file():
            print(f"❌ Error: {target_dir} is a file, not a directory")
            return
        
        if list(target_dir.iterdir()) and not args.force:
            print(f"❌ Error: {target_dir} is not empty")
            print("Use --force to overwrite existing directory")
            return
        
        if args.force and not args.dry_run:
            print(f"⚠️  Overwriting existing directory: {target_dir}")
    
    # Get list of files to copy
    print("📂 Scanning PydanticAI template files...")
    files_to_copy = get_template_files()
    
    if not files_to_copy:
        print("❌ Error: No template files found. Make sure you're running this from the template directory.")
        return
    
    print(f"Found {len(files_to_copy)} files to copy")
    
    if args.dry_run:
        print(f"\n🔍 Dry run - would copy to: {target_dir}")
        for _, rel_path in files_to_copy:
            print(f"  → {rel_path}")
        return
    
    # Create target directory and structure
    print(f"\n📁 Creating directory structure in: {target_dir}")
    target_dir.mkdir(parents=True, exist_ok=True)
    create_directory_structure(target_dir, files_to_copy)
    
    # Copy files
    print(f"\n📋 Copying template files:")
    copied_count = copy_template_files(target_dir, files_to_copy)
    
    # Validate template integrity
    print(f"\n✅ Copied {copied_count}/{len(files_to_copy)} files successfully")
    
    if validate_template_integrity(target_dir):
        print("✅ Template integrity check passed")
        print_next_steps(target_dir)
    else:
        print("⚠️  Template may be incomplete. Check for missing files.")


if __name__ == "__main__":
    main()