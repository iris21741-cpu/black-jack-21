# 🃏 Full-Stack Blackjack (21 點) Game

## 專案簡介

本專案為一個 **全端 21 點（Blackjack）遊戲**，完整實作從前端使用者操作到後端遊戲邏輯計算的整體流程。
是一款由 前端工程師 Doris 與 後端工程師 Iris Tseng共同協作完成的 Blackjack 遊戲。
玩家可透過網頁介面進行下注、要牌、停牌等操作，並即時取得遊戲結果。

專案重點在於：

* 清楚的前後端職責切分
* 完整的 Blackjack 遊戲規則實作
* 可維護、可擴充的 API 設計

---

## 系統架構

```
Frontend (Web UI)
   │  HTTP / JSON
   ▼
Backend API (Blackjack Game Logic)
   │
   ▼
Database / Cache (Game State, User Data)
```

* **前端**：負責 UI 呈現、動畫效果、玩家操作流程與 API 串接
* **後端**：負責 21 點核心遊戲邏輯、狀態控管與 後端API 設計

---

## 為何選擇 FastAPI + JWT + Redis（系統設計說明）

本專案在後端架構設計上，選擇 **FastAPI + JWT + Redis** 作為核心技術組合，主要考量為效能、可維護性與實務可擴充性。

### 為何選擇 FastAPI

* **高效能**：FastAPI 基於 ASGI 與非同步架構，能有效支援即時互動的遊戲 API（如 Hit / Stand 等高頻請求）。
* **型別安全與可讀性**：結合 Python type hints 與 Pydantic（Schema 驗證），使 API 輸入輸出結構明確，降低前後端溝通成本。
* **自動文件產生**：內建 OpenAPI / Swagger UI，方便前端快速理解與串接遊戲相關 API。
* **適合遊戲狀態機實作**：清楚的路由與 service 分層，利於管理 Blackjack 不同遊戲狀態（NEW / BET / PLAYER_OPERATION / STATEMENT / GAME_OVER）。

### 為何使用 JWT（JSON Web Token）

* **無狀態驗證（Stateless Authentication）**：JWT 不依賴 Server Session，適合前後端分離架構。
* **前端整合容易**：Token 可安全存放於 LocalStorage，並隨 API Request Header 傳送。
* **權限與身分驗證清楚**：可於 Token 中攜帶使用者識別資訊，確保每一局遊戲狀態皆正確對應使用者。
* **可搭配 2FA 強化安全性**：本專案結合 Email 2FA 驗證流程，提高帳戶與遊戲資源安全。

### 為何使用 Redis

* **高速存取遊戲狀態**：Redis 適合儲存即時遊戲狀態與暫存資料，避免頻繁存取資料庫。
* **支援短生命週期資料**：如進行中的牌局、玩家操作階段狀態、Token 黑名單等。
* **為未來擴充預留彈性**：可延伸支援多玩家對戰、房間系統、排行榜或 WebSocket 即時推播。

### 技術組合總結

FastAPI 提供清楚、快速且可測試的 API 架構；JWT 負責安全且可擴充的身分驗證；Redis 則補足高頻率遊戲狀態存取的效能需求。三者結合，使本專案在 **效能、安全性與可擴充性** 上均符合實務級全端專案標準。

---

## 技術分工

## 使用技術總覽

### Frontend（由 Doris 製作）

* **Framework**：Next.js 16（App Router）
* **UI Library**：React（React Hooks）
* **Language**：TypeScript
* **State Management**：Zustand
* **Data Validation**：ZOD
* **Styling**：Tailwind CSS
* **Animation**：Framer Motion
* **Auth Handling**：LocalStorage Token 持久化

### Backend（由 Iris Tseng 製作）

* **Language / Framework**：Python / FastAPI
* **Authentication**：

  * JWT Token 產生與驗證
  * Email 2FA 驗證機制
* **Game Logic**：

  * Blackjack 核心邏輯（洗牌、發牌、要牌、停牌、Double、結算）
  * 遊戲狀態管理（NEW / BET / PLAYER_OPERATION / STATEMENT / GAME_OVER）
  * 籌碼（Chips）計算與更新
* **Cache / Session**：Redis 連線與狀態支援

---

## 技術分工

### Frontend

**負責人：Doris**

* 設計並實作整體前端 UI
* 製作遊戲動畫與互動效果
* 規劃並實作完整遊戲流程（下注 → 發牌 → 玩家操作 → 結算）
* 與後端 API 串接，處理資料顯示與狀態更新

### Backend

**負責人：Iris**

* 設計並實作 Blackjack（21 點）遊戲核心邏輯
* 控制遊戲流程與狀態（New / Bet / Player Turn / Dealer Turn / Settlement）
* 設計 RESTful API，提供前端操作與資料取得
* 負責遊戲結果判定與規則一致性

---

## 遊戲規則簡述

* 使用標準 21 點規則
* 玩家可進行：

  * 下注（Bet）
  * 要牌（Hit）
  * 停牌（Stand）
  * 雙倍（Double）
* 莊家依固定規則補牌
* 系統自動計算勝負與結算結果

---

## 專案特色（後端設計邏輯亮點）

### 🧠 1. 以「狀態機」為核心的 Blackjack 遊戲引擎設計

後端 API 處理遊戲行為以**明確的遊戲狀態機（State Machine）**作為整體設計核心：

* `NEW`：建立新遊戲，初始化牌堆與玩家資料
* `BET`：僅允許下注相關操作，防止非法流程呼叫
* `PLAYER_OPERATION`：玩家操作階段（Hit / Stand / Double）
* `STATEMENT`：莊家補牌與結果計算階段
* `GAME_OVER`：結算完成，等待重新開局

所有 API 皆會依據當前狀態進行合法性驗證，確保：

* 遊戲流程不可被跳步或重複執行
* 前端即使誤呼叫 API，也不會破壞遊戲一致性

---

### 🃏 2. Blackjack 核心規則完整封裝

後端完整實作 Blackjack 核心遊戲邏輯，並集中於服務層管理：

* 洗牌（Shuffle）與發牌（Deal）
* 點數計算（Ace 動態 1 / 11）
* 玩家行為：Hit / Stand / Double
* 莊家自動補牌邏輯（Dealer Rules）
* 勝負判定與結算（Blackjack / Bust / Push）

遊戲邏輯與 API Controller 分離，使規則：

* 可測試
* 可維護
* 可擴充（如 Split / Insurance）

---

### 🔐 3. JWT + Email 2FA 的身分與安全設計

* 採用 **JWT（Stateless）** 作為主要驗證機制，符合前後端分離架構
* Token 中攜帶使用者識別資訊，確保每一局遊戲與玩家正確對應
* 結合 **Email 2FA 驗證流程**，提升帳戶安全性
* API 層統一驗證 Token，有效避免未授權操作遊戲資源

---

### ⚡ 4. Redis 驅動的高效即時狀態管理

* 使用 Redis 儲存進行中遊戲狀態與暫存資料
* 避免高頻操作（Hit / Stand）直接寫入資料庫
* 適合短生命週期資料（遊戲局、狀態、操作階段）
* 為未來功能預留彈性：

  * 多人遊戲
  * 排行榜
  * WebSocket 即時推播

---

### 📐 5. API 設計以「前端可預測性」為目標

後端 API 回傳結構高度一致，前端僅需依據回傳欄位即可驅動畫面：

* `status`：驅動整體遊戲流程
* `cards` / `dealer_cards`：畫面渲染
* `value`：即時計算點數顯示
* `chips`：籌碼更新與下注結果

此設計讓前端：

* 不需重寫遊戲邏輯
* 專注於 UI / UX / 動畫節奏
* 能在不修改後端的情況下優化使用者體驗

---

## 專案特色

* 前後端清楚分離，符合實務開發模式
* 遊戲邏輯集中於後端，確保公平性與可測試性
* 前端專注於使用者體驗與互動流暢度
* 架構可延伸（如：多玩家、排行榜、帳戶系統）

---

## 專案安裝與執行

### Frontend 專案安裝（Frontend）

```bash
git clone <frontend-repo-url>
cd black-jack-nextproject
npm install
npm run dev
```

* 預設執行位置：`http://localhost:3000`

---

### Backend 專案安裝（Backend）

```bash
git clone <backend-repo-url>
cd <backend-project>
python -m venv venv
source venv/bin/activate  # Windows 使用 venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

* 預設 API 啟動於：`http://localhost:8000`

---

## 🔌 前端 API 設定（Frontend）

請於前端專案根目錄新增 `.env.local`：

```env
NEXT_PUBLIC_API_BASE_URL=https://your-backend-api-url
```

此設定將作為前端呼叫後端 Blackjack API 的統一入口。

---

## 部署方式

### 前端部署

前端可部署於以下任一平台：

* **Vercel（推薦）**
* Netlify
* 任何支援 Next.js 的部署平台

部署前請確認：

* `.env` 中的 `NEXT_PUBLIC_API_BASE_URL` 已指向正確的後端 API 位置
* 後端已允許對應前端網域的 **CORS 存取**

---
協作收穫與工程實務經驗

透過本次與前端工程師的實際協作開發，本專案不僅完成遊戲功能，也讓我在後端工程實務上真實處理並落地以下議題：

CORS Domain Restriction：實際設定並驗證僅允許指定前端網域存取所有後端路由，確保 API 不被未授權來源呼叫。

前後端 API Flow 對齊：根據前端實際 UI 與動畫流程，反覆調整後端 API 設計與回傳結構，使狀態流（status / chips / cards）能穩定驅動畫面。

Environment Separation（Local / Prod）：分層管理環境變數（如 env.local、production settings），避免設定耦合，並支援本地開發與正式部署環境切換。

協作中調整後端設計：在不破壞核心遊戲邏輯的前提下，主動因應前端需求優化 API 行為與流程，而非僅被動提供介面。

這些經驗使本專案更貼近實際企業級前後端協作模式，也強化了後端在系統整合與跨端溝通中的角色。

## 專案用途

* 全端作品集展示
* Blackjack 遊戲邏輯與 API 設計實例
* 前後端協作開發範例

---

## License

This project is for learning and portfolio purposes.
