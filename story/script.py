# story/script.py

# 劇情數據模組，使用字典儲存所有對話腳本

# --- 遊戲初始介紹 ---
INTRO_SCENE = {
    "id": "INTRO_01",
    "text": "歡迎來到 UnderPy 的世界。你醒來時，發現自己被困在一個未知的洞穴裡。",
    "speaker": "旁白",
    "next": "NPC_MEET"  # 指向下一個劇情段落
}

# --- 遇到 NPC 的對話 ---
NPC_MEET = {
    "id": "NPC_02",
    "text": "一位看起來很友善的 NPC 站在前方。 '嗨！陌生人，你還好嗎？'",
    "speaker": "NPC A",
    "next": "CHOICE_1"  # 指向一個選項
}

# --- 戰鬥前的對話 ---
PRE_BATTLE = {
    "id": "BATTLE_01",
    "text": "NPC 突然變臉：'抱歉，這是規定！準備好戰鬥吧！'",
    "speaker": "NPC A",
    "next_action": "START_BATTLE"  # 特殊指令，告訴 manager.py 啟動 Pygame
}

# 使用字典儲存選項與分支 (Choices and Branches)

CHOICE_1 = {
    "id": "CHOICE_01",
    "text": "你要如何回應這位友善的 NPC？",
    "speaker": "旁白",
    "options": [
        {
            "text": "1. 友好地打招呼。",
            "target": "BATTLE_01"  # 選項 1 導向戰鬥
        },
        {
            "text": "2. 保持沉默。",
            "target": "ENDING_PACIFIST" # 選項 2 導向和平結局（如果選擇製作）
        }
    ]
}

# 儲存結局文本 (Ending Text)

# --- 新增的劇本資料 (可放在 GameManager 外部，讓流程負責人單獨維護) ---
SCENE_SCRIPT = {
    "START": {
        "text": "你進入了一個地下城。前方出現一隻史萊姆！",
        "choices": {
            "調查": "SLIME_INFO",
            "戰鬥": "BATTLE_SLIME", # 特殊動作代號
            "逃跑": "END_RUN"
        }
    },
    "SLIME_INFO": {
        "text": "史萊姆看起來很飢餓。你確認了，這確實是一隻史萊姆。",
        "choices": {
            "準備戰鬥": "BATTLE_SLIME",
            "偷偷溜走": "END_RUN"
        }
    },
    "WIN_SLIME": {
        "text": "你贏了！史萊姆倒下了。你發現了一把生鏽的鑰匙。",
        "choices": {
            "繼續探索": "SCENE_2_ROOM"
        }
    },
    "SCENE_2_ROOM": {
        "text": "你來到了一扇古老的門前，這似乎是地下城的第二層入口。",
        "choices": {
            "用鑰匙開門": "END_WIN",
            "返回": "START" # 範例: 回到起點
        }
    },
    "END_RUN": {
        "text": "你成功逃跑了！遊戲結束。",
        "choices": {}
    },
    "END_WIN": {
        "text": "你打開了門，通往更深處的光芒籠罩了你。恭喜你完成了第一階段的探索！",
        "choices": {}
    },
}
# 戰鬥相關的場景 ID (例如 BATTLE_SLIME) 是特殊動作，由 GameManager 判斷處理。
