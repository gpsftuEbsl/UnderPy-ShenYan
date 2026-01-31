# story/script.py
# 沈硯版：社畜的逃脫

SCENE_SCRIPT = {
    # ==========================================
    # 第一層：實習生 Kevin
    # ==========================================
    "START": {
        "text": """妳叫沈硯，是一個平凡的科技業社畜。
妳沒有新鮮的肝，也沒有改變世界的熱情。
在這個充滿 Bug 的世界裡，
妳唯一的目標，就是安穩地活到退休。

. . .     
. . .     

【週一 09:00 AM】
沈硯在辦公桌前醒來，頭痛欲裂。
「我為什麼還在這裡？昨天不是加班到三點嗎？」
妳揉了揉太陽穴，準備去茶水間倒咖啡。
突然，一團看起來很迷茫的生物擋住了去路。
那是... 新來的實習生 Kevin！""",
        
        "choices": {
            "查看他的問題 (調查)": "SLIME_INFO",
            "叫他讓開 (戰鬥)": "BATTLE_SLIME",
            "裝作沒看到 (逃跑)": "END_RUN",
            "檢查備份 (讀取)": "LOAD_GAME"
            # [DEBUG] 按鈕已移除
        },
        "image": "assets/images/office_cubicle.png",
        "type": "NORMAL"
    },

    # --- 二周目輪迴開場 ---
    "START_LOOP": {
        "text": """妳叫沈硯，是一個已經看穿體制的科技業前社畜。
經過多年的努力，妳失去了新鮮的肝，
得到了孱弱的椎間盤，還有偶爾來訪的坐骨神經痛。
萬幸的是，妳也準備好了充分的資金，
現在妳唯一的目標，就是打破這無限輪迴。

. . .     
. . .     

妳又在辦公桌前醒來。
空氣中瀰漫著熟悉的過期咖啡味。
妳的直覺告訴妳，妳已經「離職」過一次了。

前方...還是那個無知的實習生。
這次，也許能徹底打破這個加班輪迴？""",
        
        "choices": {
            "查看他的問題 (調查)": "SLIME_INFO",
            "叫他讓開 (戰鬥)": "BATTLE_SLIME",
            "裝作沒看到 (逃跑)": "END_RUN",
            "檢查備份 (讀取)": "LOAD_GAME"
            # [DEBUG] 按鈕已移除
        },
        "image": "assets/images/office_cubicle.png",
        "type": "NORMAL"
    },

    # ---------------------------

    "SLIME_INFO": {
        "text": """實習生 Kevin 一臉無辜地看著妳...
(一股想吐的胃酸味襲來)

Kevin：「硯姊... 那個... 
客戶的伺服器好像被我格式化了...」

妳看著他天真無邪的眼神，手裡的咖啡杯差點捏碎。
他正源源不絕地製造 Bug 子彈。""",
        "choices": {
            "幫他修 Code (戰鬥)": "BATTLE_SLIME",
            "請假回家 (逃跑)": "END_RUN"
        },
        "image": "assets/images/slime_intern.png"
    },

    "WIN_SLIME": {
        "text": """妳花了三小時把實習生搞砸的 Code 修好了。

Kevin：「謝謝硯姊！妳好厲害喔！那我先下班囉！」
(實習生開心地滾走了)

妳看著空蕩蕩的辦公室，發現通往二樓會議室的樓梯...""",
        "choices": {
            "前往二樓會議室": "LEVEL_2_GOBLIN",
            "在茶水間休息 (存檔)": "SAFE_ZONE_1"
        },
        "image": "assets/images/office_hallway.png"
    },

    # ---  存檔點 (茶水間) ---
    "SAFE_ZONE_1": {
        "text": """【茶水間 (Safe Zone)】
妳坐在飲水機旁，吞了一顆胃藥。
這裡看起來暫時是安全的，沒有主管出沒。

(妳可以在這裡更新工作日誌)""",
        "choices": {
            "寫日誌 (存檔)": "SAVE_GAME",
            "繼續前進": "LEVEL_2_GOBLIN"
        },
        "image": "assets/images/pantry.png"
    },

    # ==========================================
    # 第二層：主管哥布林
    # ==========================================
    "LEVEL_2_GOBLIN": {
        "text": """【第二層：地獄會議室】
【主管嘲諷：理智下降】【主管HP：45】

主管：「沈硯啊，客戶說那個功能明天就要，
妳今晚通個宵沒問題吧？」

前方出現一隻穿著不合身西裝的哥布林主管！
(他攔住了妳，看來不講道理是不行了！)""",
        "choices": {
            "拒絕加班 (戰鬥)": "START_GOBLIN_BATTLE"
        },
        "image": "assets/images/goblin_manager.png"
    },

    "GOBLIN_DEFEATED": {
        "text": """主管被妳的邏輯連擊駁倒了！

主管：「好啦好啦... 那時程延後兩天... 
不過妳要負責去跟老闆解釋喔！」

(主管甩鍋後逃跑了，徹底失去了戰意)""",
        "choices": {
            "逼他簽字": "GOBLIN_KILLED",
            "放過他": "GOBLIN_SPARED"
        },
        "image": "assets/images/manager_cry.png"
    },

    "GOBLIN_KILLED": {
        "text": """妳擔心放走主管會有隱患，
心想:「此人只會畫大餅，留著也是禍害!」
於是妳逼他簽下了「不加班保證書」。

世界清靜了。
但是... 他身上什麼都沒有。
妳總覺得好像錯過了什麼重要資訊......""",
        "choices": {
            "前往大門": "LEVEL_2_GATE"
        },
        "image": "assets/images/empty_meeting_room.png"
    },

    "GOBLIN_SPARED": {
        "text": """主管感動涕零：
「沈硯妳人真好！
...我想...這個加班代碼妳應該會需要--9527--」

(妳記住了密碼 9527)
妳繼續往公司深處走去，主管趁機溜走了。""",
        "choices": {
            "前往大門": "LEVEL_2_GATE"
        },
        "image": "assets/images/manager_happy.png"
    },

    "LEVEL_2_GATE": {
        "text": """妳來到公司核心區域的大門前。
門禁系統顯示：『請輸入加班通行密碼』""",
        "choices": {}, 
        "type": "INPUT", 
        "image": "assets/images/security_gate.png"
    },

    # ==========================================
    # 第三層：核心機房
    # ==========================================
    "LEVEL_3_START": {
        "text": """【第三層：核心機房】
大門開啟後，妳被冷氣凍得發抖。
這裡不再是會議室，而是充滿嗡嗡聲的伺服器機房！
(這是公司的心臟，也是埋藏所有技術債的地方。)

機房連接著三個區域：""",
        "choices": {
            "Legacy Code 區 (左)": "L3_DOOR_ROOM",
            "歷史文檔室 (右)": "L3_ART_ROOM",
            "系統終端機 (前)": "L3_PUZZLE_ROOM"
        },
        "image": "assets/images/server_room.png",
        "type": "NORMAL"
    },

    # --- 房間 1：Legacy Code ---
    "L3_DOOR_ROOM": {
        "text": """妳走進左側區域，盡頭是一扇貼著「勿動」封條的黑色機櫃。
那是傳說中的 Legacy Code (遺留代碼)。
妳試著打開它，但權限不足。

看來不解開終端機的鎖是過不去的。""",
        "choices": {
            "返回機房": "LEVEL_3_START"
        },
        "image": "assets/images/legacy_server.png",
        "type": "NORMAL"
    },

    # --- 房間 2：文檔室 ---
    "L3_ART_ROOM": {
        "text": """這是一個堆滿紙箱的文檔室。
妳注意到牆上掛著公司創辦人的三句名言 (雖然都沒做到)：

1.『創新』：要像圓形一樣圓融，滾動向前。
2.『誠信』：要像正方形一樣正直，方方正正。
3.『穩定』：要像三角形一樣穩固，支撐一切。""",
        "choices": {
            "返回機房": "LEVEL_3_START"
        },
        "image": "assets/images/history_wall.png",
        "type": "NORMAL"
    },

    # --- 房間 3：終端機謎題 (PUZZLE 模式) ---
    "L3_PUZZLE_ROOM": {
        "text": """這個終端機螢幕發出微弱的光。
螢幕上顯示著「系統重置程序」。

根據文檔室那三句騙人的鬼話，順序應該是？""",
        "choices": {
            "█ (正直)": "PUSH_SQUARE",
            "◯ (圓融)": "PUSH_CIRCLE",
            "△ (穩固)": "PUSH_TRIANGLE",
            "放棄": "LEVEL_3_START"
        },
        "type": "PUZZLE",
        "image": "assets/images/terminal_screen.png"
    },

    # --- 解謎成功 ---
    "L3_UNLOCK_SUCCESS": {
        "text": """【系統】嗶——！權限解鎖成功！
隨著正確的順序被按下，機房地板開始震動。
遠處傳來了電梯運作的聲音，那扇黑色的總裁電梯門打開了！""",
        "choices": {
            "前往頂樓前廳": "SAFE_ZONE_2"
        },
        "image": "assets/images/elevator_open.png"
    },

    # --- 最終存檔點 (頂樓前廳) ---
    "SAFE_ZONE_2": {
        "text": """【系統提示：偵測到高壓反應】
妳站在總裁辦公室前。
想起剛才茶水間好像還沒關燈...

是否要休息一下?
(這將是妳遞出辭呈前最後的存檔機會)""",
        "choices": {
            "是 (存檔)": "SAVE_GAME",
            "深呼吸，推開大門": "BOSS_PRELUDE",
            "返回機房": "LEVEL_3_START"
        },
        "image": "assets/images/pantry.png"
    },

    # --- Boss 戰前奏 (一周目) ---
    "BOSS_PRELUDE": {
        "text": """妳走進辦公室，一股強大的壓迫感撲面而來...
那是資本主義的氣息。
(這裡就是終點了嗎？)""",
        "choices": {
            "遞出辭呈 (戰鬥)": "BOSS_BATTLE"
        },
        "image": "assets/images/boss_desk.png"
    },

    # --- Boss 戰前奏 (二周目/真相篇) ---
    "BOSS_PRELUDE_LOOP": {
        "text": """妳推開大門，但這次沒有壓迫感。
「體制」靜靜地坐在那裡，彷彿在等妳。

『...又是妳，沈硯。』
『既然妳帶著記憶歸來，代表妳已經看穿了這家公司的本質。』

『實習生、主管... 其實都只是用來磨損妳熱情的「耗材」。』
『而我們... 只是被困在這個名為 [UnderPy Inc.] 的牢籠裡的數據。』

『來吧，說服我讓妳走。或是繼續加班。』""",
        "choices": {
            "準備離職 (迎接終結)": "BOSS_BATTLE"
        },
        "image": "assets/images/boss_desk.png"
    },

    # --- 戰勝 Boss (一周目) ---
    "BOSS_WIN": {
        "text": """老闆:『............』
『妳......』
『妳真的要放棄年終獎金嗎?......』

隨著【老闆】的崩潰，辦公室的牆壁開始崩塌
【警告：公司體制受損...】

一道耀眼的白光出現在前方。
那是...出口？還是另一家公司的面試通知？""",
        "choices": {
            "走向白光": "END_WIN"
        },
        "image": "assets/images/office_collapse.png"
    },

    # --- 戰勝 Boss (二周目/真結局) ---
    "BOSS_WIN_LOOP": {
        "text": """體制倒下了，但他臉上帶著解脫的笑容。

『做得好... 妳終於自由了...』

四周的程式碼開始剝落，露出了背後的 [打卡鐘]。
妳意識到，妳終於可以輸入那個指令了。""",
        "choices": {
            "永久登出 (結束輪迴)": "TRUE_END"
        },
        "image": "assets/images/office_collapse.png"
    },

    "TRUE_END": {
        "text": """恭喜妳，打破了社畜輪迴。
妳已經超越了這家公司的邏輯。

「遊戲結束... 但沈硯的新人生才剛開始。」

(真結局達成 ! 感謝遊玩 UnderPy！)
(press ESC to exit)""",
        "choices": {}, 
        "image": "assets/images/end_credit.png"
    },

    # --- 結局 ---
    "END_RUN": {"text": "妳逃回家睡覺了。但明天還是要上班。\n(Bad End: 社畜輪迴)", "choices": {}, "image": "assets/images/hospital_ceiling.png"},
    "END_LOSE": {"text": "妳過勞倒下了。\n(Bad End: 肝臟過勞)", "choices": {}, "image": "assets/images/hospital_ceiling.png"},
    "END_WIN": {"text": "恭喜離職！開啟新人生！", "choices": {}, "image": "assets/images/freedom_sky.png"},

    # ==========================================
    # 除錯模式 (Orphan Node - Unreachable by players)
    # ==========================================
    "DEBUG_MENU": {
        "text": """[Developer Debug Mode]
Please select a chapter to jump to...

(Warning: Jumping may break story consistency)""",
        "choices": {
            "1. Intern (Level 1)": "START",
            "2. Manager (Level 2)": "LEVEL_2_GOBLIN",
            "3. Server Room (Level 3)": "LEVEL_3_START",
            "4. Boss (Normal)": "BOSS_PRELUDE",
            "5. Boss (True Loop)": "BOSS_PRELUDE_LOOP",
            "6. Back to Start": "START"
        },
        "image": "assets/images/terminal_screen.png",
        "type": "NORMAL"
    }
}


# =================================================================
#  [Developer Debugger]
#  Usage: Run `python story/script.py` directly.
#  Features: View script content in plain text.
# =================================================================
if __name__ == "__main__":
    import os
    import sys

    # Disable screen clearing to prevent black screen on some terminals
    def clear_screen():
        # os.system('cls' if os.name == 'nt' else 'clear') 
        print("\n" * 3)

    def print_scene(scene_id):
        # Display single scene info
        if scene_id not in SCENE_SCRIPT:
            print(f"\n[Error] Scene ID not found: {scene_id}")
            return

        scene = SCENE_SCRIPT[scene_id]
        clear_screen()
        print("="*60)
        print(f"[Scene ID] : {scene_id}")
        print(f"[Type]     : {scene.get('type', 'NORMAL')}")
        print(f"[Image]    : {scene.get('image')}")
        print("="*60)
        print("\n=== [Text Content] ===\n")
        print(scene["text"])
        print("\n" + "-"*30)
        print("=== [Choices] ===")
        
        if scene.get("type") == "INPUT":
            print("  > [Input Mode] (No fixed choices)")
        else:
            for text, next_id in scene.get("choices", {}).items():
                print(f"  > [{text}]  ---> Jump to: {next_id}")
        
        print("\n" + "="*60)

    # --- Debug Loop ---
    while True:
        clear_screen()
        print("██ UnderPy Script Debugger Tool ██\n")
        print("For developer use only. Inspect raw text logic.")
        print(f"Loaded Scenes: {len(SCENE_SCRIPT)}\n")
        
        # List all scenes
        scene_keys = list(SCENE_SCRIPT.keys())
        for i, key in enumerate(scene_keys):
            print(f"{i+1:02d}. {key}")

        print("\n" + "-"*40)
        user_input = input("Enter [Index] or [Scene ID] (q to quit): ").strip()

        if user_input.lower() == 'q':
            print("Debugger closed.")
            break

        target_id = None
        
        # Parse input
        if user_input.isdigit():
            idx = int(user_input) - 1
            if 0 <= idx < len(scene_keys):
                target_id = scene_keys[idx]
        elif user_input in SCENE_SCRIPT:
            target_id = user_input
        
        if target_id:
            print_scene(target_id)
            input("\nPress Enter to return...")
        else:
            input("\nInvalid input, press Enter to retry...")