/**
MCP Server 運作流程圖

此圖表展示了 MCP Server 從使用者請求到服務就緒的完整流程：

```mermaid
flowchart TD
    A["使用者請求"] --> B{"OAuth 驗證"}
    B -->|"未驗證"| C["GitHub OAuth 流程"]
    B -->|"已驗證"| D["建立 MCP Agent"]
    
    C --> C1["重定向到 GitHub"]
    C1 --> C2["GitHub 回調"]
    C2 --> C3["交換 Access Token"]
    C3 --> C4["獲取使用者資訊"]
    C4 --> D
    
    D --> E["初始化 MyMCP"]
    E --> F["註冊工具"]
    F --> G{"檢查權限"}
    
    G -->|"一般使用者"| H["註冊唯讀工具<br/>listTables<br/>queryDatabase"]
    G -->|"特權使用者"| I["註冊所有工具<br/>+ executeDatabase"]
    
    H --> J["MCP Server 就緒"]
    I --> J
    
    J --> K{"協議選擇"}
    K -->|"HTTP"| L["/mcp 端點"]
    K -->|"SSE"| M["/sse 端點"]
```
*/

import OAuthProvider from "@cloudflare/workers-oauth-provider";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { McpAgent } from "agents/mcp";
import { Props } from "./types";
import { GitHubHandler } from "./auth/github-handler";
import { closeDb } from "./database/connection";
import { registerAllTools } from "./tools/register-tools";

export class MyMCP extends McpAgent<Env, Record<string, never>, Props> {
	server = new McpServer({
		name: "PostgreSQL Database MCP Server",
		version: "1.0.0",
	});

	/**
	 * Cleanup database connections when Durable Object is shutting down
	 */
	async cleanup(): Promise<void> {
		try {
			await closeDb();
			console.log('Database connections closed successfully');
		} catch (error) {
			console.error('Error during database cleanup:', error);
		}
	}

	/**
	 * Durable Objects alarm handler - used for cleanup
	 */
	async alarm(): Promise<void> {
		await this.cleanup();
	}

	async init() {
		// Register all tools based on user permissions
		registerAllTools(this.server, this.env, this.props);
	}
}

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