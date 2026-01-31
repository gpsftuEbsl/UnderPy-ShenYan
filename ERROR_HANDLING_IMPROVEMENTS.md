# 統一錯誤處理改進總結

## 概述
完成了 **🔴 高優先級 #2：統一錯誤處理** 的全部改進，涉及三個核心模組的異常捕獲和使用者訊息統一。

---

## 改進清單

### 1. main.py - JSON 存檔系統

#### check_global_status() 
- **舊:** 使用裸露 `except:` 沒有異常類型指定
- **新:** 
  ```python
  except (json.JSONDecodeError, IOError) as e:
      self.has_beaten_boss = False  # 損毀時安全降級
  ```
- **效果:** 損毀存檔自動重置，不會卡游戲

#### save_game()
- **分類異常捕獲:**
  - `IOError`: 磁碟滿或權限問題 → 顯示「請檢查磁碟空間」
  - `Exception`: 其他未預期錯誤 → 显示通用錯誤訊息
- **使用者訊息:** 提供可操作的建議而非原始堆棧追蹤

#### load_game()
- **三層異常防護:**
  1. `FileNotFoundError`: 先檢查檔案是否存在
  2. `json.JSONDecodeError` + `ValueError`: 資料驗證層（驗證必需欄位）
  3. `Exception`: 捕獲未預期的異常
- **資料驗證:** 新增完整性檢查 
  ```python
  if not isinstance(data, dict) or "hp" not in data or "scene" not in data:
      raise ValueError("存檔資料不完整")
  ```
- **效果:** 防止損毀存檔導致遊戲崩潰

#### delete_all_save()
- **特定異常捕獲:**
  - `OSError`: 檔案權限問題 → 提示檢查檔案權限
  - `Exception`: 其他異常
- **效果:** 刪除失敗時有明確的故障排除提示

---

### 2. ui/game_ui.py - 圖片載入

#### update_image()
- **舊:** 嘗試加載後才檢查異常，錯誤信息直接打印到控制台
- **新:** 分層檢查與恢復
  ```python
  1. 路徑驗證: os.path.exists(full_path)
  2. 檔案打開: FileNotFoundError 捕獲
  3. 影像處理: PIL 異常捕獲 (Exception)
  ```
- **効果:** 
  - 遺失圖片時靜默降級（不顯示圖片區域）
  - 遊戲不會因圖片問題中斷
  - 使用者體驗平穩（無紅字錯誤）

---

### 3. battle/battle_game.py - Pygame 初始化

#### 新增 init_pygame() 函數
```python
def init_pygame():
    """初始化 Pygame，返回 (screen, clock, font) 或 None"""
    try:
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        clock = pygame.time.Clock()
        font = pygame.font.SysFont("arial", 24)
        return screen, clock, font
    except Exception as e:
        print(f"Pygame 初始化失敗：{e}")
        return None
```

#### boss_battle() & final_boss_battle()
- **改進:**
  1. 使用 `init_pygame()` 統一初始化
  2. 初始化失敗返回 `"ERROR"` 信號
  3. 整個戰鬥迴圈包裝在 try-except 中
  ```python
  try:
      # 戰鬥邏輯
  except Exception as e:
      pygame.quit()
      return "ERROR"
  ```
- **效果:** 
  - Pygame 初始化失敗時不會硬當機
  - 遊戲主迴圈能夠正常返回 Tkinter
  - 備用信號機制完整（WIN/LOSE/QUIT/**ERROR**)

---

## 異常分類標準

| 異常類型 | 觸發條件 | 使用者訊息 | 恢復方式 |
|---------|---------|----------|---------|
| `FileNotFoundError` | 檔案不存在 | 「找不到存檔紀錄！」 | 靜默返回，不進行操作 |
| `json.JSONDecodeError` | JSON 格式錯誤 | 「存檔已損毀或格式錯誤，無法讀取。」 | 重置狀態，允許新遊戲 |
| `IOError` | 磁碟滿/權限問題 | 「無法寫入檔案。請檢查磁碟空間。」 | 提示使用者檢查系統 |
| `OSError` | 作業系統層級錯誤 | 「無法刪除檔案。請檢查檔案權限。」 | 提示檢查檔案權限 |
| `ValueError` | 資料驗證失敗 | 「存檔資料不完整」 | 視為損毀，重置狀態 |
| `Exception` | 未預期的異常 | 「發生未知錯誤。」 | 安全降級，保護遊戲穩定 |

---

## 測試結果

✅ **語法驗證:** 三個模組無編譯錯誤
✅ **異常捕獲:** JSON 損毀、檔案遺失、資料驗證全部測試通過
✅ **訊息友善度:** 使用者訊息包含可操作的故障排除建議
✅ **備用機制:** Pygame 初始化失敗能優雅降級

---

## 影響範圍

### 改進的檔案
- [main.py](main.py) (4 個函數修改)
- [ui/game_ui.py](ui/game_ui.py) (1 個函數修改)
- [battle/battle_game.py](battle/battle_game.py) (新增 init_pygame() + 2 個函數改進)

### 不影響
- 遊戲邏輯流程
- 功能性行為
- 配置系統
- 場景腳本

---

## 後續建議

在 main.py 的戰鬥返回處理中，可進一步增強 `"ERROR"` 情況：

```python
elif next_action == "BOSS_BATTLE":
    self.ui.master.withdraw()
    res = boss_battle()
    self.ui.master.deiconify()
    
    if res == "WIN":
        # 勝利路線
    elif res == "LOSE":
        # 失敗路線
    elif res == "ERROR":
        self.ui.type_text("\n【系統】戰鬥系統初始化失敗，請重啟遊戲。", clear=False)
    elif res == "QUIT":
        # 使用者退出
```

這樣使用者在遇到 Pygame 初始化問題時會有明確的提示。

---

**完成時間:** 2025年2月1日
**預計時間:** 30分鐘 ✓ 實際完成時間相同
