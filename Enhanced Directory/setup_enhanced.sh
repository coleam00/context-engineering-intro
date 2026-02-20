#!/bin/bash

# Enhanced Context Engineering Setup Script
# Run this script in your project root directory

echo "🚀 Setting up Enhanced Context Engineering..."

# Create new directories
echo "Creating directory structure..."
mkdir -p PRPs/knowledge_base
mkdir -p PRPs/analysis_reports
mkdir -p .claude/commands

# Create Python requirements file
echo "Creating requirements.txt..."
cat > requirements.txt << 'EOF'
# Enhanced Context Engineering Dependencies
pyyaml>=6.0
requests>=2.25.0
python-dotenv>=0.19.0
click>=8.0.0
EOF

# Create .gitignore additions for new files
echo "Updating .gitignore..."
cat >> .gitignore << 'EOF'

# Enhanced Context Engineering
PRPs/analysis_reports/*.yaml
PRPs/analysis_reports/*.json
.env
context_engineering_cache/
EOF

# Create initial knowledge base files
echo "Creating initial knowledge base files..."

# This will be replaced with actual YAML content
cat > PRPs/knowledge_base/failure_patterns.yaml << 'EOF'
failure_patterns: []
EOF

cat > PRPs/knowledge_base/success_metrics.yaml << 'EOF'
success_metrics: []
EOF

cat > PRPs/knowledge_base/template_versions.yaml << 'EOF'
template_versions: []
EOF

cat > PRPs/knowledge_base/library_gotchas.yaml << 'EOF'
library_gotchas: {}
EOF

# Create .env.example
cat > .env.example << 'EOF'
# Enhanced Context Engineering Configuration
CE_PROJECT_NAME=my_project
CE_TEAM_SIZE=5
CE_COMPLEXITY_THRESHOLD=7

# Analytics (optional)
CE_ANALYTICS_ENABLED=false
CE_REPORT_ENDPOINT=

# Performance Tuning
CE_CONTEXT_CACHE_TTL=3600
CE_VALIDATION_TIMEOUT=300
EOF

echo "✅ Directory structure created!"
echo ""
echo "Next steps:"
echo "1. Install Python dependencies: pip install -r requirements.txt"
echo "2. Copy the enhanced files from Claude artifacts"
echo "3. Initialize knowledge base: python context_engineering_utils.py init"
echo "4. Test the system: /validate-prp INITIAL.md"
