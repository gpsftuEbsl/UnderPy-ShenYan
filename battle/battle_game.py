import pygame
import random
import sys

# ------------ 設定 ------------
WIDTH, HEIGHT = 480, 360
FPS = 60

BOX_RECT = pygame.Rect(80, 60, 320, 240)  # 心臟活動區域
HEART_SPEED = 4
BULLET_SPEED = 4
SPAWN_RATE = 25 
PLAYER_HP = 5

# ------------ Pygame 初始化 ------------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Boss Battle – UnderPy")
clock = pygame.time.Clock()

font = pygame.font.SysFont("arial", 24)

# ------------ 玩家（心臟）物件 ------------
class Heart:
    def __init__(self):
        self.x = BOX_RECT.centerx
        self.y = BOX_RECT.centery
        self.r = 8  # 心臟半徑
        self.hp = PLAYER_HP

    def move(self, keys):
        if keys[pygame.K_UP] and self.y - self.r > BOX_RECT.top:
            self.y -= HEART_SPEED
        if keys[pygame.K_DOWN] and self.y + self.r < BOX_RECT.bottom:
            self.y += HEART_SPEED
        if keys[pygame.K_LEFT] and self.x - self.r > BOX_RECT.left:
            self.x -= HEART_SPEED
        if keys[pygame.K_RIGHT] and self.x + self.r < BOX_RECT.right:
            self.x += HEART_SPEED

    def draw(self):
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.r)

# ------------ 子彈（魔王攻擊） ------------
class Bullet:
    def __init__(self):
        # 從上方隨機位置出現
        self.x = random.randint(BOX_RECT.left, BOX_RECT.right)
        self.y = BOX_RECT.top
        self.size = 8

    def update(self):
        self.y += BULLET_SPEED

    def draw(self):
        pygame.draw.rect(screen, (255, 255, 0), (self.x, self.y, self.size, self.size))

    def is_off_screen(self):
        return self.y > BOX_RECT.bottom

# ------------ 主程式（Boss 戰 Loop） ------------
def boss_battle():
    heart = Heart()
    bullets = []
    frame = 0

    running = True
    while running:
        clock.tick(FPS)
        screen.fill((0, 0, 0))

        # ---- 處理事件 ----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # ---- 玩家移動 ----
        keys = pygame.key.get_pressed()
        heart.move(keys)

        # ---- 生成子彈 ----
        frame += 1
        if frame % SPAWN_RATE == 0:
            bullets.append(Bullet())

        # ---- 更新子彈 & 碰撞 ----
        for b in bullets[:]:
            b.update()
            if b.is_off_screen():
                bullets.remove(b)
                continue

            # 碰撞檢查
            if pygame.Rect(b.x, b.y, b.size, b.size).colliderect(
                pygame.Rect(heart.x - heart.r, heart.y - heart.r, heart.r*2, heart.r*2)
            ):
                heart.hp -= 1
                bullets.remove(b)

                if heart.hp <= 0:
                    return "LOSE"

        # ---- 畫區域、玩家、子彈 ----
        pygame.draw.rect(screen, (255, 255, 255), BOX_RECT, 2)
        heart.draw()

        for b in bullets:
            b.draw()

        # ---- 畫 HP ----
        hp_text = font.render(f"HP: {heart.hp}", True, (255, 255, 255))
        screen.blit(hp_text, (20, 20))

        pygame.display.update()

        # ---- 勝利條件：60 秒沒死 ----
        if frame > FPS * 60:
            return "WIN"


# ------------ 單獨測試用 ------------
if __name__ == "__main__":
    result = boss_battle()
    print("Battle Result:", result)