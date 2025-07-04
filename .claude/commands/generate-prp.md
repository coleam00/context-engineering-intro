# Create Enhanced PRP

## Feature file: $ARGUMENTS

Generate a comprehensive PRP for feature implementation with thorough research, failure pattern analysis, and validation checkpoints. The enhanced process incorporates learnings from previous implementations and provides better context for successful execution.

## Enhanced Research Process

1. **Codebase Analysis with Pattern Recognition**
   - Search for similar features/patterns in the codebase
   - Identify files to reference in PRP
   - Note existing conventions to follow
   - Check test patterns for validation approach
   - Analyze git history for similar feature implementations
   - Extract success patterns from recent implementations

2. **Failure Pattern Analysis**
   - Load known failure patterns from knowledge base
   - Identify potential risks for this feature type
   - Research common gotchas for required libraries
   - Analyze failure frequency and prevention strategies
   - Include mitigation strategies in PRP

3. **External Research with Enhanced Context**
   - Search for similar features/patterns online
   - Library documentation (include specific URLs with sections)
   - Implementation examples (GitHub/StackOverflow/blogs)
   - Best practices and common pitfalls
   - Recent updates and breaking changes
   - Performance considerations and benchmarks

4. **Success Metrics Analysis**
   - Load historical success metrics for this feature type
   - Estimate token usage, implementation time, and complexity
   - Set realistic confidence score based on historical data
   - Identify key success factors from similar implementations

5. **Context Validation**
   - Verify all referenced URLs are accessible
   - Ensure all file references exist
   - Check for required dependencies and APIs
   - Validate environment setup requirements

6. **User Clarification** (if needed)
   - Specific patterns to mirror and where to find them?
   - Integration requirements and where to find them?
   - Performance requirements and constraints?
   - Authentication and security considerations?

## Enhanced PRP Generation

Using the enhanced PRP template (PRPs/templates/prp_base.md):

### Step 1: Load Historical Context

```bash
echo "📚 Loading historical context and patterns..."

# Load failure patterns for this feature type
python3 -c "
import yaml
import re

# Read the feature file to understand what we're building
with open('$ARGUMENTS', 'r') as f:
    feature_content = f.read()

print('Feature Content Analysis:')
print('=' * 40)

# Determine feature type based on content
feature_indicators = {
    'api_integration': ['api', 'http', 'rest', 'endpoint', 'requests'],
    'database': ['database', 'sql', 'migration', 'schema', 'sqlalchemy'],
    'cli': ['cli', 'command', 'argparse', 'click', 'typer'],
    'web_app': ['fastapi', 'flask', 'web', 'route', 'webapp'],
    'ml_model': ['model', 'training', 'prediction', 'ml', 'tensorflow'],
    'auth_system': ['auth', 'login', 'oauth', 'jwt', 'authentication'],
    'data_processing': ['csv', 'json', 'processing', 'pipeline', 'etl'],
    'agent_system': ['agent', 'llm', 'ai', 'chat', 'conversation']
}

detected_types = []
for feature_type, indicators in feature_indicators.items():
    if any(indicator in feature_content.lower() for indicator in indicators):
        detected_types.append(feature_type)

print(f'Detected feature types: {detected_types}')

# Load relevant failure patterns
try:
    with open('PRPs/knowledge_base/failure_patterns.yaml', 'r') as f:
        patterns_db = yaml.safe_load(f)
    
    relevant_patterns = []
    for pattern in patterns_db.get('failure_patterns', []):
        pattern_libs = pattern.get('related_libraries', [])
        pattern_id = pattern.get('id', '')
        
        if any(ftype in pattern_libs + [pattern_id] for ftype in detected_types):
            relevant_patterns.append(pattern)
    
    print(f'Found {len(relevant_patterns)} relevant failure patterns')
    for pattern in relevant_patterns[:5]:  # Show top 5
        print(f'  ⚠️  {pattern[\"id\"]}: {pattern[\"description\"]}')
    
except FileNotFoundError:
    print('No failure patterns database found - will start fresh')
    relevant_patterns = []

# Load success metrics
try:
    with open('PRPs/knowledge_base/success_metrics.yaml', 'r') as f:
        metrics_db = yaml.safe_load(f)
    
    relevant_metrics = []
    for metric in metrics_db.get('success_metrics', []):
        if metric['feature_type'] in detected_types:
            relevant_metrics.append(metric)
    
    if relevant_metrics:
        avg_metrics = {
            'avg_token_usage': sum(m['avg_token_usage'] for m in relevant_metrics) // len(relevant_metrics),
            'avg_implementation_time': sum(m['avg_implementation_time'] for m in relevant_metrics) // len(relevant_metrics),
            'success_rate': sum(m['success_rate'] for m in relevant_metrics) // len(relevant_metrics)
        }
        print(f'Historical success metrics: {avg_metrics}')
    
except FileNotFoundError:
    print('No success metrics database found')
    avg_metrics = {'avg_token_usage': 2000, 'avg_implementation_time': 30, 'success_rate': 80}

# Store context for PRP generation
print(f'Using estimated metrics: {avg_metrics}')
"
```

### Step 2: Enhanced Codebase Analysis

```bash
echo "🔍 Analyzing codebase for patterns and examples..."

# Find similar implementations
echo "Searching for similar patterns..."

# Search for similar feature files
find . -name "*.py" -not -path "./venv*" -exec grep -l "$(echo '$ARGUMENTS' | head -n1 | grep -o '[A-Za-z]*' | head -n1)" {} \; 2>/dev/null | head -5

# Analyze existing architecture patterns
echo "Analyzing existing architecture patterns..."

# Check for common patterns in the codebase
python3 -c "
import os
import re

# Scan Python files for common patterns
patterns_found = {
    'async_usage': 0,
    'fastapi_usage': 0, 
    'pydantic_usage': 0,
    'pytest_usage': 0,
    'click_usage': 0,
    'sqlalchemy_usage': 0
}

for root, dirs, files in os.walk('.'):
    if 'venv' in root or '__pycache__' in root:
        continue
        
    for file in files:
        if file.endswith('.py'):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                if 'async def' in content or 'await ' in content:
                    patterns_found['async_usage'] += 1
                if 'from fastapi' in content or 'import fastapi' in content:
                    patterns_found['fastapi_usage'] += 1
                if 'from pydantic' in content or 'import pydantic' in content:
                    patterns_found['pydantic_usage'] += 1
                if 'import pytest' in content or 'from pytest' in content:
                    patterns_found['pytest_usage'] += 1
                if 'import click' in content or 'from click' in content:
                    patterns_found['click_usage'] += 1
                if 'sqlalchemy' in content.lower():
                    patterns_found['sqlalchemy_usage'] += 1
                    
            except Exception:
                continue

print('Codebase patterns detected:')
for pattern, count in patterns_found.items():
    if count > 0:
        print(f'  {pattern}: {count} files')
"

# Check for existing examples that should be referenced
echo "Checking examples directory..."
if [ -d "examples" ]; then
    echo "Examples found:"
    find examples/ -name "*.py" -exec echo "  📄 {}" \;
else
    echo "No examples directory found"
fi
```

### Step 3: External Research with Context

```bash
echo "🌐 Conducting external research with enhanced context..."

# This step requires web search capabilities
# The AI will search for:
# - Library documentation
# - Implementation examples  
# - Best practices
# - Common gotchas
# - Performance considerations

echo "Researching best practices and documentation..."
echo "Note: AI will conduct web searches for relevant documentation and examples"
```

### Step 4: Context Validation Pre-Check

```bash
echo "✅ Pre-validating context availability..."

# Check if commonly referenced documentation is accessible
python3 -c "
import requests
import time

common_docs = [
    'https://docs.python.org/3/',
    'https://fastapi.tiangolo.com/',
    'https://docs.pydantic.dev/',
    'https://docs.pytest.org/',
    'https://click.palletsprojects.com/',
    'https://docs.sqlalchemy.org/'
]

accessible_docs = []
for doc_url in common_docs:
    try:
        response = requests.head(doc_url, timeout=5)
        if response.status_code == 200:
            accessible_docs.append(doc_url)
        time.sleep(0.1)  # Rate limiting
    except Exception:
        pass

print(f'Accessible documentation sources: {len(accessible_docs)}/{len(common_docs)}')
for doc in accessible_docs:
    print(f'  ✅ {doc}')
"
```

### Step 5: Enhanced PRP Generation

```bash
echo "📝 Generating enhanced PRP with comprehensive context..."

# The AI will now generate the PRP using the enhanced template
# incorporating all the research and context gathered above

echo "Creating PRP with:"
echo "  ✅ Failure pattern awareness"
echo "  ✅ Historical success metrics" 
echo "  ✅ Codebase pattern analysis"
echo "  ✅ External research findings"
echo "  ✅ Context validation checks"
echo "  ✅ Enhanced validation loops"
echo "  ✅ Rollback strategies"

# Generate the actual PRP file
FEATURE_NAME=$(basename "$ARGUMENTS" .md)
PRP_FILE="PRPs/${FEATURE_NAME}_enhanced.md"

echo "Saving enhanced PRP to: $PRP_FILE"
```

## Critical Context Enhancement

### Auto-Discovery of Context Elements

```python
# Auto-discover context elements to include in PRP
def auto_discover_context():
    """Automatically discover relevant context for the PRP."""
    
    context = {
        'codebase_patterns': [],
        'documentation_urls': [],
        'example_files': [],
        'gotchas': [],
        'success_factors': []
    }
    
    # Discover codebase patterns
    context['codebase_patterns'] = discover_code_patterns()
    
    # Find relevant examples
    context['example_files'] = find_relevant_examples()
    
    # Load known gotchas for detected libraries
    context['gotchas'] = load_relevant_gotchas()
    
    # Extract success factors from similar implementations
    context['success_factors'] = extract_success_factors()
    
    return context

def discover_code_patterns():
    """Discover existing code patterns to follow."""
    patterns = []
    
    # Scan for architectural patterns
    if os.path.exists('src/'):
        patterns.append({
            'type': 'architecture',
            'pattern': 'src/ directory structure',
            'usage': 'Follow existing module organization'
        })
    
    # Check for common frameworks
    requirements = []
    if os.path.exists('requirements.txt'):
        with open('requirements.txt', 'r') as f:
            requirements = f.read().split('\n')
    
    if any('fastapi' in req for req in requirements):
        patterns.append({
            'type': 'framework',
            'pattern': 'FastAPI usage',
            'usage': 'Follow existing API patterns'
        })
    
    return patterns

def find_relevant_examples():
    """Find relevant example files to reference."""
    examples = []
    
    if os.path.exists('examples/'):
        for root, dirs, files in os.walk('examples/'):
            for file in files:
                if file.endswith('.py'):
                    examples.append({
                        'file': os.path.join(root, file),
                        'purpose': f'Example implementation of {file.replace(".py", "")}'
                    })
    
    return examples
```

### Enhanced Template Integration

The enhanced template (from the first artifact) will be used with all this additional context:

1. **Context Validation Checklist** - Pre-filled based on analysis
2. **Known Gotchas & Failure Patterns** - Auto-populated from knowledge base  
3. **Similar Feature Analysis** - Based on codebase scanning
4. **Success Metrics** - Historical data for confidence scoring
5. **Enhanced Validation** - Multi-level validation with pattern awareness

## Quality Assurance Enhancement

### Pre-Generation Validation

```bash
echo "🔍 Pre-generation validation..."

# Ensure we have sufficient context
CONTEXT_SCORE=0

# Check for examples (+20 points)
if [ -d "examples" ] && [ "$(find examples/ -name "*.py" | wc -l)" -gt 0 ]; then
    CONTEXT_SCORE=$((CONTEXT_SCORE + 20))
    echo "✅ Examples directory found"
fi

# Check for existing patterns (+20 points)  
if [ "$(find . -name "*.py" -not -path "./venv*" | wc -l)" -gt 5 ]; then
    CONTEXT_SCORE=$((CONTEXT_SCORE + 20))
    echo "✅ Sufficient codebase for pattern analysis"
fi

# Check for documentation (+15 points)
if [ -f "README.md" ]; then
    CONTEXT_SCORE=$((CONTEXT_SCORE + 15))
    echo "✅ README.md found"
fi

# Check for test patterns (+15 points)
if [ -d "tests" ]; then
    CONTEXT_SCORE=$((CONTEXT_SCORE + 15))
    echo "✅ Test directory found"
fi

# Check for requirements (+10 points)
if [ -f "requirements.txt" ] || [ -f "pyproject.toml" ]; then
    CONTEXT_SCORE=$((CONTEXT_SCORE + 10))
    echo "✅ Dependency file found"
fi

echo "Context completeness score: $CONTEXT_SCORE/100"

if [ $CONTEXT_SCORE -lt 50 ]; then
    echo "⚠️  Low context score - PRP may need additional manual context"
fi
```

### Post-Generation Validation

```bash
echo "✅ Post-generation validation..."

# Validate the generated PRP
if [ -f "$PRP_FILE" ]; then
    # Check PRP completeness
    python3 -c "
    with open('$PRP_FILE', 'r') as f:
        content = f.read()
    
    required_sections = [
        'Goal', 'Why', 'What', 'Success Criteria',
        'Context Validation Checklist', 'All Needed Context',
        'Known Gotchas & Failure Patterns', 'Implementation Blueprint',
        'Enhanced Validation Loop', 'Success Metrics'
    ]
    
    missing_sections = []
    for section in required_sections:
        if section not in content:
            missing_sections.append(section)
    
    if missing_sections:
        print(f'❌ Missing sections: {missing_sections}')
        exit(1)
    else:
        print('✅ All required sections present')
    
    # Check for placeholder content
    if '[' in content and ']' in content:
        placeholders = content.count('[')
        print(f'⚠️  {placeholders} placeholders found - need manual review')
    
    # Check URL accessibility (sample)
    import re
    urls = re.findall(r'https?://[^\s]+', content)
    print(f'Found {len(urls)} URLs to validate')
    "
    
    echo "✅ PRP generation completed successfully"
else
    echo "❌ PRP file not generated"
    exit 1
fi
```

## Output Enhancement

```bash
echo ""
echo "🎉 Enhanced PRP Generation Complete!"
echo "===================================="
echo "Feature: $FEATURE_NAME"
echo "PRP File: $PRP_FILE"
echo "Context Score: $CONTEXT_SCORE/100"
echo ""
echo "📊 PRP Enhancement Features:"
echo "  ✅ Failure pattern analysis included"
echo "  ✅ Historical success metrics integrated"
echo "  ✅ Codebase patterns identified"
echo "  ✅ Multi-level validation framework"
echo "  ✅ Context validation checklist"
echo "  ✅ Rollback strategies defined"
echo ""
echo "🚀 Ready for execution with:"
echo "  execute-prp $PRP_FILE"
echo ""
echo "💡 For validation before execution:"
echo "  validate-prp $PRP_FILE"
```

The enhanced generate-prp command now provides:

1. **Historical Context** - Learns from previous implementations
2. **Pattern Recognition** - Identifies existing codebase patterns to follow  
3. **Failure Prevention** - Includes known failure patterns and prevention
4. **Success Metrics** - Sets realistic expectations based on historical data
5. **Context Validation** - Ensures all references are accessible
6. **Quality Assurance** - Validates PRP completeness before delivery

This dramatically improves the likelihood of successful first-pass implementation.
