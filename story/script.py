# story/script.py
# 這裡用來放劇本腳本    

SCENE_SCRIPT = {
    # ==========================================
    # 第一層：史萊姆
    # ==========================================
    "START": {
        "text": "你在一個地下城裡醒來。\n你:「我為什麼會在這裡?」\n你站起身來四處張望。\n發現前方有一隻不知道從哪冒出來的史萊姆。",
        "choices": {
            "調查": "SLIME_INFO",
            "戰鬥 (Pygame)": "BATTLE_SLIME",
            "逃跑": "END_RUN"
        },
        "image": "assets/images/dungeon.png"
    },
    "SLIME_INFO": {
        "text": "史萊姆看起來黏糊糊的...\n(一股史萊姆的味道襲來)\n呃阿......(你邊摀住口鼻邊倒退)\n...這...確實是一隻史萊姆......\n說話間，史萊姆突然開始向你彈射從體內冒出的強酸子彈。",
        "choices": {
            "開始戰鬥": "BATTLE_SLIME",
            "偷偷溜走": "END_RUN"
        },
        "image": "assets/images/silme.png"
    },
    "WIN_SLIME": {
        "text": "你贏了！史萊姆似乎用完了所有「彈藥」。\n你在史萊姆後方發現一條向下延伸的的階梯......",
        "choices": {
            "前往第二層": "LEVEL_2_GOBLIN"
        },
        "image": "assets/images/stairs_down.png"
    },

    # ==========================================
    # 第二層：哥布林與密碼門
    # ==========================================
    # TODO: 獨立出哥布林資訊場景 並且所有受傷特效需再哥布林攻擊後觸發
    "LEVEL_2_GOBLIN": {
        "text": "【第二層：回音洞穴】【哥布林嘲諷：HP下降】【哥布HP：45】\n哥布林：『喂！你看起來一臉 Bug 很多跑不動的樣子！』\n前方出現一隻穿著吊嘎的深綠色哥布林！\n(哥布林攔住了你，看來不教訓他不行了！)",
        "choices": {
            "進入戰鬥": "START_GOBLIN_BATTLE"
        },
        "image": "assets/images/goblin_taunt.png"
    },
    "GOBLIN_DEFEATED": {
        "text": "哥布林：『哎唷！君子動口不動手啊！大哥饒命！』\n你手中的劍架在牠的脖子上，牠已經徹底失去了戰意。",
        "choices": {
            "殺死牠": "GOBLIN_KILLED",
            "放走牠": "GOBLIN_SPARED"
        },
        "image": "assets/images/goblin_cry.png"
    },
    "GOBLIN_KILLED": {
        "text": "你擔心放走哥布林會留下隱患，心想:「此子心機頗深，斷不可留!」\n於是你一劍解決了哥布林。世界清靜了。\n但是... 牠身上什麼都沒有。\n你總覺得好像錯過了什麼......",
        "choices": {
            "前往大門": "LEVEL_2_GATE"
        },
        "image": "assets/images/empty_room.png"
    },
    "GOBLIN_SPARED": {
        "text": "哥布林感動涕零：「大哥你人真好！\n...我想...這個數字你應該會需要--9527--」\n(你記住了密碼 9527)\n你繼續往洞穴深處走去，突然想起自己還沒問個哥布林這是什麼地方......\n你回頭望去，發現剛剛的哥布林不見了。",
        "choices": {
            "前往大門": "LEVEL_2_GATE"
        },
        "image": "assets/images/goblin_happy.png"
    },
    "LEVEL_2_GATE": {
        "text": "繼續往迷宮的深處前進\n你來到一扇長滿青苔的巨大石門前。\n門上有個數字鎖，上面寫著：『請輸入通行密碼』",
        "choices": {}, 
        "type": "INPUT", 
        "image": "assets/images/door_locked.png"
    },

    # ==========================================
    # 第三層：失落的地下皇宮
    # ==========================================
    # TODO: 增加提示按鈕 並減少純文字敘述中的提示
    "LEVEL_3_START": {
        "text": "【第三層：失落皇宮】\n大門開啟後，你被眼前的景象震驚了。\n這裡不再是潮濕的洞穴，而是一座埋藏在地底、金碧輝煌的宮殿！\n(太奇怪了，到底是誰，又為了什麼把皇宮蓋在這種鬼地方？)\n\n宮殿大廳連接著三個不同的房間：",
        "choices": {
            "左側長廊": "L3_DOOR_ROOM",
            "右側藏寶室": "L3_ART_ROOM",
            "前方陰暗房間": "L3_PUZZLE_ROOM"
        },
        "image": "assets/images/palace_hall.png"
    },

    # --- 房間 1：封閉的黑門 ---
    "L3_DOOR_ROOM": {
        "text": "你走過長廊，盡頭是一扇壓迫感極強的深黑色大門。\n它由某種未知的重金屬製成，表面沒有任何鎖孔。\n你試著用肩膀撞擊，門紋絲不動，甚至連聲音都被金屬吸收了。\n\n看來不解開機關是過不去的。",
        "choices": {
            "返回大廳": "LEVEL_3_START"
        },
        "image": "assets/images/black_door_closed.png"
        # "image": "assets/images/black_door_closed.png" # TODO: 製作門打開後的圖片
    },

    # --- 房間 2：線索畫作 ---
    "L3_ART_ROOM": {
        "text": "這是一個華麗的藏寶室，可惜寶箱都被撬開了，空無一物。\n你注意到牆上掛著三幅積滿灰塵的畫，似乎在訴說著這座宮殿的歷史：\n\n1.『創世』：混沌之中，一顆金球緩緩升起。\n2.『戰爭』：兩軍對峙，士兵們舉著盾牌排成的$@.?&#\n3.『毀滅』：一切歸於塵土，只剩下黑色的正方形石碑。",
        "choices": {
            "返回大廳": "LEVEL_3_START"
        },
        "image": "assets/images/art_room.png"
    },

    # --- 房間 3：謎題機關 (PUZZLE 模式) ---
    "L3_PUZZLE_ROOM": {
        "text": "這個房間沒有一絲光線，空氣中瀰漫著古老的氣味。\n藉著微弱的光，你發現地板上有三個刻著神秘文字的形狀按鈕。\n\n根據你在藏寶室看到的歷史，該依照什麼順序按下它們？",
        "choices": {
            "█": "PUSH_SQUARE",
            "◯": "PUSH_CIRCLE",
            "△": "PUSH_TRIANGLE",
            "放棄": "LEVEL_3_START"
        },
        "type": "PUZZLE", # 標記為謎題模式
        "image": "assets/images/dark_puzzle_room.png"
    },

    # --- 解謎成功 ---
    "L3_UNLOCK_SUCCESS": {
        "text": "【系統】轟隆隆隆——！\n隨著正確的順序被按下，地板開始震動。\n遠處傳來了沉重的金屬摩擦聲，那扇深黑色的大門打開了！",
        "choices": {
            "進入黑色大門 (BOSS戰)": "BOSS_PRELUDE"
        },
        "image": "assets/images/door_open_metal.png"
    },

    # --- Boss 戰前奏 ---
    "BOSS_PRELUDE": {
        "text": "你走進大門，一股強大的亂流撲面而來...\n(這裡就是終點了嗎？)",
        "choices": {
            "準備戰鬥": "BOSS_BATTLE" # 這裡改為觸發 Boss 戰
        },
        "image": "assets/images/boss_room.png"
    },

    # --- 戰勝 Boss (新增) ---
    "BOSS_WIN": {
        "text": "【系統警告：核心程序受損...】\n虛空領主的外殼碎裂，化作無數光點消散在虛空中。\n\n隨著領主的消失，周圍的牆壁開始崩塌，一道耀眼的白光出現在前方。\n那是...出口？還是另一個輪迴的開始？",
        "choices": {
            "走向白光": "END_WIN"
        },
        "image": "assets/images/boss_explode.png"
    },

    # --- 結局 ---
    "END_RUN": {"text": "你逃跑了。Game Over。", "choices": {}, "image": "assets/images/the_end.png"},
    "END_LOSE": {"text": "你死了。Game Over。", "choices": {}, "image": "assets/images/the_end.png"},
    "END_WIN": {"text": "恭喜通關目前版本！", "choices": {}, "image": "assets/images/the_end.png"}
}