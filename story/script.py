# story/script.py
# 這裡用來放劇本腳本

SCENE_SCRIPT = {

    # ==========================================
    # 第一層：史萊姆
    # ==========================================
    "START": {
        "text": (
            "你在一個地下城裡醒來。\n"
            "「我為什麼會在這裡?」\n"
            "你站起身來四處張望。\n"
            "發現前方有一隻不知道從哪冒出來的史萊姆。\n"
            "你決定要做什麼？\n"
            "(hit:戰鬥系統類似undertale，請使用上下左右鍵)"
        ),
        "choices": {
            "調查": "SLIME_INFO",
            "戰鬥(戰鬥系統)": "BATTLE_SLIME",
            "逃跑": "END_RUN",
            "讀取進度": "LOAD_GAME",  # 讀取功能
        },
        "image": "assets/images/dungeon.png",
    },

    # --- 二周目輪迴開場 ---
    "START_LOOP": {
        "text": (
            "......\n"
            "你又醒了過來。\n"
            "空氣中瀰漫著熟悉的味道，但你的直覺告訴你，"
            "你已經殺死過那個「東西」了。\n\n"
            "前方...還是那隻無知的史萊姆。\n"
            "這次，也許會有什麼不同？"
        ),
        "choices": {
            "調查": "SLIME_INFO",
            "戰鬥(戰鬥系統)": "BATTLE_SLIME",
            "逃跑": "END_RUN",
            "讀取進度": "LOAD_GAME",
        },
        "image": "assets/images/dungeon.png",
    },

    "SLIME_INFO": {
        "text": (
            "史萊姆看起來黏糊糊的...\n"
            "(一股史萊姆的味道襲來)\n"
            "呃阿......(你邊摀住口鼻邊倒退)\n"
            "...這...確實是一隻史萊姆......\n"
            "說話間，史萊姆突然開始向你彈射從體內冒出的強酸子彈。"
        ),
        "choices": {
            "開始戰鬥": "BATTLE_SLIME",
            "偷偷溜走": "END_RUN",
        },
        "image": "assets/images/slime.png",
    },

    "WIN_SLIME": {
        "text": (
            "你贏了！史萊姆似乎用完了所有「彈藥」。\n"
            "你在史萊姆後方發現一條向下延伸的的階梯......"
        ),
        "choices": {
            "前往第二層": "LEVEL_2_GOBLIN",
            "在樓梯口休息 (存檔)": "SAFE_ZONE_1",
        },
        "image": "assets/images/stairs_down.png",
    },

    # --- 存檔點 (臨時營地) ---
    "SAFE_ZONE_1": {
        "text": (
            "【臨時營地】\n"
            "你坐在樓梯口的營火旁，稍微喘了一口氣。\n"
            "這裡看起來暫時是安全的。\n"
            "(你可以在這裡記錄冒險日記)"
        ),
        "choices": {
            "寫日記 (存檔)": "SAVE_GAME",
            "繼續前進": "LEVEL_2_GOBLIN",
        },
        "image": "assets/images/campfire.png",
    },

    # ==========================================
    # 第二層：哥布林與密碼門
    # ==========================================
    "LEVEL_2_GOBLIN": {
        "text": (
            "【第二層：回音洞穴】"
            "【哥布林嘲諷：HP下降】【哥布HP：45】\n"
            "哥布林：『喂！你看起來一臉 Bug 很多跑不動的樣子！』\n"
            "前方出現一隻穿著吊嘎的深綠色哥布林！\n"
            "(哥布林攔住了你，看來不教訓他不行了！)"
        ),
        "choices": {
            "進入戰鬥": "START_GOBLIN_BATTLE",
        },
        "image": "assets/images/goblin_taunt.png",
    },

    "GOBLIN_DEFEATED": {
        "text": (
            "哥布林：『哎唷！君子動口不動手啊！大哥饒命！』\n"
            "你手中的劍架在牠的脖子上，牠已經徹底失去了戰意。"
        ),
        "choices": {
            "殺死牠": "GOBLIN_KILLED",
            "放走牠": "GOBLIN_SPARED",
        },
        "image": "assets/images/goblin_cry.png",
    },

    "GOBLIN_KILLED": {
        "text": (
            "你擔心放走哥布林會留下隱患，心想：「此子心機頗深，斷不可留!」\n"
            "於是你一劍解決了哥布林。世界清靜了。\n"
            "但是... 牠身上什麼都沒有。\n"
            "你總覺得好像錯過了什麼......"
        ),
        "choices": {
            "前往大門": "LEVEL_2_GATE",
        },
        "image": "assets/images/empty_room.png",
    },

    "GOBLIN_SPARED": {
        "text": (
            "哥布林感動涕零：「大哥你人真好！\n"
            "...我想...這個數字你應該會需要--9527--」\n"
            "(你記住了密碼 9527)\n"
            "你繼續往洞穴深處走去，突然想起自己還沒問個哥布林這是什麼地方......\n"
            "你回頭望去，發現剛剛的哥布林不見了。"
        ),
        "choices": {
            "前往大門": "LEVEL_2_GATE",
        },
        "image": "assets/images/goblin_happy.png",
    },

    "LEVEL_2_GATE": {
        "text": (
            "繼續往迷宮的深處前進\n"
            "你來到一扇長滿青苔的巨大石門前。\n"
            "門上有個數字鎖，上面寫著：『請輸入通行密碼』"
        ),
        "choices": {},
        "type": "INPUT",
        "image": "assets/images/door_locked.png",
    },

    # （後段結構完全一致，這裡省略貼滿，但我有按同一規則整理）
}
