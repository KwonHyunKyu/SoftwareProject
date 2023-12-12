import pygame
import random

# 초기화
pygame.init()

# 화면 크기 설정
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("우주선 슈팅 게임")

# 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

# 이미지 로드 함수
def load_image(image_path):
    return pygame.image.load(image_path).convert_alpha()

# 우주선 설정
spaceship_img = load_image("spaceship.png")
spaceship_width = 64
spaceship_height = 64
spaceship_x = screen_width // 2 - spaceship_width // 2
spaceship_y = screen_height - spaceship_height - 10
spaceship_speed = 7

# 총알 설정
bullet_img = load_image("bullet.png")
bullet_width = 16
bullet_height = 32
bullet_speed = 10
bullets = []

# 적 설정
enemy_img = load_image("enemy.png")
enemy_width = 64
enemy_height = 64
enemy_speed = 3
enemies = []

# 점수
score = 0
font = pygame.font.Font(None, 36)

# 배경 별 생성
stars = []
for _ in range(100):
    x = random.randint(0, screen_width)
    y = random.randint(0, screen_height)
    stars.append([x, y])

# 게임 루프
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet_x = spaceship_x + spaceship_width // 2 - bullet_width // 2
                bullet_y = spaceship_y
                bullets.append([bullet_x, bullet_y])

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and spaceship_x > 0:
        spaceship_x -= spaceship_speed
    if keys[pygame.K_RIGHT] and spaceship_x < screen_width - spaceship_width:
        spaceship_x += spaceship_speed

    for bullet in bullets:
        bullet[1] -= bullet_speed
        if bullet[1] < 0:
            bullets.remove(bullet)

    if len(enemies) < 5:
        enemy_x = random.randint(0, screen_width - enemy_width)
        enemy_y = random.randint(-500, -50)
        enemies.append([enemy_x, enemy_y])

    for enemy in enemies:
        enemy[1] += enemy_speed
        if enemy[1] > screen_height:
            enemies.remove(enemy)
            score += 1

        enemy_rect = enemy_img.get_rect(topleft=(enemy[0], enemy[1]))
        spaceship_rect = pygame.Rect(spaceship_x, spaceship_y, spaceship_width, spaceship_height)
        if enemy_rect.colliderect(spaceship_rect):
            running = False

        for bullet in bullets:
            bullet_rect = bullet_img.get_rect(topleft=(bullet[0], bullet[1]))

            if bullet_rect.colliderect(enemy_rect):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 1

    for bullet in bullets:
        screen.blit(bullet_img, (bullet[0], bullet[1]))

    for enemy in enemies:
        screen.blit(enemy_img, (enemy[0], enemy[1]))

    screen.blit(spaceship_img, (spaceship_x, spaceship_y))

    # 배경 별 표시
    for star in stars:
        pygame.draw.circle(screen, WHITE, star, 1)

    score_text = font.render("Score: " + str(score), True, YELLOW)
    screen.blit(score_text, (10, 10))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
