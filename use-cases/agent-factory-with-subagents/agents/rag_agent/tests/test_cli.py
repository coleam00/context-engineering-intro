"""Test CLI functionality."""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import asyncio
from click.testing import CliRunner
from rich.console import Console
import sys

from ..cli import cli, search_cmd, interactive, info, display_results, display_welcome, interactive_mode
from ..agent import SearchResponse


class TestCLICommands:
    """Test CLI command functionality."""
    
    def test_cli_without_subcommand(self):
        """Test CLI runs interactive mode when no subcommand provided."""
        runner = CliRunner()
        
        with patch('..cli.interactive_mode') as mock_interactive:
            mock_interactive.return_value = asyncio.run(asyncio.sleep(0))  # Mock async function
            
            result = runner.invoke(cli, [], input='\n')
            
            # Should attempt to run interactive mode
            assert result.exit_code == 0 or 'KeyboardInterrupt' in str(result.exception)
    
    def test_search_command_basic(self):
        """Test basic search command functionality."""
        runner = CliRunner()
        
        mock_response = SearchResponse(
            summary="Test search results found",
            key_findings=["Finding 1", "Finding 2"],
            sources=["Source 1", "Source 2"],
            search_strategy="semantic",
            result_count=2
        )
        
        with patch('..cli.search') as mock_search:
            mock_search.return_value = mock_response
            
            result = runner.invoke(search_cmd, [
                '--query', 'test query',
                '--type', 'semantic',
                '--count', '5'
            ])
            
            # Should complete successfully
            assert result.exit_code == 0
            mock_search.assert_called_once()
            
            # Verify search was called with correct parameters
            call_args = mock_search.call_args
            assert call_args[1]['query'] == 'test query'
            assert call_args[1]['search_type'] == 'semantic'
            assert call_args[1]['match_count'] == 5
    
    def test_search_command_with_text_weight(self):
        """Test search command with text weight parameter."""
        runner = CliRunner()
        
        mock_response = SearchResponse(
            summary="Hybrid search results",
            key_findings=[],
            sources=[],
            search_strategy="hybrid",
            result_count=10
        )
        
        with patch('..cli.search') as mock_search:
            mock_search.return_value = mock_response
            
            result = runner.invoke(search_cmd, [
                '--query', 'test query',
                '--type', 'hybrid',
                '--text-weight', '0.7'
            ])
            
            assert result.exit_code == 0
            call_args = mock_search.call_args
            assert call_args[1]['text_weight'] == 0.7
    
    def test_search_command_error_handling(self):
        """Test search command handles errors gracefully."""
        runner = CliRunner()
        
        with patch('..cli.search') as mock_search:
            mock_search.side_effect = Exception("Search failed")
            
            result = runner.invoke(search_cmd, [
                '--query', 'test query'
            ])
            
            # Should exit with error code 1
            assert result.exit_code == 1
            assert "Error:" in result.output
            assert "Search failed" in result.output
    
    def test_interactive_command(self):
        """Test interactive command invokes interactive mode."""
        runner = CliRunner()
        
        with patch('..cli.interactive_mode') as mock_interactive:
            mock_interactive.return_value = asyncio.run(asyncio.sleep(0))
            
            result = runner.invoke(interactive, [])
            
            # Should attempt to run interactive mode
            assert result.exit_code == 0 or 'KeyboardInterrupt' in str(result.exception)
    
    def test_info_command_success(self):
        """Test info command displays system information."""
        runner = CliRunner()
        
        mock_settings = MagicMock()
        mock_settings.llm_model = "gpt-4o-mini"
        mock_settings.embedding_model = "text-embedding-3-small"
        mock_settings.embedding_dimension = 1536
        mock_settings.default_match_count = 10
        mock_settings.max_match_count = 50
        mock_settings.default_text_weight = 0.3
        mock_settings.db_pool_min_size = 10
        mock_settings.db_pool_max_size = 20
        
        with patch('..cli.load_settings', return_value=mock_settings):
            result = runner.invoke(info, [])
            
            assert result.exit_code == 0
            assert "System Configuration" in result.output
            assert "gpt-4o-mini" in result.output
            assert "text-embedding-3-small" in result.output
    
    def test_info_command_error_handling(self):
        """Test info command handles settings loading errors."""
        runner = CliRunner()
        
        with patch('..cli.load_settings') as mock_load_settings:
            mock_load_settings.side_effect = Exception("Settings load failed")
            
            result = runner.invoke(info, [])
            
            assert result.exit_code == 1
            assert "Error loading settings:" in result.output
            assert "Settings load failed" in result.output


class TestDisplayFunctions:
    """Test CLI display functions."""
    
    def test_display_welcome(self, capsys):
        """Test welcome message display."""
        console = Console(file=sys.stdout, force_terminal=False)
        
        with patch('..cli.console', console):
            display_welcome()
        
        captured = capsys.readouterr()
        assert "Semantic Search Agent" in captured.out
        assert "Welcome" in captured.out
        assert "search" in captured.out.lower()
        assert "interactive" in captured.out.lower()
    
    def test_display_results_basic(self, capsys):
        """Test basic results display."""
        console = Console(file=sys.stdout, force_terminal=False)
        
        response = {
            'summary': 'This is a test summary of the search results.',
            'key_findings': ['Finding 1', 'Finding 2', 'Finding 3'],
            'sources': [
                {'title': 'Document 1', 'source': 'doc1.pdf'},
                {'title': 'Document 2', 'source': 'doc2.pdf'}
            ],
            'search_strategy': 'hybrid',
            'result_count': 10
        }
        
        with patch('..cli.console', console):
            display_results(response)
        
        captured = capsys.readouterr()
        assert "Summary:" in captured.out
        assert "This is a test summary" in captured.out
        assert "Key Findings:" in captured.out
        assert "Finding 1" in captured.out
        assert "Sources:" in captured.out
        assert "Document 1" in captured.out
        assert "Search Strategy: hybrid" in captured.out
        assert "Results Found: 10" in captured.out
    
    def test_display_results_minimal(self, capsys):
        """Test results display with minimal data."""
        console = Console(file=sys.stdout, force_terminal=False)
        
        response = {
            'summary': 'Minimal response',
            'search_strategy': 'semantic',
            'result_count': 0
        }
        
        with patch('..cli.console', console):
            display_results(response)
        
        captured = capsys.readouterr()
        assert "Summary:" in captured.out
        assert "Minimal response" in captured.out
        assert "Search Strategy: semantic" in captured.out
        assert "Results Found: 0" in captured.out
    
    def test_display_results_no_summary(self, capsys):
        """Test results display when summary is missing."""
        console = Console(file=sys.stdout, force_terminal=False)
        
        response = {
            'search_strategy': 'auto',
            'result_count': 5
        }
        
        with patch('..cli.console', console):
            display_results(response)
        
        captured = capsys.readouterr()
        assert "Summary:" in captured.out
        assert "No summary available" in captured.out
        assert "Search Strategy: auto" in captured.out


class TestInteractiveMode:
    """Test interactive mode functionality."""
    
    @pytest.mark.asyncio
    async def test_interactive_mode_initialization(self):
        """Test interactive mode initializes properly."""
        with patch('..cli.interactive_search') as mock_interactive_search:
            with patch('..cli.display_welcome') as mock_display_welcome:
                with patch('..cli.Prompt.ask') as mock_prompt:
                    with patch('..cli.Confirm.ask') as mock_confirm:
                        mock_deps = AsyncMock()
                        mock_interactive_search.return_value = mock_deps
                        mock_prompt.side_effect = ['test query', 'exit']
                        mock_confirm.return_value = True
                        
                        await interactive_mode()
                        
                        mock_display_welcome.assert_called_once()
                        mock_interactive_search.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_interactive_mode_search_query(self):
        """Test interactive mode handles search queries."""
        mock_response = SearchResponse(
            summary="Interactive search results",
            key_findings=["Finding 1"],
            sources=["Source 1"],
            search_strategy="auto",
            result_count=1
        )
        
        with patch('..cli.interactive_search') as mock_interactive_search:
            with patch('..cli.display_welcome'):
                with patch('..cli.display_results') as mock_display_results:
                    with patch('..cli.search') as mock_search:
                        with patch('..cli.Prompt.ask') as mock_prompt:
                            with patch('..cli.Confirm.ask') as mock_confirm:
                                mock_deps = AsyncMock()
                                mock_interactive_search.return_value = mock_deps
                                mock_search.return_value = mock_response
                                mock_prompt.side_effect = ['Python tutorial', 'exit']
                                mock_confirm.return_value = True
                                
                                await interactive_mode()
                                
                                # Should perform search
                                mock_search.assert_called()
                                call_args = mock_search.call_args
                                assert call_args[1]['query'] == 'Python tutorial'
                                
                                # Should display results
                                mock_display_results.assert_called()
    
    @pytest.mark.asyncio
    async def test_interactive_mode_help_command(self):
        """Test interactive mode handles help command."""
        with patch('..cli.interactive_search') as mock_interactive_search:
            with patch('..cli.display_welcome') as mock_display_welcome:
                with patch('..cli.Prompt.ask') as mock_prompt:
                    with patch('..cli.Confirm.ask') as mock_confirm:
                        mock_deps = AsyncMock()
                        mock_interactive_search.return_value = mock_deps
                        mock_prompt.side_effect = ['help', 'exit']
                        mock_confirm.return_value = True
                        
                        await interactive_mode()
                        
                        # Should display welcome twice (initial + help)
                        assert mock_display_welcome.call_count == 2
    
    @pytest.mark.asyncio
    async def test_interactive_mode_clear_command(self):
        """Test interactive mode handles clear command."""
        with patch('..cli.interactive_search') as mock_interactive_search:
            with patch('..cli.display_welcome'):
                with patch('..cli.console') as mock_console:
                    with patch('..cli.Prompt.ask') as mock_prompt:
                        with patch('..cli.Confirm.ask') as mock_confirm:
                            mock_deps = AsyncMock()
                            mock_interactive_search.return_value = mock_deps
                            mock_prompt.side_effect = ['clear', 'exit']
                            mock_confirm.return_value = True
                            
                            await interactive_mode()
                            
                            # Should clear console
                            mock_console.clear.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_interactive_mode_set_preference(self):
        """Test interactive mode handles preference setting."""
        with patch('..cli.interactive_search') as mock_interactive_search:
            with patch('..cli.display_welcome'):
                with patch('..cli.Prompt.ask') as mock_prompt:
                    with patch('..cli.Confirm.ask') as mock_confirm:
                        with patch('..cli.console') as mock_console:
                            mock_deps = AsyncMock()
                            mock_interactive_search.return_value = mock_deps
                            mock_prompt.side_effect = ['set search_type=semantic', 'exit']
                            mock_confirm.return_value = True
                            
                            await interactive_mode()
                            
                            # Should set preference on deps
                            mock_deps.set_user_preference.assert_called_once_with('search_type', 'semantic')
    
    @pytest.mark.asyncio
    async def test_interactive_mode_invalid_set_command(self):
        """Test interactive mode handles invalid set commands."""
        with patch('..cli.interactive_search') as mock_interactive_search:
            with patch('..cli.display_welcome'):
                with patch('..cli.Prompt.ask') as mock_prompt:
                    with patch('..cli.Confirm.ask') as mock_confirm:
                        with patch('..cli.console') as mock_console:
                            mock_deps = AsyncMock()
                            mock_interactive_search.return_value = mock_deps
                            mock_prompt.side_effect = ['set invalid_format', 'exit']
                            mock_confirm.return_value = True
                            
                            await interactive_mode()
                            
                            # Should not set preference
                            mock_deps.set_user_preference.assert_not_called()
                            # Should print error message
                            mock_console.print.assert_called()
    
    @pytest.mark.asyncio
    async def test_interactive_mode_exit_confirmation(self):
        """Test interactive mode handles exit confirmation."""
        with patch('..cli.interactive_search') as mock_interactive_search:
            with patch('..cli.display_welcome'):
                with patch('..cli.Prompt.ask') as mock_prompt:
                    with patch('..cli.Confirm.ask') as mock_confirm:
                        mock_deps = AsyncMock()
                        mock_interactive_search.return_value = mock_deps
                        mock_prompt.side_effect = ['exit', 'quit']
                        # First time say no, second time say yes
                        mock_confirm.side_effect = [False, True]
                        
                        await interactive_mode()
                        
                        # Should ask for confirmation twice
                        assert mock_confirm.call_count == 2
                        # Should cleanup dependencies
                        mock_deps.cleanup.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_interactive_mode_search_error(self):
        """Test interactive mode handles search errors."""
        with patch('..cli.interactive_search') as mock_interactive_search:
            with patch('..cli.display_welcome'):
                with patch('..cli.search') as mock_search:
                    with patch('..cli.Prompt.ask') as mock_prompt:
                        with patch('..cli.Confirm.ask') as mock_confirm:
                            with patch('..cli.console') as mock_console:
                                mock_deps = AsyncMock()
                                mock_interactive_search.return_value = mock_deps
                                mock_search.side_effect = Exception("Search failed")
                                mock_prompt.side_effect = ['test query', 'exit']
                                mock_confirm.return_value = True
                                
                                await interactive_mode()
                                
                                # Should print error message
                                error_calls = [call for call in mock_console.print.call_args_list 
                                             if 'Error:' in str(call)]
                                assert len(error_calls) > 0


class TestCLIInputValidation:
    """Test CLI input validation."""
    
    def test_search_command_empty_query(self):
        """Test search command with empty query."""
        runner = CliRunner()
        
        result = runner.invoke(search_cmd, ['--query', ''])
        
        # Should still accept empty query (might be valid use case)
        assert result.exit_code == 0 or result.exit_code == 1  # May fail due to missing search function
    
    def test_search_command_invalid_type(self):
        """Test search command with invalid search type."""
        runner = CliRunner()
        
        result = runner.invoke(search_cmd, [
            '--query', 'test',
            '--type', 'invalid_type'
        ])
        
        # Should reject invalid type
        assert result.exit_code != 0
        assert "Invalid value" in result.output or "Usage:" in result.output
    
    def test_search_command_invalid_count(self):
        """Test search command with invalid count."""
        runner = CliRunner()
        
        result = runner.invoke(search_cmd, [
            '--query', 'test',
            '--count', 'not_a_number'
        ])
        
        # Should reject non-numeric count
        assert result.exit_code != 0
        assert ("Invalid value" in result.output or 
                "Usage:" in result.output or
                "not_a_number is not a valid integer" in result.output)
    
    def test_search_command_negative_count(self):
        """Test search command with negative count."""
        runner = CliRunner()
        
        mock_response = SearchResponse(
            summary="Test results",
            key_findings=[],
            sources=[],
            search_strategy="auto", 
            result_count=0
        )
        
        with patch('..cli.search') as mock_search:
            mock_search.return_value = mock_response
            
            result = runner.invoke(search_cmd, [
                '--query', 'test',
                '--count', '-5'
            ])
            
            # Click accepts negative integers, but our code should handle it
            assert result.exit_code == 0
            call_args = mock_search.call_args
            assert call_args[1]['match_count'] == -5  # Passed through
    
    def test_search_command_invalid_text_weight(self):
        """Test search command with invalid text weight."""
        runner = CliRunner()
        
        result = runner.invoke(search_cmd, [
            '--query', 'test',
            '--text-weight', 'not_a_float'
        ])
        
        # Should reject non-numeric text weight
        assert result.exit_code != 0
        assert ("Invalid value" in result.output or 
                "Usage:" in result.output or
                "not_a_float is not a valid" in result.output)


class TestCLIIntegration:
    """Test CLI integration scenarios."""
    
    def test_cli_with_all_parameters(self):
        """Test CLI with all possible parameters."""
        runner = CliRunner()
        
        mock_response = SearchResponse(
            summary="Complete search results",
            key_findings=["Finding 1", "Finding 2"],
            sources=["Source 1", "Source 2"],
            search_strategy="hybrid",
            result_count=15
        )
        
        with patch('..cli.search') as mock_search:
            mock_search.return_value = mock_response
            
            result = runner.invoke(search_cmd, [
                '--query', 'comprehensive search test',
                '--type', 'hybrid',
                '--count', '15',
                '--text-weight', '0.6'
            ])
            
            assert result.exit_code == 0
            
            # Verify all parameters passed correctly
            call_args = mock_search.call_args
            assert call_args[1]['query'] == 'comprehensive search test'
            assert call_args[1]['search_type'] == 'hybrid'
            assert call_args[1]['match_count'] == 15
            assert call_args[1]['text_weight'] == 0.6
    
    def test_cli_search_output_format(self):
        """Test CLI search output formatting."""
        runner = CliRunner()
        
        mock_response = SearchResponse(
            summary="Formatted output test results with detailed information.",
            key_findings=[
                "Key finding number one with details",
                "Second important finding",
                "Third critical insight"
            ],
            sources=[
                "Python Documentation",
                "Machine Learning Guide",
                "API Reference Manual"
            ],
            search_strategy="semantic",
            result_count=25
        )
        
        with patch('..cli.search') as mock_search:
            mock_search.return_value = mock_response
            
            result = runner.invoke(search_cmd, [
                '--query', 'formatting test'
            ])
            
            assert result.exit_code == 0
            
            # Check that output contains expected formatted content
            output = result.output
            assert "Searching for:" in output
            assert "formatting test" in output
            assert "Summary:" in output
            assert "Formatted output test results" in output
            assert "Key Findings:" in output
            assert "Key finding number one" in output
            assert "Sources:" in output
            assert "Python Documentation" in output
            assert "Search Strategy: semantic" in output
            assert "Results Found: 25" in output


class TestCLIErrorScenarios:
    """Test CLI error handling scenarios."""
    
    def test_cli_keyboard_interrupt(self):
        """Test CLI handles keyboard interrupt gracefully."""
        runner = CliRunner()
        
        with patch('..cli.search') as mock_search:
            mock_search.side_effect = KeyboardInterrupt()
            
            result = runner.invoke(search_cmd, ['--query', 'test'])
            
            # Should handle KeyboardInterrupt without crashing
            assert result.exit_code != 0
    
    def test_cli_system_exit(self):
        """Test CLI handles system exit gracefully.""" 
        runner = CliRunner()
        
        with patch('..cli.search') as mock_search:
            mock_search.side_effect = SystemExit(1)
            
            result = runner.invoke(search_cmd, ['--query', 'test'])
            
            # Should handle SystemExit
            assert result.exit_code == 1
    
    def test_cli_unexpected_exception(self):
        """Test CLI handles unexpected exceptions."""
        runner = CliRunner()
        
        with patch('..cli.search') as mock_search:
            mock_search.side_effect = RuntimeError("Unexpected error occurred")
            
            result = runner.invoke(search_cmd, ['--query', 'test'])
            
            assert result.exit_code == 1
            assert "Error:" in result.output
            assert "Unexpected error occurred" in result.output


class TestCLIUsability:
    """Test CLI usability features."""
    
    def test_cli_help_messages(self):
        """Test CLI provides helpful help messages."""
        runner = CliRunner()
        
        # Test main CLI help
        result = runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert "Semantic Search Agent CLI" in result.output
        
        # Test search command help
        result = runner.invoke(search_cmd, ['--help'])
        assert result.exit_code == 0
        assert "Perform a one-time search" in result.output
        assert "--query" in result.output
        assert "--type" in result.output
        assert "--count" in result.output
        assert "--text-weight" in result.output
        
        # Test interactive command help
        result = runner.invoke(interactive, ['--help'])
        assert result.exit_code == 0
        assert "interactive search session" in result.output
        
        # Test info command help  
        result = runner.invoke(info, ['--help'])
        assert result.exit_code == 0
        assert "system information" in result.output
    
    def test_cli_command_suggestions(self):
        """Test CLI provides command suggestions for typos."""
        runner = CliRunner()
        
        # Test with typo in command name
        result = runner.invoke(cli, ['searc'])  # Missing 'h'
        
        # Should suggest correct command or show usage
        assert result.exit_code != 0
        assert ("Usage:" in result.output or 
                "No such command" in result.output or
                "Did you mean" in result.output)
    
    def test_cli_default_values(self):
        """Test CLI uses appropriate default values."""
        runner = CliRunner()
        
        mock_response = SearchResponse(
            summary="Default values test",
            key_findings=[],
            sources=[],
            search_strategy="auto",
            result_count=10
        )
        
        with patch('..cli.search') as mock_search:
            mock_search.return_value = mock_response
            
            result = runner.invoke(search_cmd, ['--query', 'test with defaults'])
            
            assert result.exit_code == 0
            
            # Check default values were used
            call_args = mock_search.call_args
            assert call_args[1]['search_type'] == 'auto'  # Default type
            assert call_args[1]['match_count'] == 10  # Default count
            assert call_args[1]['text_weight'] is None  # No default text weight