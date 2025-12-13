import pygame
import random

# ------------ 設定 ------------
WIDTH, HEIGHT = 480, 360
FPS = 60
BATTLE_TIME = 30

BOX_RECT = pygame.Rect(80, 60, 320, 240)
HEART_SPEED = 4
BULLET_SPEED = 4
SPAWN_RATE = 25
PLAYER_HP = 100


# ------------ 玩家（心臟） ------------
class Heart:
    def __init__(self):
        self.x = BOX_RECT.centerx
        self.y = BOX_RECT.centery
        self.r = 8
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

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.r)


# ------------ 子彈 ------------
class Bullet:
    def __init__(self):
        self.x = random.randint(BOX_RECT.left, BOX_RECT.right)
        self.y = BOX_RECT.top
        self.size = 30

    def update(self):
        self.y += BULLET_SPEED

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 0), (self.x, self.y, self.size, self.size))

    def is_off_screen(self):
        return self.y > BOX_RECT.bottom


# ------------ Boss 戰主函式 ------------
def boss_battle():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Boss Battle – UnderPy")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 24)

    heart = Heart()
    bullets = []
    frame = 0

    running = True
    while running:
        clock.tick(FPS)
        screen.fill((0, 0, 0))

        # ---- 事件 ----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "QUIT"

        # ---- 玩家移動 ----
        keys = pygame.key.get_pressed()
        heart.move(keys)

        # ---- 時間 ----
        frame += 1
        remaining_time = max(0, BATTLE_TIME - frame // FPS)

        # ---- 生成子彈 ----
        if frame % SPAWN_RATE == 0:
            bullets.append(Bullet())

        # ---- 子彈更新 & 碰撞 ----
        for b in bullets[:]:
            b.update()

            if b.is_off_screen():
                bullets.remove(b)
                continue

            if pygame.Rect(b.x, b.y, b.size, b.size).colliderect(
                pygame.Rect(heart.x - heart.r, heart.y - heart.r, heart.r * 2, heart.r * 2)
            ):
                heart.hp -= 20
                bullets.remove(b)

                if heart.hp <= 0:
                    pygame.quit()
                    return "LOSE"

        # ---- 繪圖 ----
        pygame.draw.rect(screen, (255, 255, 255), BOX_RECT, 2)
        heart.draw(screen)

        for b in bullets:
            b.draw(screen)

        screen.blit(font.render(f"HP: {heart.hp}", True, (255, 255, 255)), (20, 20))
        screen.blit(font.render(f"Time: {remaining_time}", True, (255, 255, 255)), (350, 20))

        pygame.display.update()

        # ---- 勝利條件 ----
        if remaining_time <= 0:
            pygame.quit()
            return "WIN"


# ------------ 單獨測試 ------------
if __name__ == "__main__":
    print(boss_battle())
