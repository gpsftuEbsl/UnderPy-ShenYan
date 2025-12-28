# main.py
# 遊戲主程式與邏輯管理

import tkinter as tk
from story.script import SCENE_SCRIPT
from ui.game_ui import GameUI

# --- 嘗試匯入戰鬥模組 (包含 Final Boss) ---
try:
    from battle.battle_game import boss_battle, final_boss_battle # 沒裝 pygame 可能會直接閃退
except ImportError:
    def boss_battle(): 
        print("【測試模式】未找到 Pygame，預設勝利")
        return "WIN"
    def final_boss_battle():
        print("【測試模式】未找到 Pygame (Final Boss)，預設勝利")
        return "WIN"

# --- 角色類別 ---
class Character:
    """
    Character 的 Docstring

    代表遊戲中的一個角色 (玩家或敵人)
    """
    def __init__(self, name, hp, atk):
        # 實體變數
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.atk = atk # 攻擊力
        
    def is_alive(self): 
        # 只要血量大於 0 就是活著
        return self.hp > 0
        
    def attack(self, target):
        """
        執行攻擊動作\n
        :param self: 攻擊者 (Character 物件)
        :param target: 被攻擊的目標 (Character 物件)
        """
        damage = self.atk
        # 扣血邏輯
        target.hp = target.hp - damage

        # 防止血量變成負數
        if target.hp < 0:
            target.hp = 0
            
        return f"{self.name} 發動攻擊，造成 {damage} 點傷害！"

# --- 遊戲管理器 ---
class GameManager:
    """
    遊戲邏輯管理器 (GameManager)
    
    負責處理所有劇情跳轉、數值計算、解謎邏輯與戰鬥流程，
    並根據邏輯判斷控制 UI 做出對應的變化。

    :param ui: 遊戲介面實例 (GameUI 類別的物件)
    """
    def __init__(self, ui):
        self.ui = ui
        self.player = Character("勇者", 100, 15)
        self.current_enemy = None # Character 物件
        self.script_data = SCENE_SCRIPT
        self.current_scene_id = "START"
        self.known_password = None # 玩家是否知道密碼 在後面開門時判斷邏輯(提示時)會用到
        
        # --- Level 3 解謎設定 ---
        self.puzzle_answer = ["◯", "△", "█"]
        self.puzzle_current = []

    def start_game(self):
        """
        遊戲剛開始的初始化
        
        從這裡開始載入第一個場景

        參數：無
        """
        self.player.hp = self.player.max_hp
        self.ui.update_status(f"HP: {self.player.hp}/{self.player.max_hp}")
        self.load_scene("START")

    def player_take_damage(self, amount, message=None):
        """
        核心：受傷與死亡判斷+呼叫ui特效
        傳回值：如果死亡回傳 True，沒死回傳 False
        參數：
        - amount: 受傷數值
        - message: 受傷後要顯示的訊息(可選)(使用: .ui.type_text(message, clear=False))
        """
        self.player.hp = self.player.hp - amount
        
        # 檢查不要讓血量變負的
        if self.player.hp < 0:
            self.player.hp = 0
            
        self.ui.update_status(f"HP: {self.player.hp}/100")
        
        # 畫面震動跟閃紅特效
        self.ui.shake_window()
        self.ui.flash_red()
        
        if message: # 如果player_take_damage的同時有傳訊息就顯示
            self.ui.type_text(message, clear=False)
            
        return self.check_death()
    
    def check_death(self):
        """萬用死亡檢查"""
        # 這裡直接寫 == False 邏輯感覺比較順
        if self.player.is_alive() == False:
            self.ui.hide_input_field()
            # 傳空陣列把按鈕清空，讓玩家不能亂按
            self.ui.set_choices([], None)
            self.ui.type_text("\n【系統】你的 HP 歸零了。冒險在此終結... (Game Over)", clear=False)
            # 在這裡可以直接載入失敗場景，避免卡在原地
            self.load_scene("END_LOSE") 
            return True
        return False
    
    def load_scene(self, scene_id):
        """
        載入場景資料並更新 UI

        (包含輸入框圖片與選項)

        :param scene_id: 場景 ID 字串
        """
        self.current_scene_id = scene_id # 將實體變數設定為傳入的 scene_id
        
        scene = self.script_data.get(scene_id) # 從劇本字典抓資料
        if scene is None:
            return
        
        self.ui.type_text(scene["text"], clear=True)
        self.ui.update_image(scene.get("image"))
        
        # 判斷是不是要顯示輸入框
        if scene.get("type") == "INPUT": # 如果是輸入框場景
            self.ui.show_input_field()
            self.ui.set_choices([], None) # 清空按鈕
        else:
            self.ui.hide_input_field()
            # 先把 keys 轉成 list 存起來，不然有時候傳進去會報錯，這樣也比較好 debug
            choices_list = list(scene["choices"].keys())
            self.ui.set_choices(choices_list, self.handle_scene_choice) # 傳入ui的按鈕處理函式

    def handle_scene_choice(self, choice):
        """
        按鈕被點擊時會執行這裡，一些特殊邏輯也會在這裡處理
        
        :param self: GameManager 物件
        :param choice: 玩家選擇的選項文字
        """
        current_scene_data = self.script_data.get(self.current_scene_id) # 找出劇情字典id
        
        # 找出choice裡面的下一個場景的id
        next_action = current_scene_data["choices"].get(choice)
        
        # --- Level 3 謎題特殊判斷 ---
        scene_type = current_scene_data.get("type")
        if scene_type == "PUZZLE":
            # 只要不是點放棄或返回，就當作是在解謎按按鈕
            if "放棄" not in choice and "返回" not in choice:
                self.handle_order_puzzle(choice)
                return

        if next_action is None:
            return

        # --- 1. 進入 Pygame 戰鬥 (第一關史萊姆) ---
        if next_action == "BATTLE_SLIME":
            self.ui.master.withdraw() # 先藏起來主視窗
            res = boss_battle()       # 跑 Pygame
            self.ui.master.deiconify() # 戰鬥完再顯示回來
            
            if res == "WIN":
                self.load_scene("WIN_SLIME") 
            elif res == "LOSE":
                self.load_scene("END_LOSE") # 統一導向失敗結局

        # --- 2. 進入 Pygame 戰鬥 (最終 Boss) ---
        elif next_action == "BOSS_BATTLE":
            self.ui.master.withdraw() 
            res = final_boss_battle() # 呼叫最終 Boss 戰
            self.ui.master.deiconify() 
            
            if res == "WIN":
                self.load_scene("BOSS_WIN")
            elif res == "LOSE":
                self.load_scene("END_LOSE")

        # --- 3. 哥布林劇情扣血 ---
        elif next_action == "LEVEL_2_GOBLIN":
            # 這裡劇情殺先扣個血
            is_dead = self.player_take_damage(10, "【系統】哥布林的冷嘲熱諷刺痛了你的心！")
            if is_dead == False:
                self.load_scene(next_action)
            
        elif next_action == "START_GOBLIN_BATTLE":
            self.current_enemy = Character("吊嘎哥布林", 45, 8)
            self.ui.type_text("【系統】你忍無可忍，拔劍衝向哥布林！", clear=False)
            self.enter_goblin_combat_loop()
            
        elif next_action == "GOBLIN_SPARED":
            self.known_password = "9527"
            self.load_scene(next_action)
            
        # --- 4. 普通場景切換 ---
        else: 
            self.load_scene(next_action)
            
        self.check_death()

    # ==========================================
    #  Level 3: 解謎邏輯 TODO: 之後可以重新命名同level的函式 或做成類別 (目前code還沒有很長所以先不做)
    # ==========================================
    
    # 因為 after 不能直接塞有參數的函式，所以寫一個獨立的函式來呼叫(可以用 lambda 但先這樣寫)
    def _delayed_puzzle_success(self):
        self.load_scene("L3_UNLOCK_SUCCESS")

    def handle_order_puzzle(self, button_name):
        self.puzzle_current.append(button_name)
        count = len(self.puzzle_current)
        
        self.ui.type_text(f"你按下了【{button_name}】... (第 {count}/3 步)", clear=False)

        if count == 3:
            if self.puzzle_current == self.puzzle_answer:
                self.ui.type_text("【系統】喀嚓！機關啟動了！地板開始震動...", clear=False)
                self.puzzle_current = [] 
                
                # 延遲一下再切換場景
                self.ui.master.after(1500, self._delayed_puzzle_success)
            else:
                self.puzzle_current = []
                msg = "【系統】嗶嗶！順序錯誤！機關發出了強烈的電擊！"
                # 懲罰扣血
                is_dead = self.player_take_damage(45, msg)
                if is_dead == False:
                    self.ui.type_text("\n可惡失敗了...\n失敗為成功之母，再逝逝好了", clear=False)

    # ==========================================
    #  Level 2: 哥布林戰鬥迴圈 TODO: 之後可以重新命名同level的函式 或做成類別
    # ==========================================
    def enter_goblin_combat_loop(self):
        self.ui.set_choices(["攻擊", "防禦"], self.handle_goblin_combat)

    def handle_goblin_combat(self, action):
        logs = []
        if action == "攻擊":
            msg = self.player.attack(self.current_enemy)
            logs.append(msg)
            
            if self.current_enemy.is_alive() == False:
                self.ui.type_text("\n".join(logs), clear=False)
                self.load_scene("GOBLIN_DEFEATED")
                return
            
            # 敵人反擊
            dmg = self.current_enemy.atk
            self.player.hp = self.player.hp - dmg
            if self.player.hp < 0:
                self.player.hp = 0
                
            logs.append(f"【系統】{self.current_enemy.name} 反擊，造成 {dmg} 點傷害！")
            
            self.ui.type_text("\n".join(logs), clear=False)
            self.ui.update_status(f"HP: {self.player.hp}/100")
            self.ui.shake_window()
            self.ui.flash_red()
        else: 
            # 防禦
            self.player.hp = self.player.hp - 2
            if self.player.hp < 0:
                self.player.hp = 0
                
            self.ui.type_text("【系統】你摀住耳朵，傷害減輕至 2 點。", clear=False)
            self.ui.update_status(f"HP: {self.player.hp}/100")
            self.ui.shake_window()

        if self.check_death(): return
        self.enter_goblin_combat_loop()

    # ==========================================
    #  Level 2: 密碼輸入 TODO: 之後可以重新命名同level的函式 或做成類別
    # ==========================================
    
    # 這個也是為了 after 寫的延遲函式
    def _delayed_level_3_start(self):
        self.load_scene("LEVEL_3_START")

    def handle_password_input(self, val):
        msgs = []
        if val:
            msgs.append(f"你輸入了：{val}")
        else:
            msgs.append("你輸入了：啥都沒有")
        
        if val == "9527":
            msgs.append("【系統】密碼正確！大門緩緩打開...")
            self.ui.type_text("\n".join(msgs), clear=False)
            self.ui.hide_input_field()
            
            # 用after方法延遲跳轉
            self.ui.master.after(1500, self._delayed_level_3_start)
        else:
            if self.player_take_damage(5): return
            msgs.append("【系統】密碼錯誤！大門發出尖銳嘲笑聲。")
            
            # 這裡用一般的 if else 比較好讀
            if self.known_password:
                msgs.append(f"提示：密碼似乎是 {self.known_password}")
            else:
                msgs.append("提示：你不知道密碼。")
                
            self.ui.type_text("\n".join(msgs), clear=False)

if __name__ == '__main__':
    root = tk.Tk()
    mgr = GameManager(None) # 先建立 GameManager 物件，並傳 None，避免循環引用
    ui = GameUI(root, mgr) # 再建立 UI 物件
    mgr.ui = ui # 把 UI 傳回給管理器
    mgr.start_game()
    root.mainloop() # 啟動 Tkinter 主迴圈 隨時待使用者互動