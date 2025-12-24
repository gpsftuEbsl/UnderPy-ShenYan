# story/script.py

SCENE_SCRIPT = {
    # --- 第一層 (原本的) ---
    "START": {
        "text": "你進入了一個地下城。前方出現一隻史萊姆！",
        "choices": {
            "調查": "SLIME_INFO",
            "戰鬥 (Pygame)": "BATTLE_SLIME",
            "逃跑": "END_RUN"
        },
        "image": "assets\images\dungeon.png"
    },
    "SLIME_INFO": {
        "text": "史萊姆看起來很飢餓。確實是一隻史萊姆。",
        "choices": {
            "準備戰鬥": "BATTLE_SLIME",
            "偷偷溜走": "END_RUN"
        },
        "image": "assets\images\silme.png"
    },
    # --- 戰鬥勝利後，導向第二層 ---
    "WIN_SLIME": {
        "text": "你贏了！史萊姆化成一灘水。你發現通往深處的樓梯。",
        "choices": {
            "前往第二層": "LEVEL_2_GOBLIN"  # 接續到哥布林劇情
        },
        "image": "assets/images/stairs_down.png"
    },
    # --- 第二層：哥布林劇情開始 ---
    "LEVEL_2_GOBLIN": {
        "text": "【第二層：回音洞穴】\n前方出現一隻穿著吊嘎的哥布林！\n哥布林：『喂！你看起來一臉 Bug 很多跑不動的樣子！』\n\n(系統：哥布林攔住了你，看來不教訓他不行了！)",
        "choices": {
            "進入戰鬥": "START_GOBLIN_BATTLE"  # 這裡標記進入戰鬥迴圈
        },
        "image": "assets/images/goblin_taunt.png"
    },
    # 戰鬥結束後的過渡場景 (哥布林血量歸零後跳轉到這)
    "GOBLIN_DEFEATED": {
        "text": "哥布林：『哎唷！君子動口不動手啊！大俠饒命！』\n你手中的劍架在她的脖子上，她已經徹底失去了戰意。",
        "choices": {
            "殺死她": "GOBLIN_KILLED",
            "放走她": "GOBLIN_SPARED"
        },
        "image": "assets/images/goblin_cry.png"
    },
    
    # --- 分支 A：殺死 ---
    "GOBLIN_KILLED": {
        "text": "你一劍解決了哥布林。世界清靜了。\n但是... 她身上什麼都沒有。你好像錯過了什麼。",
        "choices": {
            "前往大門": "LEVEL_2_GATE"
        },
        "image": "assets/images/empty_room.png"
    },
    
    # --- 分支 B：放走 (獲得密碼) ---
    "GOBLIN_SPARED": {
        "text": "哥布林感動涕零：『大哥你人真好！這是我家大門密碼 9527，送你啦！』\n(系統：你記住了密碼 9527)",
        "choices": {
            "前往大門": "LEVEL_2_GATE"
        },
        "image": "assets/images/goblin_happy.png"
    },

    # --- 密碼門 (特殊場景：需要輸入框) ---
    "LEVEL_2_GATE": {
        "text": "你來到一扇巨大的石門前。\n門上有個電子鎖，上面寫著：『請輸入通行密碼』",
        "choices": {}, # 這裡沒有按鈕，因為我們要顯示輸入框
        "type": "INPUT", # 標記這個場景需要輸入框
        "image": "assets/images/door_locked.png"
    },
    
    # --- 第三層 (通過後) ---
    "LEVEL_3_START": {
        "text": "【系統】密碼正確！大門緩緩打開...\n歡迎來到第三層！",
        "choices": {
            "暫時結束": "END_WIN"
        },
        "image": "assets/images/door_open.png"
    },
    
    # --- 結局 ---
    "END_RUN": {"text": "你逃跑了。Game Over。", "choices": {}, "image": "assets/images/the_end.png"},
    "END_LOSE": {"text": "你死了。Game Over。", "choices": {}, "image": "assets/images/the_end.png"},
    "END_WIN": {"text": "恭喜通關目前版本！", "choices": {}, "image": "assets/images/the_end.png"}
}
