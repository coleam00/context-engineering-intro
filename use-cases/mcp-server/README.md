# MCP Server Builder - Context Engineering 用例

## MCP Server 整體架構圖

以下架構圖展示了基於 Cloudflare Workers 的 MCP Server 完整技術堆疊，包含身份驗證、MCP 核心、工具系統和外部整合：

```mermaid
flowchart TD
    A["MCP Server<br/>Cloudflare Workers"]
    A --> B["身份驗證層"]
    A --> C["MCP 核心"]
    A --> D["工具系統"]
    
    B --> B1["GitHub OAuth 2.0"]
    B --> B2["HMAC 簽名 Cookie"]
    B --> B3["角色權限控制"]
    
    C --> C1["McpAgent<br/>Durable Objects"]
    C --> C2["McpServer SDK"]
    C --> C3["雙協議支持<br/>HTTP + SSE"]
    
    D --> D1["資料庫工具"]
    D --> D2["模組化註冊"]
    D --> D3["Zod 驗證"]
    
    E["外部整合"] --> E1["PostgreSQL"]
    E --> E2["GitHub API"]
    E --> E3["Sentry 監控"]
    
    D1 --> E1
    B1 --> E2
    C --> E3
```

---

## MCP Server PRP 工作流程圖

此流程圖說明了使用 Context Engineering 建立 MCP Server 的完整流程，從定義需求到部署生產：

```mermaid
flowchart LR
    A["1.定義需求<br/>PRPs/INITIAL.md"] --> B["2.生成 MCP PRP<br/>/prp-mcp-create"]
    B --> C["3.審查與調整<br/>PRPs/your-server.md"]
    C --> D["4.執行 PRP<br/>/prp-mcp-execute"]
    D --> E["5.本地測試<br/>wrangler dev"]
    E --> F["6.部署生產<br/>wrangler deploy"]
    
    G["MCP 模板與模式"] --> B
    H["現有程式碼範例"] --> B
    I["驗證循環"] --> D
    
    E --> E1["MCP Inspector<br/>測試"]
    E --> E2["Claude Desktop<br/>整合"]
```

此用例演示如何使用**Context Engineering**和**PRP (Product Requirements Prompt) 流程**來構建生產就緒的 Model Context Protocol (MCP) 伺服器。它提供了一個經過驗證的模板和工作流程，用於創建具有 GitHub OAuth 身份驗證、資料庫集成和 Cloudflare Workers 部署的 MCP 伺服器。

> PRP 是 PRD + 精選代碼庫智能 + agent/runbook — 這是 AI 在首次嘗試時就能合理交付生產就緒代碼所需的最小可行包。

## 🎯 你將學到什麼

此用例教你如何：

- **使用 PRP 流程**系統性地構建複雜的 MCP 伺服器
- **利用專業化的 context engineering**進行 MCP 開發
- **遵循經過驗證的模式**，使用生產就緒的 MCP 伺服器模板
- **實施安全身份驗證**，包括 GitHub OAuth 和基於角色的存取控制
- **部署到 Cloudflare Workers**，具備監控和錯誤處理功能

## 📋 工作原理 - MCP 伺服器的 PRP 流程

### 1. 定義你的 MCP 伺服器 (initial.md)

首先在 `PRPs/INITIAL.md` 中描述你想要構建的確切 MCP 伺服器：

```markdown
## FEATURE:
我們想要創建一個天氣 MCP 伺服器，提供實時天氣數據，
具備快取和速率限制功能。

## ADDITIONAL FEATURES:
- 與 OpenWeatherMap API 集成
- Redis 快取以提升效能
- 每用戶速率限制
- 歷史天氣數據存取
- 地點搜尋和自動完成

## OTHER CONSIDERATIONS:
- 外部服務的 API 金鑰管理
- API 故障的適當錯誤處理
- 地點查詢的座標驗證
```

### 2. 生成你的 PRP

使用專業化的 MCP PRP 指令來創建全面的實作計劃：

```bash
/prp-mcp-create INITIAL.md
```

**此指令的作用：**
- 讀取你的功能需求
- 研究現有的 MCP 代碼庫模式
- 學習身份驗證和資料庫集成模式
- 在 `PRPs/your-server-name.md` 中創建全面的 PRP
- 包括所有上下文、驗證循環和逐步任務

> 在生成 PRP 後驗證所有內容是很重要的！使用 PRP 框架時，你需要參與流程以確保所有上下文的品質！執行的好壞完全取決於你的 PRP。將 /prp-mcp-create 用作一個堅實的起點。

### 3. 執行你的 PRP

使用專業化的 MCP 執行指令來構建你的伺服器：

```bash
/prp-mcp-execute PRPs/your-server-name.md
```

**此指令的作用：**
- 載入包含所有上下文的完整 PRP
- 使用 TodoWrite 創建詳細的實作計劃
- 遵循經過驗證的模式實施每個組件
- 運行全面驗證（TypeScript、測試、部署）
- 確保你的 MCP 伺服器端到端正常工作

## 🏗️ MCP 專用 Context Engineering

此用例包括專門為 MCP 伺服器開發設計的專業化 context engineering 組件：

### 專業化 Slash 指令

位於 `.claude/commands/`：

- **`/prp-mcp-create`** - 專門為 MCP 伺服器生成 PRP
- **`/prp-mcp-execute`** - 執行 MCP PRP 並進行全面驗證

這些是根目錄 `.claude/commands/` 中通用指令的專業化版本，但針對 MCP 開發模式進行了調整。

### 專業化 PRP 模板

模板 `PRPs/templates/prp_mcp_base.md` 包括：

- **MCP 專用模式**用於工具註冊和身份驗證
- **Cloudflare Workers 配置**用於部署
- **GitHub OAuth 集成**模式
- **資料庫安全性**和 SQL 注入保護
- **全面驗證循環**從 TypeScript 到生產環境

### AI 文檔

`PRPs/ai_docs/` 資料夾包含：

- **`mcp_patterns.md`** - 核心 MCP 開發模式和安全實踐
- **`claude_api_usage.md`** - 如何集成 Anthropic 的 API 以實現 LLM 驅動的功能

## 🔧 模板架構

此模板提供了一個完整的生產就緒 MCP 伺服器，包含：

### 核心組件

```
src/
├── index.ts                 # 主要的身份驗證 MCP 伺服器
├── index_sentry.ts         # 具有 Sentry 監控的版本
├── simple-math.ts          # 基本 MCP 範例（無身份驗證）
├── github-handler.ts       # 完整的 GitHub OAuth 實作
├── database.ts             # 具有安全模式的 PostgreSQL
├── utils.ts                # OAuth 輔助工具和實用程式
├── workers-oauth-utils.ts  # HMAC 簽名 cookie 系統
└── tools/                  # 模組化工具註冊系統
    └── register-tools.ts   # 中央工具註冊表
```

### 範例工具

`examples/` 資料夾顯示如何創建 MCP 工具：

- **`database-tools.ts`** - 具有適當模式的範例資料庫工具
- **`database-tools-sentry.ts`** - 具有 Sentry 監控的相同工具

### 主要功能

- **🔐 GitHub OAuth** - 完整的身份驗證流程，具有基於角色的存取控制
- **🗄️ 資料庫集成** - 具有連接池和安全性的 PostgreSQL
- **🛠️ 模組化工具** - 清晰的關注點分離和中央註冊
- **☁️ Cloudflare Workers** - 全球邊緣部署與 Durable Objects
- **📊 監控** - 生產環境的可選 Sentry 集成
- **🧪 測試** - 從 TypeScript 到部署的全面驗證

## 🚀 快速開始

### 先決條件

- 已安裝 Node.js 和 npm
- Cloudflare 帳戶（免費方案可用）
- GitHub 帳戶用於 OAuth
- PostgreSQL 資料庫（本地或託管）

### 步驟 1：克隆和設置

```bash
# 克隆 context engineering 模板
git clone https://github.com/coleam00/Context-Engineering-Intro.git
cd Context-Engineering-Intro/use-cases/mcp-server

# 安裝依賴
npm install

# 全局安裝 Wrangler CLI
npm install -g wrangler

# 使用 Cloudflare 進行身份驗證
wrangler login
```

### 步驟 2：配置環境

```bash
# 創建環境文件
cp .dev.vars.example .dev.vars

# 編輯 .dev.vars 輸入你的憑證
# - GitHub OAuth 應用程式憑證
# - 資料庫連接字符串
# - Cookie 加密金鑰
```

### 步驟 3：定義你的 MCP 伺服器

編輯 `PRPs/INITIAL.md` 來描述你的特定 MCP 伺服器需求：

```markdown
## FEATURE:
準確描述你的 MCP 伺服器應該做什麼 - 具體說明
功能、數據來源和用戶交互。

## ADDITIONAL FEATURES:
- 列出基本 CRUD 操作之外的特定功能
- 包括與外部 API 的集成
- 提及任何特殊要求

## OTHER CONSIDERATIONS:
- 身份驗證要求
- 效能考慮
- 安全要求
- 速率限制需求
```

### 步驟 4：生成和執行 PRP

```bash
# 生成全面的 PRP
/prp-mcp-create INITIAL.md

# 執行 PRP 來構建你的伺服器
/prp-mcp-execute PRPs/your-server-name.md
```

### 步驟 5：測試和部署

```bash
# 本地測試
wrangler dev

# 使用 MCP Inspector 測試
npx @modelcontextprotocol/inspector@latest
# 連接到：http://localhost:8792/mcp

# 部署到生產環境
wrangler deploy
```

## 🔍 需要理解的關鍵文件

要完全理解此用例，請檢查這些文件：

### Context Engineering 組件

- **`PRPs/templates/prp_mcp_base.md`** - 專業化 MCP PRP 模板
- **`.claude/commands/prp-mcp-create.md`** - MCP 專用 PRP 生成
- **`.claude/commands/prp-mcp-execute.md`** - MCP 專用執行

### 實作模式

- **`src/index.ts`** - 具有身份驗證的完整 MCP 伺服器
- **`examples/database-tools.ts`** - 工具創建和註冊模式
- **`src/tools/register-tools.ts`** - 模組化工具註冊系統

### 配置和部署

- **`wrangler.jsonc`** - Cloudflare Workers 配置
- **`.dev.vars.example`** - 環境變數模板
- **`CLAUDE.md`** - 實作指南和模式

## 📈 成功指標

當你成功使用此流程時，你將實現：

- **快速實作** - 以最少的迭代快速擁有 MCP 伺服器
- **生產就緒** - 安全身份驗證、監控和錯誤處理
- **可擴展架構** - 清晰的關注點分離和模組化設計
- **全面測試** - 從 TypeScript 到生產部署的驗證

## 🤝 貢獻

此用例演示了 Context Engineering 在複雜軟件開發中的威力。要改進它：

1. **添加新的 MCP 伺服器範例**以展示不同模式
2. **增強 PRP 模板**，提供更全面的上下文
3. **改進驗證循環**以更好地檢測錯誤
4. **記錄邊緣情況**和常見陷阱

目標是通過全面的 context engineering 使 MCP 伺服器開發變得可預測和成功。

---

**準備好構建你的 MCP 伺服器了嗎？**從編輯 `PRPs/INITIAL.md` 開始，然後運行 `/prp-mcp-create INITIAL.md` 來生成你的全面實作計劃。