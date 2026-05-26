# MCP Server Development Patterns

This document contains proven patterns for developing Model Context Protocol (MCP) servers using TypeScript and Cloudflare Workers, based on the implementation in this codebase.

## Core MCP Server Architecture

### Base Server Class Pattern

```typescript
import { McpAgent } from "agents/mcp";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";

// Authentication props from OAuth flow
type Props = {
  login: string;
  name: string;
  email: string;
  accessToken: string;
};

export class CustomMCP extends McpAgent<Env, Record<string, never>, Props> {
  server = new McpServer({
    name: "Your MCP Server Name",
    version: "1.0.0",
  });

  // CRITICAL: Implement cleanup for Durable Objects
  async cleanup(): Promise<void> {
    try {
      // Close database connections
      await closeDb();
      console.log('Database connections closed successfully');
    } catch (error) {
      console.error('Error during database cleanup:', error);
    }
  }

  // CRITICAL: Durable Objects alarm handler
  async alarm(): Promise<void> {
    await this.cleanup();
  }

  // Initialize all tools and resources
  async init() {
    // Register tools here
    this.registerTools();
    
    // Register resources if needed
    this.registerResources();
  }

  private registerTools() {
    // Tool registration logic
  }

  private registerResources() {
    // Resource registration logic
  }
}
```

### Tool Registration Pattern

```typescript
// Basic tool registration
this.server.tool(
  "toolName",
  "Tool description for the LLM",
  {
    param1: z.string().describe("Parameter description"),
    param2: z.number().optional().describe("Optional parameter"),
  },
  async ({ param1, param2 }) => {
    try {
      // Tool implementation
      const result = await performOperation(param1, param2);
      
      return {
        content: [
          {
            type: "text",
            text: `Success: ${JSON.stringify(result, null, 2)}`
          }
        ]
      };
    } catch (error) {
      console.error('Tool error:', error);
      return {
        content: [
          {
            type: "text",
            text: `Error: ${error.message}`,
            isError: true
          }
        ]
      };
    }
  }
);
```

### Conditional Tool Registration (Based on Permissions)

```typescript
// Permission-based tool availability
const ALLOWED_USERNAMES = new Set<string>([
  'admin1',
  'admin2'
]);

// Register privileged tools only for authorized users
if (ALLOWED_USERNAMES.has(this.props.login)) {
  this.server.tool(
    "privilegedTool",
    "Tool only available to authorized users",
    { /* parameters */ },
    async (params) => {
      // Privileged operation
      return {
        content: [
          {
            type: "text",
            text: `Privileged operation executed by: ${this.props.login}`
          }
        ]
      };
    }
  );
}
```

## Database Integration Patterns

### Database Connection Pattern

```typescript
import { withDatabase, validateSqlQuery, isWriteOperation, formatDatabaseError } from "./database";

// Database operation with connection management
async function performDatabaseOperation(sql: string) {
  try {
    // Validate SQL query
    const validation = validateSqlQuery(sql);
    if (!validation.isValid) {
      return {
        content: [
          {
            type: "text",
            text: `Invalid SQL query: ${validation.error}`,
            isError: true
          }
        ]
      };
    }

    // Execute with automatic connection management
    return await withDatabase(this.env.DATABASE_URL, async (db) => {
      const results = await db.unsafe(sql);
      
      return {
        content: [
          {
            type: "text",
            text: `**Query Results**\n\`\`\`sql\n${sql}\n\`\`\`\n\n**Results:**\n\`\`\`json\n${JSON.stringify(results, null, 2)}\n\`\`\`\n\n**Rows returned:** ${Array.isArray(results) ? results.length : 1}`
          }
        ]
      };
    });
  } catch (error) {
    console.error('Database operation error:', error);
    return {
      content: [
        {
          type: "text",
          text: `Database error: ${formatDatabaseError(error)}`,
          isError: true
        }
      ]
    };
  }
}
```

### Read vs Write Operation Handling

```typescript
// Check if operation is read-only
if (isWriteOperation(sql)) {
  return {
    content: [
      {
        type: "text",
        text: "Write operations are not allowed with this tool. Use the privileged tool if you have write permissions.",
        isError: true
      }
    ]
  };
}
```

## Authentication & Authorization Patterns

### OAuth Integration Pattern

```typescript
import OAuthProvider from "@cloudflare/workers-oauth-provider";
import { GitHubHandler } from "./github-handler";

// OAuth configuration
export default new OAuthProvider({
  apiHandlers: {
    '/sse': MyMCP.serveSSE('/sse') as any,
    '/mcp': MyMCP.serve('/mcp') as any,
  },
  authorizeEndpoint: "/authorize",
  clientRegistrationEndpoint: "/register",
  defaultHandler: GitHubHandler as any,
  tokenEndpoint: "/token",
});
```

### User Permission Checking

```typescript
// Permission validation pattern
function hasPermission(username: string, operation: string): boolean {
  const WRITE_PERMISSIONS = new Set(['admin1', 'admin2']);
  const READ_PERMISSIONS = new Set(['user1', 'user2', ...WRITE_PERMISSIONS]);
  
  switch (operation) {
    case 'read':
      return READ_PERMISSIONS.has(username);
    case 'write':
      return WRITE_PERMISSIONS.has(username);
    default:
      return false;
  }
}
```

## Error Handling Patterns

### Standardized Error Response

```typescript
// Error response pattern
function createErrorResponse(error: Error, operation: string) {
  console.error(`${operation} error:`, error);
  
  return {
    content: [
      {
        type: "text",
        text: `${operation} failed: ${error.message}`,
        isError: true
      }
    ]
  };
}
```

### Database Error Formatting

```typescript
// Use the built-in database error formatter
import { formatDatabaseError } from "./database";

try {
  // Database operation
} catch (error) {
  return {
    content: [
      {
        type: "text",
        text: `Database error: ${formatDatabaseError(error)}`,
        isError: true
      }
    ]
  };
}
```

## Resource Registration Patterns

### Basic Resource Pattern

```typescript
// Resource registration
this.server.resource(
  "resource://example/{id}",
  "Resource description",
  async (uri) => {
    const id = uri.path.split('/').pop();
    
    try {
      const data = await fetchResourceData(id);
      
      return {
        contents: [
          {
            uri: uri.href,
            mimeType: "application/json",
            text: JSON.stringify(data, null, 2)
          }
        ]
      };
    } catch (error) {
      throw new Error(`Failed to fetch resource: ${error.message}`);
    }
  }
);
```

## Testing Patterns

### Tool Testing Pattern

```typescript
// Test tool functionality
async function testTool(toolName: string, params: any) {
  try {
    const result = await server.callTool(toolName, params);
    console.log(`${toolName} test passed:`, result);
    return true;
  } catch (error) {
    console.error(`${toolName} test failed:`, error);
    return false;
  }
}
```

### Database Connection Testing

```typescript
// Test database connectivity
async function testDatabaseConnection() {
  try {
    await withDatabase(process.env.DATABASE_URL, async (db) => {
      const result = await db`SELECT 1 as test`;
      console.log('Database connection test passed:', result);
    });
    return true;
  } catch (error) {
    console.error('Database connection test failed:', error);
    return false;
  }
}
```

## Security Best Practices

### Input Validation

```typescript
// Always validate inputs with Zod
const inputSchema = z.object({
  query: z.string().min(1).max(1000),
  parameters: z.array(z.string()).optional()
});

// In tool handler
try {
  const validated = inputSchema.parse(params);
  // Use validated data
} catch (error) {
  return createErrorResponse(error, "Input validation");
}
```

### SQL Injection Prevention

```typescript
// Use the built-in SQL validation
import { validateSqlQuery } from "./database";

const validation = validateSqlQuery(sql);
if (!validation.isValid) {
  return createErrorResponse(new Error(validation.error), "SQL validation");
}
```

### Access Control

```typescript
// Always check permissions before executing sensitive operations
if (!hasPermission(this.props.login, 'write')) {
  return {
    content: [
      {
        type: "text",
        text: "Access denied: insufficient permissions",
        isError: true
      }
    ]
  };
}
```

## Performance Patterns

### Connection Pooling

```typescript
// Use the built-in connection pooling
import { withDatabase } from "./database";

// The withDatabase function handles connection pooling automatically
await withDatabase(databaseUrl, async (db) => {
  // Database operations
});
```

### Resource Cleanup

```typescript
// Implement proper cleanup in Durable Objects
async cleanup(): Promise<void> {
  try {
    // Close database connections
    await closeDb();
    
    // Clean up other resources
    await cleanupResources();
    
    console.log('Cleanup completed successfully');
  } catch (error) {
    console.error('Cleanup error:', error);
  }
}
```

## Common Gotchas

### 1. Missing Cleanup Implementation
- Always implement `cleanup()` method in Durable Objects
- Handle database connection cleanup properly
- Set up alarm handler for automatic cleanup

### 2. SQL Injection Vulnerabilities
- Always use `validateSqlQuery()` before executing SQL
- Never concatenate user input directly into SQL strings
- Use parameterized queries when possible

### 3. Permission Bypasses
- Check permissions for every sensitive operation
- Don't rely on tool registration alone for security
- Always validate user identity from props

### 4. Error Information Leakage
- Use `formatDatabaseError()` to sanitize error messages
- Don't expose internal system details in error responses
- Log detailed errors server-side, return generic messages to client

### 5. Resource Leaks
- Always use `withDatabase()` for database operations
- Implement proper error handling in async operations
- Clean up resources in finally blocks

## Environment Configuration

### Required Environment Variables

```typescript
// Environment type definition
interface Env {
  DATABASE_URL: string;
  GITHUB_CLIENT_ID: string;
  GITHUB_CLIENT_SECRET: string;
  OAUTH_KV: KVNamespace;
  // Add other bindings as needed
}
```

### Wrangler Configuration Pattern

```toml
# wrangler.toml
name = "mcp-server"
main = "src/index.ts"
compatibility_date = "2024-01-01"

[[kv_namespaces]]
binding = "OAUTH_KV"
id = "your-kv-namespace-id"

[env.production]
# Production-specific configuration
```

This document provides the core patterns for building secure, scalable MCP servers using the proven architecture in this codebase.