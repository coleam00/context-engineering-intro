# MCP Server 搭配 GitHub OAuth - 實作指南

## MCP Server 技術架構圖

下圖展示了 MCP Server 的完整技術堆疊，包含運行環境、程式語言、MCP 框架和資料層的詳細組成：

```mermaid
flowchart TD
    A["技術堆疊"]
    A --> B["運行環境<br/>Cloudflare Workers"]
    A --> C["程式語言<br/>TypeScript + Node.js"]
    A --> D["MCP 框架"]
    A --> E["資料層"]
    
    B --> B1["V8 Isolates"]
    B --> B2["Durable Objects"]
    B --> B3["KV Storage"]
    B --> B4["Workers AI"]
    
    C --> C1["TypeScript 嚴格模式"]
    C --> C2["Zod 輸入驗證"]
    C --> C3["npm 套件管理"]
    
    D --> D1["@modelcontextprotocol/sdk"]
    D --> D2["agents/mcp"]
    D --> D3["workers-mcp"]
    
    E --> E1["PostgreSQL"]
    E --> E2["連接池管理"]
    E --> E3["SQL 注入防護"]
```

---

## 開發工作流程圖

此流程圖說明了從本地開發到生產部署的完整開發工作流程，包含測試、配置和監控各個環節：

```mermaid
flowchart LR
    A["開發階段"] --> B["本地開發<br/>wrangler dev"]
    B --> C["型別檢查<br/>npm run type-check"]
    C --> D["測試驗證<br/>MCP Inspector"]
    D --> E["部署階段"]
    
    E --> F["環境配置<br/>.dev.vars"]
    F --> G["生產部署<br/>wrangler deploy"]
    G --> H["監控整合<br/>Sentry"]
    
    I["工具管理"] --> I1["註冊新工具"]
    I1 --> I2["Zod Schema"]
    I1 --> I3["權限檢查"]
    I1 --> I4["錯誤處理"]
    
    I --> J["register-tools.ts"]
```

本指南提供使用 Node.js、TypeScript 和 Cloudflare Workers 建構具有 GitHub OAuth 身份驗證的 MCP (Model Context Protocol) 伺服器的實作模式和標準。關於「要建構什麼」的資訊，請參閱 PRP (Product Requirement Prompt) 文件。

## 核心原則

**重要：您必須在所有程式碼變更和 PRP 生成中遵循這些原則：**

### KISS (Keep It Simple, Stupid)

- 簡潔性應該是設計的關鍵目標
- 在可能的情況下，選擇直接的解決方案而不是複雜的方案
- 簡單的解決方案更容易理解、維護和除錯

### YAGNI (You Aren't Gonna Need It)

- 避免基於推測來建構功能
- 只在需要時實作功能，而不是在您預期未來可能有用時

### 開放/封閉原則

- 軟體實體應該對擴展開放，對修改封閉
- 設計系統時，新功能可以在對現有程式碼進行最小變更的情況下添加

## 套件管理與工具

**關鍵：此專案使用 npm 進行 Node.js 套件管理，使用 Wrangler CLI 進行 Cloudflare Workers 開發。**

### 基本 npm 指令

```bash
# 從 package.json 安裝依賴項
npm install

# 新增依賴項
npm install package-name

# 新增開發依賴項
npm install --save-dev package-name

# 移除套件
npm uninstall package-name

# 更新依賴項
npm update

# 執行 package.json 中定義的腳本
npm run dev
npm run deploy
npm run type-check
```

### 基本 Wrangler CLI 指令

**關鍵：使用 Wrangler CLI 進行所有 Cloudflare Workers 開發、測試和部署。**

```bash
# 身份驗證
wrangler login          # 登入 Cloudflare 帳戶
wrangler logout         # 登出 Cloudflare
wrangler whoami         # 檢查目前使用者

# 開發與測試
wrangler dev           # 啟動本地開發伺服器（預設端口 8787）

# 部署
wrangler deploy        # 部署 Worker 至 Cloudflare
wrangler deploy --dry-run  # 測試部署而不實際部署

# 設定與型別
wrangler types         # 從 Worker 設定生成 TypeScript 型別
```

## 專案架構

**重要：這是一個具有 GitHub OAuth 身份驗證的 Cloudflare Workers MCP 伺服器，用於安全資料庫存取。**

### 目前專案結構

```
/
├── src/                          # TypeScript 原始碼
│   ├── index.ts                  # 主要 MCP 伺服器（標準版）
│   ├── index_sentry.ts          # 啟用 Sentry 的 MCP 伺服器
│   ├── simple-math.ts           # 基本 MCP 範例（無身份驗證）
│   ├── github-handler.ts        # GitHub OAuth 流程實作
│   ├── database.ts              # PostgreSQL 連線與工具
│   ├── utils.ts                 # OAuth 輔助函式
│   ├── workers-oauth-utils.ts   # 基於 cookie 的核准系統
│   └── tools/                   # 工具註冊系統
│       └── register-tools.ts    # 集中化工具註冊
├── PRPs/                        # Product Requirement Prompts
│   ├── README.md
│   └── templates/
│       └── prp_mcp_base.md
├── examples/                    # 工具建立與註冊範例 - 永不編輯或從此資料夾匯入
│   ├── database-tools.ts        # Postgres MCP 伺服器範例工具，展示工具建立與註冊的最佳實踐
│   └── database-tools-sentry.ts # Postgres MCP 伺服器的範例工具，但具有 Sentry 整合，用於生產環境監控
├── wrangler.jsonc              # 主要 Cloudflare Workers 設定
├── wrangler-simple.jsonc       # 簡單數學範例設定
├── package.json                # npm 依賴項與腳本
├── tsconfig.json               # TypeScript 設定
├── worker-configuration.d.ts   # 生成的 Cloudflare 型別
└── CLAUDE.md                   # 此實作指南
```

### 主要檔案用途（請始終在此添加新檔案）

**主要實作檔案：**

- `src/index.ts` - 具有 GitHub OAuth + PostgreSQL 的生產 MCP 伺服器
- `src/index_sentry.ts` - 與上述相同，但具有 Sentry 監控整合

**身份驗證與安全性：**

- `src/github-handler.ts` - 完整的 GitHub OAuth 2.0 流程
- `src/workers-oauth-utils.ts` - HMAC 簽章 cookie 核准系統
- `src/utils.ts` - OAuth 權杖交換和 URL 構建輔助函式

**資料庫整合：**

- `src/database.ts` - PostgreSQL 連線池、SQL 驗證、安全性

**工具註冊：**

- `src/tools/register-tools.ts` - 集中化工具註冊系統，匯入並註冊所有工具

**設定檔案：**

- `wrangler.jsonc` - 主要 Worker 設定，包含 Durable Objects、KV、AI 綁定
- `wrangler-simple.jsonc` - 簡單範例設定
- `tsconfig.json` - 適用於 Cloudflare Workers 的 TypeScript 編譯器設定

## 開發指令

### 核心工作流程指令

```bash
# 設定與依賴項
npm install                  # 安裝所有依賴項
npm install --save-dev @types/package  # 添加具有型別的開發依賴項

# 開發
wrangler dev                # 啟動本地開發伺服器
npm run dev                 # 透過 npm 腳本的替代方案

# 型別檢查與驗證
npm run type-check          # 執行 TypeScript 編譯器檢查
wrangler types              # 生成 Cloudflare Worker 型別
npx tsc --noEmit           # 不編譯的型別檢查

# 測試
npx vitest                  # 執行單元測試（如果已設定）

# 程式碼品質
npx prettier --write .      # 格式化程式碼
npx eslint src/            # 檢查 TypeScript 程式碼
```

### 環境設定

**環境變數設定：**

```bash
# 根據 .dev.vars.example 建立 .dev.vars 檔案，用於本地開發
cp .dev.vars.example .dev.vars

# 生產環境密鑰（透過 Wrangler）
wrangler secret put GITHUB_CLIENT_ID
wrangler secret put GITHUB_CLIENT_SECRET
wrangler secret put COOKIE_ENCRYPTION_KEY
wrangler secret put DATABASE_URL
wrangler secret put SENTRY_DSN
```

## MCP 開發環境

**重要：此專案使用 Node.js/TypeScript 在 Cloudflare Workers 上建構具有 GitHub OAuth 身份驗證的生產就緒 MCP 伺服器。**

### MCP 技術堆疊

**核心技術：**

- **@modelcontextprotocol/sdk** - 官方 MCP TypeScript SDK
- **agents/mcp** - Cloudflare Workers MCP 代理框架
- **workers-mcp** - 適用於 Workers 的 MCP 傳輸層
- **@cloudflare/workers-oauth-provider** - OAuth 2.1 伺服器實作

**Cloudflare 平台：**

- **Cloudflare Workers** - 無伺服器運行時（V8 isolates）
- **Durable Objects** - 用於 MCP 代理持久性的有狀態物件
- **KV Storage** - OAuth 狀態與會話管理

### MCP 伺服器架構

此專案將 MCP 伺服器實作為 Cloudflare Workers，具有三種主要模式：

**1. 經身份驗證的資料庫 MCP 伺服器（`src/index.ts`）：**

```typescript
export class MyMCP extends McpAgent<Env, Record<string, never>, Props> {
  server = new McpServer({
    name: "PostgreSQL Database MCP Server",
    version: "1.0.0",
  });

  // 根據使用者權限提供的 MCP 工具
  // - listTables（所有使用者）
  // - queryDatabase（所有使用者，唯讀）
  // - executeDatabase（僅限特權使用者）
}
```

**2. 監控的 MCP 伺服器（`src/index_sentry.ts`）：**

- 與上述相同的功能，但具有 Sentry 檢測
- MCP 工具呼叫的分散式追蹤
- 具有事件 ID 的錯誤追蹤
- 性能監控

### MCP 開發指令

**本地開發與測試：**

```bash
# 啟動主要 MCP 伺服器（具有 OAuth）
wrangler dev                    # 可在 http://localhost:8792/mcp 存取
```

### Claude Desktop 整合

**用於本地開發：**

```json
{
  "mcpServers": {
    "database-mcp": {
      "command": "npx",
      "args": ["mcp-remote", "http://localhost:8792/mcp"],
      "env": {}
    }
  }
}
```

**用於生產部署：**

```json
{
  "mcpServers": {
    "database-mcp": {
      "command": "npx",
      "args": ["mcp-remote", "https://your-worker.workers.dev/mcp"],
      "env": {}
    }
  }
}
```

### 此專案的 MCP 關鍵概念

- **工具**：資料庫操作（listTables、queryDatabase、executeDatabase）
- **身份驗證**：具有角色型存取控制的 GitHub OAuth
- **傳輸**：對 HTTP（`/mcp`）和 SSE（`/sse`）協議的雙重支援
- **狀態**：Durable Objects 維護經身份驗證的使用者環境
- **安全性**：SQL 注入防護、權限驗證、錯誤清理

## 資料庫整合與安全性

**關鍵：此專案透過具有角色型權限的 MCP 工具提供安全的 PostgreSQL 資料庫存取。**

### 資料庫架構

**連線管理（`src/database.ts`）：**

```typescript
// 具有 Cloudflare Workers 限制的單例連線池
export function getDb(databaseUrl: string): postgres.Sql {
  if (!dbInstance) {
    dbInstance = postgres(databaseUrl, {
      max: 5, // Workers 最多 5 個連線
      idle_timeout: 20,
      connect_timeout: 10,
      prepare: true, // 啟用預處理語句
    });
  }
  return dbInstance;
}

// 具有錯誤處理的連線包裝器
export async function withDatabase<T>(databaseUrl: string, operation: (db: postgres.Sql) => Promise<T>): Promise<T> {
  const db = getDb(databaseUrl);
  // 執行具有計時和錯誤處理的操作
}
```

### 安全性實作

**SQL 注入防護：**

```typescript
export function validateSqlQuery(sql: string): { isValid: boolean; error?: string } {
  const dangerousPatterns = [
    /;\s*drop\s+/i,
    /;\s*delete\s+.*\s+where\s+1\s*=\s*1/i,
    /;\s*truncate\s+/i,
    // ... 更多模式
  ];
  // 基於模式的安全性驗證
}

export function isWriteOperation(sql: string): boolean {
  const writeKeywords = ["insert", "update", "delete", "create", "drop", "alter"];
  return writeKeywords.some((keyword) => sql.trim().toLowerCase().startsWith(keyword));
}
```

**存取控制（`src/index.ts`）：**

```typescript
const ALLOWED_USERNAMES = new Set<string>([
  'coleam00'  // 只有這些 GitHub 使用者名稱可以執行寫入操作
]);

// 根據使用者權限提供的工具
if (ALLOWED_USERNAMES.has(this.props.login)) {
  // 為特權使用者註冊 executeDatabase 工具
  this.server.tool("executeDatabase", ...);
}
```

### MCP 工具實作

**工具註冊系統：**

工具現在以模組化方式組織，具有集中化註冊：

1. **工具註冊（`src/tools/register-tools.ts`）：**
   - 匯入所有工具模組的中央註冊表
   - 呼叫個別註冊函式
   - 將伺服器、環境和使用者屬性傳遞給每個模組

2. **工具實作模式：**
   - 每個功能/領域獲得自己的工具檔案（例如，`database-tools.ts`）
   - 工具被匯出為註冊函式
   - 註冊函式接收伺服器實例、環境和使用者屬性
   - 權限檢查在註冊期間進行

**工具註冊範例：**

```typescript
// src/tools/register-tools.ts
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { Props } from "../types";
import { registerDatabaseTools } from "../../examples/database-tools";

export function registerAllTools(server: McpServer, env: Env, props: Props) {
  // 註冊資料庫工具
  registerDatabaseTools(server, env, props);
  
  // 未來的工具可以在此註冊
  // registerAnalyticsTools(server, env, props);
  // registerReportingTools(server, env, props);
}
```

**工具模組範例（`examples/database-tools.ts`）：**

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { Props } from "../types";

const ALLOWED_USERNAMES = new Set<string>(['coleam00']);

export function registerDatabaseTools(server: McpServer, env: Env, props: Props) {
  // 工具 1：適用於所有經身份驗證的使用者
  server.tool(
    "listTables",
    "取得資料庫中所有資料表的清單",
    ListTablesSchema,
    async () => {
      // 實作
    }
  );

  // 工具 2：適用於所有經身份驗證的使用者
  server.tool(
    "queryDatabase",
    "執行唯讀 SQL 查詢",
    QueryDatabaseSchema,
    async ({ sql }) => {
      // 具有驗證的實作
    }
  );

  // 工具 3：僅限特權使用者
  if (ALLOWED_USERNAMES.has(props.login)) {
    server.tool(
      "executeDatabase",
      "執行任何 SQL 語句（特權）",
      ExecuteDatabaseSchema,
      async ({ sql }) => {
        // 實作
      }
    );
  }
}
```

**範例中可用的資料庫工具：**

1. **`listTables`** - 架構發現（所有經身份驗證的使用者）
2. **`queryDatabase`** - 唯讀 SQL 查詢（所有經身份驗證的使用者）
3. **`executeDatabase`** - 寫入操作（僅限特權使用者）

## GitHub OAuth 實作

**關鍵：此專案實作安全的 GitHub OAuth 2.0 流程，具有基於簽章 cookie 的核准系統。**

### OAuth 流程架構

**身份驗證流程（`src/github-handler.ts`）：**

```typescript
// 1. 授權請求
app.get("/authorize", async (c) => {
  const oauthReqInfo = await c.env.OAUTH_PROVIDER.parseAuthRequest(c.req.raw);

  // 透過簽章 cookie 檢查客戶端是否已核准
  if (await clientIdAlreadyApproved(c.req.raw, oauthReqInfo.clientId, c.env.COOKIE_ENCRYPTION_KEY)) {
    return redirectToGithub(c.req.raw, oauthReqInfo, c.env, {});
  }

  // 顯示核准對話框
  return renderApprovalDialog(c.req.raw, { client, server, state });
});

// 2. GitHub 回呼
app.get("/callback", async (c) => {
  // 交換代碼以獲取存取權杖
  const [accessToken, errResponse] = await fetchUpstreamAuthToken({
    client_id: c.env.GITHUB_CLIENT_ID,
    client_secret: c.env.GITHUB_CLIENT_SECRET,
    code: c.req.query("code"),
    redirect_uri: new URL("/callback", c.req.url).href,
  });

  // 取得 GitHub 使用者資訊
  const user = await new Octokit({ auth: accessToken }).rest.users.getAuthenticated();

  // 使用使用者屬性完成授權
  return c.env.OAUTH_PROVIDER.completeAuthorization({
    props: { accessToken, email, login, name } as Props,
    userId: login,
  });
});
```

### Cookie 安全系統

**HMAC 簽章核准 Cookie（`src/workers-oauth-utils.ts`）：**

```typescript
// 為客戶端核准生成簽章 cookie
async function signData(key: CryptoKey, data: string): Promise<string> {
  const signatureBuffer = await crypto.subtle.sign("HMAC", key, enc.encode(data));
  return Array.from(new Uint8Array(signatureBuffer))
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");
}

// 驗證 cookie 完整性
async function verifySignature(key: CryptoKey, signatureHex: string, data: string): Promise<boolean> {
  const signatureBytes = new Uint8Array(signatureHex.match(/.{1,2}/g)!.map((byte) => parseInt(byte, 16)));
  return await crypto.subtle.verify("HMAC", key, signatureBytes.buffer, enc.encode(data));
}
```

### 使用者環境與權限

**經身份驗證的使用者屬性：**

```typescript
type Props = {
  login: string; // GitHub 使用者名稱
  name: string; // 顯示名稱
  email: string; // 電子郵件地址
  accessToken: string; // GitHub 存取權杖
};

// 在 MCP 工具中透過 this.props 可用
class MyMCP extends McpAgent<Env, Record<string, never>, Props> {
  async init() {
    // 在任何工具中存取使用者環境
    const username = this.props.login;
    const hasWriteAccess = ALLOWED_USERNAMES.has(username);
  }
}
```

## 監控與可觀察性

**關鍵：此專案支援可選的 Sentry 整合，用於生產環境監控，並包含內建的主控台記錄。**

### 記錄架構

**兩個部署選項：**

1. **標準版本（`src/index.ts`）**：僅主控台記錄
2. **Sentry 版本（`src/index_sentry.ts`）**：完整的 Sentry 檢測

### Sentry 整合（可選）

**啟用 Sentry 監控：**

```typescript
// src/index_sentry.ts - 具有監控的生產就緒版本
import * as Sentry from "@sentry/cloudflare";

// Sentry 設定
function getSentryConfig(env: Env) {
  return {
    dsn: env.SENTRY_DSN,
    tracesSampleRate: 1,  // 100% 追蹤採樣
  };
}

// 使用追蹤檢測 MCP 工具
private registerTool(name: string, description: string, schema: any, handler: any) {
  this.server.tool(name, description, schema, async (args: any) => {
    return await Sentry.startNewTrace(async () => {
      return await Sentry.startSpan({
        name: `mcp.tool/${name}`,
        attributes: extractMcpParameters(args),
      }, async (span) => {
        // 設定使用者環境
        Sentry.setUser({
          username: this.props.login,
          email: this.props.email,
        });

        try {
          return await handler(args);
        } catch (error) {
          span.setStatus({ code: 2 }); // 錯誤
          return handleError(error);  // 回傳具有事件 ID 的使用者友好錯誤
        }
      });
    });
  });
}
```

**已啟用的 Sentry 功能：**

- **錯誤追蹤**：具有環境的自動例外捕獲
- **性能監控**：具有 100% 採樣率的完整請求追蹤
- **使用者環境**：GitHub 使用者資訊綁定到事件
- **工具追蹤**：每個 MCP 工具呼叫都會追蹤參數
- **分散式追蹤**：跨 Cloudflare Workers 的請求流程

### 生產記錄模式

**主控台記錄（標準）：**

```typescript
// 資料庫操作
console.log(`Database operation completed successfully in ${duration}ms`);
console.error(`Database operation failed after ${duration}ms:`, error);

// 身份驗證事件
console.log(`User authenticated: ${this.props.login} (${this.props.name})`);

// 工具執行
console.log(`Tool called: ${toolName} by ${this.props.login}`);
console.error(`Tool failed: ${toolName}`, error);
```

**結構化錯誤處理：**

```typescript
// 安全性錯誤清理
export function formatDatabaseError(error: unknown): string {
  if (error instanceof Error) {
    if (error.message.includes("password")) {
      return "Database authentication failed. Please check credentials.";
    }
    if (error.message.includes("timeout")) {
      return "Database connection timed out. Please try again.";
    }
    return `Database error: ${error.message}`;
  }
  return "Unknown database error occurred.";
}
```

### 監控設定

**開發監控：**

```bash
# 在開發中啟用 Sentry
echo 'SENTRY_DSN=https://your-dsn@sentry.io/project' >> .dev.vars
echo 'NODE_ENV=development' >> .dev.vars

# 使用啟用 Sentry 的版本
wrangler dev --config wrangler.jsonc  # 確保 main = "src/index_sentry.ts"
```

**生產監控：**

```bash
# 設定生產密鑰
wrangler secret put SENTRY_DSN
wrangler secret put NODE_ENV  # 設定為 "production"

# 使用監控部署
wrangler deploy
```

## TypeScript 開發標準

**關鍵：所有 MCP 工具必須遵循 TypeScript 最佳實踐，具有 Zod 驗證和適當的錯誤處理。**

### 標準回應格式

**所有工具必須回傳 MCP 相容的回應物件：**

```typescript
import { z } from "zod";

// 遵循標準回應格式的工具
this.server.tool(
  "standardizedTool",
  "遵循標準回應格式的工具",
  {
    name: z.string().min(1, "名稱不能為空"),
    options: z.object({}).optional(),
  },
  async ({ name, options }) => {
    try {
      // 輸入已由 Zod 架構驗證
      const result = await processName(name, options);

      // 回傳標準化成功回應
      return {
        content: [
          {
            type: "text",
            text: `**成功**\n\n已處理：${name}\n\n**結果：**\n\`\`\`json\n${JSON.stringify(result, null, 2)}\n\`\`\`\n\n**處理時間：** 0.5s`,
          },
        ],
      };
    } catch (error) {
      // 回傳標準化錯誤回應
      return {
        content: [
          {
            type: "text",
            text: `**錯誤**\n\n處理失敗：${error instanceof Error ? error.message : String(error)}`,
            isError: true,
          },
        ],
      };
    }
  },
);
```

### 使用 Zod 進行輸入驗證

**所有工具輸入必須使用 Zod 架構進行驗證：**

```typescript
import { z } from "zod";

// 定義驗證架構
const DatabaseQuerySchema = z.object({
  sql: z
    .string()
    .min(1, "SQL 查詢不能為空")
    .refine((sql) => sql.trim().toLowerCase().startsWith("select"), {
      message: "僅允許 SELECT 查詢",
    }),
  limit: z.number().int().positive().max(1000).optional(),
});

// 在工具定義中使用
this.server.tool(
  "queryDatabase",
  "執行唯讀 SQL 查詢",
  DatabaseQuerySchema, // Zod 架構提供自動驗證
  async ({ sql, limit }) => {
    // sql 和 limit 已經過驗證並正確型別化
    const results = await db.unsafe(sql);
    return { content: [{ type: "text", text: JSON.stringify(results, null, 2) }] };
  },
);
```

### 錯誤處理模式

**標準化錯誤回應：**

```typescript
// 錯誤處理工具
function createErrorResponse(message: string, details?: any): any {
  return {
    content: [{
      type: "text",
      text: `**錯誤**\n\n${message}${details ? `\n\n**詳細資訊：**\n\`\`\`json\n${JSON.stringify(details, null, 2)}\n\`\`\`` : ''}`,
      isError: true
    }]
  };
}

// 權限錯誤
if (!ALLOWED_USERNAMES.has(this.props.login)) {
  return createErrorResponse(
    "此操作權限不足",
    { requiredRole: "特權", userRole: "標準" }
  );
}

// 驗證錯誤
if (isWriteOperation(sql)) {
  return createErrorResponse(
    "此工具不允許寫入操作",
    { operation: "寫入", allowedOperations: ["select", "show", "describe"] }
  );
}

// 資料庫錯誤
catch (error) {
  return createErrorResponse(
    "資料庫操作失敗",
    { error: formatDatabaseError(error) }
  );
}
```

### 型別安全規則

**強制的 TypeScript 模式：**

1. **嚴格型別**：所有參數和回傳型別明確型別化
2. **Zod 驗證**：所有輸入都使用 Zod 架構驗證
3. **錯誤處理**：所有非同步操作都包裝在 try/catch 中
4. **使用者環境**：使用 GitHub 使用者資訊進行 Props 型別化
5. **環境**：使用 `wrangler types` 生成 Cloudflare Workers 型別

## 程式碼風格偏好

### TypeScript 風格

- 對所有函式參數和回傳型別使用明確的型別註解
- 對所有匯出的函式和類別使用 JSDoc 註解
- 對所有非同步操作優先使用 async/await
- **強制**：對所有輸入驗證使用 Zod 架構
- **強制**：使用 try/catch 區塊進行適當的錯誤處理
- 保持函式小而專注（單一責任原則）

### 檔案組織

- 每個 MCP 伺服器應該獨立包含在單一 TypeScript 檔案中
- 組織匯入語句：Node.js 內建、第三方套件、本地匯入
- 在 src/ 目錄中使用相對匯入
- **為所有模組匯入 Zod 進行驗證和適當的型別**

### 測試慣例

- 使用 MCP Inspector 進行整合測試：`npx @modelcontextprotocol/inspector@latest`
- 使用本地開發伺服器測試：`wrangler dev`
- 使用描述性的工具名稱和描述
- **測試身份驗證和權限場景**
- **使用無效資料測試輸入驗證**

## 重要注意事項

### 不應該做的事

- **永不**將密鑰或環境變數提交到儲存庫
- **永不**在簡單的解決方案能夠工作時構建複雜的解決方案
- **永不**跳過使用 Zod 架構的輸入驗證

### 應該做的事

- **始終**使用 TypeScript 嚴格模式和適當的型別
- **始終**使用 Zod 架構驗證輸入
- **始終**遵循核心原則（KISS、YAGNI 等）
- **始終**使用 Wrangler CLI 進行所有開發和部署

## Git 工作流程

```bash
# 提交之前，始終運行：
npm run type-check              # 確保 TypeScript 編譯
wrangler dev --dry-run          # 測試部署設定

# 使用描述性訊息提交
git add .
git commit -m "feat: 為資料庫查詢添加新的 MCP 工具"
```

## 快速參考

### 添加新的 MCP 工具

1. **在你的專案中建立新的工具模組**（遵循 `examples/` 中的模式）：
   ```typescript
   // src/tools/your-feature-tools.ts
   export function registerYourFeatureTools(server: McpServer, env: Env, props: Props) {
     // 在此註冊你的工具
   }
   ```

2. **在你的型別檔案中定義 Zod 架構**進行輸入驗證

3. **使用範例中的模式實作工具處理程序**，具有適當的錯誤處理

4. **在 `src/tools/register-tools.ts` 中註冊你的工具**：
   ```typescript
   import { registerYourFeatureTools } from "./your-feature-tools";
   
   export function registerAllTools(server: McpServer, env: Env, props: Props) {
     // 現有註冊
     registerDatabaseTools(server, env, props);
     
     // 添加你的新註冊
     registerYourFeatureTools(server, env, props);
   }
   ```

5. **如需要更新文件**