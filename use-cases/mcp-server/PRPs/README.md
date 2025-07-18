# Product Requirement Prompt (PRP) 概念

"過度指定要構建什麼，卻未充分說明背景和如何構建，這就是為什麼許多 AI 驅動的編碼嘗試會在完成 80% 時停滯不前。Product Requirement Prompt (PRP) 通過融合經典 Product Requirements Document (PRD) 的嚴謹範圍與現代 prompt engineering 的「背景為王」思維來解決這個問題。"

## 什麼是 PRP？

Product Requirement Prompt (PRP) 是一種結構化的 prompt，它為 AI 編碼代理提供交付可運行軟體垂直切片所需的一切——不多不少。

### 與 PRD 的區別

傳統的 PRD 闡明產品必須做什麼以及客戶為什麼需要它，但刻意避免說明如何構建。

PRP 保留了 PRD 的目標和理由部分，但增加了三個對 AI 至關重要的層面：

### 背景
* 精確的檔案路徑和內容、程式庫版本和程式庫背景、程式碼片段範例。當提供直接的 in-prompt 參考而非廣泛描述時，LLMs 會生成更高品質的程式碼。使用 ai_docs/ 目錄來匯入程式庫和其他文檔。

### 實施細節和策略
* 與傳統 PRD 相反，PRP 明確說明產品將如何構建。這包括使用 API endpoints、測試執行器或代理模式（ReAct、Plan-and-Execute）。使用 typehints、依賴項、架構模式和其他工具來確保程式碼正確構建。

### 驗證閘門
* 確定性檢查，如 pytest、ruff 或靜態類型檢查「左移」品質控制可以及早發現缺陷，比後期返工更便宜。範例：每個新函數都應該單獨測試，驗證閘門 = 所有測試通過。

### PRP 層 存在的原因
* PRP 資料夾用於準備並將 PRPs 傳送給 agentic coder。

## 為什麼背景不可或缺

大型語言模型的輸出受其 context window 限制；不相關或缺失的背景會實際上擠出有用的 tokens

業界格言「垃圾進→垃圾出」在 prompt engineering 中加倍適用，特別是在 agentic engineering 中：草率的輸入會產生脆弱的程式碼

## 簡而言之

PRP 是 PRD + 精心策劃的程式碼庫智慧 + agent/runbook——AI 在第一次嘗試中合理交付生產就緒程式碼所需的最小可行封包。

PRP 可以很小，專注於單一任務，也可以很大，涵蓋多個任務。PRP 的真正力量在於能夠在 PRP 中將任務串聯起來，以構建、自我驗證並交付複雜功能。
