---
名稱: "prp-mcp-execute"
描述: 此命令旨在根據作為參數傳遞的特定產品需求提示 (Product Requirement Prompt, PRP) 創建一個全面的模型上下文協議 (Model Context Protocol, MCP) 伺服器，參考此程式碼庫模式，鏡像工具設定以滿足使用者的特定需求。
使用方式: /prp-mcp-execute path/to/prp.md
---

# 執行 MCP Server PRP

執行一個全面的產品需求提示 (Product Requirement Prompt, PRP)，用於建構具有身份驗證、資料庫整合和 Cloudflare Workers 部署的模型上下文協定 (Model Context Protocol, MCP) 伺服器。

要執行的 PRP：$ARGUMENTS

## 目的

執行 MCP 伺服器 PRP，包含全面的驗證、測試和部署驗證，遵循此程式碼庫中經過驗證的模式。

## 執行流程

1. **載入與分析 PRP**
   - 完整讀取指定的 PRP 檔案
   - 理解所有上下文、需求和驗證標準
   - 使用 TodoWrite 工具建立全面的待辦事項清單
   - 識別所有相依性和整合點

2. **上下文收集與研究**
   - 使用 Task agents 研究現有的 MCP 伺服器模式
   - 研究身份驗證流程和資料庫整合模式
   - 研究 Cloudflare Workers 部署和環境設定
   - 收集所有必要的文件和程式碼範例

3. **實作階段**
   - 按正確順序執行所有實作任務
   - 遵循現有程式碼庫的 TypeScript 模式
   - 實作 MCP 工具、資源和身份驗證流程
   - 新增全面的錯誤處理和日誌記錄

## 註記

- 使用 TodoWrite 工具進行全面的任務管理
- 遵循經過驗證的程式碼庫實作中的所有模式
- 包含全面的錯誤處理和復原機制
- 針對 Claude Code 的驗證迴圈進行最佳化
- 具備監控和日誌記錄功能，可用於生產環境
- 相容於 MCP Inspector 和 Claude Desktop
