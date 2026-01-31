# 🏰 UnderPy - 雙引擎職場逃脫 RPG (Office Escape RPG)

> **結合 MUD 文字冒險的深度與 彈幕射擊(Bullet Hell) 的刺激，一款以 Python 打造的黑色幽默職場題材 RPG。**

![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green) ![Pygame](https://img.shields.io/badge/Engine-Pygame-red) ![Status](https://img.shields.io/badge/Status-Release-orange)

## 📖 專案簡介 (Introduction)
**UnderPy** 是一個採用 **「雙引擎架構 (Dual-Engine Architecture)」** 開發的 RPG 遊戲。
遊戲本體採用 **Tkinter** 構建經典的文字冒險介面，強調劇本敘事與解謎；而當遭遇強敵時，系統將無縫切換至 **Pygame** 引擎，進入即時動作戰鬥模式。

玩家將化身為一名試圖逃離公司的勇者，在不負責的菜鳥實習生、油膩主管與遺留代碼的辦公迷宮中探索。從破解終端機謎題到穿越伺服器機房，你必須打破無限加班的輪迴，尋找「刪除世界」的終極真相。

## ✨ 核心特色 (Key Features)

### 🎮 遊戲體驗
* **多重結局系統**：包含普通結局、死亡結局與二周目隱藏的「真結局 (True Ending)」。
* **混合戰鬥模式**：
    * 一般戰鬥：策略回合制 (文字描述)。
    * BOSS 戰鬥：Undertale 風格的彈幕閃避 (Pygame)。
* **沉浸式敘事**：實作打字機文字特效與動態震動回饋。
* **完整存檔機制**：支援 JSON 進度保存，重啟遊戲後可延續冒險。

### 🛠️ 技術亮點 (Technical Highlights)
本專案在技術實作上解決了多項 GUI 開發難題：
1.  **異質視窗整合 (Integration)**：實現 Tkinter 主視窗與 Pygame 戰鬥視窗的無縫切換與控制權轉移。
2.  **資料驅動架構 (Data-Driven)**：將劇本邏輯與程式碼分離，透過 `Dictionary` 結構管理龐大的對話與選項。
3.  **非阻塞式延遲 (Non-blocking Delay)**：捨棄 `time.sleep`，全面採用 `root.after` 搭配 `Recursion` 實作動畫，確保介面永不卡死。
4.  **穩健的架構設計**：採用 `GameManager` (邏輯) 與 `GameUI` (顯示) 分離的設計模式，並解決了 Python 常見的循環引用 (Circular Dependency) 問題。

## 📂 專案結構 (Project Structure)

```text
UnderPy/
├── main.py              # 遊戲入口與核心管理器 (GameManager)
├── config.py            # 集中式配置檔案 (遊戲參數、UI設定、戰鬥數值)
├── requirements.txt     # 依賴套件列表
├── story/
│   └── script.py        # 劇本資料庫 (所有對話與場景設定)
├── ui/
│   └── game_ui.py       # Tkinter 介面封裝 (負責繪圖與特效)
├── battle/
│   └── battle_game.py   # Pygame 戰鬥系統 (Boss 戰邏輯)
├── assets/              # 遊戲素材 (圖片/音效)
│   └── images/
└── savefile.json        # 自動生成的存檔紀錄
```

## 🔧 安裝與執行 (Installation & Running)

### 環境需求
- Python 3.8+
- Tkinter (通常已包含在 Python)
- Pygame 2.1+
- Pillow 9.0+

### 快速開始
```bash
# 安裝依賴
pip install -r requirements.txt

# 執行遊戲
python main.py
```

## 📝 更新日誌 (Changelog)

### [v1.1.0] - 2026年2月1日 (Error Handling & Config Refactor)

#### ✨ 新增功能
- 📋 **集中式配置系統 (config.py)**：所有遊戲參數、UI 色彩、戰鬥數值統一管理
- 🛡️ **統一錯誤處理**：全面改進異常捕獲與使用者友善的錯誤訊息

#### 🔧 改進內容

**main.py - JSON 存檔系統**
- ✅ `check_global_status()`：具體異常捕獲 (JSONDecodeError, IOError)
- ✅ `save_game()`：區分磁碟空間錯誤，提供可操作提示
- ✅ `load_game()`：三層驗證 (檔案 → 格式 → 資料完整性)
- ✅ `delete_all_save()`：捕獲 OSError 提示檔案權限問題

**ui/game_ui.py - 圖片載入**
- ✅ `update_image()`：先驗證檔案存在再打開，缺失圖片靜默降級

**battle/battle_game.py - Pygame 初始化**
- ✅ 新增 `init_pygame()` 統一初始化函數
- ✅ 戰鬥失敗返回 ERROR 信號而非崩潰

#### 🎯 場景命名優化 (v1.0.5)
- 移除舊 RPG 通用名稱 (SLIME, GOBLIN 等)
- 使用職場逃脫主題命名：
  - `INTERN_CRISIS` - 實習生危機
  - `MANAGER_ENCOUNTER` - 主管對話
  - `SERVER_ROOM_START` - 伺服器室
  - `LEGACY_CODE_AREA` - 遺留代碼區域
  - `TERMINAL_PUZZLE` - 終端機謎題

#### 💾 技術改進
- 配置參數集中管理（消除魔法數字）
- 異常分類清晰（FileNotFoundError, JSONDecodeError, IOError, OSError）
- 使用者訊息統一格式與親和度

### [v1.0.0] - 初始版本
- 雙引擎架構完成
- Tkinter 敘事 + Pygame 戰鬥系統
- 多重結局與存檔機制
