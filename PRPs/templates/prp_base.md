# PRP (Product Requirements Prompt) 模板

## PRP 執行流程圖

此流程圖展示了 PRP 的完整執行過程，包含載入上下文、執行任務、驗證循環和最終驗證：

```mermaid
flowchart TD
    A["開始執行 PRP"]
    A --> B["載入所有上下文"]
    B --> C["分析任務清單"]
    C --> D["執行任務 1"]
    D --> E["驗證循環"]
    
    E --> E1{"語法與風格<br/>檢查通過"}
    E1 -->|"否"| E2["修復錯誤"]
    E2 --> E1
    E1 -->|"是"| E3{"單元測試<br/>通過"}
    E3 -->|"否"| E4["修復測試"]
    E4 --> E3
    E3 -->|"是"| E5{"整合測試<br/>通過"}
    E5 -->|"否"| E6["修復整合"]
    E6 --> E5
    E5 -->|"是"| F["任務完成"]
    
    F --> G{"還有<br/>更多任務"}
    G -->|"是"| H["執行下一個任務"]
    H --> E
    G -->|"否"| I["最終驗證"]
    I --> J["PRP 執行完成"]
```

---

## 驗證循環層級圖

下圖說明了程式碼驗證的三個層級，從語法檢查到整合測試的完整驗證流程：

```mermaid
flowchart LR
    A["程式碼實作"] --> B["級別1<br/>語法與風格"]
    B --> B1["ruff check"]
    B --> B2["mypy"]
    
    B --> C["級別2<br/>單元測試"]
    C --> C1["pytest"]
    C --> C2["覆蓋率檢查"]
    
    C --> D["級別3<br/>整合測試"]
    D --> D1["服務啟動"]
    D --> D2["API 測試"]
    D --> D3["端到端驗證"]
    
    D --> E["通過所有驗證"]
```

## 目的
針對 AI agent 優化的模板，用於實作具有充分上下文和自我驗證能力的功能，通過迭代優化達到可運行的程式碼。

## 核心原則
1. **Context 至上**：包含所有必要的文件、範例和注意事項
2. **驗證循環**：提供 AI 可以執行和修復的可執行測試/檢查
3. **資訊密集**：使用程式碼庫中的關鍵字和模式
4. **漸進成功**：從簡單開始，驗證，然後增強
5. **全域規則**：確保遵循 CLAUDE.md 中的所有規則

---

## 目標
[需要建構什麼 - 具體說明最終狀態和需求]

## 為什麼
- [商業價值和使用者影響]
- [與現有功能的整合]
- [解決什麼問題以及為誰解決]

## 什麼
[使用者可見的行為和技術需求]

### 成功標準
- [ ] [具體的可衡量結果]

## 所有需要的上下文

### 文件與參考資料 (列出實作功能所需的所有上下文)
```yaml
# 必讀 - 將這些包含在你的上下文視窗中
- url: [官方 API 文件 URL]
  why: [你需要的特定章節/方法]
  
- file: [path/to/example.py]
  why: [要遵循的模式，要避免的陷阱]
  
- doc: [函式庫文件 URL] 
  section: [關於常見陷阱的特定章節]
  critical: [防止常見錯誤的關鍵見解]

- docfile: [PRPs/ai_docs/file.md]
  why: [使用者貼到專案中的文件]

```

### 當前程式碼庫結構 (在專案根目錄執行 `tree` 來獲得程式碼庫概覽)
```bash

```

### 期望的程式碼庫結構，包含要新增的檔案及檔案職責
```bash

```

### 我們程式碼庫的已知陷阱與函式庫特殊性
```python
# 關鍵：[函式庫名稱] 需要 [特定設定]
# 範例：FastAPI 需要 async 函數來處理 endpoints
# 範例：這個 ORM 不支援超過 1000 條記錄的批次插入
# 範例：我們使用 pydantic v2 並且  
```

## 實作藍圖

### 資料模型和結構

建立核心資料模型，確保型別安全性和一致性。
```python
範例: 
 - orm 模型
 - pydantic 模型
 - pydantic schemas
 - pydantic validators

```

### 按完成順序列出完成此 PRP 需要完成的任務清單

```yaml
任務 1:
修改 src/existing_module.py:
  - 尋找模式: "class OldImplementation"
  - 在包含 "def __init__" 的行後插入
  - 保留現有方法簽名

建立 src/new_feature.py:
  - 參考模式來自: src/similar_feature.py
  - 修改類別名稱和核心邏輯
  - 保持錯誤處理模式完全相同

...(...)

任務 N:
...

```

### 每個任務的偽程式碼 (根據需要新增到每個任務)
```python

# 任務 1
# 包含關鍵細節的偽程式碼，不要寫完整程式碼
async def new_feature(param: str) -> Result:
    # 模式：總是先驗證輸入 (參見 src/validators.py)
    validated = validate_input(param)  # 拋出 ValidationError
    
    # 陷阱：這個函式庫需要連接池
    async with get_connection() as conn:  # 參見 src/db/pool.py
        # 模式：使用現有的重試裝飾器
        @retry(attempts=3, backoff=exponential)
        async def _inner():
            # 關鍵：API 如果 >10 req/sec 會返回 429
            await rate_limiter.acquire()
            return await external_api.call(validated)
        
        result = await _inner()
    
    # 模式：標準化回應格式
    return format_response(result)  # 參見 src/utils/responses.py
```

### 整合點
```yaml
DATABASE:
  - migration: "在 users 表中新增欄位 'feature_enabled'"
  - index: "CREATE INDEX idx_feature_lookup ON users(feature_id)"
  
CONFIG:
  - 新增到: config/settings.py
  - 模式: "FEATURE_TIMEOUT = int(os.getenv('FEATURE_TIMEOUT', '30'))"
  
ROUTES:
  - 新增到: src/api/routes.py  
  - 模式: "router.include_router(feature_router, prefix='/feature')"
```

## 驗證循環

### 級別 1：語法與風格
```bash
# 首先執行這些 - 在繼續之前修復任何錯誤
ruff check src/new_feature.py --fix  # 自動修復可能的問題
mypy src/new_feature.py              # 型別檢查

# 預期：沒有錯誤。如果有錯誤，讀取錯誤並修復。
```

### 級別 2：單元測試，每個新功能/檔案/函數使用現有測試模式
```python
# 建立 test_new_feature.py 包含這些測試案例：
def test_happy_path():
    """基本功能正常運作"""
    result = new_feature("valid_input")
    assert result.status == "success"

def test_validation_error():
    """無效輸入拋出 ValidationError"""
    with pytest.raises(ValidationError):
        new_feature("")

def test_external_api_timeout():
    """優雅地處理超時"""
    with mock.patch('external_api.call', side_effect=TimeoutError):
        result = new_feature("valid")
        assert result.status == "error"
        assert "timeout" in result.message
```

```bash
# 執行並迭代直到通過：
uv run pytest test_new_feature.py -v
# 如果失敗：讀取錯誤，理解根本原因，修復程式碼，重新執行 (不要透過 mock 來通過)
```

### 級別 3：整合測試
```bash
# 啟動服務
uv run python -m src.main --dev

# 測試端點
curl -X POST http://localhost:8000/feature \
  -H "Content-Type: application/json" \
  -d '{"param": "test_value"}'

# 預期：{"status": "success", "data": {...}}
# 如果錯誤：檢查 logs/app.log 中的堆疊追蹤
```

## 最終驗證檢查清單
- [ ] 所有測試通過：`uv run pytest tests/ -v`
- [ ] 沒有 linting 錯誤：`uv run ruff check src/`
- [ ] 沒有型別錯誤：`uv run mypy src/`
- [ ] 手動測試成功：[具體的 curl/命令]
- [ ] 錯誤情況得到優雅處理
- [ ] 日誌有資訊性但不冗長
- [ ] 如需要則更新文件

---

## 要避免的反模式
- ❌ 當現有模式有效時不要建立新模式
- ❌ 不要因為"應該可以工作"而跳過驗證
- ❌ 不要忽略失敗的測試 - 修復它們
- ❌ 不要在 async 上下文中使用 sync 函數
- ❌ 不要硬編碼應該是配置的值
- ❌ 不要捕獲所有異常 - 要具體
