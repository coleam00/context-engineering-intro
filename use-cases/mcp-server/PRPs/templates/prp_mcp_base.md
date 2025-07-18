---
name: "MCP Server PRP Template"
description: 這個模板旨在使用此程式碼庫中經過驗證的模式，提供一個生產就緒的 Model Context Protocol (MCP) 伺服器。
---

# MCP Server PRP 模板

## 目的

這個模板專為 AI agents 優化，用於實現生產就緒的 Model Context Protocol (MCP) servers，採用此程式碼庫中經過驗證的模式，包含 GitHub OAuth 認證、資料庫整合和 Cloudflare Workers 部署。

## 核心原則

1. **Context 為王**：包含所有必要的 MCP 模式、認證流程和部署配置
2. **驗證循環**：提供從 TypeScript 編譯到生產部署的可執行測試
3. **安全優先**：內建認證、授權和 SQL injection 防護
4. **生產就緒**：包含監控、錯誤處理和部署自動化

---

## 目標

建構一個生產就緒的 MCP (Model Context Protocol) server，包含：

- [特定 MCP 功能] - 描述要實現的特定工具和資源
- GitHub OAuth 認證與基於角色的存取控制
- Cloudflare Workers 部署與監控
- [額外功能] - 基礎認證/資料庫之外的任何特定功能

## 為什麼

- **開發者生產力**：讓 AI 助理安全存取 [特定資料/操作]
- **企業級安全**：GitHub OAuth 與細粒度權限系統
- **可擴展性**：Cloudflare Workers 全球邊緣部署
- **整合性**：[如何與現有系統整合]
- **使用者價值**：[對終端使用者的具體好處]

## 做什麼

### MCP Server 功能

**核心 MCP 工具：**

- 工具以模組化檔案組織，並透過 `src/tools/register-tools.ts` 註冊
- 每個功能/領域都有自己的工具註冊檔案（例如：`database-tools.ts`、`analytics-tools.ts`）
- [列出特定工具] - 例如："queryDatabase"、"listTables"、"executeOperations"
- 使用者認證和權限驗證在工具註冊期間進行
- 全面的錯誤處理和日誌記錄
- [領域特定工具] - 針對您使用案例的特定工具

**認證與授權：**

- GitHub OAuth 2.0 整合，搭配簽署的 cookie 核准系統
- 基於角色的存取控制（唯讀 vs 特權使用者）
- 使用者上下文傳播到所有 MCP 工具
- 使用 HMAC 簽署的 cookies 進行安全會話管理

**資料庫整合：**

- PostgreSQL 連線池與自動清理
- SQL injection 防護和查詢驗證
- 基於使用者權限的讀/寫操作分離
- 錯誤清理以防止資訊洩漏

**部署與監控：**

- Cloudflare Workers 搭配 Durable Objects 進行狀態管理
- 可選的 Sentry 整合用於錯誤追蹤和效能監控
- 基於環境的配置（開發 vs 生產）
- 即時日誌和警報

### 成功標準

- [ ] MCP server 通過 MCP Inspector 驗證
- [ ] GitHub OAuth 流程端到端運作（授權 → 回調 → MCP 存取）
- [ ] TypeScript 編譯成功，無錯誤
- [ ] 本地開發伺服器啟動並正確回應
- [ ] 成功部署到 Cloudflare Workers 生產環境
- [ ] 認證防止未授權存取敏感操作
- [ ] 錯誤處理提供使用者友好的訊息，不洩漏系統細節
- [ ] [領域特定成功標準]

## 所需的所有上下文

### 文件與參考資料（必讀）

```yaml
# 關鍵 MCP 模式 - 請先閱讀這些
- docfile: PRPs/ai_docs/mcp_patterns.md
  why: 核心 MCP 開發模式、安全實踐和錯誤處理

# 關鍵程式碼範例
- docfile: PRPs/ai_docs/claude_api_usage.md
  why: 如何使用 Anthropic API 從 LLM 獲得回應

# 工具註冊系統 - 了解模組化方法
- file: src/tools/register-tools.ts
  why: 中央註冊表顯示如何導入和註冊所有工具 - 研究這個模式

# MCP 工具範例 - 查看如何建立和註冊新工具
- file: examples/database-tools.ts
  why: Postgres MCP server 的範例工具，展示工具建立和註冊的最佳實踐

- file: examples/database-tools-sentry.ts
  why: Postgres MCP server 的範例工具，但包含用於生產監控的 Sentry 整合

# 現有程式碼庫模式 - 研究這些實現
- file: src/index.ts
  why: 完整的 MCP server，包含認證、資料庫和工具 - 模仿這個模式

- file: src/github-handler.ts
  why: OAuth 流程實現 - 使用這個確切的認證模式

- file: src/database.ts
  why: 資料庫安全、連線池、SQL 驗證 - 遵循這些模式

- file: wrangler.jsonc
  why: Cloudflare Workers 配置 - 複製這個部署模式

# 官方 MCP 文件
- url: https://modelcontextprotocol.io/docs/concepts/tools
  why: MCP 工具註冊和 schema 定義模式

- url: https://modelcontextprotocol.io/docs/concepts/resources
  why: MCP 資源實現（如果需要）

# 根據使用者的使用案例，在下方添加相關文件
```

### 當前程式碼庫樹狀結構（在專案根目錄執行 `tree -I node_modules`）

```bash
# 在此處插入實際的樹狀輸出
/
├── src/
│   ├── index.ts                 # 主要認證 MCP server ← 研究這個
│   ├── index_sentry.ts         # Sentry 監控版本
│   ├── simple-math.ts          # 基本 MCP 範例 ← 好的起點
│   ├── github-handler.ts       # OAuth 實現 ← 使用這個模式
│   ├── database.ts             # 資料庫工具 ← 安全模式
│   ├── utils.ts                # OAuth 輔助工具
│   ├── workers-oauth-utils.ts  # Cookie 安全系統
│   └── tools/                  # 工具註冊系統
│       └── register-tools.ts   # 中央工具註冊表 ← 理解這個
├── PRPs/
│   ├── templates/prp_mcp_base.md  # 這個模板
│   └── ai_docs/                   # 實現指南 ← 閱讀全部
├── examples/                   # 範例工具實現
│   ├── database-tools.ts       # 資料庫工具範例 ← 遵循模式
│   └── database-tools-sentry.ts # 包含 Sentry 監控
├── wrangler.jsonc              # Cloudflare 配置 ← 複製模式
├── package.json                # 依賴項
└── tsconfig.json               # TypeScript 配置
```

### 期望的程式碼庫樹狀結構（根據使用者的使用案例，需要添加/修改的檔案）

```bash

```

### 已知陷阱與關鍵 MCP/Cloudflare 模式

```typescript
// 關鍵：Cloudflare Workers 需要特定模式
// 1. 總是為 Durable Objects 實現清理
export class YourMCP extends McpAgent<Env, Record<string, never>, Props> {
  async cleanup(): Promise<void> {
    await closeDb(); // 關鍵：關閉資料庫連線
  }

  async alarm(): Promise<void> {
    await this.cleanup(); // 關鍵：處理 Durable Object alarms
  }
}

// 2. 總是驗證 SQL 以防止 injection（使用現有模式）
const validation = validateSqlQuery(sql); // 來自 src/database.ts
if (!validation.isValid) {
  return createErrorResponse(validation.error);
}

// 3. 總是在敏感操作前檢查權限
const ALLOWED_USERNAMES = new Set(["admin1", "admin2"]);
if (!ALLOWED_USERNAMES.has(this.props.login)) {
  return createErrorResponse("權限不足");
}

// 4. 總是使用 withDatabase wrapper 進行連線管理
return await withDatabase(this.env.DATABASE_URL, async (db) => {
  // 資料庫操作在此
});

// 5. 總是使用 Zod 進行輸入驗證
import { z } from "zod";
const schema = z.object({
  param: z.string().min(1).max(100),
});

// 6. TypeScript 編譯需要精確的介面匹配
interface Env {
  DATABASE_URL: string;
  GITHUB_CLIENT_ID: string;
  GITHUB_CLIENT_SECRET: string;
  OAUTH_KV: KVNamespace;
  // 在此添加您的環境變數
}
```

## 實現藍圖

### 資料模型與類型

定義 TypeScript interfaces 和 Zod schemas 以確保類型安全和驗證。

```typescript
// 使用者認證 props（繼承自 OAuth）
type Props = {
  login: string; // GitHub 使用者名稱
  name: string; // 顯示名稱
  email: string; // 電子郵件地址
  accessToken: string; // GitHub access token
};

// MCP 工具輸入 schemas（為您的工具自訂）
const YourToolSchema = z.object({
  param1: z.string().min(1, "參數不能為空"),
  param2: z.number().int().positive().optional(),
  options: z.object({}).optional(),
});

// 環境介面（添加您的變數）
interface Env {
  DATABASE_URL: string;
  GITHUB_CLIENT_ID: string;
  GITHUB_CLIENT_SECRET: string;
  OAUTH_KV: KVNamespace;
  // YOUR_SPECIFIC_ENV_VAR: string;
}

// 權限等級（為您的使用案例自訂）
enum Permission {
  READ = "read",
  WRITE = "write",
  ADMIN = "admin",
}
```

### 任務列表（按順序完成）

```yaml
任務 1 - 專案設定：
  複製 wrangler.jsonc 到 wrangler-[server-name].jsonc：
    - 修改 name 欄位為 "[server-name]"
    - 添加任何新的環境變數到 vars 區段
    - 保留現有的 OAuth 和資料庫配置

  建立 .dev.vars 檔案（如果不存在）：
    - 添加 GITHUB_CLIENT_ID=your_client_id
    - 添加 GITHUB_CLIENT_SECRET=your_client_secret
    - 添加 DATABASE_URL=postgresql://...
    - 添加 COOKIE_ENCRYPTION_KEY=your_32_byte_key
    - 添加任何領域特定的環境變數

任務 2 - GitHub OAuth App：
  建立新的 GitHub OAuth app：
    - 設定首頁 URL：https://your-worker.workers.dev
    - 設定回調 URL：https://your-worker.workers.dev/callback
    - 複製 client ID 和 secret 到 .dev.vars

  或重用現有的 OAuth app：
    - 如果使用不同的子網域，更新回調 URL
    - 驗證環境中的 client ID 和 secret

任務 3 - MCP Server 實現：
  建立 src/[server-name].ts 或修改 src/index.ts：
    - 複製 src/index.ts 的類別結構
    - 在 McpServer 建構函式中修改 server 名稱和版本
    - 在 init() 方法中呼叫 registerAllTools(server, env, props)
    - 保持認證和資料庫模式相同

  建立工具模組：
    - 按照 examples/database-tools.ts 模式建立新的工具檔案
    - 匯出接受 (server, env, props) 的註冊函式
    - 使用 Zod schemas 進行輸入驗證
    - 使用 createErrorResponse 實現適當的錯誤處理
    - 在工具註冊期間添加權限檢查

  更新工具註冊表：
    - 修改 src/tools/register-tools.ts 以匯入您的新工具
    - 在 registerAllTools() 中添加您的註冊函式呼叫

任務 4 - 資料庫整合（如需要）：
  使用 src/database.ts 的現有資料庫模式：
    - 匯入 withDatabase、validateSqlQuery、isWriteOperation
    - 使用安全驗證實現資料庫操作
    - 基於使用者權限分離讀寫操作
    - 使用 formatDatabaseError 提供使用者友好的錯誤訊息

任務 5 - 環境配置：
  設定 Cloudflare KV namespace：
    - 執行：wrangler kv namespace create "OAUTH_KV"
    - 使用返回的 namespace ID 更新 wrangler.jsonc

  設定生產環境 secrets：
    - 執行：wrangler secret put GITHUB_CLIENT_ID
    - 執行：wrangler secret put GITHUB_CLIENT_SECRET
    - 執行：wrangler secret put DATABASE_URL
    - 執行：wrangler secret put COOKIE_ENCRYPTION_KEY

任務 6 - 本地測試：
  測試基本功能：
    - 執行：wrangler dev
    - 驗證伺服器無錯誤啟動
    - 測試 OAuth 流程：http://localhost:8792/authorize
    - 驗證 MCP 端點：http://localhost:8792/mcp

任務 7 - 生產部署：
  部署到 Cloudflare Workers：
    - 執行：wrangler deploy
    - 驗證部署成功
    - 測試生產環境 OAuth 流程
    - 驗證 MCP 端點可存取性
```

### 每個任務的實現細節

```typescript
// 任務 3 - MCP Server 實現模式
export class YourMCP extends McpAgent<Env, Record<string, never>, Props> {
  server = new McpServer({
    name: "您的 MCP Server 名稱",
    version: "1.0.0",
  });

  // 關鍵：總是實現清理
  async cleanup(): Promise<void> {
    try {
      await closeDb();
      console.log("資料庫連線成功關閉");
    } catch (error) {
      console.error("資料庫清理期間發生錯誤：", error);
    }
  }

  async alarm(): Promise<void> {
    await this.cleanup();
  }

  async init() {
    // 模式：使用集中式工具註冊
    registerAllTools(this.server, this.env, this.props);
  }
}

// 任務 3 - 工具模組模式（例如：src/tools/your-feature-tools.ts）
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { Props } from "../types";
import { z } from "zod";

const PRIVILEGED_USERS = new Set(["admin1", "admin2"]);

export function registerYourFeatureTools(server: McpServer, env: Env, props: Props) {
  // 工具 1：所有已認證使用者可用
  server.tool(
    "yourBasicTool",
    "您的基本工具描述",
    YourToolSchema, // Zod 驗證 schema
    async ({ param1, param2, options }) => {
      try {
        // 模式：帶錯誤處理的工具實現
        const result = await performOperation(param1, param2, options);

        return {
          content: [
            {
              type: "text",
              text: `**成功**\n\n操作完成\n\n**結果：**\n\`\`\`json\n${JSON.stringify(result, null, 2)}\n\`\`\``,
            },
          ],
        };
      } catch (error) {
        return createErrorResponse(`操作失敗：${error.message}`);
      }
    },
  );

  // 工具 2：僅限特權使用者
  if (PRIVILEGED_USERS.has(props.login)) {
    server.tool(
      "privilegedTool",
      "特權使用者的管理工具",
      { action: z.string() },
      async ({ action }) => {
        // 實現
        return {
          content: [
            {
              type: "text",
              text: `管理動作 '${action}' 由 ${props.login} 執行`,
            },
          ],
        };
      },
    );
  }
}

// 任務 3 - 更新工具註冊表（src/tools/register-tools.ts）
import { registerYourFeatureTools } from "./your-feature-tools";

export function registerAllTools(server: McpServer, env: Env, props: Props) {
  // 現有註冊
  registerDatabaseTools(server, env, props);
  
  // 添加您的新註冊
  registerYourFeatureTools(server, env, props);
}

// 模式：匯出帶有 MCP 端點的 OAuth provider
export default new OAuthProvider({
  apiHandlers: {
    "/sse": YourMCP.serveSSE("/sse") as any,
    "/mcp": YourMCP.serve("/mcp") as any,
  },
  authorizeEndpoint: "/authorize",
  clientRegistrationEndpoint: "/register",
  defaultHandler: GitHubHandler as any,
  tokenEndpoint: "/token",
});
```

### 整合點

```yaml
CLOUDFLARE_WORKERS：
  - wrangler.jsonc：更新名稱、環境變數、KV bindings
  - 環境 secrets：GitHub OAuth 憑證、資料庫 URL、加密金鑰
  - Durable Objects：配置 MCP agent binding 以進行狀態持久化

GITHUB_OAUTH：
  - GitHub App：建立時回調 URL 需匹配您的 Workers 網域
  - Client 憑證：儲存為 Cloudflare Workers secrets
  - 回調 URL：必須完全匹配：https://your-worker.workers.dev/callback

DATABASE：
  - PostgreSQL 連線：使用現有的連線池模式
  - 環境變數：DATABASE_URL 包含完整連線字串
  - 安全性：對所有 SQL 使用 validateSqlQuery 和 isWriteOperation

ENVIRONMENT_VARIABLES：
  - 開發：.dev.vars 檔案用於本地測試
  - 生產：Cloudflare Workers secrets 用於部署
  - 必需：GITHUB_CLIENT_ID、GITHUB_CLIENT_SECRET、DATABASE_URL、COOKIE_ENCRYPTION_KEY

KV_STORAGE：
  - OAuth 狀態：OAuth provider 用於狀態管理
  - Namespace：使用 `wrangler kv namespace create "OAUTH_KV"` 建立
  - 配置：將 namespace ID 添加到 wrangler.jsonc bindings
```

## 驗證閘門

### 第 1 級：TypeScript 和配置

```bash
# 關鍵：首先執行這些 - 在繼續之前修復任何錯誤
npm run type-check                 # TypeScript 編譯
wrangler types                     # 生成 Cloudflare Workers 類型

# 預期：無 TypeScript 錯誤
# 如有錯誤：修復類型問題、缺少的 interfaces、匯入問題
```

### 第 2 級：本地開發測試

```bash
# 啟動本地開發伺服器
wrangler dev

# 測試 OAuth 流程（應重定向到 GitHub）
curl -v http://localhost:8792/authorize

# 測試 MCP 端點（應返回伺服器資訊）
curl -v http://localhost:8792/mcp

# 預期：伺服器啟動、OAuth 重定向到 GitHub、MCP 回應伺服器資訊
# 如有錯誤：檢查控制台輸出、驗證環境變數、修復配置
```

### 第 3 級：單元測試每個功能、函式和檔案，遵循現有的測試模式（如果有的話）

```bash
npm run test
```

執行上述命令（Vitest）來執行單元測試，確保所有功能正常運作。

### 第 4 級：資料庫整合測試（如適用）

```bash
# 測試資料庫連線
curl -X POST http://localhost:8792/mcp \
  -H "Content-Type: application/json" \
  -d '{"method": "tools/call", "params": {"name": "listTables", "arguments": {}}}'

# 測試權限驗證
# 測試 SQL injection 防護和其他類型的安全性（如適用）
# 測試資料庫故障的錯誤處理

# 預期：資料庫操作正常、權限執行、錯誤優雅處理等
# 如有錯誤：檢查 DATABASE_URL、連線設定、權限邏輯
```

## 最終驗證清單

### 核心功能

- [ ] TypeScript 編譯：`npm run type-check` 通過
- [ ] 單元測試通過：`npm run test` 通過
- [ ] 本地伺服器啟動：`wrangler dev` 無錯誤執行
- [ ] MCP 端點回應：`curl http://localhost:8792/mcp` 返回伺服器資訊
- [ ] OAuth 流程正常：認證重定向並成功完成

---

## 要避免的反模式

### MCP 特定

- ❌ 不要跳過使用 Zod 的輸入驗證 - 總是驗證工具參數
- ❌ 不要忘記為 Durable Objects 實現 cleanup() 方法
- ❌ 不要硬編碼使用者權限 - 使用可配置的權限系統

### 開發流程

- ❌ 不要跳過驗證循環 - 每個級別都能捕捉不同的問題
- ❌ 不要猜測 OAuth 配置 - 測試完整流程
- ❌ 不要在沒有監控的情況下部署 - 實現日誌記錄和錯誤追蹤
- ❌ 不要忽略 TypeScript 錯誤 - 在部署前修復所有類型問題
