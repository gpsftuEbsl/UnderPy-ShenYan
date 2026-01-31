# config.py
# 遊戲配置集中管理

# ==========================================
#  遊戲主設定
# ==========================================
GAME_TITLE = "UnderPy - Dungeon Adventure"
SAVE_FILE = "savefile.json"

# ==========================================
#  玩家角色設定
# ==========================================
PLAYER_NAME = "勇者"
PLAYER_MAX_HP = 100
PLAYER_ATK = 15

# ==========================================
#  戰鬥難度設定 (可調整難度)
# ==========================================
# 第一關（實習生）戰鬥時間
INTERN_BATTLE_TIME = 20  # 秒

# 最終 Boss 戰鬥時間
FINAL_BOSS_BATTLE_TIME = 50  # 秒

# 玩家受傷數值
SCENARIO_DAMAGE_MANAGER = 10  # 主管劇情傷害
PASSWORD_ERROR_DAMAGE = 5    # 密碼錯誤傷害
PUZZLE_FAILURE_DAMAGE = 45   # 解謎失敗傷害

# ==========================================
#  敵人設定
# ==========================================
MANAGER_NAME = "吊嘎主管"
MANAGER_HP = 45
MANAGER_ATK = 8

# ==========================================
#  謎題設定
# ==========================================
PUZZLE_ANSWER = ["◯", "△", "█"]

# ==========================================
#  密碼設定
# ==========================================
CORRECT_PASSWORD = "9527"

# ==========================================
#  場景映射（二周目覆蓋）
# ==========================================
SCENE_OVERRIDES = {
    "START": "START_LOOP",
    "BOSS_PRELUDE": "BOSS_PRELUDE_LOOP"
}

# ==========================================
#  Pygame 戰鬥視窗設定
# ==========================================
BATTLE_WINDOW_WIDTH = 480
BATTLE_WINDOW_HEIGHT = 360
BATTLE_FPS = 60

# 遊戲區域（戰鬥邊界）
BATTLE_BOX_RECT = (80, 60, 320, 240)  # (x, y, width, height)

# 玩家（心形）設定
HEART_SIZE = 12
HEART_SPEED = 4
HEART_HP = 100

# 普通Boss子彈設定
BULLET_SIZE = 30
BULLET_SPEED = 4
BULLET_SPAWN_INTERVAL = 25  # 幀數
BULLET_DAMAGE = 20

# 最終Boss子彈設定
CIRCLE_BULLET_RADIUS = 8
CIRCLE_BULLET_SPEED = 3
CIRCLE_BULLET_SPAWN_INTERVAL = 20
CIRCLE_BULLET_DAMAGE = 10

WAVE_BULLET_SIZE = 10
WAVE_BULLET_SPEED = 3
WAVE_BULLET_SPAWN_INTERVAL = 20
WAVE_BULLET_AMPLITUDE = 40
WAVE_BULLET_DAMAGE = 10

HOMING_BULLET_SIZE = 10
HOMING_BULLET_SPAWN_INTERVAL = 20
HOMING_BULLET_LIFE = 90  # 幀數（3秒）
HOMING_BULLET_POWER = 0.015  # 追蹤速度
HOMING_BULLET_DAMAGE = 20

# ==========================================
#  UI 配置（顏色、字體）
# ==========================================
UI_COLORS = {
    "bg_main": "#000000",
    "bg_text": "#121D25",
    "fg_text": "#ECF0F1",
    "fg_accent": "#E74C3C",
    "btn_bg": "#121D25",
    "btn_fg": "#FFFFFF",
    "btn_hover": "#434343",
    "input_bg": "#ECF0F1",
    "input_fg": "#2C3E50"
}

UI_FONTS = {
    "main": ("Microsoft JhengHei", 18),
    "mono": ("Consolas", 16),
    "bold": ("Microsoft JhengHei", 16, "bold"),
    "status": ("Impact", 20)
}

# 打字機效果速度（毫秒）
TYPEWRITER_SPEED = 50

# UI 元素尺寸
UI_IMAGE_WIDTH = 500
UI_IMAGE_HEIGHT = 350
UI_TEXT_HEIGHT = 8  # 文字區行數

# UI 特效設定
SHAKE_WINDOW_OFFSETS = [(12, 7), (-12, -7), (10, -5), (-10, 5), (6, 3), (-6, -3), (0, 0)]
SHAKE_WINDOW_INTERVAL = 25  # 毫秒
FLASH_RED_DURATION = 100  # 毫秒

# ==========================================
#  遊戲邏輯設定
# ==========================================
# 場景轉換延遲（毫秒）
SCENE_TRANSITION_DELAY = 2000

# 存檔讀檔延遲
LOAD_GAME_DELAY = 2000

# ==========================================
#  資源路徑設定
# ==========================================
ASSETS_IMAGES_DIR = "assets/images/"
