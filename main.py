import tkinter as tk
from functools import partial

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

# --- 2. Controller 層: 遊戲管理器 (由場景與流程負責人主要實作) ---
class GameManager:
    def __init__(self, ui):
        self.ui = ui
        self.player = Character("勇者", 100, 15)
        self.current_enemy = None
        self.game_state = "EXPLORE" # 遊戲狀態：探索 / 戰鬥

    def start_game(self):
        self.ui.update_status(f"HP: {self.player.hp}/{self.player.max_hp}")
        self.ui.update_text("你進入了一個地下城。前方出現一隻史萊姆！")
        self.current_enemy = Character("史萊姆", 30, 5)
        self.game_state = "EXPLORE"
        # 設定探索時的按鈕選項，點擊後呼叫 handle_explore_choice
        self.ui.set_choices(["調查", "戰鬥", "逃跑"], self.handle_explore_choice)

    def handle_explore_choice(self, choice):
        if choice == "戰鬥":
            self.game_state = "BATTLE"
            self.ui.update_text(f"進入戰鬥！面對 {self.current_enemy.name} (HP: {self.current_enemy.hp})")
            self.ui.set_choices(["攻擊", "防禦", "逃跑"], self.handle_battle_choice)
        elif choice == "調查":
            self.ui.update_text("史萊姆看起來很飢餓。")
        elif choice == "逃跑":
             self.ui.update_text("你逃跑了！遊戲結束。")
             self.ui.set_choices([], None)
             
    # 戰鬥演算法設計的核心部分
    def handle_battle_choice(self, action):
        # 1. 玩家行動
        if action == "攻擊":
            message = self.player.attack(self.current_enemy)
            self.ui.append_text(message)

        # 2. 判定勝負
        if not self.current_enemy.is_alive():
            self.ui.append_text("你贏了！史萊姆倒下了。")
            self.game_state = "EXPLORE"
            self.ui.set_choices(["繼續探索"], self.start_game)
            return

        # 3. 敵人反擊
        enemy_message = self.current_enemy.attack(self.player)
        self.ui.append_text(enemy_message)
        self.ui.update_status(f"HP: {self.player.hp}/{self.player.max_hp}")

        # 4. 判定玩家是否戰敗
        if not self.player.is_alive():
            self.ui.append_text("你戰敗了！Game Over。")
            self.ui.set_choices([], None)
            return

        # 保持在戰鬥狀態，等待下一次輸入
        self.ui.set_choices(["攻擊", "防禦", "逃跑"], self.handle_battle_choice)


# --- 3. View 層: 介面類別 (由介面整合負責人主要實作) ---
class GameUI:
    def __init__(self, master, game_manager):
        self.master = master
        self.game = game_manager
        self.master.title("UnderPy 雛形")
        self.master.geometry("600x400")
        
        # 狀態顯示區
        self.status_label = tk.Label(master, text="HP:", anchor="w", fg="red")
        self.status_label.pack(pady=(10, 5), padx=20, fill="x")

        # 劇情文字區
        self.text_area = tk.Text(master, height=10, state='disabled')
        self.text_area.pack(pady=10, padx=20, fill="x")

        # 按鈕區 (Frame 容器)
        self.button_frame = tk.Frame(master)
        self.button_frame.pack(pady=10)

    # UI 方法：更新狀態欄文字
    def update_status(self, text):
        self.status_label.config(text=text)

    # UI 方法：更新劇情文字
    def update_text(self, text):
        self.text_area.config(state='normal')
        self.text_area.delete('1.0', tk.END)
        self.text_area.insert(tk.END, text + "\n")
        self.text_area.config(state='disabled')
    
    # UI 方法：附加劇情文字
    def append_text(self, text):
        self.text_area.config(state='normal')
        self.text_area.insert(tk.END, text + "\n")
        self.text_area.see(tk.END) # 滾動到底部
        self.text_area.config(state='disabled')

    # UI 方法：動態生成按鈕 (這是分工整合的關鍵)
    def set_choices(self, choices, handler_function):
        # 清除舊按鈕
        for widget in self.button_frame.winfo_children():
            widget.destroy()

        # 生成新按鈕
        for choice in choices:
            # 使用 partial 函式將 choice 作為參數傳遞給 handler_function
            command = partial(handler_function, choice)
            btn = tk.Button(self.button_frame, text=choice, command=command, width=15)
            btn.pack(side="left", padx=10)


# --- 4. 程式啟動 ---
if __name__ == '__main__':
    root = tk.Tk()
    
    # 初始化 Game Manager 和 UI，並將兩者連接
    game_manager = GameManager(None) # 先傳 None，後面再傳入 UI 實例
    game_ui = GameUI(root, game_manager)
    game_manager.ui = game_ui # 建立雙向連接

    # 開始遊戲
    game_manager.start_game()
    root.mainloop()