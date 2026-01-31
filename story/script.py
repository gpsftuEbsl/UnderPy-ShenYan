SCENE_SCRIPT = {
    # ==========================================
    # 第一層：新人史萊姆 (The Intern Slime)
    # ==========================================
    "START": {
        "text": "【星期一 09:00 AM】\n沈硯在辦公桌前醒來。\n「我為什麼還在這裡？昨天不是加班到三點嗎？」\n你揉了揉太陽穴，準備去茶水間倒咖啡。\n突然，一團黏糊糊的、看起來很迷茫的生物擋住了去路。\n那是... 新來的實習生史萊姆！",
        "choices": {
            "查看工牌 (調查)": "SLIME_INFO",
            "叫他讓開 (戰鬥)": "BATTLE_SLIME",
            "裝作沒看到 (逃跑)": "END_RUN",
            "檢查備份 (讀取)": "LOAD_GAME"
        },
        "image": "assets/images/office_cubicle.png" 
    },

    "SLIME_INFO": {
        "text": "【實習生史萊姆】\nHP: 10 | 攻擊力: 0 (但在幫倒忙時會造成 999 點精神傷害)\n\n史萊姆：「硯姊... 那個... 客戶的伺服器好像被我格式化了...」\n(一股胃酸逆流的感覺襲來)\n你看著史萊姆天真無邪的眼神，手裡的咖啡杯差點捏碎。",
        "choices": {
            "修正他的錯誤 (戰鬥)": "BATTLE_SLIME",
            "請假回家 (逃跑)": "END_RUN"
        },
        "image": "assets/images/slime_intern.png"
    },

    "WIN_SLIME": {
        "text": "你花了三小時把實習生搞砸的 Code 修好了。\n史萊姆：「謝謝硯姊！妳好厲害喔！那我先下班囉！」\n(史萊姆開心地滾走了)\n\n你看著空蕩蕩的辦公室，發現通往二樓會議室的樓梯...",
        "choices": {
            "前往二樓會議室": "LEVEL_2_GOBLIN",
            "在茶水間休息 (存檔)": "SAFE_ZONE_1"
        },
        "image": "assets/images/stairs_up.png"
    },

    # --- 存檔點 (茶水間) ---
    "SAFE_ZONE_1": {
        "text": "【茶水間 (Safe Zone)】\n這裡有無限供應的難喝咖啡和過期的餅乾。\n你吞了一顆胃藥，感覺生命值稍微恢復了一點。\n(是否要更新工作日誌？)",
        "choices": {
            "更新日誌 (存檔)": "SAVE_GAME",
            "回到工位": "LEVEL_2_GOBLIN"
        },
        "image": "assets/images/pantry.png"
    },

    # ==========================================
    # 第二層：主管哥布林 (The Manager Goblin)
    # ==========================================
    "LEVEL_2_GOBLIN": {
        "text": "【第二層：地獄會議室】【Debuff：專案時程 -50%】\n\n一隻穿著不合身西裝的哥布林主管擋在門口！\n主管：「沈硯啊，客戶說那個功能明天就要，妳今晚通個宵沒問題吧？」\n(你的理智線發出了斷裂的聲音)",
        "choices": {
            "拒絕加班 (戰鬥)": "START_GOBLIN_BATTLE"
        },
        "image": "assets/images/goblin_manager.png"
    },

    "GOBLIN_DEFEATED": {
        "text": "主管被你的邏輯連擊駁倒了！\n主管：「好啦好啦... 那時程延後兩天... \n不過妳要負責去跟老闆解釋喔！」\n(主管甩鍋後逃跑了)",
        "choices": {
            "去老闆辦公室": "LEVEL_2_GATE",
            "無視他": "GOBLIN_SPARED" # 這裡可以做分支
        },
        "image": "assets/images/goblin_run.png"
    },
    
    # 分支：如果選擇放過哥布林 (接受加班?)
    "GOBLIN_SPARED": {
        "text": "你嘆了口氣，決定還是幫主管扛這一次。\n主管：「謝啦！就知道妳最可靠了！對了，大門密碼是 996 (暗示工時)。」\n(你獲得了密碼，但也獲得了黑眼圈)",
        "choices": {
             "前往大門": "LEVEL_2_GATE"
        },
        "image": "assets/images/goblin_happy.png"
    },

    "LEVEL_2_GATE": {
        "text": "你來到了公司核心區域的大門前。\n門禁系統顯示：『請輸入加班密碼』",
        "choices": {}, 
        "type": "INPUT", 
        "image": "assets/images/security_gate.png"
    },

    # ==========================================
    # 第三層：核心機房 (The Server Room)
    # ==========================================
    "LEVEL_3_START": {
        "text": "【第三層：核心機房】\n這裡冷氣開得很強，伺服器的風扇聲嗡嗡作響。\n這是公司的心臟，也是埋藏所有技術債的地方。\n\n前方有三條路：",
        "choices": {
            "Legacy Code 區 (左)": "L3_DOOR_ROOM",
            "歷史文檔室 (右)": "L3_ART_ROOM",
            "系統終端機 (中)": "L3_PUZZLE_ROOM"
        },
        "image": "assets/images/server_room.png"
    },

    # --- 謎題提示改版 ---
    "L3_ART_ROOM": {
        "text": "【歷史文檔室】\n牆上掛著公司創辦人的三句名言 (雖然都沒做到)：\n\n1.『創新』：要像圓形一樣圓融，滾動向前。\n2.『誠信』：要像正方形一樣正直，方方正正。\n3.『穩定』：要像三角形一樣穩固，支撐一切。\n\n(沈硯吐槽：結果現在公司根本是個不規則的多邊形。)",
        "choices": {
            "返回機房": "LEVEL_3_START"
        },
        "image": "assets/images/history_wall.png"
    },

    # --- 謎題房間 ---
    "L3_PUZZLE_ROOM": {
        "text": "【系統終端機】\n螢幕上顯示著「系統重置程序」。\n需要輸入正確的圖形順序才能啟動。\n\n根據文檔室那三句騙人的鬼話，順序應該是？",
        "choices": {
            "◯ (圓融)": "PUSH_CIRCLE",
            "█ (正直)": "PUSH_SQUARE",
            "△ (穩固)": "PUSH_TRIANGLE",
            "算了，不想重置": "LEVEL_3_START"
        },
        "type": "PUZZLE",
        "image": "assets/images/terminal_screen.png"
    },

    "L3_UNLOCK_SUCCESS": {
        "text": "【系統提示：權限解鎖】\n嗶——！\n終端機發出綠光，後方隱藏的總裁電梯門打開了。\n這也是通往「自由」的唯一路徑。",
        "choices": {
            "搭電梯上去": "SAFE_ZONE_2"
        },
        "image": "assets/images/elevator_open.png"
    },

    # --- 最終存檔點 (頂樓前廳) ---
    "SAFE_ZONE_2": {
        "text": "【頂樓前廳】\n電梯門開了，前方就是董事長辦公室。\n你整理了一下儀容，摸了摸口袋裡的辭職信。\n這是最後的機會了。\n(是否要在這裡備份進度？)",
        "choices": {
            "備份進度 (存檔)": "SAVE_GAME",
            "推開大門": "BOSS_PRELUDE",
            "回機房吹冷氣": "LEVEL_3_START"
        },
        "image": "assets/images/pantry_luxury.png"
    },

    # ==========================================
    # Boss 戰：體制巨獸 (The Corporate Beast)
    # ==========================================
    "BOSS_PRELUDE": {
        "text": "你推開沉重的檜木大門。\n辦公椅緩緩轉過來，但上面坐的不是人。\n而是一團由合約、鈔票、和無數肝臟組成的黑色聚合物——【體制】。\n\n體制：「沈硯... 妳想去哪裡？妳的房貸繳完了嗎？妳的退休金存夠了嗎？」\n體制：「留下來吧... 外面的世界很可怕的...」",
        "choices": {
            "遞出辭呈 (戰鬥)": "BOSS_BATTLE"
        },
        "image": "assets/images/boss_corporate.png"
    },

    # --- 真結局分支 (二周目) ---
    # 如果玩家已經通關過一次，沈硯會覺醒
    "BOSS_PRELUDE_LOOP": {
        "text": "你再次推開大門。\n這次，你看著那團黑色聚合物，只是冷冷一笑。\n\n沈硯：「少拿房貸嚇唬我。我已經算過了，只要我不買特斯拉，不喝星巴克，我現在就能活。」\n體制：「什...什麼？妳的慾望... 怎麼這麼低？我的攻擊無效？」\n\n沈硯：「因為我是用 Windows XP 運行的。你的恐懼病毒對我無效。」",
        "choices": {
            "格式化體制 (終結)": "BOSS_BATTLE"
        },
        "image": "assets/images/boss_glitch.png"
    },

    "BOSS_WIN": {
        "text": "體制發出刺耳的尖叫聲：\n『不！！！妳不能走！妳走了誰來維護 Legacy Code ！！！』\n\n隨著巨獸崩解，辦公室的落地窗碎裂了。\n外面不是高樓大廈，而是一片廣闊的藍天。\n\n妳手裡的辭職信化作了一把鑰匙。",
        "choices": {
            "走出公司 (自由)": "END_WIN"
        },
        "image": "assets/images/sky_freedom.png"
    },

    "TRUE_END": {
        "text": "【真結局：離職快樂】\n沈硯走出了大樓，陽光有點刺眼。\n手機響了，是主管打來的。\n妳看了一眼，將手機丟進了門口的噴水池。\n\n「好了，接下來要去哪裡呢？」\n「先去吃個早餐吧，這次我要加洋蔥。」\n\n(感謝遊玩 UnderPy: Resignation)",
        "choices": {},
        "image": "assets/images/end_credits.png"
    },

    # --- 結局分支 ---
    "END_RUN": {"text": "妳逃回了家裡，繼續忍受這一切。\n(Bad End: 社畜輪迴)", "choices": {}, "image": "assets/images/bad_end_home.png"},
    "END_LOSE": {"text": "妳過勞倒下了。\n(Bad End: 肝臟過勞)", "choices": {}, "image": "assets/images/bad_end_hospital.png"},
    "END_WIN": {"text": "恭喜離職！開啟新人生！", "choices": {}, "image": "assets/images/good_end.png"}
}