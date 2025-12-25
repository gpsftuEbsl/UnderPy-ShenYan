# main.py
# 這裡放遊戲的主要邏輯與管理器

import tkinter as tk
from story.script import SCENE_SCRIPT
from ui.game_ui import GameUI

# --- 嘗試匯入戰鬥模組 (Pygame) ---
try:
    from battle.battle_game import boss_battle
except ImportError:
    # 如果沒有 Pygame 環境，提供一個測試用的假戰鬥
    def boss_battle(): 
        print("【測試模式】未找到 Pygame 戰鬥模組，預設勝利")
        return "WIN"

# --- Model 層: 角色類別 ---
class Character:
    def __init__(self, name, hp, atk):
        self.name, self.max_hp, self.hp, self.atk = name, hp, hp, atk
        
    def is_alive(self): 
        return self.hp > 0
        
    def attack(self, target):
        damage = self.atk
        target.hp = max(0, target.hp - damage)
        return f"{self.name} 發動攻擊，造成 {damage} 點傷害！"

# --- Controller 層: 遊戲管理器 ---
class GameManager:
    def __init__(self, ui):
        self.ui = ui
        self.player = Character("勇者", 100, 15)
        self.current_enemy = None 
        self.script_data = SCENE_SCRIPT
        self.current_scene_id = "START"
        self.known_password = None 
        
        # --- Level 3 謎題設定 ---
        # 正確順序：圓形(創世) -> 三角形(戰爭) -> 方形(毀滅)
        self.puzzle_answer = ["圓形按鈕", "三角形按鈕", "方形按鈕"]
        self.puzzle_current = []

    def start_game(self, *args):
        """ 遊戲初始化 """
        self.player.hp = self.player.max_hp
        self.ui.update_status(f"HP: {self.player.hp}/{self.player.max_hp}")
        self.load_scene("START")

    # ==========================================
    # ★★★ 核心邏輯：中央受傷與死亡系統 ★★★
    # ==========================================
    def player_take_damage(self, amount, message=None):
        """ 中央受傷系統：處理扣血、UI、特效與死亡檢查 """
        self.player.hp = max(0, self.player.hp - amount)
        self.ui.update_status(f"HP: {self.player.hp}/100")
        
        # 視覺回饋
        self.ui.shake_window()
        self.ui.flash_red()
        
        if message: 
            self.ui.type_text(message, clear=False)
            
        return self.check_death()
    
    def check_death(self):
        """ 檢查玩家是否死亡，若死亡則顯示 Game Over 並鎖定操作 """
        if not self.player.is_alive():
            self.ui.hide_input_field()
            self.ui.set_choices([], None)
            self.ui.type_text("\n【系統】你的 HP 歸零了。冒險在此終結... (Game Over)", clear=False)
            return True
        return False
    
    # ==========================================
    # ★★★ 場景載入與選項處理 ★★★
    # ==========================================
    def load_scene(self, scene_id):
        """ 加載並顯示指定場景 """
        self.current_scene_id = scene_id
        scene = self.script_data.get(scene_id)
        if not scene: return
        
        self.ui.type_text(scene["text"], clear=True)
        self.ui.update_image(scene.get("image"))
        
        if scene.get("type") == "INPUT":
            self.ui.show_input_field()
            self.ui.set_choices([], None)
        else:
            self.ui.hide_input_field()
            # 如果是謎題模式，按鈕不需要重新刷新(如果是同一場景)，但在這裡統一刷新也沒問題
            self.ui.set_choices(list(scene["choices"].keys()), self.handle_scene_choice)

    def handle_scene_choice(self, choice):
        """ 處理場景選擇按鈕點擊 """
        current_scene_data = self.script_data.get(self.current_scene_id)
        next_action = current_scene_data["choices"].get(choice)
        
        # --- 特殊判斷：Level 3 謎題模式 ---
        # 如果當前場景是 PUZZLE 且 玩家點的不是「放棄/返回」類的選項，就視為解謎操作
        if current_scene_data.get("type") == "PUZZLE" and "放棄" not in choice and "返回" not in choice:
            self.handle_order_puzzle(choice)
            return

        if not next_action: return

        # --- 1. Pygame 戰鬥觸發 (史萊姆 / Boss) ---
        if next_action == "BATTLE_SLIME" or next_action == "BOSS_BATTLE":
            self.ui.master.withdraw() # 隱藏主視窗
            res = boss_battle()       # 進入 Pygame
            self.ui.master.deiconify() # 顯示主視窗
            
            if res == "WIN":
                # 根據是誰贏了跳轉不同結局，這裡是史萊姆的例子
                self.load_scene("WIN_SLIME") 
            elif res == "LOSE":
                # 戰敗處理：直接扣光 HP 並檢查死亡
                self.ui.type_text("", clear=True)
                self.player.hp = 0
                self.ui.update_status(f"HP: 0/100")
                self.check_death() # 這會觸發 Game Over 文字

        # --- 2. 哥布林特殊劇情 ---
        elif next_action == "LEVEL_2_GOBLIN":
            # 遭遇哥布林前先扣血 (劇情殺)
            if self.player_take_damage(10, "【系統】哥布林的冷嘲熱諷刺痛了你的心！"): return
            self.load_scene(next_action)
            
        elif next_action == "START_GOBLIN_BATTLE":
            self.current_enemy = Character("吊嘎哥布林", 40, 8)
            self.ui.type_text("【系統】你忍無可忍，拔劍衝向哥布林！", clear=False)
            self.enter_goblin_combat_loop()
            
        elif next_action == "GOBLIN_SPARED":
            self.known_password = "9527"
            self.load_scene(next_action)
            
        # --- 3. 一般場景跳轉 ---
        else: 
            self.load_scene(next_action)
            
        # 每次跳轉後都檢查一次是否活著 (保險起見)
        if self.check_death(): return 

    # ==========================================
    # ★★★ Level 3: 形狀順序謎題 ★★★
    # ==========================================
    def handle_order_puzzle(self, button_name):
        self.puzzle_current.append(button_name)
        count = len(self.puzzle_current)
        
        self.ui.type_text(f"你按下了【{button_name}】... (第 {count}/3 步)", clear=False)

        # 因為只有三個正確步驟，按滿 3 次就檢查
        if count == 3:
            if self.puzzle_current == self.puzzle_answer:
                self.ui.type_text("【系統】喀嚓！機關啟動了！地板開始震動...", clear=False)
                self.puzzle_current = [] # 清空狀態
                # 延遲 1.5 秒後跳轉到成功場景
                self.ui.master.after(1500, lambda: self.load_scene("L3_UNLOCK_SUCCESS"))
            else:
                # 答錯扣血
                self.puzzle_current = [] # 重置順序
                msg = "【系統】嗶嗶！順序錯誤！機關發出了強烈的電擊！"
                if self.player_take_damage(10, msg):
                    return
                self.ui.type_text("\n(順序已重置，請重新開始。)", clear=False)

    # ==========================================
    # ★★★ Level 2: 哥布林戰鬥迴圈 ★★★
    # ==========================================
    def enter_goblin_combat_loop(self):
        """ 進入哥布林戰鬥迴圈，顯示戰鬥按鈕 """
        self.ui.set_choices(["攻擊", "防禦"], self.handle_goblin_combat)

    def handle_goblin_combat(self, action):
        """ 處理哥布林戰鬥選擇 """
        logs = []
        if action == "攻擊":
            logs.append(self.player.attack(self.current_enemy))
            if not self.current_enemy.is_alive():
                self.ui.type_text("\n".join(logs), clear=False)
                self.load_scene("GOBLIN_DEFEATED"); return
            
            # 哥布林反擊
            dmg = self.current_enemy.atk
            self.player.hp = max(0, self.player.hp - dmg)
            logs.append(f"【系統】{self.current_enemy.name} 反擊，造成 {dmg} 點傷害！")
            
            # 統一輸出訊息
            self.ui.type_text("\n".join(logs), clear=False)
            self.ui.update_status(f"HP: {self.player.hp}/100")
            self.ui.shake_window(); self.ui.flash_red()
        else: # 防禦
            self.player.hp = max(0, self.player.hp - 2)
            self.ui.type_text("【系統】你摀住耳朵，傷害減輕至 2 點。", clear=False)
            self.ui.update_status(f"HP: {self.player.hp}/100")
            self.ui.shake_window()

        if self.check_death(): return
        self.enter_goblin_combat_loop() # 繼續下一回合

    # ==========================================
    # ★★★ Level 2: 密碼輸入處理 ★★★
    # ==========================================
    def handle_password_input(self, val):
        """ 處理密碼輸入框的提交 """
        msgs = [f"你輸入了：{(val if val else '啥都沒有')}"]
        
        if val == "9527":
            msgs.append("【系統】密碼正確！大門緩緩打開...")
            self.ui.type_text("\n".join(msgs), clear=False)
            self.ui.hide_input_field()
            self.ui.master.after(1500, lambda: self.load_scene("LEVEL_3_START"))
        else:
            if self.player_take_damage(5): return
            msgs.append("【系統】密碼錯誤！大門發出尖銳嘲笑聲。")
            msgs.append(f"提示：密碼似乎是 {self.known_password}" if self.known_password else "提示：你不知道密碼。")
            self.ui.type_text("\n".join(msgs), clear=False)

if __name__ == '__main__':
    root = tk.Tk()
    mgr = GameManager(None)
    ui = GameUI(root, mgr)
    mgr.ui = ui
    mgr.start_game()
    root.mainloop()