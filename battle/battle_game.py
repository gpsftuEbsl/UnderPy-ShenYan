import pygame
import random
import math
import sys
from config import (
    BATTLE_WINDOW_WIDTH, BATTLE_WINDOW_HEIGHT, BATTLE_FPS,
    BATTLE_BOX_RECT, HEART_SIZE, HEART_SPEED, HEART_HP,
    BULLET_SIZE, BULLET_SPEED, BULLET_SPAWN_INTERVAL, BULLET_DAMAGE,
    CIRCLE_BULLET_RADIUS, CIRCLE_BULLET_SPEED, CIRCLE_BULLET_SPAWN_INTERVAL, CIRCLE_BULLET_DAMAGE,
    WAVE_BULLET_SIZE, WAVE_BULLET_SPEED, WAVE_BULLET_SPAWN_INTERVAL, WAVE_BULLET_AMPLITUDE, WAVE_BULLET_DAMAGE,
    HOMING_BULLET_SIZE, HOMING_BULLET_SPAWN_INTERVAL, HOMING_BULLET_LIFE, HOMING_BULLET_POWER, HOMING_BULLET_DAMAGE,
    INTERN_BATTLE_TIME, FINAL_BOSS_BATTLE_TIME
)


# ================= 基本設定與初始化 =================
WIDTH, HEIGHT = BATTLE_WINDOW_WIDTH, BATTLE_WINDOW_HEIGHT
FPS = BATTLE_FPS

# 轉換 BATTLE_BOX_RECT 為 pygame.Rect
_x, _y, _w, _h = BATTLE_BOX_RECT
BOX_RECT = pygame.Rect(_x, _y, _w, _h)

HEART_SPEED = HEART_SPEED
PLAYER_HP = HEART_HP


def init_pygame():
    """初始化 Pygame，返回 (screen, clock, font) 或 None 以表示失敗"""
    try:
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        clock = pygame.time.Clock()
        font = pygame.font.SysFont("arial", 24)
        return screen, clock, font
    except Exception as e:
        print(f"Pygame 初始化失敗：{e}")
        return None


# ================= 玩家（心型） =================
class Heart:
    def __init__(self):
        self.x = BOX_RECT.centerx
        self.y = BOX_RECT.centery
        self.size = HEART_SIZE
        self.hp = PLAYER_HP

    def move(self, keys):
        if keys[pygame.K_UP] and self.y - self.size > BOX_RECT.top:
            self.y -= HEART_SPEED
        if keys[pygame.K_DOWN] and self.y + self.size < BOX_RECT.bottom:
            self.y += HEART_SPEED
        if keys[pygame.K_LEFT] and self.x - self.size > BOX_RECT.left:
            self.x -= HEART_SPEED
        if keys[pygame.K_RIGHT] and self.x + self.size < BOX_RECT.right:
            self.x += HEART_SPEED

    def draw(self, screen):
        points = []
        for t in range(0, 360, 12):
            rad = math.radians(t)
            x = 16 * math.sin(rad) ** 3
            y = (
                13 * math.cos(rad)
                - 5 * math.cos(2 * rad)
                - 2 * math.cos(3 * rad)
                - math.cos(4 * rad)
            )
            px = self.x + x * self.size / 16
            py = self.y - y * self.size / 16
            points.append((px, py))
        pygame.draw.polygon(screen, (255, 0, 0), points)


# ================= 普通 Boss 子彈 =================
class Bullet:
    def __init__(self):
        self.size = BULLET_SIZE
        self.x = random.randint(BOX_RECT.left, BOX_RECT.right - self.size)
        self.y = BOX_RECT.top
        self.speed = BULLET_SPEED

    def update(self):
        self.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 0),
                         (self.x, self.y, self.size, self.size))

    def rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def is_off(self):
        return self.y > BOX_RECT.bottom


# ================= 普通 Boss（原本保留） =================
def boss_battle():
    """第一關實習生戰鬥"""
    init_result = init_pygame()
    if init_result is None:
        return "ERROR"
    
    screen, clock, font = init_result
    pygame.display.set_caption("Boss Battle")
    
    try:
        heart = Heart()
        bullets = []
        frame = 0
        TOTAL_TIME = INTERN_BATTLE_TIME  # set 15-20 (正常)

        while True:
            clock.tick(FPS)
            screen.fill((0, 0, 0))
            frame += 1
            remaining_time = max(0, TOTAL_TIME - frame // FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return "QUIT"

            heart.move(pygame.key.get_pressed())

            if frame % BULLET_SPAWN_INTERVAL == 0:
                bullets.append(Bullet())

            for b in bullets[:]:
                b.update()
                if b.is_off():
                    bullets.remove(b)
                    continue

                if b.rect().colliderect(
                    pygame.Rect(
                        heart.x - heart.size,
                        heart.y - heart.size,
                        heart.size * 2,
                        heart.size * 2
                    )
                ):
                    heart.hp -= BULLET_DAMAGE
                    bullets.remove(b)
                    if heart.hp <= 0:
                        pygame.quit()
                        return "LOSE"

            pygame.draw.rect(screen, (255, 255, 255), BOX_RECT, 2)
            heart.draw(screen)
            for b in bullets:
                b.draw(screen)

            screen.blit(font.render(f"HP: {heart.hp}", True, (255, 255, 255)), (20, 20))
            screen.blit(font.render(f"Time: {remaining_time}", True, (255, 255, 255)), (350, 20))

            pygame.display.update()

            if remaining_time <= 0:
                pygame.quit()
                return "WIN"
    except Exception as e:
        print(f"戰鬥過程出錯：{e}")
        pygame.quit()
        return "ERROR"


# ================= Final Boss 子彈 =================
class CircleBullet:
    def __init__(self):
        self.r = CIRCLE_BULLET_RADIUS
        self.x = random.randint(BOX_RECT.left, BOX_RECT.right)
        self.y = BOX_RECT.top
        self.speed = CIRCLE_BULLET_SPEED

    def update(self):
        self.y += self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 200, 0), (self.x, self.y), self.r)

    def rect(self):
        return pygame.Rect(self.x - self.r, self.y - self.r, self.r * 2, self.r * 2)


class WaveBullet:
    def __init__(self):
        self.base_x = random.randint(BOX_RECT.left, BOX_RECT.right)
        self.y = BOX_RECT.top
        self.t = random.randint(0, 360)
        self.size = WAVE_BULLET_SIZE

    def update(self):
        self.y += WAVE_BULLET_SPEED
        self.t += 10
        self.x = self.base_x + math.sin(math.radians(self.t)) * WAVE_BULLET_AMPLITUDE

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 200, 255),
                         (self.x, self.y, self.size, self.size))

    def rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)


class HomingBullet:
    """追蹤子彈（有壽命，會自爆）"""
    def __init__(self, target):
        self.target = target
        self.x = random.choice([BOX_RECT.left, BOX_RECT.right])
        self.y = random.randint(BOX_RECT.top, BOX_RECT.bottom)
        self.size = HOMING_BULLET_SIZE

        self.life = HOMING_BULLET_LIFE        # ★ 追蹤 3 秒後自爆
        self.homing_power = HOMING_BULLET_POWER

    def update(self):
        self.x += (self.target.x - self.x) * self.homing_power
        self.y += (self.target.y - self.y) * self.homing_power
        self.life -= 1

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 80, 80),
                           (int(self.x), int(self.y)), self.size)

    def rect(self):
        return pygame.Rect(
            self.x - self.size,
            self.y - self.size,
            self.size * 2,
            self.size * 2
        )


# ================= Final Boss（三階段） =================
def final_boss_battle():
    """最終 Boss 三階段戰鬥"""
    init_result = init_pygame()
    if init_result is None:
        return "ERROR"
    
    screen, clock, font = init_result
    pygame.display.set_caption("FINAL BOSS")
    
    try:
        heart = Heart()
        bullets = []
        frame = 0
        TOTAL_TIME = FINAL_BOSS_BATTLE_TIME # set 50 (>50 我覺得太難了)

        while True:
            clock.tick(FPS)
            screen.fill((0, 0, 0))
            frame += 1
            remaining_time = max(0, TOTAL_TIME - frame // FPS)

            # ---- Phase 判定 ----
            if remaining_time > 40:
                phase = 1
            elif remaining_time > 20:
                phase = 2
            else:
                phase = 3

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return "QUIT"

            heart.move(pygame.key.get_pressed())

            # ---- 生成子彈 ----
            if phase == 1:
                if frame % CIRCLE_BULLET_SPAWN_INTERVAL == 0:
                    bullets.append(CircleBullet())

            elif phase == 2:
                if frame % WAVE_BULLET_SPAWN_INTERVAL == 0:
                    bullets.append(WaveBullet())

            else:
                if frame % HOMING_BULLET_SPAWN_INTERVAL == 0:
                    bullets.append(HomingBullet(heart))

                if frame % (CIRCLE_BULLET_SPAWN_INTERVAL * 2) == 0:
                    bullets.append(CircleBullet())


            # ---- 更新子彈 ----
            for b in bullets[:]:
                b.update()

                # ★ 追蹤子彈自爆（時間到）
                if isinstance(b, HomingBullet) and b.life <= 0:
                    bullets.remove(b)
                    continue

                if not BOX_RECT.colliderect(b.rect()):
                    bullets.remove(b)
                    continue

                if b.rect().colliderect(
                    pygame.Rect(
                        heart.x - heart.size,
                        heart.y - heart.size,
                        heart.size * 2,
                        heart.size * 2
                    )
                ):
                    heart.hp -= CIRCLE_BULLET_DAMAGE if phase < 3 else HOMING_BULLET_DAMAGE
                    bullets.remove(b)
                    if heart.hp <= 0:
                        pygame.quit()
                        return "LOSE"

            # ---- 繪圖 ----
            pygame.draw.rect(screen, (255, 0, 0), BOX_RECT, 2)
            heart.draw(screen)
            for b in bullets:
                b.draw(screen)

            screen.blit(font.render(f"FINAL BOSS PHASE {phase}", True, (255, 100, 100)), (120, 10))
            screen.blit(font.render(f"HP: {heart.hp}", True, (255, 255, 255)), (20, 330))
            screen.blit(font.render(f"Time: {remaining_time}", True, (255, 255, 255)), (350, 330))

            pygame.display.update()

            if remaining_time <= 0:
                pygame.quit()
                return "WIN"
    except Exception as e:
        print(f"戰鬥過程出錯：{e}")
        pygame.quit()
        return "ERROR"


# ================= 測試選單 =================
def main():
    print("=== Battle Test Menu ===")
    print("1. Normal Boss Battle")
    print("2. Final Boss Battle")
    print("3. Exit")

    choice = input("Choose: ")

    if choice == "1":
        print(boss_battle())
    elif choice == "2":
        print(final_boss_battle())
    else:
        sys.exit()


if __name__ == "__main__":
    main()
