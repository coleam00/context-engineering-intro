# Exercise 2: Multi-Agent System

> **"Building a multi-agent system tests every aspect of Context Engineering - from individual agent patterns to complex orchestration workflows."**

This advanced exercise guides you through building a complete multi-agent system using the research/email agent example as inspiration. You'll apply Context Engineering at scale and learn how to manage complexity through systematic context design.

## 🎯 Exercise Objectives

By the end of this exercise, you will have:
- Built a working multi-agent system with proper context inheritance
- Implemented agent-as-tool patterns with context propagation
- Created comprehensive testing strategies for multi-agent systems
- Designed validation loops for complex, asynchronous workflows
- Extracted reusable patterns for future multi-agent development

## 📋 Prerequisites

Before starting this exercise:
- [ ] Completed Exercise 1 (Simple Feature Implementation)
- [ ] Read Chapter 11 (Advanced Patterns) and Chapter 12 (Real-World Examples)
- [ ] Have access to external APIs (or can mock them effectively)
- [ ] Understand async/await patterns in your chosen language

## 🚀 Exercise Overview

We'll build a **Research and Analysis System** that demonstrates sophisticated Context Engineering patterns:

**System Components:**
- **Research Agent**: Web search and data gathering
- **Analysis Agent**: Data processing and insight extraction  
- **Report Agent**: Document generation and formatting
- **Orchestration Agent**: Workflow coordination and decision making

**Context Engineering Challenges:**
- Context inheritance across agent boundaries
- Token usage tracking in multi-agent scenarios
- Error handling and recovery in complex workflows
- Testing strategies that don't require expensive API calls
- Performance optimization for multi-step processes

## 📝 Phase 1: System Design and Context Architecture (30 minutes)

### **Step 1.1: Create System INITIAL.md**

Create a comprehensive system specification:

```markdown
# research-analysis-system-requirements.md

## FEATURE:
Multi-agent research and analysis system with the following capabilities:

### Core System Architecture:
- **Research Agent**: Web search using Brave Search API, document retrieval, source validation
- **Analysis Agent**: Data processing, pattern recognition, insight extraction, statistical analysis
- **Report Agent**: Document generation, formatting, visualization integration
- **Orchestration Agent**: Workflow management, agent coordination, error recovery

### Agent Interaction Patterns:
- Research Agent → Analysis Agent: Raw data with metadata and source credibility
- Analysis Agent → Report Agent: Processed insights with supporting evidence
- Orchestration Agent → All: Task delegation, progress monitoring, error handling
- All Agents → Orchestration Agent: Status updates, completion notifications, error reports

### Technical Requirements:
- Async operation with proper token usage tracking across agent boundaries
- Comprehensive error handling with graceful degradation
- Configurable agent personalities and specializations
- Memory and context persistence across multi-step workflows
- Performance monitoring and optimization

### Business Requirements:
- Research requests should be completed within 5 minutes for standard queries
- System should handle concurrent research requests (up to 10 simultaneous)
- All agent interactions should be logged for debugging and optimization
- Results should be reproducible given the same inputs and timeframe

## EXAMPLES:
- examples/multi_agent_reference/ - Multi-agent architecture patterns (from use-cases/pydantic-ai)
- examples/async_orchestration/ - Async workflow coordination patterns
- examples/error_recovery/ - Error handling in complex systems
- examples/token_tracking/ - Token usage management across agents
- examples/testing_multi_agent/ - Testing strategies for agent systems

## DOCUMENTATION:
- Pydantic AI Multi-Agent: https://ai.pydantic.dev/multi-agent-applications/
- Brave Search API: https://api-dashboard.search.brave.com/app/documentation
- OpenAI API (if using): https://platform.openai.com/docs/api-reference
- Async patterns: https://docs.python.org/3/library/asyncio.html

## OTHER CONSIDERATIONS:
### Context Engineering Challenges:
- **Context Inheritance**: Each agent needs project patterns + domain specialization
- **Token Accounting**: Usage tracking must work across agent boundaries
- **Error Recovery**: Failed agents shouldn't crash entire workflow
- **Testing Strategy**: Avoid API costs while ensuring system reliability
- **Performance**: Multi-agent systems can be slow without proper optimization

### Integration Constraints:
- External APIs have rate limits and quotas
- Agent-to-agent communication must preserve conversation context
- System must be configurable for different LLM providers
- All agent interactions must be observable for debugging

### Quality Requirements:
- Research quality: Sources must be credible and recent
- Analysis quality: Insights must be supported by evidence
- Report quality: Output must be well-formatted and actionable
- System reliability: 95% success rate for standard research queries
```

### **Step 1.2: Design Context Architecture**

Plan your context inheritance strategy:

```markdown
# context-architecture-design.md

## Context Layer Architecture:

### Layer 1: Global Context (CLAUDE.md)
- Multi-agent coordination patterns
- Async programming standards
- Error handling conventions
- Token usage tracking requirements
- Testing and validation standards

### Layer 2: Domain Context (Agent-Specific)
- Research Agent: Web search patterns, source validation, data extraction
- Analysis Agent: Data processing, statistical analysis, insight generation
- Report Agent: Document formatting, visualization, presentation patterns
- Orchestration Agent: Workflow management, task delegation, error recovery

### Layer 3: Integration Context (Cross-Agent)
- Agent communication protocols
- Context serialization/deserialization
- Error propagation and recovery
- Performance monitoring and optimization

### Layer 4: Execution Context (Runtime)
- User request context
- Conversation history
- Token usage tracking
- Performance metrics
```

### **Step 1.3: Plan Validation Strategy**

Design comprehensive validation for complex system:

```markdown
# validation-strategy.md

## Multi-Level Validation for Multi-Agent System:

### Level 1: Individual Agent Testing (< 30 seconds)
- Unit tests for each agent with mocked dependencies
- Tool function testing with mock external APIs
- Context inheritance validation
- Error handling scenario testing

### Level 2: Agent Integration Testing (< 2 minutes)
- Agent-to-agent communication testing
- Context propagation validation
- Token usage tracking verification
- Error recovery workflow testing

### Level 3: System Workflow Testing (< 5 minutes)
- End-to-end research workflow with mock data
- Concurrent request handling
- Performance under load
- Memory and resource usage validation

### Level 4: Real Integration Testing (< 10 minutes)
- Full system test with real APIs (limited scope)
- External service integration validation
- Rate limiting and quota management
- Production-like scenario testing
```

## 🛠️ Phase 2: Context Engineering Setup (45 minutes)

### **Step 2.1: Enhance Global Context (CLAUDE.md)**

Add multi-agent specific rules to your CLAUDE.md:

```markdown
### 🤖 Multi-Agent System Patterns
- **Agent Architecture**: Use dependency injection with RunContext for all agents
- **Context Inheritance**: Global context + domain context + execution context
- **Token Tracking**: Always pass ctx.usage between agents for accurate accounting
- **Error Handling**: Agent failures should not crash the orchestration system
- **Testing**: Use TestModel and FunctionModel to avoid API costs during testing

### Agent Communication Patterns:
- **Context Serialization**: Use structured data transfer between agents
- **Async Coordination**: All agent communication must be async with proper error handling
- **Memory Management**: Preserve conversation context across agent boundaries
- **Performance**: Monitor and optimize token usage and response times

### Examples to Follow:
- examples/multi_agent_reference/ - Primary patterns for agent architecture
- examples/orchestration/ - Workflow coordination and error recovery
- examples/testing_agents/ - Testing strategies that avoid API costs
```

### **Step 2.2: Create Agent-Specific Examples**

Build examples for each agent type:

```python
# examples/agents/research_agent_example.py
"""
Research Agent pattern showing web search integration with error handling.
Use this pattern for agents that interact with external APIs.
"""

from pydantic_ai import Agent, RunContext
from typing import List, Dict, Any
import httpx
import asyncio
from dataclasses import dataclass

@dataclass
class ResearchDeps:
    """Dependencies for research agent."""
    brave_api_key: str
    max_results: int = 10
    timeout: float = 30.0

class ResearchAgent:
    """
    Research agent with robust external API integration.
    
    Key patterns:
    - Dependency injection for configuration
    - Comprehensive error handling with retries
    - Structured data return with metadata
    - Token usage tracking through context
    """
    
    def __init__(self):
        self.agent = Agent(
            'openai:gpt-4',
            deps_type=ResearchDeps,
            system_prompt="""You are a research specialist focused on gathering 
            accurate, credible information from web sources. Always validate source 
            credibility and provide metadata about your findings."""
        )
        
        # Register tools with proper error handling
        self.agent.tool(self.search_web)
        self.agent.tool(self.validate_sources)
    
    async def search_web(self, ctx: RunContext[ResearchDeps], query: str, num_results: int = 5) -> Dict[str, Any]:
        """
        Search web with comprehensive error handling and retry logic.
        
        Pattern: External API integration with resilience
        - Multiple retry attempts with exponential backoff
        - Structured error responses
        - Rate limiting awareness
        - Metadata preservation
        """
        
        for attempt in range(3):
            try:
                async with httpx.AsyncClient() as client:
                    headers = {"X-Subscription-Token": ctx.deps.brave_api_key}
                    params = {"q": query, "count": min(num_results, ctx.deps.max_results)}
                    
                    response = await client.get(
                        "https://api.search.brave.com/res/v1/web/search",
                        headers=headers,
                        params=params,
                        timeout=ctx.deps.timeout
                    )
                    
                    if response.status_code == 429:  # Rate limited
                        wait_time = int(response.headers.get("Retry-After", 60))
                        await asyncio.sleep(wait_time)
                        continue
                    
                    response.raise_for_status()
                    data = response.json()
                    
                    return {
                        "results": data.get("web", {}).get("results", []),
                        "query": query,
                        "timestamp": datetime.utcnow().isoformat(),
                        "metadata": {
                            "attempt": attempt + 1,
                            "source": "brave_search",
                            "num_results": len(data.get("web", {}).get("results", []))
                        }
                    }
                    
            except httpx.TimeoutException:
                if attempt == 2:  # Last attempt
                    return {
                        "error": "Search timeout after retries",
                        "query": query,
                        "metadata": {"attempts": 3, "last_error": "timeout"}
                    }
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
                
            except Exception as e:
                if attempt == 2:  # Last attempt
                    return {
                        "error": f"Search failed: {str(e)}",
                        "query": query,
                        "metadata": {"attempts": 3, "last_error": str(e)}
                    }
                await asyncio.sleep(2 ** attempt)
        
        return {"error": "Unexpected search failure", "query": query}
    
    async def validate_sources(self, ctx: RunContext[ResearchDeps], sources: List[Dict]) -> Dict[str, Any]:
        """Validate source credibility and extract metadata."""
        
        validated_sources = []
        for source in sources:
            # Pattern: Source validation logic
            credibility_score = self._calculate_credibility_score(source)
            
            validated_source = {
                **source,
                "credibility_score": credibility_score,
                "validation_timestamp": datetime.utcnow().isoformat(),
                "validation_criteria": self._get_validation_criteria(source)
            }
            validated_sources.append(validated_source)
        
        return {
            "validated_sources": validated_sources,
            "summary": {
                "total_sources": len(sources),
                "high_credibility": len([s for s in validated_sources if s["credibility_score"] > 0.7]),
                "validation_timestamp": datetime.utcnow().isoformat()
            }
        }
```

```python
# examples/orchestration/multi_agent_orchestrator.py
"""
Multi-agent orchestrator pattern showing context propagation and error recovery.
Use this pattern for coordinating multiple specialized agents.
"""

class MultiAgentOrchestrator:
    """
    Orchestrates multiple agents with proper context management.
    
    Key patterns:
    - Context inheritance and propagation
    - Error recovery and graceful degradation
    - Token usage tracking across agents
    - Async workflow coordination
    """
    
    def __init__(self, research_agent: Agent, analysis_agent: Agent, report_agent: Agent):
        self.research_agent = research_agent
        self.analysis_agent = analysis_agent
        self.report_agent = report_agent
        
        # Track agent performance and errors
        self.performance_tracker = PerformanceTracker()
        self.error_recovery = ErrorRecoverySystem()
    
    async def execute_research_workflow(
        self, 
        research_request: ResearchRequest,
        base_context: RunContext
    ) -> WorkflowResult:
        """
        Execute complete research workflow with context propagation.
        
        Pattern: Multi-agent workflow with error recovery
        - Context flows between agents
        - Failures are handled gracefully
        - Performance is monitored throughout
        - Results are validated at each step
        """
        
        workflow_id = str(uuid.uuid4())
        self.performance_tracker.start_workflow(workflow_id)
        
        try:
            # Phase 1: Research with context inheritance
            research_result = await self._execute_research_phase(
                research_request, base_context, workflow_id
            )
            
            if research_result.failed:
                return await self.error_recovery.handle_research_failure(
                    research_result, research_request
                )
            
            # Phase 2: Analysis with inherited context + research data
            analysis_result = await self._execute_analysis_phase(
                research_result, base_context, workflow_id
            )
            
            if analysis_result.failed:
                return await self.error_recovery.handle_analysis_failure(
                    analysis_result, research_result
                )
            
            # Phase 3: Report generation with full context
            report_result = await self._execute_report_phase(
                analysis_result, base_context, workflow_id
            )
            
            # Track successful completion
            self.performance_tracker.complete_workflow(workflow_id, success=True)
            
            return WorkflowResult(
                success=True,
                research_data=research_result.data,
                analysis_insights=analysis_result.data,
                final_report=report_result.data,
                workflow_id=workflow_id,
                performance_metrics=self.performance_tracker.get_metrics(workflow_id)
            )
            
        except Exception as e:
            # Global error recovery
            self.performance_tracker.complete_workflow(workflow_id, success=False, error=str(e))
            
            return await self.error_recovery.handle_workflow_failure(
                error=e,
                workflow_id=workflow_id,
                research_request=research_request
            )
    
    async def _execute_research_phase(
        self, 
        request: ResearchRequest, 
        base_context: RunContext,
        workflow_id: str
    ) -> PhaseResult:
        """Execute research phase with proper context inheritance."""
        
        # Create research-specific context
        research_context = self._create_research_context(base_context, request)
        
        try:
            # CRITICAL: Pass usage from base context for token tracking
            result = await self.research_agent.run(
                f"Research the following topic: {request.query}",
                deps=research_context.deps,
                usage=base_context.usage  # Token tracking continuity
            )
            
            return PhaseResult(
                success=True,
                data=result.data,
                phase="research",
                workflow_id=workflow_id,
                token_usage=result.usage
            )
            
        except Exception as e:
            return PhaseResult(
                success=False,
                error=str(e),
                phase="research",
                workflow_id=workflow_id
            )
```

### **Step 2.3: Create Testing Examples**

Build comprehensive testing patterns:

```python
# examples/testing/test_multi_agent_system.py
"""
Multi-agent system testing patterns that avoid API costs.
Use these patterns for testing complex agent interactions.
"""

import pytest
from pydantic_ai import Agent, TestModel, FunctionModel
from unittest.mock import AsyncMock, patch

class TestMultiAgentSystem:
    """
    Test multi-agent system using TestModel and FunctionModel.
    
    Key patterns:
    - No real API calls during testing
    - Comprehensive workflow testing
    - Error scenario validation
    - Performance characteristic testing
    """
    
    @pytest.fixture
    def mock_research_agent(self):
        """Create research agent with mocked responses."""
        
        def mock_research_response(query: str) -> str:
            """Mock research responses based on query patterns."""
            if "error" in query.lower():
                return "Research failed due to external service error"
            elif "timeout" in query.lower():
                raise TimeoutError("Request timed out")
            else:
                return f"Research results for: {query}\n- Source 1: credible information\n- Source 2: supporting evidence"
        
        agent = Agent('test', system_prompt="Research specialist")
        agent.override(model=FunctionModel(mock_research_response))
        return agent
    
    @pytest.fixture
    def mock_analysis_agent(self):
        """Create analysis agent with mocked responses."""
        
        def mock_analysis_response(data: str) -> str:
            """Mock analysis responses based on input data."""
            if "error" in data.lower():
                return "Cannot analyze incomplete research data"
            else:
                return f"Analysis insights:\n- Key finding 1\n- Key finding 2\n- Recommendation based on {data[:50]}..."
        
        agent = Agent('test', system_prompt="Data analyst")
        agent.override(model=FunctionModel(mock_analysis_response))
        return agent
    
    async def test_successful_workflow(self, mock_research_agent, mock_analysis_agent):
        """Test successful multi-agent workflow."""
        
        orchestrator = MultiAgentOrchestrator(
            research_agent=mock_research_agent,
            analysis_agent=mock_analysis_agent,
            report_agent=self._create_mock_report_agent()
        )
        
        request = ResearchRequest(
            query="AI in healthcare applications",
            depth="comprehensive",
            format="executive_summary"
        )
        
        base_context = self._create_test_context()
        
        result = await orchestrator.execute_research_workflow(request, base_context)
        
        assert result.success
        assert result.research_data is not None
        assert result.analysis_insights is not None
        assert result.final_report is not None
        assert result.workflow_id is not None
    
    async def test_research_failure_recovery(self, mock_analysis_agent):
        """Test error recovery when research phase fails."""
        
        # Create failing research agent
        failing_research_agent = Agent('test', system_prompt="Research specialist")
        failing_research_agent.override(model=FunctionModel(lambda x: "Research error occurred"))
        
        orchestrator = MultiAgentOrchestrator(
            research_agent=failing_research_agent,
            analysis_agent=mock_analysis_agent,
            report_agent=self._create_mock_report_agent()
        )
        
        request = ResearchRequest(query="test error scenario")
        base_context = self._create_test_context()
        
        result = await orchestrator.execute_research_workflow(request, base_context)
        
        # Should handle failure gracefully
        assert not result.success
        assert result.error_message is not None
        assert result.recovery_attempted is True
    
    async def test_token_usage_tracking(self, mock_research_agent, mock_analysis_agent):
        """Test that token usage is properly tracked across agents."""
        
        orchestrator = MultiAgentOrchestrator(
            research_agent=mock_research_agent,
            analysis_agent=mock_analysis_agent,
            report_agent=self._create_mock_report_agent()
        )
        
        request = ResearchRequest(query="token usage test")
        base_context = self._create_test_context()
        
        result = await orchestrator.execute_research_workflow(request, base_context)
        
        # Verify token usage was tracked
        assert result.performance_metrics.total_tokens > 0
        assert result.performance_metrics.research_tokens > 0
        assert result.performance_metrics.analysis_tokens > 0
        assert result.performance_metrics.report_tokens > 0
    
    async def test_concurrent_workflows(self, mock_research_agent, mock_analysis_agent):
        """Test system handling multiple concurrent workflows."""
        
        orchestrator = MultiAgentOrchestrator(
            research_agent=mock_research_agent,
            analysis_agent=mock_analysis_agent,
            report_agent=self._create_mock_report_agent()
        )
        
        # Create multiple concurrent requests
        requests = [
            ResearchRequest(query=f"concurrent test {i}")
            for i in range(5)
        ]
        
        base_context = self._create_test_context()
        
        # Execute concurrently
        tasks = [
            orchestrator.execute_research_workflow(req, base_context)
            for req in requests
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # All should complete successfully
        successful_results = [r for r in results if isinstance(r, WorkflowResult) and r.success]
        assert len(successful_results) == len(requests)
        
        # Each should have unique workflow ID
        workflow_ids = [r.workflow_id for r in successful_results]
        assert len(set(workflow_ids)) == len(workflow_ids)
```

## 🔨 Phase 3: Implementation (90 minutes)

### **Step 3.1: Generate Comprehensive PRP**

Run your PRP generation with the comprehensive INITIAL.md:

```bash
/generate-prp research-analysis-system-requirements.md
```

**Expected PRP Quality Check:**
- References specific multi-agent patterns from examples
- Includes comprehensive testing strategy with TestModel/FunctionModel
- Has executable validation commands for each system component
- Addresses token usage tracking and error recovery
- Includes performance monitoring and optimization guidance

### **Step 3.2: Execute Multi-Agent Implementation**

```bash
/execute-prp PRPs/research-analysis-system.md
```

**Monitor Progress During Implementation:**
- Ensure agents are created with proper dependency injection
- Verify context inheritance patterns are followed
- Check that token usage tracking is implemented correctly
- Validate error handling for each agent and the orchestration layer

### **Step 3.3: Validate Implementation Incrementally**

Run validation after each major component:

```bash
# After implementing individual agents
pytest tests/unit/test_research_agent.py -v
pytest tests/unit/test_analysis_agent.py -v
pytest tests/unit/test_report_agent.py -v

# After implementing orchestration
pytest tests/integration/test_agent_orchestration.py -v

# After implementing full system
pytest tests/system/test_complete_workflow.py -v
```

## ✅ Phase 4: Advanced Validation and Optimization (45 minutes)

### **Step 4.1: Performance Validation**

Test system performance characteristics:

```python
# tests/performance/test_system_performance.py
import pytest
import asyncio
import time
from unittest.mock import patch

class TestSystemPerformance:
    """Test performance characteristics of multi-agent system."""
    
    async def test_workflow_completion_time(self, complete_system):
        """Test that workflows complete within acceptable time."""
        
        start_time = time.time()
        
        result = await complete_system.execute_research_workflow(
            ResearchRequest(query="performance test query"),
            self._create_test_context()
        )
        
        completion_time = time.time() - start_time
        
        assert result.success
        assert completion_time < 30.0  # Should complete within 30 seconds
    
    async def test_concurrent_workflow_performance(self, complete_system):
        """Test performance under concurrent load."""
        
        # Create 10 concurrent workflows
        tasks = []
        for i in range(10):
            task = complete_system.execute_research_workflow(
                ResearchRequest(query=f"concurrent performance test {i}"),
                self._create_test_context()
            )
            tasks.append(task)
        
        start_time = time.time()
        results = await asyncio.gather(*tasks)
        completion_time = time.time() - start_time
        
        # All should succeed
        assert all(r.success for r in results)
        
        # Should complete within reasonable time for concurrent execution
        assert completion_time < 60.0  # 60 seconds for 10 concurrent workflows
        
        # Check resource usage
        total_tokens = sum(r.performance_metrics.total_tokens for r in results)
        assert total_tokens > 0  # Verify token tracking works
    
    async def test_memory_usage_stability(self, complete_system):
        """Test that system doesn't have memory leaks."""
        
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # Execute multiple workflows
        for i in range(20):
            result = await complete_system.execute_research_workflow(
                ResearchRequest(query=f"memory test {i}"),
                self._create_test_context()
            )
            assert result.success
        
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable (less than 100MB)
        assert memory_increase < 100 * 1024 * 1024
```

### **Step 4.2: Error Recovery Validation**

Test comprehensive error scenarios:

```python
# tests/error_recovery/test_error_scenarios.py
class TestErrorRecovery:
    """Test error recovery capabilities of multi-agent system."""
    
    async def test_research_agent_failure_recovery(self, system_with_failing_research):
        """Test recovery when research agent fails."""
        
        result = await system_with_failing_research.execute_research_workflow(
            ResearchRequest(query="test research failure"),
            self._create_test_context()
        )
        
        # Should attempt recovery
        assert result.recovery_attempted
        assert result.error_message is not None
        
        # Should provide partial results if possible
        if result.partial_results:
            assert len(result.partial_results) > 0
    
    async def test_external_api_failure_handling(self, complete_system):
        """Test handling of external API failures."""
        
        # Mock external API failure
        with patch('httpx.AsyncClient.get') as mock_get:
            mock_get.side_effect = httpx.TimeoutException("API timeout")
            
            result = await complete_system.execute_research_workflow(
                ResearchRequest(query="test API failure"),
                self._create_test_context()
            )
            
            # Should handle gracefully without crashing
            assert not result.success
            assert "timeout" in result.error_message.lower()
            assert result.workflow_id is not None
    
    async def test_partial_workflow_completion(self, system_with_failing_analysis):
        """Test system behavior when middle agent fails."""
        
        result = await system_with_failing_analysis.execute_research_workflow(
            ResearchRequest(query="test analysis failure"),
            self._create_test_context()
        )
        
        # Should have research data but no analysis
        assert result.research_data is not None
        assert result.analysis_insights is None
        assert result.final_report is None
        
        # Should indicate where failure occurred
        assert result.failure_phase == "analysis"
```

### **Step 4.3: Context Consistency Validation**

Verify context flows correctly between agents:

```python
# tests/context/test_context_propagation.py
class TestContextPropagation:
    """Test context inheritance and propagation across agents."""
    
    async def test_context_inheritance_chain(self, complete_system):
        """Test that context flows correctly through agent chain."""
        
        # Create context with specific attributes
        base_context = self._create_test_context()
        base_context.user_preferences = {"format": "detailed", "language": "en"}
        base_context.research_constraints = {"max_sources": 10, "credibility_threshold": 0.7}
        
        result = await complete_system.execute_research_workflow(
            ResearchRequest(query="context propagation test"),
            base_context
        )
        
        assert result.success
        
        # Verify context was used throughout workflow
        assert result.context_usage.user_preferences_applied
        assert result.context_usage.research_constraints_applied
        assert result.context_usage.token_tracking_maintained
    
    async def test_token_usage_accumulation(self, complete_system):
        """Test that token usage accumulates correctly across agents."""
        
        base_context = self._create_test_context()
        
        result = await complete_system.execute_research_workflow(
            ResearchRequest(query="token tracking test"),
            base_context
        )
        
        metrics = result.performance_metrics
        
        # Verify token usage was tracked for each agent
        assert metrics.research_tokens > 0
        assert metrics.analysis_tokens > 0
        assert metrics.report_tokens > 0
        
        # Total should equal sum of individual agents
        expected_total = (metrics.research_tokens + 
                         metrics.analysis_tokens + 
                         metrics.report_tokens)
        assert metrics.total_tokens == expected_total
```

## 🎓 Phase 5: Learning Extraction and Pattern Documentation (30 minutes)

### **Step 5.1: Extract Multi-Agent Patterns**

Document the patterns you've successfully implemented:

```markdown
# patterns/multi_agent_patterns.md

## Multi-Agent Context Engineering Patterns

### Pattern 1: Context Inheritance Chain
**Problem**: Agents need project patterns + domain specialization + execution context
**Solution**: Layered context architecture
```python
# Layer 1: Global project context (CLAUDE.md rules)
# Layer 2: Domain-specific context (agent specialization)
# Layer 3: Execution context (runtime information)

agent_context = AgentContext()
agent_context.add_layer(global_context.get_base_context())
agent_context.add_layer(domain_context.get_specialized_context(agent_type))
agent_context.add_layer(execution_context.get_runtime_context())
```

### Pattern 2: Token Usage Propagation
**Problem**: Multi-agent systems need accurate token accounting
**Solution**: Context usage threading
```python
# CRITICAL: Always pass usage from parent context
result = await child_agent.run(
    task_description,
    deps=agent_deps,
    usage=parent_context.usage  # Maintains token continuity
)
```

### Pattern 3: Error Recovery with Graceful Degradation
**Problem**: Agent failures shouldn't crash entire workflow
**Solution**: Phase-based error recovery
```python
async def execute_workflow_with_recovery(self, request, context):
    try:
        research_result = await self._research_phase(request, context)
        if research_result.failed:
            return await self._handle_research_failure(research_result)
        
        analysis_result = await self._analysis_phase(research_result, context)
        if analysis_result.failed:
            # Provide partial results
            return PartialResult(research=research_result, analysis_error=analysis_result.error)
    except Exception as e:
        return await self._global_error_recovery(e, request)
```

### Pattern 4: Testing Multi-Agent Systems Without API Costs
**Problem**: Testing complex agent interactions is expensive
**Solution**: TestModel and FunctionModel with realistic mocking
```python
def create_mock_research_agent():
    def mock_response(query: str) -> str:
        if "error" in query:
            return "Error occurred during research"
        return f"Research results for: {query}"
    
    agent = Agent('test', system_prompt="Research specialist")
    agent.override(model=FunctionModel(mock_response))
    return agent
```
```

### **Step 5.2: Update Examples Library**

Add the successful patterns to your examples library:

```
examples/
├── multi_agent/
│   ├── orchestration_patterns.py          # Workflow coordination
│   ├── context_inheritance.py             # Context layering and propagation
│   ├── error_recovery_patterns.py         # Error handling in complex systems
│   └── token_usage_tracking.py            # Token accounting across agents
├── testing/
│   ├── multi_agent_testing.py             # Testing strategies for agent systems
│   └── mock_agent_patterns.py             # Realistic mocking without API costs
└── performance/
    ├── concurrent_workflow_patterns.py     # Performance optimization
    └── memory_management_patterns.py       # Resource management in agent systems
```

### **Step 5.3: Document Lessons Learned**

Create comprehensive lessons learned document:

```markdown
# lessons-learned-multi-agent.md

## Key Insights from Multi-Agent Implementation

### What Worked Exceptionally Well:
1. **Layered Context Architecture**: Context inheritance prevented pattern duplication across agents
2. **TestModel for Development**: Rapid iteration without API costs enabled complex system development
3. **Phase-based Error Recovery**: Graceful degradation provided better user experience than all-or-nothing failures
4. **Performance Monitoring**: Built-in metrics enabled optimization and debugging

### What Was More Challenging Than Expected:
1. **Token Usage Tracking**: Ensuring accurate accounting across agent boundaries required careful attention
2. **Error Propagation**: Deciding when to fail fast vs. attempt recovery required business logic consideration
3. **Context Serialization**: Passing complex context between agents needed thoughtful design
4. **Testing Complexity**: Multi-agent systems have exponentially more interaction scenarios to test

### Patterns That Emerged During Development:
1. **Agent Specialization**: Each agent should have a single, well-defined responsibility
2. **Context Composition**: Build context dynamically based on workflow requirements
3. **Async Throughout**: Any synchronous operations block the entire workflow
4. **Monitoring is Essential**: Complex systems need observability for debugging and optimization

### Recommendations for Future Multi-Agent Projects:
1. **Start Simple**: Begin with 2 agents and add complexity gradually
2. **Design for Observability**: Build monitoring and logging from the beginning
3. **Test Error Scenarios**: Multi-agent systems have many failure modes to consider
4. **Optimize Token Usage**: Monitor and optimize token consumption across agents
5. **Plan for Scale**: Consider resource usage and performance implications early
```

## ✅ Exercise 2 Completion Checklist

Before considering this exercise complete, ensure you have:

**✅ System Implementation**
- [ ] Working multi-agent system with 3+ specialized agents
- [ ] Proper context inheritance across all agents
- [ ] Token usage tracking throughout the system
- [ ] Comprehensive error handling and recovery

**✅ Quality Assurance**
- [ ] All tests pass using TestModel/FunctionModel (no API costs)
- [ ] Performance validation shows acceptable response times
- [ ] Error recovery testing demonstrates graceful failure handling
- [ ] Context propagation testing verifies proper inheritance

**✅ Documentation and Learning**
- [ ] Extracted reusable patterns for future multi-agent development
- [ ] Added successful patterns to examples library
- [ ] Documented lessons learned and recommendations
- [ ] Updated CLAUDE.md with multi-agent specific guidance

**✅ Advanced Features**
- [ ] Concurrent workflow handling
- [ ] Performance monitoring and optimization
- [ ] Memory management and resource efficiency
- [ ] Extensible architecture for adding new agent types

## 🔄 Reflection Questions

Take time to reflect on this advanced exercise:

1. **Context Engineering at Scale**: How did managing context across multiple agents differ from single-agent scenarios?

2. **Error Recovery Strategy**: What trade-offs did you discover between failing fast and attempting recovery?

3. **Testing Complexity**: How did testing strategies need to evolve for multi-agent systems?

4. **Performance Considerations**: What performance bottlenecks emerged and how did you address them?

5. **Pattern Reusability**: Which patterns from this exercise would be valuable for other complex systems?

## 📈 Success Metrics

**Excellent Exercise Completion (9-10/10):**
- Multi-agent system works flawlessly with proper context inheritance
- Comprehensive testing strategy avoids API costs while ensuring reliability
- Error recovery provides graceful degradation and useful feedback
- Performance is optimized for concurrent workflows
- Extracted patterns are well-documented and reusable

**Good Exercise Completion (7-8/10):**
- Multi-agent system works with minor issues
- Testing covers main scenarios effectively
- Basic error handling prevents system crashes
- Performance is acceptable for normal load
- Some patterns extracted and documented

**Adequate Exercise Completion (5-6/10):**
- Basic multi-agent functionality working
- Some testing implemented
- Error handling present but basic
- System works but performance not optimized
- Learning occurred but not systematically captured

## 🚀 Next Steps

**Ready for Production**: If you scored 8+, you're ready to build production multi-agent systems

**Need More Practice**: If you scored 6-7, try simplifying the system and focus on one advanced pattern at a time

**Foundation Building**: If you scored below 6, consider returning to Exercise 1 and building more experience with single-agent systems first

## 🎯 Advanced Extensions

If you want to push further:

1. **Add Real-Time Collaboration**: Multiple users researching simultaneously
2. **Implement Learning**: Agents that improve based on user feedback
3. **Add Visual Components**: Integration with charting and visualization tools
4. **Build Configuration UI**: Allow users to customize agent behavior
5. **Add Workflow Persistence**: Save and resume complex research projects

---

**Congratulations!** You've completed a sophisticated multi-agent Context Engineering implementation. You now understand how to apply Context Engineering principles to complex, distributed systems with multiple AI agents working together.

*This exercise represents advanced Context Engineering mastery - the patterns and insights you've gained will serve you well in building production AI systems.*