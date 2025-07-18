# MCP Server 功能需求 - PRP 任務管理系統

## 系統架構圖

```mermaid
flowchart TD
    A["PRP 任務管理 MCP Server"]
    A --> B["PRP 解析系統"]
    A --> C["任務管理系統"]
    A --> D["資料庫層"]
    
    B --> B1["Anthropic LLM<br/>資訊擷取"]
    B --> B2["PRP 文件解析"]
    B --> B3["自動任務建立"]
    
    C --> C1["CRUD 操作"]
    C --> C2["任務查詢"]
    C --> C3["標籤管理"]
    C --> C4["文檔管理"]
    
    D --> D1["任務表"]
    D --> D2["文檔表"]
    D --> D3["標籤表"]
    D --> D4["關聯表"]
```

## 資料流程圖

```mermaid
flowchart LR
    A["PRP 文件"] --> B["解析工具<br/>parsePRP"]
    B --> C["Anthropic API<br/>擷取資訊"]
    C --> D["結構化資料"]
    
    D --> E["儲存到資料庫"]
    E --> E1["任務"]
    E --> E2["目標"]
    E --> E3["使用者"]
    E --> E4["文檔"]
    
    F["查詢工具"] --> G["從資料庫獲取"]
    G --> H["返回結果"]
    
    I["修改工具"] --> J["更新資料庫"]
```

## FEATURE:

We want to create a MCP server using this repos template

The goal of the MCP server is to create a simple version of taskmaster mcp that instead of parsing PRDs we parse PRPs.

Additional features:

- LLM powered PRP information extraction using anthropic
- Crud operation on tasks, documentation, tags, etc to and from the DB

We need tools for parsing PRPs this tool should take a filled PRP and use anthropic to extract the tasks into tasks and save them to the db, including surrounding documentation from the prp like the goals what whys, target users, etc.

We need:

- To be able to perform CRUD operations on tasks, documentation, tags, etc
- A task fetch tool to get the tasks from the
- To be able to list all tasks
- To be able to add information to a task
- To be able to fetch the additional documentation from the db
- To be able to modify the additional documentation
- DB tables needs to be updated to match our new data models

## EXAMPLES & DOCUMENTATION:

All examples are already referenced in prp_mcp_base.md - do any additional research as needed.

## OTHER CONSIDERATIONS:

- Do not use complex regex or complex parsing patterns, we use an LLM to parse PRPs.
- Model and API key for Anthropic both need to be environment variables - these are set up in .dev.vars.example
- It's very important that we create one task per file to keep concerns separate