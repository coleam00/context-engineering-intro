#!/usr/bin/env python3
"""
Context Engineering Utilities
Helper functions for enhanced PRP generation, validation, and analysis.
"""

import os
import re
import yaml
import json
import subprocess
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path


class ContextEngineeringUtils:
    """Utility class for context engineering operations."""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.knowledge_base_path = self.project_root / "PRPs" / "knowledge_base"
        self.ensure_knowledge_base_exists()
    
    def ensure_knowledge_base_exists(self):
        """Ensure knowledge base directory and files exist."""
        self.knowledge_base_path.mkdir(parents=True, exist_ok=True)
        
        # Create default files if they don't exist
        default_files = {
            "failure_patterns.yaml": {"failure_patterns": []},
            "success_metrics.yaml": {"success_metrics": []},
            "template_versions.yaml": {"template_versions": []},
            "library_gotchas.yaml": {"library_gotchas": {}}
        }
        
        for filename, default_content in default_files.items():
            file_path = self.knowledge_base_path / filename
            if not file_path.exists():
                with open(file_path, 'w') as f:
                    yaml.dump(default_content, f, default_flow_style=False)
    
    def load_failure_patterns(self) -> List[Dict[str, Any]]:
        """Load failure patterns from knowledge base."""
        try:
            with open(self.knowledge_base_path / "failure_patterns.yaml", 'r') as f:
                data = yaml.safe_load(f) or {}
                return data.get('failure_patterns', [])
        except FileNotFoundError:
            return []
    
    def load_success_metrics(self) -> List[Dict[str, Any]]:
        """Load success metrics from knowledge base."""
        try:
            with open(self.knowledge_base_path / "success_metrics.yaml", 'r') as f:
                data = yaml.safe_load(f) or {}
                return data.get('success_metrics', [])
        except FileNotFoundError:
            return []
    
    def load_library_gotchas(self) -> Dict[str, List[Dict[str, str]]]:
        """Load library-specific gotchas."""
        try:
            with open(self.knowledge_base_path / "library_gotchas.yaml", 'r') as f:
                data = yaml.safe_load(f) or {}
                return data.get('library_gotchas', {})
        except FileNotFoundError:
            return {}
    
    def detect_feature_type(self, content: str) -> List[str]:
        """Detect feature type from content."""
        feature_indicators = {
            'api_integration': ['api', 'http', 'rest', 'endpoint', 'requests', 'aiohttp', 'httpx'],
            'database': ['database', 'sql', 'migration', 'schema', 'sqlalchemy', 'postgres', 'sqlite'],
            'cli': ['cli', 'command', 'argparse', 'click', 'typer', 'terminal'],
            'web_app': ['fastapi', 'flask', 'web', 'route', 'webapp', 'server'],
            'ml_model': ['model', 'training', 'prediction', 'ml', 'tensorflow', 'pytorch', 'sklearn'],
            'auth_system': ['auth', 'login', 'oauth', 'jwt', 'authentication', 'authorization'],
            'data_processing': ['csv', 'json', 'processing', 'pipeline', 'etl', 'pandas'],
            'agent_system': ['agent', 'llm', 'ai', 'chat', 'conversation', 'pydantic-ai']
        }
        
        detected_types = []
        content_lower = content.lower()
        
        for feature_type, indicators in feature_indicators.items():
            if any(indicator in content_lower for indicator in indicators):
                detected_types.append(feature_type)
        
        return detected_types
    
    def get_relevant_failure_patterns(self, feature_types: List[str]) -> List[Dict[str, Any]]:
        """Get failure patterns relevant to feature types."""
        all_patterns = self.load_failure_patterns()
        relevant_patterns = []
        
        for pattern in all_patterns:
            related_libs = pattern.get('related_libraries', [])
            pattern_id = pattern.get('id', '')
            
            if (any(ftype in related_libs for ftype in feature_types) or 
                any(ftype in pattern_id for ftype in feature_types) or
                '*' in related_libs):
                relevant_patterns.append(pattern)
        
        # Sort by frequency and recency
        relevant_patterns.sort(key=lambda x: (
            x.get('frequency_count', 0),
            x.get('last_seen', '2020-01-01')
        ), reverse=True)
        
        return relevant_patterns
    
    def get_relevant_success_metrics(self, feature_types: List[str]) -> Dict[str, Any]:
        """Get success metrics for feature types."""
        all_metrics = self.load_success_metrics()
        relevant_metrics = [m for m in all_metrics if m['feature_type'] in feature_types]
        
        if not relevant_metrics:
            # Return default metrics
            return {
                'avg_token_usage': 2000,
                'avg_implementation_time': 30,
                'success_rate': 80,
                'confidence_accuracy': 75
            }
        
        # Calculate averages
        return {
            'avg_token_usage': sum(m['avg_token_usage'] for m in relevant_metrics) // len(relevant_metrics),
            'avg_implementation_time': sum(m['avg_implementation_time'] for m in relevant_metrics) // len(relevant_metrics),
            'success_rate': sum(m['success_rate'] for m in relevant_metrics) // len(relevant_metrics),
            'confidence_accuracy': sum(m.get('confidence_accuracy', 75) for m in relevant_metrics) // len(relevant_metrics)
        }
    
    def analyze_codebase_patterns(self) -> Dict[str, Any]:
        """Analyze existing codebase patterns."""
        patterns = {
            'architecture': [],
            'frameworks': [],
            'testing': [],
            'async_usage': 0,
            'total_python_files': 0
        }
        
        # Scan Python files
        for py_file in self.project_root.rglob("*.py"):
            if 'venv' in str(py_file) or '__pycache__' in str(py_file):
                continue
            
            patterns['total_python_files'] += 1
            
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for async usage
                if 'async def' in content or 'await ' in content:
                    patterns['async_usage'] += 1
                
                # Check for frameworks
                if 'from fastapi' in content or 'import fastapi' in content:
                    if 'fastapi' not in patterns['frameworks']:
                        patterns['frameworks'].append('fastapi')
                
                if 'from flask' in content or 'import flask' in content:
                    if 'flask' not in patterns['frameworks']:
                        patterns['frameworks'].append('flask')
                
                if 'import click' in content or 'from click' in content:
                    if 'click' not in patterns['frameworks']:
                        patterns['frameworks'].append('click')
                
                if 'import typer' in content or 'from typer' in content:
                    if 'typer' not in patterns['frameworks']:
                        patterns['frameworks'].append('typer')
                
            except Exception:
                continue
        
        # Check architecture patterns
        if (self.project_root / "src").exists():
            patterns['architecture'].append('src_directory_structure')
        
        if (self.project_root / "tests").exists():
            patterns['testing'].append('pytest_structure')
        
        if (self.project_root / "examples").exists():
            patterns['architecture'].append('examples_directory')
        
        return patterns
    
    def validate_url_accessibility(self, urls: List[str]) -> Dict[str, bool]:
        """Validate if URLs are accessible."""
        results = {}
        
        for url in urls:
            try:
                response = requests.head(url, timeout=5, allow_redirects=True)
                results[url] = response.status_code == 200
            except Exception:
                results[url] = False
        
        return results
    
    def collect_implementation_metrics(self, start_time: datetime) -> Dict[str, Any]:
        """Collect metrics from recent implementation."""
        end_time = datetime.now()
        implementation_time = (end_time - start_time).total_seconds() / 60
        
        # Git metrics
        git_metrics = self.get_git_metrics_since(start_time)
        
        # Test metrics
        test_metrics = self.get_test_metrics()
        
        # Code quality metrics
        quality_metrics = self.get_code_quality_metrics()
        
        return {
            'implementation_time_minutes': round(implementation_time, 1),
            'commits': git_metrics['commits'],
            'files_changed': git_metrics['files_changed'],
            'lines_added': git_metrics['lines_added'],
            'lines_deleted': git_metrics['lines_deleted'],
            'tests_passed': test_metrics['passed'],
            'tests_failed': test_metrics['failed'],
            'ruff_issues': quality_metrics['ruff_issues'],
            'mypy_errors': quality_metrics['mypy_errors']
        }
    
    def get_git_metrics_since(self, since_time: datetime) -> Dict[str, int]:
        """Get git metrics since a specific time."""
        since_str = since_time.strftime('%Y-%m-%d %H:%M:%S')
        
        try:
            # Count commits
            commits_output = subprocess.check_output([
                'git', 'rev-list', '--count', 'HEAD', f'--since={since_str}'
            ], text=True).strip()
            commits = int(commits_output) if commits_output else 0
            
            # Get changed files
            if commits > 0:
                files_output = subprocess.check_output([
                    'git', 'diff', '--name-only', f'HEAD~{commits}', 'HEAD'
                ], text=True).strip()
                files_changed = len(files_output.split('\n')) if files_output else 0
                
                # Get line changes
                stats_output = subprocess.check_output([
                    'git', 'diff', '--shortstat', f'HEAD~{commits}', 'HEAD'
                ], text=True).strip()
                
                lines_added = 0
                lines_deleted = 0
                if stats_output:
                    if 'insertion' in stats_output:
                        lines_added = int(re.search(r'(\d+) insertion', stats_output).group(1))
                    if 'deletion' in stats_output:
                        lines_deleted = int(re.search(r'(\d+) deletion', stats_output).group(1))
            else:
                files_changed = 0
                lines_added = 0
                lines_deleted = 0
            
            return {
                'commits': commits,
                'files_changed': files_changed,
                'lines_added': lines_added,
                'lines_deleted': lines_deleted
            }
        except Exception:
            return {'commits': 0, 'files_changed': 0, 'lines_added': 0, 'lines_deleted': 0}
    
    def get_test_metrics(self) -> Dict[str, int]:
        """Get test execution metrics."""
        try:
            result = subprocess.run([
                'python', '-m', 'pytest', 'tests/', '--tb=no', '-q'
            ], capture_output=True, text=True, timeout=60)
            
            output = result.stdout
            
            passed = 0
            failed = 0
            
            if 'passed' in output:
                passed_match = re.search(r'(\d+) passed', output)
                if passed_match:
                    passed = int(passed_match.group(1))
            
            if 'failed' in output:
                failed_match = re.search(r'(\d+) failed', output)
                if failed_match:
                    failed = int(failed_match.group(1))
            
            return {'passed': passed, 'failed': failed}
        except Exception:
            return {'passed': 0, 'failed': 0}
    
    def get_code_quality_metrics(self) -> Dict[str, int]:
        """Get code quality metrics."""
        metrics = {'ruff_issues': 0, 'mypy_errors': 0}
        
        # Ruff check
        try:
            result = subprocess.run([
                'ruff', 'check', '.'
            ], capture_output=True, text=True, timeout=30)
            
            if result.stdout:
                metrics['ruff_issues'] = len(result.stdout.strip().split('\n'))
        except Exception:
            pass
        
        # MyPy check
        try:
            result = subprocess.run([
                'mypy', '.'
            ], capture_output=True, text=True, timeout=30)
            
            if result.stdout:
                error_lines = [line for line in result.stdout.split('\n') if 'error:' in line]
                metrics['mypy_errors'] = len(error_lines)
        except Exception:
            pass
        
        return metrics
    
    def update_failure_patterns(self, new_patterns: List[Dict[str, Any]]):
        """Update failure patterns database."""
        existing_patterns = self.load_failure_patterns()
        
        for new_pattern in new_patterns:
            # Check if pattern already exists
            existing = next((p for p in existing_patterns if p.get('id') == new_pattern['id']), None)
            
            if existing:
                # Update existing pattern
                existing['last_seen'] = datetime.now().isoformat()
                existing['frequency_count'] = existing.get('frequency_count', 0) + 1
                # Update frequency category based on count
                if existing['frequency_count'] > 10:
                    existing['frequency'] = 'high'
                elif existing['frequency_count'] > 5:
                    existing['frequency'] = 'medium'
            else:
                # Add new pattern
                new_pattern.update({
                    'first_seen': datetime.now().isoformat(),
                    'last_seen': datetime.now().isoformat(),
                    'frequency_count': 1
                })
                existing_patterns.append(new_pattern)
        
        # Save updated patterns
        with open(self.knowledge_base_path / "failure_patterns.yaml", 'w') as f:
            yaml.dump({'failure_patterns': existing_patterns}, f, default_flow_style=False)
    
    def update_success_metrics(self, feature_type: str, metrics: Dict[str, Any]):
        """Update success metrics for a feature type."""
        existing_metrics = self.load_success_metrics()
        
        # Find existing entry for this feature type
        existing = next((m for m in existing_metrics if m['feature_type'] == feature_type), None)
        
        if existing:
            # Update running averages
            existing['implementations'] += 1
            n = existing['implementations']
            
            # Update averages
            for key in ['avg_token_usage', 'avg_implementation_time']:
                if key in metrics:
                    old_avg = existing[key]
                    new_value = metrics[key]
                    existing[key] = ((old_avg * (n - 1)) + new_value) / n
            
            # Update success rate
            if 'success' in metrics:
                success_value = 100 if metrics['success'] else 0
                old_rate = existing['success_rate']
                existing['success_rate'] = ((old_rate * (n - 1)) + success_value) / n
            
            existing['last_updated'] = datetime.now().isoformat()
        else:
            # Create new entry
            new_entry = {
                'feature_type': feature_type,
                'implementations': 1,
                'avg_token_usage': metrics.get('avg_token_usage', 2000),
                'avg_implementation_time': metrics.get('avg_implementation_time', 30),
                'success_rate': 100 if metrics.get('success', True) else 0,
                'confidence_accuracy': 75,
                'last_updated': datetime.now().isoformat()
            }
            existing_metrics.append(new_entry)
        
        # Save updated metrics
        with open(self.knowledge_base_path / "success_metrics.yaml", 'w') as f:
            yaml.dump({'success_metrics': existing_metrics}, f, default_flow_style=False)
    
    def calculate_context_completeness_score(self, prp_content: str) -> int:
        """Calculate context completeness score for a PRP."""
        score = 0
        
        # Check for required sections (40 points)
        required_sections = [
            'Goal', 'Why', 'What', 'Success Criteria',
            'All Needed Context', 'Implementation Blueprint',
            'Validation Loop'
        ]
        
        for section in required_sections:
            if section in prp_content:
                score += 5
        
        # Check for URLs (20 points)
        urls = re.findall(r'https?://[^\s]+', prp_content)
        if urls:
            score += min(20, len(urls) * 2)
        
        # Check for file references (20 points)
        file_refs = re.findall(r'file: [^\s]+', prp_content)
        if file_refs:
            score += min(20, len(file_refs) * 4)
        
        # Check for examples (10 points)
        if 'examples/' in prp_content:
            score += 10
        
        # Check for gotchas/anti-patterns (10 points)
        if 'CRITICAL:' in prp_content or 'GOTCHA:' in prp_content or 'Anti-Pattern' in prp_content:
            score += 10
        
        return min(score, 100)
    
    def generate_analysis_report(self, prp_file: str, metrics: Dict[str, Any]) -> str:
        """Generate a comprehensive analysis report."""
        with open(prp_file, 'r') as f:
            prp_content = f.read()
        
        # Extract original confidence
        confidence_match = re.search(r'Confidence Score: (\d+)/10', prp_content)
        original_confidence = int(confidence_match.group(1)) if confidence_match else None
        
        # Calculate actual performance score
        actual_score = 10
        if metrics['tests_failed'] > 0:
            actual_score -= 2
        if metrics['mypy_errors'] > 0:
            actual_score -= 1
        if metrics['ruff_issues'] > 10:
            actual_score -= 1
        if metrics['implementation_time_minutes'] > 90:
            actual_score -= 2
        if metrics['commits'] > 10:
            actual_score -= 1
        
        actual_score = max(actual_score, 1)
        
        # Calculate context effectiveness
        context_score = self.calculate_context_completeness_score(prp_content)
        
        report = f"""
# PRP Analysis Report

## Implementation Summary
- PRP File: {prp_file}
- Execution Date: {datetime.now().isoformat()}
- Overall Success: {"SUCCESS" if metrics['tests_failed'] == 0 and metrics['mypy_errors'] == 0 else "PARTIAL"}

## Metrics
- Commits during implementation: {metrics['commits']}
- Files changed: {metrics['files_changed']}
- Lines added/deleted: {metrics['lines_added']}/{metrics['lines_deleted']}
- Implementation time: {metrics['implementation_time_minutes']} minutes
- Tests: {metrics['tests_passed']} passed, {metrics['tests_failed']} failed
- Code quality: {metrics['ruff_issues']} style issues, {metrics['mypy_errors']} type errors

## Context Analysis
- Context completeness score: {context_score}/100
- Original confidence estimate: {original_confidence}/10
- Actual performance score: {actual_score}/10
- Prediction accuracy: {"Good" if original_confidence and abs(original_confidence - actual_score) <= 2 else "Needs improvement"}

## Recommendations
"""
        
        # Add recommendations based on metrics
        if metrics['tests_failed'] > 0:
            report += "- Add more comprehensive test cases to PRP template\n"
        
        if metrics['ruff_issues'] > 5:
            report += "- Include stricter style checking in validation loop\n"
        
        if metrics['implementation_time_minutes'] > 60:
            report += "- Break down complex features into smaller PRPs\n"
        
        if context_score < 70:
            report += "- Improve context completeness in PRP generation\n"
        
        return report


def main():
    """CLI interface for context engineering utilities."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python context_engineering_utils.py <command> [args...]")
        print("Commands:")
        print("  analyze-patterns <feature_content>")
        print("  validate-context <prp_file>")
        print("  collect-metrics <start_time_iso>")
        return
    
    utils = ContextEngineeringUtils()
    command = sys.argv[1]
    
    if command == "analyze-patterns":
        if len(sys.argv) < 3:
            print("Usage: analyze-patterns <feature_content>")
            return
        
        content = sys.argv[2]
        feature_types = utils.detect_feature_type(content)
        patterns = utils.get_relevant_failure_patterns(feature_types)
        metrics = utils.get_relevant_success_metrics(feature_types)
        
        print(f"Detected feature types: {feature_types}")
        print(f"Relevant failure patterns: {len(patterns)}")
        print(f"Success metrics: {metrics}")
    
    elif command == "validate-context":
        if len(sys.argv) < 3:
            print("Usage: validate-context <prp_file>")
            return
        
        prp_file = sys.argv[2]
        with open(prp_file, 'r') as f:
            content = f.read()
        
        score = utils.calculate_context_completeness_score(content)
        print(f"Context completeness score: {score}/100")
    
    elif command == "collect-metrics":
        if len(sys.argv) < 3:
            print("Usage: collect-metrics <start_time_iso>")
            return
        
        start_time = datetime.fromisoformat(sys.argv[2])
        metrics = utils.collect_implementation_metrics(start_time)
        print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
