import tkinter as tk
from functools import partial
from story.script import SCENE_SCRIPT # 匯入劇本資料
from PIL import Image, ImageTk

# --- 1. Model 層: 角色類別 (由戰鬥系統負責人主要實作) ---
class Character:
    def __init__(self, name, hp, atk):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.atk = atk

    def is_alive(self):
        return self.hp > 0

    def attack(self, target):
        damage = self.atk # 簡化：不計算亂數
        target.hp -= damage
        if target.hp < 0:
            target.hp = 0
        return f"{self.name} 攻擊了 {target.name}，造成 {damage} 點傷害！"

# --- 2. Controller 層: 遊戲管理器 (修改後的主程式) ---
class GameManager:
    def __init__(self, ui):
        self.ui = ui
        self.player = Character("勇者", 100, 15)
        self.current_enemy = None
        self.game_state = "SCENE" # 初始狀態設為 SCENE (劇情/探索)
        self.script_data = SCENE_SCRIPT # 載入劇本
        self.current_scene_id = "START" # 追蹤目前場景

    # --- 核心邏輯修改 ---
    
    # 刪除：start_game (用 load_scene 取代)
    def start_game(self, *args):
        """遊戲啟動和重置點：載入起始場景。"""
        self.player.hp = self.player.max_hp # 重置 HP
        self.ui.update_status(f"HP: {self.player.hp}/{self.player.max_hp}")
        self.load_scene("START")
        
    # 新增：載入場景
    def load_scene(self, scene_id):
        self.current_scene_id = scene_id
        scene = self.script_data.get(scene_id)
        
        if not scene:
            self.ui.update_text(f"錯誤：找不到場景 ID: {scene_id}")
            self.ui.set_choices([], None)
            return

        self.game_state = "SCENE"
        self.ui.update_text(scene["text"])
        
        # 設置按鈕，所有劇情按鈕都導向 handle_scene_choice
        choices = list(scene["choices"].keys())
        self.ui.set_choices(choices, self.handle_scene_choice)

    # 刪除：handle_explore_choice (用 handle_scene_choice 取代)
    # 新增：處理劇情選項的通用函式
    def handle_scene_choice(self, choice):
        current_scene = self.script_data[self.current_scene_id]
        next_action = current_scene["choices"].get(choice)

        if not next_action:
            self.ui.append_text("無效的選項。")
            return
            
        # 處理特殊動作：戰鬥
        if next_action == "BATTLE_SLIME":
            self.enter_battle("史萊姆", 30, 5) # 進入戰鬥專屬流程
            return
        
        # 處理特殊動作：遊戲結束
        elif next_action.startswith("END"):
            self.load_scene(next_action) # 載入結束畫面 (例如 END_RUN)
            self.ui.set_choices([], None) # 清空按鈕
            return
        
        # 處理場景切換
        else:
            self.load_scene(next_action)

    # 新增：專門用於處理進入戰鬥的函式
    def enter_battle(self, enemy_name, hp, atk):
        self.game_state = "BATTLE"
        self.current_enemy = Character(enemy_name, hp, atk)
        self.ui.update_text(f"進入戰鬥！面對 {self.current_enemy.name} (HP: {self.current_enemy.hp}/{self.current_enemy.max_hp})")
        self.ui.set_choices(["攻擊", "防禦", "逃跑"], self.handle_battle_choice)

    # 戰鬥演算法設計的核心部分 (微調結束邏輯)
    def handle_battle_choice(self, action):
        # 1. 玩家行動... (不變)
        if action == "攻擊":
            message = self.player.attack(self.current_enemy)
            self.ui.append_text(message)

        # 2. 判定勝負 (玩家勝利)
        if not self.current_enemy.is_alive():
            self.ui.append_text(f"你贏了！{self.current_enemy.name} 倒下了。")
            self.game_state = "SCENE"
            # 戰勝後，跳轉到 'WIN_SLIME' 場景
            self.load_scene("WIN_SLIME") 
            return

        # 3. 敵人反擊... (不變)
        enemy_message = self.current_enemy.attack(self.player)
        self.ui.append_text(enemy_message)
        self.ui.update_status(f"HP: {self.player.hp}/{self.player.max_hp}")

        # 4. 判定玩家是否戰敗... (不變)
        if not self.player.is_alive():
            self.ui.append_text("你戰敗了！Game Over。")
            self.ui.set_choices([], None)
            return

        # 保持在戰鬥狀態... (不變)
        self.ui.set_choices(["攻擊", "防禦", "逃跑"], self.handle_battle_choice)

# --- 3. View 層: 介面類別 (由介面整合負責人主要實作) ---
# from PIL import Image, ImageTk  # 需要安裝 Pillow: pip install pillow

class GameUI:
    def __init__(self, master, game_manager):
        self.master = master
        self.game = game_manager
        self.master.title("UnderPy")
        self.master.geometry("600x500")  # 稍微加高一點

        # 狀態顯示區
        self.status_label = tk.Label(master, text="HP:", anchor="w", fg="red")
        self.status_label.pack(pady=(10, 5), padx=20, fill="x")

        # 圖片顯示區
        self.image_label = tk.Label(master)
        self.image_label.pack(pady=5)

        # 劇情文字區
        self.text_area = tk.Text(master, height=10, state='disabled')
        self.text_area.pack(pady=10, padx=20, fill="x")

        # 按鈕區 (Frame 容器)
        self.button_frame = tk.Frame(master)
        self.button_frame.pack(pady=10)

        # 儲存目前的圖片，避免被 GC 回收
        self.current_image = None

    # 更新圖片
    def update_image(self, image_path=None):
        if image_path:
            try:
                img = Image.open(image_path)
                img = img.resize((400, 200), Image.ANTIALIAS)  # 調整大小
                self.current_image = ImageTk.PhotoImage(img)
                self.image_label.config(image=self.current_image)
            except Exception as e:
                print(f"載入圖片失敗: {e}")
                self.image_label.config(image="")
        else:
            self.image_label.config(image="")


# --- 4. 程式啟動 ---
if __name__ == '__main__':
    root = tk.Tk()
    
    # 初始化 Game Manager 和 UI，並將兩者連接
    game_manager = GameManager(None) # 先傳 None，後面再傳入 UI 實例
    game_ui = GameUI(root, game_manager)
    game_manager.ui = game_ui # 建立雙向連接

    # 開始遊戲
    game_manager.start_game()
    root.mainloop() # loop untill close window
