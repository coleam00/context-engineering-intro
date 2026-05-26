"""
Comprehensive PydanticAI Testing Examples

Demonstrates testing patterns and best practices for PydanticAI agents:
- TestModel for fast development validation
- FunctionModel for custom behavior testing
- Agent.override() for test isolation
- Pytest fixtures and async testing
- Tool validation and error handling tests
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock
from dataclasses import dataclass
from typing import Optional, List
from pydantic import BaseModel
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.test import TestModel, FunctionModel


@dataclass
class TestDependencies:
    """Test dependencies for agent testing."""
    database: Mock
    api_client: Mock
    user_id: str = "test_user_123"


class TestResponse(BaseModel):
    """Test response model for validation."""
    message: str
    confidence: float = 0.8
    actions: List[str] = []


# Create test agent for demonstrations
test_agent = Agent(
    model="openai:gpt-4o-mini",  # Will be overridden in tests
    deps_type=TestDependencies,
    result_type=TestResponse,
    system_prompt="You are a helpful test assistant."
)


@test_agent.tool
async def mock_database_query(
    ctx: RunContext[TestDependencies], 
    query: str
) -> str:
    """Mock database query tool for testing."""
    try:
        # Simulate database call
        result = await ctx.deps.database.execute_query(query)
        return f"Database result: {result}"
    except Exception as e:
        return f"Database error: {str(e)}"


@test_agent.tool
def mock_api_call(
    ctx: RunContext[TestDependencies],
    endpoint: str,
    data: Optional[dict] = None
) -> str:
    """Mock API call tool for testing."""
    try:
        # Simulate API call
        response = ctx.deps.api_client.post(endpoint, json=data)
        return f"API response: {response}"
    except Exception as e:
        return f"API error: {str(e)}"


class TestAgentBasics:
    """Test basic agent functionality with TestModel."""
    
    @pytest.fixture
    def test_dependencies(self):
        """Create mock dependencies for testing."""
        return TestDependencies(
            database=AsyncMock(),
            api_client=Mock(),
            user_id="test_user_123"
        )
    
    def test_agent_with_test_model(self, test_dependencies):
        """Test agent behavior with TestModel."""
        test_model = TestModel()
        
        with test_agent.override(model=test_model):
            result = test_agent.run_sync(
                "Hello, please help me with a simple task.",
                deps=test_dependencies
            )
            
            # TestModel returns a JSON summary by default
            assert result.data.message is not None
            assert isinstance(result.data.confidence, float)
            assert isinstance(result.data.actions, list)
    
    def test_agent_custom_test_model_output(self, test_dependencies):
        """Test agent with custom TestModel output."""
        test_model = TestModel(
            custom_output_text='{"message": "Custom test response", "confidence": 0.9, "actions": ["test_action"]}'
        )
        
        with test_agent.override(model=test_model):
            result = test_agent.run_sync(
                "Test message",
                deps=test_dependencies
            )
            
            assert result.data.message == "Custom test response"
            assert result.data.confidence == 0.9
            assert result.data.actions == ["test_action"]
    
    @pytest.mark.asyncio
    async def test_agent_async_with_test_model(self, test_dependencies):
        """Test async agent behavior with TestModel."""
        test_model = TestModel()
        
        with test_agent.override(model=test_model):
            result = await test_agent.run(
                "Async test message",
                deps=test_dependencies
            )
            
            assert result.data.message is not None
            assert result.data.confidence >= 0.0


class TestAgentTools:
    """Test agent tool functionality."""
    
    @pytest.fixture
    def mock_dependencies(self):
        """Create mock dependencies with configured responses."""
        database_mock = AsyncMock()
        database_mock.execute_query.return_value = "Test data from database"
        
        api_mock = Mock()
        api_mock.post.return_value = {"status": "success", "data": "test_data"}
        
        return TestDependencies(
            database=database_mock,
            api_client=api_mock,
            user_id="test_user_456"
        )
    
    @pytest.mark.asyncio
    async def test_database_tool_success(self, mock_dependencies):
        """Test database tool with successful response."""
        test_model = TestModel(call_tools=['mock_database_query'])
        
        with test_agent.override(model=test_model):
            result = await test_agent.run(
                "Please query the database for user data",
                deps=mock_dependencies
            )
            
            # Verify database was called
            mock_dependencies.database.execute_query.assert_called()
            
            # TestModel should include tool results
            assert "mock_database_query" in result.data.message
    
    @pytest.mark.asyncio
    async def test_database_tool_error(self, mock_dependencies):
        """Test database tool with error handling."""
        # Configure mock to raise exception
        mock_dependencies.database.execute_query.side_effect = Exception("Connection failed")
        
        test_model = TestModel(call_tools=['mock_database_query'])
        
        with test_agent.override(model=test_model):
            result = await test_agent.run(
                "Query the database",
                deps=mock_dependencies
            )
            
            # Tool should handle the error gracefully
            assert "mock_database_query" in result.data.message
    
    def test_api_tool_with_data(self, mock_dependencies):
        """Test API tool with POST data."""
        test_model = TestModel(call_tools=['mock_api_call'])
        
        with test_agent.override(model=test_model):
            result = test_agent.run_sync(
                "Make an API call to create a new record",
                deps=mock_dependencies
            )
            
            # Verify API was called
            mock_dependencies.api_client.post.assert_called()
            
            # Check tool execution in response
            assert "mock_api_call" in result.data.message


class TestAgentWithFunctionModel:
    """Test agent behavior with FunctionModel for custom responses."""
    
    @pytest.fixture
    def test_dependencies(self):
        """Create basic test dependencies."""
        return TestDependencies(
            database=AsyncMock(),
            api_client=Mock()
        )
    
    def test_function_model_custom_behavior(self, test_dependencies):
        """Test agent with FunctionModel for custom behavior."""
        def custom_response_func(messages, tools):
            """Custom function to generate specific responses."""
            last_message = messages[-1].content if messages else ""
            
            if "error" in last_message.lower():
                return '{"message": "Error detected and handled", "confidence": 0.6, "actions": ["error_handling"]}'
            else:
                return '{"message": "Normal operation", "confidence": 0.9, "actions": ["standard_response"]}'
        
        function_model = FunctionModel(function=custom_response_func)
        
        with test_agent.override(model=function_model):
            # Test normal case
            result1 = test_agent.run_sync(
                "Please help me with a normal request",
                deps=test_dependencies
            )
            assert result1.data.message == "Normal operation"
            assert result1.data.confidence == 0.9
            
            # Test error case
            result2 = test_agent.run_sync(
                "There's an error in the system",
                deps=test_dependencies
            )
            assert result2.data.message == "Error detected and handled"
            assert result2.data.confidence == 0.6
            assert "error_handling" in result2.data.actions


class TestAgentValidation:
    """Test agent output validation and error scenarios."""
    
    @pytest.fixture
    def test_dependencies(self):
        """Create test dependencies."""
        return TestDependencies(
            database=AsyncMock(),
            api_client=Mock()
        )
    
    def test_invalid_output_handling(self, test_dependencies):
        """Test how agent handles invalid output format."""
        # TestModel with invalid JSON output
        test_model = TestModel(
            custom_output_text='{"message": "test", "invalid_field": "should_not_exist"}'
        )
        
        with test_agent.override(model=test_model):
            # This should either succeed with validation or raise appropriate error
            try:
                result = test_agent.run_sync(
                    "Test invalid output",
                    deps=test_dependencies
                )
                # If it succeeds, Pydantic should filter out invalid fields
                assert hasattr(result.data, 'message')
                assert not hasattr(result.data, 'invalid_field')
            except Exception as e:
                # Or it might raise a validation error, which is also acceptable
                assert "validation" in str(e).lower() or "error" in str(e).lower()
    
    def test_missing_required_fields(self, test_dependencies):
        """Test handling of missing required fields in output."""
        # TestModel with missing required message field
        test_model = TestModel(
            custom_output_text='{"confidence": 0.8}'
        )
        
        with test_agent.override(model=test_model):
            try:
                result = test_agent.run_sync(
                    "Test missing fields",
                    deps=test_dependencies
                )
                # Should either provide default or raise validation error
                if hasattr(result.data, 'message'):
                    assert result.data.message is not None
            except Exception as e:
                # Validation error is expected for missing required fields
                assert any(keyword in str(e).lower() for keyword in ['validation', 'required', 'missing'])


class TestAgentIntegration:
    """Integration tests for complete agent workflows."""
    
    @pytest.fixture
    def full_mock_dependencies(self):
        """Create fully configured mock dependencies."""
        database_mock = AsyncMock()
        database_mock.execute_query.return_value = {
            "user_id": "123",
            "name": "Test User",
            "status": "active"
        }
        
        api_mock = Mock()
        api_mock.post.return_value = {
            "status": "success",
            "transaction_id": "txn_123456"
        }
        
        return TestDependencies(
            database=database_mock,
            api_client=api_mock,
            user_id="test_integration_user"
        )
    
    @pytest.mark.asyncio
    async def test_complete_workflow(self, full_mock_dependencies):
        """Test complete agent workflow with multiple tools."""
        test_model = TestModel(call_tools='all')  # Call all available tools
        
        with test_agent.override(model=test_model):
            result = await test_agent.run(
                "Please look up user information and create a new transaction",
                deps=full_mock_dependencies
            )
            
            # Verify both tools were potentially called
            assert result.data.message is not None
            assert isinstance(result.data.actions, list)
            
            # Verify mocks were called
            full_mock_dependencies.database.execute_query.assert_called()
            full_mock_dependencies.api_client.post.assert_called()


class TestAgentErrorRecovery:
    """Test agent error handling and recovery patterns."""
    
    @pytest.fixture
    def failing_dependencies(self):
        """Create dependencies that will fail for testing error handling."""
        database_mock = AsyncMock()
        database_mock.execute_query.side_effect = Exception("Database connection failed")
        
        api_mock = Mock()
        api_mock.post.side_effect = Exception("API service unavailable")
        
        return TestDependencies(
            database=database_mock,
            api_client=api_mock,
            user_id="failing_test_user"
        )
    
    @pytest.mark.asyncio
    async def test_tool_error_recovery(self, failing_dependencies):
        """Test agent behavior when tools fail."""
        test_model = TestModel(call_tools='all')
        
        with test_agent.override(model=test_model):
            # Agent should handle tool failures gracefully
            result = await test_agent.run(
                "Try to access database and API",
                deps=failing_dependencies
            )
            
            # Even with tool failures, agent should return a valid response
            assert result.data.message is not None
            assert isinstance(result.data.confidence, float)


# Pytest configuration and utilities
@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )


if __name__ == "__main__":
    # Run tests directly
    pytest.main([__file__, "-v"])