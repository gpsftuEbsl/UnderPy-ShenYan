# main.py
# 這裡放遊戲的主要邏輯與管理器
# GameManager類別中重要的函數如下:
# 1. handle_goblin_combat: 處理哥布林戰鬥選擇
# 2. enter_goblin_combat_loop: 進入哥布林戰鬥迴圈
# 3. handle_password_input: 處理密碼輸入框的提交
# 4. load_scene: 加載並顯示指定場景
# 5. handle_scene_choice: 處理場景選擇按鈕點擊
# 6. player_take_damage: 中央受傷系統
# 7. check_death: 檢查玩家是否死亡 etc.

import tkinter as tk
from story.script import SCENE_SCRIPT
from ui.game_ui import GameUI

try:
    from battle.battle_game import boss_battle
except ImportError:
    def boss_battle(): return "WIN"

class Character:
    def __init__(self, name, hp, atk):
        self.name, self.max_hp, self.hp, self.atk = name, hp, hp, atk
    def is_alive(self): return self.hp > 0
    def attack(self, target):
        damage = self.atk
        target.hp = max(0, target.hp - damage)
        return f"{self.name} 發動攻擊，造成 {damage} 點傷害！"

class GameManager:
    def __init__(self, ui):
        self.ui, self.player = ui, Character("勇者", 100, 15)
        self.script_data, self.current_scene_id = SCENE_SCRIPT, "START"
        self.known_password = None 

    def start_game(self, *args):
        self.player.hp = self.player.max_hp
        self.ui.update_status(f"HP: {self.player.hp}/{self.player.max_hp}")
        self.load_scene("START")

    def player_take_damage(self, amount, message=None):
        """ 中央受傷系統：處理扣血、UI、特效與死亡檢查 """
        self.player.hp = max(0, self.player.hp - amount)
        self.ui.update_status(f"HP: {self.player.hp}/100")
        self.ui.shake_window()
        self.ui.flash_red()
        if message: self.ui.type_text(message, clear=False)
        return self.check_death()
    
    def check_death(self):
        """ 檢查玩家是否死亡，若死亡則顯示 Game Over 訊息並結束遊戲 """
        if not self.player.is_alive():
            self.ui.hide_input_field()
            self.ui.set_choices([], None)
            self.ui.type_text("\n【系統】你的 HP 歸零了。冒險在此終結... (Game Over)", clear=False)
            return True
        return False
    
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
            self.ui.set_choices(list(scene["choices"].keys()), self.handle_scene_choice)

    def handle_scene_choice(self, choice):
        """ 處理場景選擇按鈕點擊 """
        next_action = self.script_data[self.current_scene_id]["choices"].get(choice)
        if not next_action: return

        if next_action == "BATTLE_SLIME":
            self.ui.master.withdraw()
            res = boss_battle(); self.ui.master.deiconify()
            # TODO: 可改進 對戰後HP不會歸零 或 無法顯示對戰失敗訊息 的問題
            if res == "WIN":
                self.load_scene("WIN_SLIME")
            elif res == "LOSE":
                self.ui.type_text("", clear=True) # 清空打字機緩存
                self.player.hp = 0
                self.ui.update_status(f"HP: {self.player.hp}/100") # 更新狀態列
                # self.load_scene("END_LOSE") # 捨棄 # FIX：劇本結局不包括死亡 死亡後直接結束遊戲
                # self.load_scene("WIN_SLIME" if res == "WIN" else "END_LOSE") 改成以上
        elif next_action == "LEVEL_2_GOBLIN":
            if self.player_take_damage(10, "【系統】哥布林的冷嘲熱諷刺痛了你的心！"): return
            self.load_scene(next_action)
        elif next_action == "START_GOBLIN_BATTLE":
            self.current_enemy = Character("吊嘎哥布林", 40, 8)
            self.ui.type_text("【系統】你忍無可忍，拔劍衝向哥布林！", clear=False)
            self.enter_goblin_combat_loop()
        elif next_action == "GOBLIN_SPARED":
            self.known_password = "9527"; self.load_scene(next_action)
        else: self.load_scene(next_action)
        if self.check_death(): return # 死亡檢查

    def enter_goblin_combat_loop(self):
        """ 進入哥布林戰鬥迴圈 """
        self.ui.set_choices(["攻擊", "防禦"], self.handle_goblin_combat) # 呼叫戰鬥選擇處理函式

    def handle_goblin_combat(self, action):
        """ 處理哥布林戰鬥選擇 """
        logs = []
        if action == "攻擊":
            logs.append(self.player.attack(self.current_enemy))
            if not self.current_enemy.is_alive():
                self.ui.type_text("\n".join(logs), clear=False)
                self.load_scene("GOBLIN_DEFEATED"); return
            
            dmg = self.current_enemy.atk
            self.player.hp = max(0, self.player.hp - dmg)
            logs.append(f"【系統】{self.current_enemy.name} 反擊，造成 {dmg} 點傷害！")
            self.ui.type_text("\n".join(logs), clear=False)
            self.ui.update_status(f"HP: {self.player.hp}/100")
            self.ui.shake_window(); self.ui.flash_red()
        else: # 防禦
            self.player.hp = max(0, self.player.hp - 2)
            self.ui.type_text("【系統】你摀住耳朵，傷害減輕至 2 點。", clear=False)
            self.ui.update_status(f"HP: {self.player.hp}/100")
            self.ui.shake_window()

        if self.check_death(): return
        self.enter_goblin_combat_loop() # 呼叫下一輪戰鬥

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
    root = tk.Tk(); mgr = GameManager(None); ui = GameUI(root, mgr)
    mgr.ui = ui; mgr.start_game(); root.mainloop()
