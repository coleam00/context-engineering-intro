# Chapter 11: Advanced Patterns

> **"Advanced Context Engineering patterns transform complex challenges into systematic solutions that scale beyond individual features to entire architectural domains."**

This chapter explores sophisticated Context Engineering patterns for complex systems, multi-agent architectures, and advanced integration scenarios. You'll learn how to apply Context Engineering to the most challenging development scenarios.

## 🎯 Learning Objectives

By the end of this chapter, you will:
- Master advanced Context Engineering patterns for complex systems
- Understand multi-agent Context Engineering architectures
- Know how to handle cross-domain integration with context systems
- Be able to design Context Engineering for microservices and distributed systems
- Recognize when and how to apply meta-context engineering patterns

## 🏗️ Advanced Architectural Patterns

### **Pattern 1: Multi-Agent Context Systems**

#### **The Agent-as-Tool Context Pattern**

```python
# Advanced multi-agent context engineering
class AgentContextOrchestrator:
    """
    Orchestrates context across multiple specialized agents.
    
    This pattern demonstrates how to maintain context consistency
    across agent boundaries while allowing for specialized contexts.
    """
    
    def __init__(self):
        self.global_context = GlobalContextManager()
        self.agent_contexts = {}
    
    async def create_specialized_agent(
        self, 
        agent_type: str, 
        domain_context: DomainContext,
        parent_context: Optional[RunContext] = None
    ) -> SpecializedAgent:
        """
        Create agent with inherited context plus domain specialization.
        
        Pattern: Context inheritance with specialization
        - Global context provides project-wide patterns
        - Domain context adds specialization
        - Parent context provides execution context
        """
        
        # Build layered context
        agent_context = AgentContext()
        
        # Layer 1: Global project context
        agent_context.add_layer(self.global_context.get_base_context())
        
        # Layer 2: Domain-specific context
        agent_context.add_layer(domain_context.get_specialized_context(agent_type))
        
        # Layer 3: Parent execution context (if available)
        if parent_context:
            agent_context.add_layer(parent_context.get_execution_context())
        
        # Create agent with composed context
        agent = SpecializedAgent(
            agent_type=agent_type,
            context=agent_context,
            tools=domain_context.get_tools_for_agent(agent_type)
        )
        
        # Register for context synchronization
        self.agent_contexts[agent.id] = agent_context
        
        return agent
    
    async def delegate_with_context_propagation(
        self,
        parent_agent: Agent,
        child_agent: Agent,
        task: Task,
        context_transfer: ContextTransfer
    ) -> TaskResult:
        """
        Delegate task between agents with proper context propagation.
        
        Pattern: Context serialization and transfer
        - Serialize execution context from parent
        - Merge with child agent's specialized context
        - Maintain token usage and conversation history
        """
        
        # Extract transferable context from parent
        transferable_context = context_transfer.extract_transferable(
            parent_agent.current_context
        )
        
        # Merge with child's context
        child_context = self._merge_contexts(
            transferable_context,
            child_agent.base_context,
            merge_strategy=context_transfer.merge_strategy
        )
        
        # Execute with composed context
        result = await child_agent.run(
            task.description,
            context=child_context,
            usage=parent_agent.current_context.usage  # Critical for token tracking
        )
        
        # Extract learnings for context improvement
        learnings = context_transfer.extract_learnings(result)
        await self._update_context_from_learnings(learnings)
        
        return result

# Example usage in complex multi-agent system
class ResearchAndAnalysisSystem:
    """
    Complex system demonstrating advanced context patterns.
    
    This system shows:
    - Hierarchical agent organization
    - Context specialization by domain
    - Cross-agent context sharing
    - Learning and context evolution
    """
    
    def __init__(self):
        self.orchestrator = AgentContextOrchestrator()
        self.research_context = ResearchDomainContext()
        self.analysis_context = AnalysisDomainContext()
        self.writing_context = WritingDomainContext()
    
    async def process_research_request(self, request: ResearchRequest) -> ResearchResult:
        """Process complex research request using multiple specialized agents."""
        
        # Create specialized agents with proper context inheritance
        web_researcher = await self.orchestrator.create_specialized_agent(
            agent_type="web_researcher",
            domain_context=self.research_context
        )
        
        data_analyst = await self.orchestrator.create_specialized_agent(
            agent_type="data_analyst", 
            domain_context=self.analysis_context
        )
        
        report_writer = await self.orchestrator.create_specialized_agent(
            agent_type="report_writer",
            domain_context=self.writing_context
        )
        
        # Execute research pipeline with context propagation
        research_data = await self.orchestrator.delegate_with_context_propagation(
            parent_agent=None,  # Top-level request
            child_agent=web_researcher,
            task=Task("research", request.query),
            context_transfer=ResearchContextTransfer()
        )
        
        analysis_results = await self.orchestrator.delegate_with_context_propagation(
            parent_agent=web_researcher,
            child_agent=data_analyst,
            task=Task("analyze", research_data),
            context_transfer=AnalysisContextTransfer()
        )
        
        final_report = await self.orchestrator.delegate_with_context_propagation(
            parent_agent=data_analyst,
            child_agent=report_writer,
            task=Task("write_report", analysis_results),
            context_transfer=WritingContextTransfer()
        )
        
        return ResearchResult(
            research_data=research_data,
            analysis=analysis_results,
            report=final_report
        )
```

### **Pattern 2: Domain-Driven Context Architecture**

```python
# Domain-driven context organization
class DomainContextArchitecture:
    """
    Organize context by business domains rather than technical layers.
    
    This pattern is essential for large systems where different domains
    have different patterns, constraints, and quality requirements.
    """
    
    def __init__(self):
        self.domains = {}
    
    def register_domain(self, domain_name: str, domain_config: DomainConfig):
        """Register a business domain with its specific context."""
        
        domain_context = DomainContext(
            name=domain_name,
            patterns=domain_config.patterns,
            constraints=domain_config.constraints,
            quality_gates=domain_config.quality_gates,
            examples=domain_config.examples
        )
        
        self.domains[domain_name] = domain_context
    
    def get_context_for_feature(self, feature: Feature) -> ContextBundle:
        """Get appropriate context bundle for a specific feature."""
        
        # Identify applicable domains
        applicable_domains = self._identify_domains_for_feature(feature)
        
        # Build layered context
        context_bundle = ContextBundle()
        
        # Add cross-cutting concerns (always applicable)
        context_bundle.add_layer(self._get_cross_cutting_context())
        
        # Add domain-specific context layers
        for domain in applicable_domains:
            domain_context = self.domains[domain]
            context_bundle.add_layer(domain_context.get_context_for_feature(feature))
        
        # Add feature-specific context
        context_bundle.add_layer(self._get_feature_specific_context(feature))
        
        return context_bundle

# Example domain contexts
class ECommerceContextArchitecture(DomainContextArchitecture):
    """E-commerce specific domain context architecture."""
    
    def __init__(self):
        super().__init__()
        self._setup_ecommerce_domains()
    
    def _setup_ecommerce_domains(self):
        """Setup e-commerce specific domain contexts."""
        
        # User Management Domain
        self.register_domain("user_management", DomainConfig(
            patterns={
                "authentication": "examples/auth/jwt_patterns.py",
                "user_registration": "examples/users/registration_flow.py",
                "profile_management": "examples/users/profile_crud.py"
            },
            constraints={
                "privacy": "All user data must be GDPR compliant",
                "security": "Passwords must meet OWASP standards",
                "performance": "Auth operations must complete in <200ms"
            },
            quality_gates=[
                "pytest tests/auth/ --cov=90",
                "python scripts/security_audit.py",
                "python scripts/gdpr_compliance_check.py"
            ],
            examples="examples/domains/user_management/"
        ))
        
        # Product Catalog Domain
        self.register_domain("product_catalog", DomainConfig(
            patterns={
                "product_search": "examples/catalog/search_patterns.py",
                "inventory_management": "examples/catalog/inventory_sync.py",
                "pricing_engine": "examples/catalog/dynamic_pricing.py"
            },
            constraints={
                "consistency": "Inventory must be eventually consistent",
                "performance": "Search must return results in <100ms",
                "accuracy": "Pricing must be accurate to 2 decimal places"
            },
            quality_gates=[
                "pytest tests/catalog/ --cov=85",
                "python scripts/search_performance_test.py",
                "python scripts/inventory_consistency_check.py"
            ],
            examples="examples/domains/product_catalog/"
        ))
        
        # Order Processing Domain
        self.register_domain("order_processing", DomainConfig(
            patterns={
                "order_workflow": "examples/orders/state_machine.py",
                "payment_processing": "examples/orders/payment_flow.py",
                "fulfillment": "examples/orders/fulfillment_pipeline.py"
            },
            constraints={
                "reliability": "Orders must not be lost or duplicated",
                "atomicity": "Payment and inventory must be atomic",
                "auditability": "All order changes must be logged"
            },
            quality_gates=[
                "pytest tests/orders/ --cov=95",
                "python scripts/order_integrity_test.py",
                "python scripts/payment_reconciliation_test.py"
            ],
            examples="examples/domains/order_processing/"
        ))
```

### **Pattern 3: Microservices Context Federation**

```python
# Microservices context federation pattern
class MicroservicesContextFederation:
    """
    Federate context across microservices while maintaining service autonomy.
    
    This pattern is crucial for organizations with multiple teams
    working on different services that need consistent patterns.
    """
    
    def __init__(self):
        self.service_contexts = {}
        self.shared_context = SharedContextRegistry()
    
    def register_service(self, service_name: str, context_config: ServiceContextConfig):
        """Register a microservice with its context configuration."""
        
        service_context = ServiceContext(
            name=service_name,
            local_patterns=context_config.local_patterns,
            shared_patterns=context_config.shared_patterns,
            integration_patterns=context_config.integration_patterns,
            service_constraints=context_config.constraints
        )
        
        self.service_contexts[service_name] = service_context
        
        # Register shared patterns for other services to use
        self.shared_context.register_patterns(
            service_name, 
            context_config.shared_patterns
        )
    
    def get_federated_context(self, service_name: str, feature_type: str) -> FederatedContext:
        """Get context that combines local and federated patterns."""
        
        service_context = self.service_contexts[service_name]
        federated_context = FederatedContext()
        
        # Layer 1: Organization-wide patterns
        federated_context.add_layer(self.shared_context.get_org_patterns())
        
        # Layer 2: Cross-service integration patterns
        integration_services = service_context.get_integration_dependencies(feature_type)
        for dep_service in integration_services:
            integration_patterns = self.shared_context.get_integration_patterns(
                service_name, dep_service
            )
            federated_context.add_layer(integration_patterns)
        
        # Layer 3: Service-specific patterns
        federated_context.add_layer(service_context.get_local_patterns(feature_type))
        
        return federated_context

# Example: E-commerce microservices federation
class ECommerceMicroservicesFederation(MicroservicesContextFederation):
    """E-commerce microservices with federated context."""
    
    def __init__(self):
        super().__init__()
        self._setup_ecommerce_services()
    
    def _setup_ecommerce_services(self):
        """Setup e-commerce microservices context federation."""
        
        # User Service
        self.register_service("user-service", ServiceContextConfig(
            local_patterns={
                "user_crud": "patterns/user_management.py",
                "auth_flow": "patterns/authentication.py",
                "profile_validation": "patterns/user_validation.py"
            },
            shared_patterns={
                "api_response_format": "shared/api_responses.py",
                "error_handling": "shared/error_patterns.py",
                "logging_format": "shared/logging_patterns.py"
            },
            integration_patterns={
                "event_publishing": "integration/user_events.py",
                "api_versioning": "integration/api_versioning.py"
            },
            constraints={
                "data_privacy": "GDPR compliance required",
                "performance": "Response time <200ms",
                "security": "JWT tokens for all endpoints"
            }
        ))
        
        # Product Service
        self.register_service("product-service", ServiceContextConfig(
            local_patterns={
                "product_search": "patterns/search_implementation.py",
                "inventory_sync": "patterns/inventory_management.py",
                "catalog_cache": "patterns/caching_strategy.py"
            },
            shared_patterns={
                "api_response_format": "shared/api_responses.py",
                "error_handling": "shared/error_patterns.py",
                "pagination": "shared/pagination_patterns.py"
            },
            integration_patterns={
                "event_consumption": "integration/inventory_events.py",
                "search_indexing": "integration/elasticsearch_patterns.py"
            },
            constraints={
                "consistency": "Eventual consistency acceptable",
                "performance": "Search results <100ms",
                "availability": "99.9% uptime required"
            }
        ))
        
        # Order Service  
        self.register_service("order-service", ServiceContextConfig(
            local_patterns={
                "order_state_machine": "patterns/order_workflow.py",
                "payment_integration": "patterns/payment_processing.py",
                "saga_patterns": "patterns/distributed_transactions.py"
            },
            shared_patterns={
                "api_response_format": "shared/api_responses.py",
                "event_sourcing": "shared/event_sourcing_patterns.py"
            },
            integration_patterns={
                "saga_orchestration": "integration/saga_patterns.py",
                "compensating_transactions": "integration/compensation.py"
            },
            constraints={
                "reliability": "Zero data loss acceptable",
                "atomicity": "Distributed transactions required",
                "auditability": "Complete audit trail required"
            }
        ))
```

## 🔄 Meta-Context Engineering Patterns

### **Pattern 4: Self-Evolving Context Systems**

```python
# Self-evolving context system
class SelfEvolvingContextSystem:
    """
    Context system that learns and improves from implementation outcomes.
    
    This represents the highest form of Context Engineering automation:
    systems that improve their own context based on results.
    """
    
    def __init__(self):
        self.context_database = ContextDatabase()
        self.pattern_analyzer = PatternAnalyzer()
        self.outcome_tracker = OutcomeTracker()
        self.context_optimizer = ContextOptimizer()
    
    async def track_implementation_outcome(
        self, 
        context_used: ContextBundle,
        implementation_result: ImplementationResult
    ):
        """Track the relationship between context and outcomes."""
        
        outcome_record = OutcomeRecord(
            context_bundle=context_used,
            result=implementation_result,
            timestamp=datetime.utcnow(),
            success_metrics=implementation_result.get_success_metrics()
        )
        
        await self.outcome_tracker.record_outcome(outcome_record)
        
        # Analyze patterns in successful vs. failed implementations
        if len(await self.outcome_tracker.get_recent_outcomes()) >= 10:
            await self._analyze_and_improve_context()
    
    async def _analyze_and_improve_context(self):
        """Analyze outcomes and improve context accordingly."""
        
        recent_outcomes = await self.outcome_tracker.get_recent_outcomes(limit=50)
        
        # Identify patterns in successful implementations
        successful_patterns = await self.pattern_analyzer.extract_success_patterns(
            [outcome for outcome in recent_outcomes if outcome.was_successful()]
        )
        
        # Identify patterns in failed implementations
        failure_patterns = await self.pattern_analyzer.extract_failure_patterns(
            [outcome for outcome in recent_outcomes if not outcome.was_successful()]
        )
        
        # Generate context improvements
        improvements = await self.context_optimizer.generate_improvements(
            success_patterns=successful_patterns,
            failure_patterns=failure_patterns,
            current_context=await self.context_database.get_current_context()
        )
        
        # Apply improvements with validation
        for improvement in improvements:
            await self._validate_and_apply_improvement(improvement)
    
    async def _validate_and_apply_improvement(self, improvement: ContextImprovement):
        """Validate context improvement before applying."""
        
        # Test improvement with historical scenarios
        validation_results = await self._test_improvement_with_history(improvement)
        
        if validation_results.success_rate > 0.8:  # 80% success threshold
            await self.context_database.apply_improvement(improvement)
            
            # Log the improvement for team awareness
            await self._log_context_evolution(improvement, validation_results)
        else:
            # Log why improvement was rejected
            await self._log_rejected_improvement(improvement, validation_results)

class PatternAnalyzer:
    """Analyze patterns in implementation outcomes to improve context."""
    
    async def extract_success_patterns(self, successful_outcomes: List[OutcomeRecord]) -> List[SuccessPattern]:
        """Extract patterns from successful implementations."""
        
        patterns = []
        
        # Analyze context elements that appear frequently in successes
        context_frequency = self._analyze_context_element_frequency(successful_outcomes)
        
        for element, frequency in context_frequency.items():
            if frequency > 0.7:  # Appears in 70%+ of successes
                pattern = SuccessPattern(
                    context_element=element,
                    success_correlation=frequency,
                    supporting_outcomes=self._get_supporting_outcomes(element, successful_outcomes)
                )
                patterns.append(pattern)
        
        # Analyze context combinations that work well together
        combination_patterns = self._analyze_context_combinations(successful_outcomes)
        patterns.extend(combination_patterns)
        
        return patterns
    
    async def extract_failure_patterns(self, failed_outcomes: List[OutcomeRecord]) -> List[FailurePattern]:
        """Extract patterns from failed implementations."""
        
        patterns = []
        
        # Analyze missing context in failures
        missing_context = self._analyze_missing_context(failed_outcomes)
        
        for missing_element, failure_rate in missing_context.items():
            if failure_rate > 0.6:  # Missing in 60%+ of failures
                pattern = FailurePattern(
                    missing_context=missing_element,
                    failure_correlation=failure_rate,
                    recommended_addition=self._recommend_context_addition(missing_element)
                )
                patterns.append(pattern)
        
        # Analyze context that correlates with failures
        problematic_context = self._analyze_problematic_context(failed_outcomes)
        
        for context_element, failure_rate in problematic_context.items():
            if failure_rate > 0.5:  # Present in 50%+ of failures
                pattern = FailurePattern(
                    problematic_context=context_element,
                    failure_correlation=failure_rate,
                    recommended_change=self._recommend_context_change(context_element)
                )
                patterns.append(pattern)
        
        return patterns
```

### **Pattern 5: Cross-Domain Context Synthesis**

```python
# Cross-domain context synthesis
class CrossDomainContextSynthesizer:
    """
    Synthesize context across different domains to handle complex features
    that span multiple business domains or technical layers.
    """
    
    def __init__(self):
        self.domain_contexts = {}
        self.synthesis_strategies = {}
    
    def register_domain_context(self, domain: str, context: DomainContext):
        """Register a domain-specific context."""
        self.domain_contexts[domain] = context
    
    def register_synthesis_strategy(self, domains: List[str], strategy: SynthesisStrategy):
        """Register how to synthesize context across specific domains."""
        domain_key = tuple(sorted(domains))
        self.synthesis_strategies[domain_key] = strategy
    
    async def synthesize_context_for_feature(self, feature: CrossDomainFeature) -> SynthesizedContext:
        """Synthesize context for a feature that spans multiple domains."""
        
        involved_domains = feature.get_involved_domains()
        domain_key = tuple(sorted(involved_domains))
        
        # Get synthesis strategy for this domain combination
        strategy = self.synthesis_strategies.get(
            domain_key, 
            self._get_default_synthesis_strategy()
        )
        
        # Collect context from each domain
        domain_contexts = {}
        for domain in involved_domains:
            domain_context = self.domain_contexts[domain]
            domain_contexts[domain] = await domain_context.get_context_for_feature(feature)
        
        # Synthesize using strategy
        synthesized_context = await strategy.synthesize(
            domain_contexts=domain_contexts,
            feature=feature,
            synthesis_rules=self._get_synthesis_rules(domain_key)
        )
        
        return synthesized_context

# Example: E-commerce checkout synthesis
class CheckoutFeatureSynthesis:
    """
    Example of cross-domain synthesis for e-commerce checkout.
    
    Checkout spans: User Management, Product Catalog, Inventory, 
    Payment Processing, Order Management, and Shipping domains.
    """
    
    def __init__(self):
        self.synthesizer = CrossDomainContextSynthesizer()
        self._setup_ecommerce_synthesis()
    
    def _setup_ecommerce_synthesis(self):
        """Setup synthesis strategies for e-commerce cross-domain features."""
        
        # Checkout feature synthesis strategy
        checkout_domains = ["user_management", "product_catalog", "inventory", 
                          "payment", "order_management", "shipping"]
        
        self.synthesizer.register_synthesis_strategy(
            checkout_domains,
            CheckoutSynthesisStrategy()
        )
        
        # Cart management synthesis strategy
        cart_domains = ["user_management", "product_catalog", "inventory", "pricing"]
        
        self.synthesizer.register_synthesis_strategy(
            cart_domains,
            CartSynthesisStrategy()
        )

class CheckoutSynthesisStrategy(SynthesisStrategy):
    """Synthesis strategy specific to checkout workflow."""
    
    async def synthesize(
        self, 
        domain_contexts: Dict[str, DomainContext],
        feature: CrossDomainFeature,
        synthesis_rules: SynthesisRules
    ) -> SynthesizedContext:
        """Synthesize checkout-specific context from multiple domains."""
        
        synthesized = SynthesizedContext()
        
        # Phase 1: User authentication and session management
        auth_context = self._synthesize_auth_context(
            domain_contexts["user_management"],
            feature.auth_requirements
        )
        synthesized.add_phase("authentication", auth_context)
        
        # Phase 2: Cart validation and pricing
        cart_context = self._synthesize_cart_context(
            domain_contexts["product_catalog"],
            domain_contexts["inventory"],
            feature.cart_requirements
        )
        synthesized.add_phase("cart_validation", cart_context)
        
        # Phase 3: Payment processing
        payment_context = self._synthesize_payment_context(
            domain_contexts["payment"],
            domain_contexts["user_management"],  # For payment methods
            feature.payment_requirements
        )
        synthesized.add_phase("payment_processing", payment_context)
        
        # Phase 4: Order creation and fulfillment
        order_context = self._synthesize_order_context(
            domain_contexts["order_management"],
            domain_contexts["inventory"],
            domain_contexts["shipping"],
            feature.fulfillment_requirements
        )
        synthesized.add_phase("order_fulfillment", order_context)
        
        # Add cross-cutting concerns
        synthesized.add_cross_cutting_context(
            error_handling=self._synthesize_error_handling(domain_contexts),
            transaction_management=self._synthesize_transaction_context(domain_contexts),
            monitoring=self._synthesize_monitoring_context(domain_contexts)
        )
        
        return synthesized
    
    def _synthesize_auth_context(self, user_context: DomainContext, auth_requirements: AuthRequirements) -> PhaseContext:
        """Synthesize authentication context for checkout."""
        
        auth_patterns = user_context.get_patterns("authentication")
        session_patterns = user_context.get_patterns("session_management")
        
        return PhaseContext(
            patterns={
                "user_verification": auth_patterns.user_verification,
                "session_validation": session_patterns.session_validation,
                "guest_checkout": auth_patterns.guest_checkout if auth_requirements.allow_guest else None
            },
            constraints={
                "session_timeout": "30 minutes for checkout flow",
                "re_auth_required": "For payment step if session > 15 minutes old"
            },
            validation=[
                "test_authenticated_checkout_flow",
                "test_guest_checkout_flow",
                "test_session_timeout_handling"
            ]
        )
```

## 🚀 Advanced Integration Patterns

### **Pattern 6: Event-Driven Context Propagation**

```python
# Event-driven context propagation
class EventDrivenContextPropagation:
    """
    Propagate context across service boundaries using events.
    
    This pattern is essential for maintaining context consistency
    in event-driven architectures and asynchronous systems.
    """
    
    def __init__(self):
        self.event_bus = EventBus()
        self.context_serializer = ContextSerializer()
        self.context_handlers = {}
    
    def register_context_handler(self, event_type: str, handler: ContextHandler):
        """Register handler for context propagation on specific event types."""
        self.context_handlers[event_type] = handler
    
    async def publish_event_with_context(
        self, 
        event: DomainEvent, 
        source_context: ExecutionContext
    ) -> EventPublicationResult:
        """Publish event with properly serialized context."""
        
        # Serialize context for transmission
        serialized_context = await self.context_serializer.serialize(
            context=source_context,
            event_type=event.event_type,
            serialization_strategy=self._get_serialization_strategy(event)
        )
        
        # Create context-aware event
        context_event = ContextAwareEvent(
            base_event=event,
            execution_context=serialized_context,
            context_metadata=self._extract_context_metadata(source_context)
        )
        
        # Publish through event bus
        publication_result = await self.event_bus.publish(context_event)
        
        # Track context propagation for analytics
        await self._track_context_propagation(context_event, publication_result)
        
        return publication_result
    
    async def handle_event_with_context(
        self, 
        context_event: ContextAwareEvent
    ) -> EventHandlingResult:
        """Handle incoming event with context reconstruction."""
        
        # Deserialize context
        execution_context = await self.context_serializer.deserialize(
            context_event.execution_context
        )
        
        # Get appropriate handler
        handler = self.context_handlers.get(
            context_event.base_event.event_type,
            self._get_default_handler()
        )
        
        # Execute handler with reconstructed context
        handling_result = await handler.handle(
            event=context_event.base_event,
            context=execution_context,
            metadata=context_event.context_metadata
        )
        
        return handling_result

# Example: Order processing with context propagation
class OrderProcessingWithContext:
    """Order processing system with event-driven context propagation."""
    
    def __init__(self):
        self.context_propagation = EventDrivenContextPropagation()
        self._setup_order_context_handlers()
    
    def _setup_order_context_handlers(self):
        """Setup context handlers for order processing events."""
        
        # Order created event
        self.context_propagation.register_context_handler(
            "order_created",
            OrderCreatedContextHandler()
        )
        
        # Payment processed event
        self.context_propagation.register_context_handler(
            "payment_processed", 
            PaymentProcessedContextHandler()
        )
        
        # Inventory reserved event
        self.context_propagation.register_context_handler(
            "inventory_reserved",
            InventoryReservedContextHandler()
        )
    
    async def create_order(self, order_request: OrderRequest, user_context: UserContext) -> OrderResult:
        """Create order with full context propagation."""
        
        # Create execution context for this order
        execution_context = ExecutionContext(
            user=user_context,
            session=order_request.session_context,
            business_rules=await self._get_order_business_rules(),
            quality_requirements=await self._get_order_quality_requirements()
        )
        
        # Process order creation
        order = await self._create_order_entity(order_request, execution_context)
        
        # Publish order created event with context
        order_created_event = OrderCreatedEvent(
            order_id=order.id,
            user_id=order.user_id,
            items=order.items,
            total_amount=order.total
        )
        
        await self.context_propagation.publish_event_with_context(
            event=order_created_event,
            source_context=execution_context
        )
        
        return OrderResult(order=order, context=execution_context)

class OrderCreatedContextHandler(ContextHandler):
    """Handle order created events with proper context."""
    
    async def handle(
        self, 
        event: OrderCreatedEvent, 
        context: ExecutionContext,
        metadata: ContextMetadata
    ) -> EventHandlingResult:
        """Handle order creation with inherited context."""
        
        results = []
        
        # Trigger inventory reservation with context
        inventory_result = await self._reserve_inventory_with_context(event, context)
        results.append(inventory_result)
        
        # Trigger payment processing with context
        payment_result = await self._process_payment_with_context(event, context)
        results.append(payment_result)
        
        # Trigger shipping calculation with context
        shipping_result = await self._calculate_shipping_with_context(event, context)
        results.append(shipping_result)
        
        return EventHandlingResult(
            success=all(r.success for r in results),
            downstream_actions=results,
            context_evolution=self._extract_context_learnings(results)
        )
```

## ✅ Chapter 11 Checklist

Before moving to Chapter 12, ensure you understand:

- [ ] **Multi-Agent Patterns**: Context orchestration and agent-as-tool patterns
- [ ] **Domain-Driven Context**: Organizing context by business domains
- [ ] **Microservices Federation**: Context sharing across service boundaries
- [ ] **Meta-Context Engineering**: Self-evolving and learning context systems
- [ ] **Cross-Domain Synthesis**: Handling features that span multiple domains
- [ ] **Event-Driven Propagation**: Context propagation in asynchronous systems

## 🎯 Key Takeaways

1. **Advanced patterns enable complex systems** - Sophisticated context architectures handle enterprise-scale challenges
2. **Domain-driven organization scales better** - Organize context by business domains, not technical layers
3. **Federation enables autonomy with consistency** - Services can maintain independence while sharing patterns
4. **Meta-context engineering enables evolution** - Systems can improve their own context based on outcomes
5. **Cross-domain synthesis handles complexity** - Sophisticated features require sophisticated context strategies
6. **Event-driven propagation maintains consistency** - Context can flow through asynchronous systems

## 📚 Next Steps

Ready to see these advanced patterns applied in real-world scenarios?

👉 **[Chapter 12: Real-World Examples](chapter-12-real-world-examples.md)**

In Chapter 12, you'll analyze real implementations that demonstrate these advanced patterns in production systems.

---

## 🔬 Advanced Pattern Practice

**Choose an advanced pattern to implement:**

1. **Multi-Agent System**: Design a context orchestration system for 3+ specialized agents
2. **Domain Federation**: Create context federation for a multi-service architecture  
3. **Cross-Domain Feature**: Design context synthesis for a feature spanning 4+ domains
4. **Self-Evolving Context**: Build a system that learns from implementation outcomes

**Implementation Guidelines:**
- Start with the pattern most relevant to your current architecture
- Focus on context flow and consistency across boundaries
- Build validation that ensures pattern effectiveness
- Document learnings for future pattern refinement

*This advanced practice will help you master the most sophisticated Context Engineering techniques.*