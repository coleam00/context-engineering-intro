# 多代理系統：研究代理與 Email 草稿子代理

## 目的
建立一個 Pydantic AI 多代理系統，其中主要的研究代理使用 Brave Search API，並有一個 Email 草稿代理（使用 Gmail API）作為工具。這展示了代理即工具的模式，並整合外部 API。

## 核心原則
1. **Context 至上**：包含所有必要的文件、範例和注意事項
2. **驗證循環**：提供 AI 可以執行和修正的測試/檢查工具
3. **資訊密集**：使用來自程式碼庫的關鍵字和模式
4. **漸進式成功**：從簡單開始，驗證後再增強

---

## 目標
創建一個生產就緒的多代理系統，讓使用者可以通過 CLI 研究主題，研究代理可以將 email 草稿任務委派給 Email 草稿代理。系統應支援多個 LLM 供應商並安全地處理 API 認證。

## 為什麼
- **商業價值**：自動化研究和 email 草稿工作流程
- **整合**：展示進階的 Pydantic AI 多代理模式
- **解決的問題**：減少基於研究的 email 通信的手動工作

## 什麼
一個基於 CLI 的應用程式，其中：
- 使用者輸入研究查詢
- 研究代理使用 Brave API 搜索
- 研究代理可以調用 Email 草稿代理來創建 Gmail 草稿
- 結果即時串流回傳給使用者

### 成功標準
- [ ] 研究代理成功透過 Brave API 搜索
- [ ] Email 代理使用適當的認證創建 Gmail 草稿
- [ ] 研究代理可以調用 Email 代理作為工具
- [ ] CLI 提供具有工具可見性的串流響應
- [ ] 所有測試通過且程式碼符合品質標準

## 所需的全部 Context

### 文件與參考資料
```yaml
# 必須閱讀 - 將這些包含在您的 context 窗口中
- url: https://ai.pydantic.dev/agents/
  why: 核心代理創建模式
  
- url: https://ai.pydantic.dev/multi-agent-applications/
  why: 多代理系統模式，特別是代理即工具
  
- url: https://developers.google.com/gmail/api/guides/sending
  why: Gmail API 認證和草稿創建
  
- url: https://api-dashboard.search.brave.com/app/documentation
  why: Brave Search API REST endpoints
  
- file: examples/agent/agent.py
  why: 代理創建、工具註冊、依賴項的模式
  
- file: examples/agent/providers.py
  why: 多供應商 LLM 配置模式
  
- file: examples/cli.py
  why: CLI 結構與串流響應和工具可見性

- url: https://github.com/googleworkspace/python-samples/blob/main/gmail/snippet/send%20mail/create_draft.py
  why: 官方 Gmail 草稿創建範例
```

### 當前程式碼庫結構
```bash
.
├── examples/
│   ├── agent/
│   │   ├── agent.py
│   │   ├── providers.py
│   │   └── ...
│   └── cli.py
├── PRPs/
│   └── templates/
│       └── prp_base.md
├── INITIAL.md
├── CLAUDE.md
└── requirements.txt
```

### 期望的程式碼庫結構與要新增的檔案
```bash
.
├── agents/
│   ├── __init__.py               # 套件初始化
│   ├── research_agent.py         # 主要代理與 Brave Search
│   ├── email_agent.py           # 具有 Gmail 功能的子代理
│   ├── providers.py             # LLM 供應商配置
│   └── models.py                # 資料驗證的 Pydantic 模型
├── tools/
│   ├── __init__.py              # 套件初始化
│   ├── brave_search.py          # Brave Search API 整合
│   └── gmail_tool.py            # Gmail API 整合
├── config/
│   ├── __init__.py              # 套件初始化
│   └── settings.py              # 環境與配置管理
├── tests/
│   ├── __init__.py              # 套件初始化
│   ├── test_research_agent.py   # 研究代理測試
│   ├── test_email_agent.py      # Email 代理測試
│   ├── test_brave_search.py     # Brave 搜索工具測試
│   ├── test_gmail_tool.py       # Gmail 工具測試
│   └── test_cli.py              # CLI 測試
├── cli.py                       # CLI 介面
├── .env.example                 # 環境變數範本
├── requirements.txt             # 更新的依賴項
├── README.md                    # 綜合文件
└── credentials/.gitkeep         # Gmail 憑證目錄
```

### 已知陷阱與函式庫特性
```python
# 關鍵：Pydantic AI 要求全程 async - 在 async context 中不能使用 sync 函數
# 關鍵：Gmail API 首次運行需要 OAuth2 流程 - 需要 credentials.json
# 關鍵：Brave API 有速率限制 - 免費版每月 2000 次請求
# 關鍵：代理即工具模式需要傳遞 ctx.usage 進行 token 追蹤
# 關鍵：Gmail 草稿需要適當的 MIME 格式的 base64 編碼
# 關鍵：總是使用絕對匯入以獲得更乾淨的程式碼
# 關鍵：將敏感憑證存儲在 .env 中，永不提交它們
```

## 實作藍圖

### 資料模型和結構

```python
# models.py - 核心資料結構
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class ResearchQuery(BaseModel):
    query: str = Field(..., description="要調查的研究主題")
    max_results: int = Field(10, ge=1, le=50)
    include_summary: bool = Field(True)

class BraveSearchResult(BaseModel):
    title: str
    url: str
    description: str
    score: float = Field(0.0, ge=0.0, le=1.0)

class EmailDraft(BaseModel):
    to: List[str] = Field(..., min_items=1)
    subject: str = Field(..., min_length=1)
    body: str = Field(..., min_length=1)
    cc: Optional[List[str]] = None
    bcc: Optional[List[str]] = None

class ResearchEmailRequest(BaseModel):
    research_query: str
    email_context: str = Field(..., description="email 生成的上下文")
    recipient_email: str
```

### 要完成的任務清單

```yaml
任務 1: 設置配置和環境
創建 config/settings.py:
  - 模式：像範例一樣使用 pydantic-settings 和 os.getenv
  - 載入環境變數和預設值
  - 驗證必需的 API 金鑰存在

創建 .env.example:
  - 包含所有必需的環境變數和說明
  - 遵循 examples/README.md 的模式

任務 2: 實作 Brave Search 工具
創建 tools/brave_search.py:
  - 模式：像 examples/agent/tools.py 一樣使用 async 函數
  - 使用 httpx（已在 requirements 中）的簡單 REST 客戶端
  - 優雅地處理速率限制和錯誤
  - 返回結構化的 BraveSearchResult 模型

任務 3: 實作 Gmail 工具
創建 tools/gmail_tool.py:
  - 模式：遵循 Gmail quickstart 的 OAuth2 流程
  - 將 token.json 存儲在 credentials/ 目錄
  - 使用適當的 MIME 編碼創建草稿
  - 自動處理認證刷新

任務 4: 創建 Email 草稿代理
創建 agents/email_agent.py:
  - 模式：遵循 examples/agent/agent.py 結構
  - 使用 Agent 與 deps_type 模式
  - 註冊 gmail_tool 作為 @agent.tool
  - 返回 EmailDraft 模型

任務 5: 創建研究代理
創建 agents/research_agent.py:
  - 模式：來自 Pydantic AI 文件的多代理模式
  - 註冊 brave_search 作為工具
  - 註冊 email_agent.run() 作為工具
  - 使用 RunContext 進行依賴注入

任務 6: 實作 CLI 介面
創建 cli.py:
  - 模式：遵循 examples/cli.py 串流模式
  - 具有工具可見性的彩色輸出
  - 使用 asyncio.run() 正確處理 async
  - 對話上下文的 session 管理

任務 7: 新增綜合測試
創建 tests/:
  - 模式：模仿範例測試結構
  - 模擬外部 API 調用
  - 測試正常路徑、邊界情況、錯誤
  - 確保 80%+ 覆蓋率

任務 8: 創建文件
創建 README.md:
  - 模式：遵循 examples/README.md 結構
  - 包含設置、安裝、使用說明
  - API 金鑰配置步驟
  - 架構圖
```

### 各任務虛擬程式碼

```python
# 任務 2: Brave Search 工具
async def search_brave(query: str, api_key: str, count: int = 10) -> List[BraveSearchResult]:
    # 模式：像範例使用 aiohttp 一樣使用 httpx
    async with httpx.AsyncClient() as client:
        headers = {"X-Subscription-Token": api_key}
        params = {"q": query, "count": count}
        
        # 陷阱：如果 API 金鑰無效，Brave API 返回 401
        response = await client.get(
            "https://api.search.brave.com/res/v1/web/search",
            headers=headers,
            params=params,
            timeout=30.0  # 關鍵：設置超時以避免掛起
        )
        
        # 模式：結構化錯誤處理
        if response.status_code != 200:
            raise BraveAPIError(f"API 返回 {response.status_code}")
        
        # 使用 Pydantic 解析和驗證
        data = response.json()
        return [BraveSearchResult(**result) for result in data.get("web", {}).get("results", [])]

# 任務 5: 具有 Email 代理作為工具的研究代理
@research_agent.tool
async def create_email_draft(
    ctx: RunContext[AgentDependencies],
    recipient: str,
    subject: str,
    context: str
) -> str:
    """基於研究上下文創建 email 草稿。"""
    # 關鍵：傳遞 usage 進行 token 追蹤
    result = await email_agent.run(
        f"創建一封給 {recipient} 關於：{context} 的 email",
        deps=EmailAgentDeps(subject=subject),
        usage=ctx.usage  # 來自多代理文件的模式
    )
    
    return f"已創建草稿，ID：{result.data}"
```

### 整合點
```yaml
環境:
  - 新增到: .env
  - 變數: |
      # LLM 配置
      LLM_PROVIDER=openai
      LLM_API_KEY=sk-...
      LLM_MODEL=gpt-4
      
      # Brave Search
      BRAVE_API_KEY=BSA...
      
      # Gmail（credentials.json 的路徑）
      GMAIL_CREDENTIALS_PATH=./credentials/credentials.json
      
配置:
  - Gmail OAuth: 首次運行會打開瀏覽器進行授權
  - Token 存儲: ./credentials/token.json（自動創建）
  
依賴項:
  - 更新 requirements.txt，新增：
    - google-api-python-client
    - google-auth-httplib2
    - google-auth-oauthlib
```

## 驗證循環

### 等級 1: 語法與風格
```bash
# 首先運行這些 - 在繼續之前修復任何錯誤
ruff check . --fix              # 自動修復風格問題
mypy .                          # 類型檢查

# 預期：無錯誤。如有錯誤，請閱讀並修復。
```

### 等級 2: 單元測試
```python
# test_research_agent.py
async def test_research_with_brave():
    """測試研究代理正確搜索"""
    agent = create_research_agent()
    result = await agent.run("AI 安全研究")
    assert result.data
    assert len(result.data) > 0

async def test_research_creates_email():
    """測試研究代理可以調用 email 代理"""
    agent = create_research_agent()
    result = await agent.run(
        "研究 AI 安全並向 john@example.com 草擬 email"
    )
    assert "draft_id" in result.data

# test_email_agent.py  
def test_gmail_authentication(monkeypatch):
    """測試 Gmail OAuth 流程處理"""
    monkeypatch.setenv("GMAIL_CREDENTIALS_PATH", "test_creds.json")
    tool = GmailTool()
    assert tool.service is not None

async def test_create_draft():
    """測試使用適當編碼創建草稿"""
    agent = create_email_agent()
    result = await agent.run(
        "創建一封給 test@example.com 關於 AI 研究的 email"
    )
    assert result.data.get("draft_id")
```

```bash
# 反覆運行測試直到通過：
pytest tests/ -v --cov=agents --cov=tools --cov-report=term-missing

# 如果失敗：調試特定測試，修復程式碼，重新運行
```

### 等級 3: 整合測試
```bash
# 測試 CLI 互動
python cli.py

# 預期的互動：
# 您：研究最新的 AI 安全發展
# 🤖 助手：[串流研究結果]
# 🛠 使用的工具：
#   1. brave_search (query='AI 安全發展', limit=10)
#
# 您：為此創建一個 email 草稿給 john@example.com  
# 🤖 助手：[創建草稿]
# 🛠 使用的工具：
#   1. create_email_draft (recipient='john@example.com', ...)

# 檢查 Gmail 草稿資料夾中的創建草稿
```

## 最終驗證檢查清單
- [ ] 所有測試通過：`pytest tests/ -v`
- [ ] 無檢查錯誤：`ruff check .`
- [ ] 無類型錯誤：`mypy .`
- [ ] Gmail OAuth 流程正常運作（瀏覽器打開，token 已保存）
- [ ] Brave Search 返回結果
- [ ] 研究代理成功調用 Email 代理
- [ ] CLI 使用工具可見性串流響應
- [ ] 錯誤情況處理優雅
- [ ] README 包含清晰的設置說明
- [ ] .env.example 包含所有必需的變數

---

## 要避免的反模式
- ❌ 不要硬編碼 API 金鑰 - 使用環境變數
- ❌ 不要在 async 代理上下文中使用 sync 函數
- ❌ 不要跳過 Gmail 的 OAuth 流程設置
- ❌ 不要忽略 API 的速率限制
- ❌ 不要忘記在多代理調用中傳遞 ctx.usage
- ❌ 不要提交 credentials.json 或 token.json 檔案

## 信心分數：9/10

高信心，因為：
- 有程式碼庫中的清晰範例可以遵循
- 外部 API 文件完善
- 多代理系統已建立的模式
- 綜合驗證關卡

對 Gmail OAuth 首次設置 UX 略有不確定性，但文件提供了清晰的指導。