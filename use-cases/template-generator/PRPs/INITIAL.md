# Template Generation Request

## TECHNOLOGY/FRAMEWORK:

**Example:** Pydantic AI agents  
**Example:** Supabase frontend applications  
**Example:** CrewAI multi-agent systems  

**Your technology:** [Specify the exact framework, library, or technology you want to create a context engineering template for]

---

## TEMPLATE PURPOSE:

**What specific use case should this template be optimized for?**

**Example for Pydantic AI:** "Building intelligent AI agents with tool integration, conversation handling, and structured data validation using Pydantic AI framework"

**Example for Supabase:** "Creating full-stack web applications with real-time data, authentication, and serverless functions using Supabase as the backend"

**Your purpose:** [Be very specific about what developers should be able to build easily with this template]

---

## CORE FEATURES:

**What are the essential features this template should help developers implement?**

**Example for Pydantic AI:**
- Agent creation with different model providers (OpenAI, Anthropic, Gemini)
- Tool integration patterns (web search, file operations, API calls)
- Conversation memory and context management
- Structured output validation with Pydantic models
- Error handling and retry mechanisms
- Testing patterns for AI agent behavior

**Example for Supabase:**
- Database schema design and migrations
- Real-time subscriptions and live data updates
- Row Level Security (RLS) policy implementation
- Authentication flows (email, OAuth, magic links)
- Serverless edge functions for backend logic
- File storage and CDN integration

**Your core features:** [List the specific capabilities developers should be able to implement easily]

---

## EXAMPLES TO INCLUDE:

**What working examples should be provided in the template?**

**Example for Pydantic AI:**
- Basic chat agent with memory
- Tool-enabled agent (web search + calculator)
- Multi-step workflow agent
- Agent with custom Pydantic models for structured outputs
- Testing examples for agent responses and tool usage

**Example for Supabase:**
- User authentication and profile management
- Real-time chat or messaging system
- File upload and sharing functionality
- Multi-tenant application patterns
- Database triggers and functions

**Your examples:** [Specify concrete, working examples that should be included]

---

## DOCUMENTATION TO RESEARCH:

**What specific documentation should be thoroughly researched and referenced?**

**Example for Pydantic AI:**
- https://ai.pydantic.dev/ - Official Pydantic AI documentation
- https://docs.pydantic.dev/ - Pydantic data validation library
- Model provider APIs (OpenAI, Anthropic) for integration patterns
- Tool integration best practices and examples
- Testing frameworks for AI applications

**Example for Supabase:**
- https://supabase.com/docs - Complete Supabase documentation
- https://supabase.com/docs/guides/auth - Authentication guide
- https://supabase.com/docs/guides/realtime - Real-time features
- Database design patterns and RLS policies
- Edge functions development and deployment

**Your documentation:** [List specific URLs and documentation sections to research deeply]

---

## DEVELOPMENT PATTERNS:

**What specific development patterns, project structures, or workflows should be researched and included?**

**Example for Pydantic AI:**
- How to structure agent modules and tool definitions
- Configuration management for different model providers
- Environment setup for development vs production
- Logging and monitoring patterns for AI agents
- Version control patterns for prompts and agent configurations

**Example for Supabase:**
- Frontend + Supabase project structure patterns
- Local development workflow with Supabase CLI
- Database migration and versioning strategies
- Environment management (local, staging, production)
- Testing strategies for full-stack Supabase applications

**Your development patterns:** [Specify the workflow and organizational patterns to research]

---

## SECURITY & BEST PRACTICES:

**What security considerations and best practices are critical for this technology?**

**Example for Pydantic AI:**
- API key management and rotation
- Input validation and sanitization for agent inputs
- Rate limiting and usage monitoring
- Prompt injection prevention
- Cost control and monitoring for model usage

**Example for Supabase:**
- Row Level Security (RLS) policy design
- API key vs JWT authentication patterns
- Database security and access control
- File upload security and virus scanning
- Rate limiting and abuse prevention

**Your security considerations:** [List technology-specific security patterns to research and document]

---

## COMMON GOTCHAS:

**What are the typical pitfalls, edge cases, or complex issues developers face with this technology?**

**Example for Pydantic AI:**
- Model context length limitations and management
- Handling model provider rate limits and errors
- Token counting and cost optimization
- Managing conversation state across requests
- Tool execution error handling and retries

**Example for Supabase:**
- RLS policy debugging and testing
- Real-time subscription performance with large datasets
- Edge function cold starts and optimization
- Database connection pooling in serverless environments
- CORS configuration for different domains

**Your gotchas:** [Identify the specific challenges developers commonly face]

---

## VALIDATION REQUIREMENTS:

**What specific validation, testing, or quality checks should be included in the template?**

**Example for Pydantic AI:**
- Agent response quality testing
- Tool integration testing
- Model provider fallback testing
- Cost and performance benchmarking
- Conversation flow validation

**Example for Supabase:**
- Database migration testing
- RLS policy validation
- Real-time functionality testing
- Authentication flow testing
- Edge function integration testing

**Your validation requirements:** [Specify the testing and validation patterns needed]

---

## INTEGRATION FOCUS:

**What specific integrations or third-party services are commonly used with this technology?**

**Example for Pydantic AI:**
- Integration with vector databases (Pinecone, Weaviate)
- Web scraping tools and APIs
- External API integrations for tools
- Monitoring services (Weights & Biases, LangSmith)
- Deployment platforms (Modal, Replicate)

**Example for Supabase:**
- Frontend frameworks (Next.js, React, Vue)
- Payment processing (Stripe)
- Email services (SendGrid, Resend)
- File processing (image optimization, document parsing)
- Analytics and monitoring tools

**Your integration focus:** [List the key integrations to research and include]

---

## ADDITIONAL NOTES:

**Any other specific requirements, constraints, or considerations for this template?**

**Example:** "Focus on TypeScript patterns and include comprehensive type definitions"  
**Example:** "Emphasize serverless deployment patterns and cost optimization"  
**Example:** "Include patterns for both beginner and advanced use cases"

**Your additional notes:** [Any other important considerations]

---

## TEMPLATE COMPLEXITY LEVEL:

**What level of complexity should this template target?**

- [ ] **Beginner-friendly** - Simple getting started patterns
- [ ] **Intermediate** - Production-ready patterns with common features  
- [ ] **Advanced** - Comprehensive patterns including complex scenarios
- [ ] **Enterprise** - Full enterprise patterns with monitoring, scaling, security

**Your choice:** [Select the appropriate complexity level and explain why]

---

**REMINDER: Be as specific as possible in each section. The more detailed you are here, the better the generated template will be. This INITIAL.md file is where you should put all your requirements, not just basic information.**