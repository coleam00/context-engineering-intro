#!/usr/bin/env python3
"""
MCP Server Template Copy Script

Copies the complete MCP server context engineering template to a target directory
for starting new MCP server development projects. Uses gitignore-aware copying
to avoid copying build artifacts and dependencies.

Usage:
    python copy_template.py <target_directory>

Example:
    python copy_template.py my-mcp-server
    python copy_template.py /path/to/my-new-server
"""

import os
import sys
import shutil
import argparse
from pathlib import Path
from typing import List, Tuple, Set
import fnmatch


def parse_gitignore(gitignore_path: Path) -> Set[str]:
    """
    Parse .gitignore file and return set of patterns to ignore.
    
    Args:
        gitignore_path: Path to .gitignore file
        
    Returns:
        Set of gitignore patterns
    """
    ignore_patterns = set()
    
    if not gitignore_path.exists():
        return ignore_patterns
    
    try:
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Skip empty lines and comments
                if line and not line.startswith('#'):
                    # Remove leading slash for consistency
                    pattern = line.lstrip('/')
                    ignore_patterns.add(pattern)
    except Exception as e:
        print(f"Warning: Could not read .gitignore: {e}")
    
    return ignore_patterns


def should_ignore_path(path: Path, template_root: Path, ignore_patterns: Set[str]) -> bool:
    """
    Check if a path should be ignored based on gitignore patterns.
    
    Args:
        path: Path to check
        template_root: Root directory of template
        ignore_patterns: Set of gitignore patterns
        
    Returns:
        True if path should be ignored, False otherwise
    """
    # Get relative path from template root
    try:
        rel_path = path.relative_to(template_root)
    except ValueError:
        return False
    
    # Convert to string with forward slashes
    rel_path_str = str(rel_path).replace('\\', '/')
    
    # Check against each ignore pattern
    for pattern in ignore_patterns:
        # Handle directory patterns (ending with /)
        if pattern.endswith('/'):
            pattern = pattern.rstrip('/')
            if rel_path_str.startswith(pattern + '/') or rel_path_str == pattern:
                return True
        # Handle glob patterns
        elif fnmatch.fnmatch(rel_path_str, pattern):
            return True
        # Handle exact matches and prefix matches
        elif rel_path_str == pattern or rel_path_str.startswith(pattern + '/'):
            return True
    
    return False


def get_template_files() -> List[Tuple[str, str]]:
    """
    Get list of template files to copy with their relative paths.
    Uses gitignore-aware filtering to exclude build artifacts and dependencies.
    
    Returns:
        List of (source_path, relative_path) tuples
    """
    template_root = Path(__file__).parent
    files_to_copy = []
    
    # Parse .gitignore patterns
    gitignore_path = template_root / '.gitignore'
    ignore_patterns = parse_gitignore(gitignore_path)
    
    # Add the copy_template.py script itself to ignore patterns
    ignore_patterns.add('copy_template.py')
    
    # Walk through all files in template directory
    for root, dirs, files in os.walk(template_root):
        root_path = Path(root)
        
        # Filter out ignored directories
        dirs[:] = [d for d in dirs if not should_ignore_path(root_path / d, template_root, ignore_patterns)]
        
        for file in files:
            file_path = root_path / file
            
            # Skip if file should be ignored
            if should_ignore_path(file_path, template_root, ignore_patterns):
                continue
            
            # Get relative path for target
            rel_path = file_path.relative_to(template_root)
            
            # Rename README.md to README_TEMPLATE.md
            if rel_path.name == 'README.md':
                target_rel_path = rel_path.parent / 'README_TEMPLATE.md'
            else:
                target_rel_path = rel_path
            
            files_to_copy.append((str(file_path), str(target_rel_path)))
    
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
        if str(dir_path) != str(target_dir):  # Don't add root directory
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
        ".claude/commands/prp-mcp-create.md",
        ".claude/commands/prp-mcp-execute.md",
        "PRPs/templates/prp_mcp_base.md",
        "PRPs/INITIAL.md",
        "package.json",
        "tsconfig.json",
        "src/index.ts",
        "src/types.ts"
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
🎉 MCP Server template successfully copied to: {target_dir}

📋 Next Steps:

1. Navigate to your new project:
   cd {target_dir}

2. Install dependencies:
   npm install

3. Set up your environment:
   # Copy environment template (if needed)
   cp .env.example .env
   # Edit .env with your configuration

4. Start building your MCP server:
   # 1. Edit PRPs/INITIAL.md with your server requirements
   # 2. Generate PRP: /prp-mcp-create PRPs/INITIAL.md
   # 3. Execute PRP: /prp-mcp-execute PRPs/generated_prp.md

5. Development workflow:
   # Run tests
   npm test
   
   # Start development server
   npm run dev
   
   # Build for production
   npm run build

6. Read the documentation:
   # Check README_TEMPLATE.md for complete usage guide
   # Check CLAUDE.md for MCP development rules

🔗 Useful Resources:
   - MCP Specification: https://spec.modelcontextprotocol.io/
   - Examples: See examples/ directory
   - Testing: See tests/ directory

Happy MCP server building! 🤖
""")


def main():
    """Main function for the copy template script."""
    parser = argparse.ArgumentParser(
        description="Copy MCP Server context engineering template to a new project directory",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python copy_template.py my-mcp-server
  python copy_template.py /path/to/my-new-server
  python copy_template.py ../customer-support-mcp
        """
    )
    
    parser.add_argument(
        "target_directory",
        help="Target directory for the new MCP server project"
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
    print("📂 Scanning MCP server template files...")
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