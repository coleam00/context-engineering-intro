---
name: "prp-mcp-create"
description: 此命令旨在創建一個全面的產品需求提示（Product Requirement Prompt, PRP），用於構建模型上下文協議（Model Context Protocol, MCP）服務器，參考此代碼庫模式，鏡像工具設置以滿足用戶的特定需求。
Usage: /prp-mcp-create path/to/prp.md
Example usage: /prp-mcp-create weather-server "用於天氣數據的 MCP 服務器，含 API 集成"
Example usage: /prp-mcp-create file-manager "鏡像 task master mcp 的 MCP 服務器"
```
---

# 創建 MCP Server PRP

創建一個全面的產品需求提示（Product Requirement Prompt, PRP），用於構建具有身份驗證、數據庫集成和 Cloudflare Workers 部署的模型上下文協議（Model Context Protocol, MCP）服務器。

在開始之前，請確保您閱讀這些關鍵文件以了解 PRP 的目標：
PRPs/README.md
PRPs/templates/prp_mcp_base.md（此基礎 PRP 已根據項目結構部分填寫，但請根據用戶的 MCP 服務器用例完成它）

## 用戶的 MCP 用例：$ARGUMENTS

## 目的

生成專為 MCP 服務器開發設計的富含上下文的 PRP，使用此代碼庫中的成熟模式，這是一個 MCP 服務器設置的腳手架，用戶可以在此基礎上構建，包括 GitHub OAuth 和生產就緒的 Cloudflare Workers 部署。

現有的工具可能都不會被重用，工具應該為用戶的用例專門創建，以滿足他們的特定需求。

## 執行流程

1. **研究與上下文收集**
   - 創建清晰的待辦事項並生成子代理來搜索代碼庫中的類似功能/模式。深入思考並規劃您的方法
   - 收集有關 MCP 工具、資源和身份驗證流程的相關文檔
   - 研究現有的工具模式，以了解如何構建用戶指定的用例
   - 研究代碼庫中現有的集成模式

2. **生成全面的 PRP**
   - 使用專門的 `PRPs/templates/prp_mcp_base.md` 模板作為基礎
   - 使用特定的服務器需求和功能自定義模板
   - 包含來自代碼庫模式和 ai_docs 的所有必要上下文
   - 為 MCP 服務器開發添加特定的驗證循環
   - 包含數據庫集成模式和安全考慮

3. **使用 AI 文檔增強**
   - 用戶可能在 PRPs/ai_docs/ 目錄中添加了文檔，您應該閱讀它們
   - 如果 PRPs/ai_docs/ 目錄中有文檔，請查看它們並在構建 PRP 時將它們納入上下文

## 實施細節

### MCP 服務器的 PRP 結構

生成的 PRP 使用專門的模板 `PRPs/templates/prp_mcp_base.md` 並包括：

- **目標**：清晰描述要構建的 MCP 服務器，包含身份驗證和數據庫集成
- **上下文**：所有必要的文檔，包括 PRPs/ai_docs/ 參考和現有代碼庫模式
- **實施藍圖**：遵循 Cloudflare Workers 模式的逐步 TypeScript 任務
- **驗證循環**：從編譯到生產部署的全面 MCP 特定測試
- **安全考慮**：GitHub OAuth 流程、數據庫訪問模式和 SQL 注入保護

### 關鍵特性

- **富含上下文**：使用此成熟代碼庫的相對路徑包含所有模式和參考
- **驗證驅動**：從語法到生產部署的多級驗證
- **安全優先**：內置身份驗證和授權模式
- **生產就緒**：Cloudflare Workers 部署和監控

### 研究領域

1. **MCP Protocol 模式**
   - 工具註冊和驗證
   - 資源服務和緩存
   - 錯誤處理和日誌記錄
   - 客戶端通信模式

2. **身份驗證集成**
   - GitHub OAuth 實施
   - 用戶權限系統
   - Token 管理和驗證
   - Session 處理模式

## 輸出

在 PRPs/ 目錄中創建一個全面的 PRP 文件，包含：

- 所有必要的上下文和代碼模式
- 逐步實施任務
- MCP 服務器開發的驗證循環

## 驗證

該命令確保：

- 所有引用的代碼模式存在於代碼庫中
- 文檔鏈接有效且可訪問
- 實施任務具體且可執行
- 驗證循環全面且可由 claude code 執行（重要）

## 與現有模式的集成

- 使用來自 `PRPs/templates/prp_mcp_base.md` 的專門 MCP 模板
- 遵循已建立的目錄結構和命名約定
- 與現有的驗證模式和工具集成
- 利用 `src/` 中當前 MCP 服務器實施的成熟模式
