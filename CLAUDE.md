# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 專案概述

這是一個 Context Engineering 教學模板專案，旨在示範如何為 AI 編程助手提供充分的上下文資訊。專案包含 PRP (Product Requirements Prompt) 工作流程和實際使用案例。

## 常用命令

### Python 開發（主專案）
```bash
# 使用虛擬環境
source venv_linux/bin/activate  # 或建立新的：python -m venv venv_linux

# 格式化程式碼
black .

# 程式碼檢查
ruff check --fix

# 型別檢查
mypy .

# 執行測試
pytest tests/ -v

# 執行單一測試
pytest tests/test_module.py::test_function -v
```

### TypeScript 開發（MCP Server use case）
```bash
cd use-cases/mcp-server

# 安裝依賴
npm install

# 開發模式
npm run dev

# 型別檢查
npm run type-check

# 執行測試
npm test

# 部署
npm run deploy
```

## 專案架構

### 核心結構
- **PRPs/**: Product Requirements Prompts - 包含功能實現的詳細規格
- **examples/**: 程式碼範例（需要填充）
- **use-cases/**: 完整的使用案例，如 MCP Server 實現
- **.claude/commands/**: 自定義 Claude Code 命令（generate-prp, execute-prp）

### PRP 工作流程
1. 在 `INITIAL.md` 中描述功能需求
2. 使用 `/generate-prp` 生成完整的 PRP 文件
3. 使用 `/execute-prp` 執行 PRP 實現功能

### Python 專案規範
- **檔案大小限制**: 永遠不要建立超過 500 行的檔案
- **模組化結構**: 
  - `agent.py` - 主要邏輯
  - `tools.py` - 工具函數
  - `prompts.py` - 系統提示
- **測試結構**: `/tests` 資料夾映射主應用程式結構
- **技術選擇**: 
  - 使用 Pydantic 進行資料驗證
  - FastAPI 處理 APIs
  - SQLAlchemy/SQLModel 作為 ORM
  - python-dotenv 管理環境變數

## 重要注意事項

### Mermaid 圖表規則
- 使用 `flowchart` 而非 `graph`
- 避免巢狀 subgraph
- 中文文字使用雙引號包圍
- 不使用背景色樣式

### 任務管理
- 新任務前檢查 `TASK.md`
- 完成後立即標記任務為已完成
- 記錄工作中發現的新子任務

### AI 行為準則
- 永遠不要假設缺失的 context
- 只使用已知、經過驗證的套件
- 在引用前確認檔案路徑存在
- 不要刪除現有程式碼除非明確指示