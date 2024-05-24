import pygame
import sys

# Инициализация Pygame
pygame.init()

# Основные параметры окна
screen_width, screen_height = 600, 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Арканоид")

# Параметры кирпичей
brick_rows = 5
brick_cols = 10
brick_width = screen_width // brick_cols
brick_height = 20
brick_gap = 5  # Промежуток между кирпичами

# Список кирпичей
bricks = [(col * (brick_width + brick_gap), row * (brick_height + brick_gap)) for row in range(brick_rows) for col in range(brick_cols)]

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# ФПС
#🧠 ФПС — количество кадров в секунду
clock = pygame.time.Clock()
fps = 60

# Параметры платформы
paddle_width, paddle_height = 100, 10
paddle_x = (screen_width - paddle_width) // 2
paddle_y = screen_height - paddle_height - 20
paddle_speed = 6

# Параметры мяча
ball_radius = 8
ball_x = screen_width // 2
ball_y = paddle_y - ball_radius
ball_speed_x = 4
ball_speed_y = -4

# Запуск основного цикла игры
running = True
while running:
# Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Движение платформы
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_x > 0:
#🧠 Данная настройка не даёт платформе выйти за пределы экрана
        paddle_x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle_x < screen_width - paddle_width:
        paddle_x += paddle_speed

# Движение мяча
    ball_x += ball_speed_x
    ball_y += ball_speed_y

# Столкновение с краями экрана
    if ball_x <= 0 or ball_x >= screen_width:
        ball_speed_x = -ball_speed_x
    if ball_y <= 0:
        ball_speed_y = -ball_speed_y
    if ball_y >= screen_height:
# Сброс мяча
        ball_x, ball_y = screen_width // 2, paddle_y - ball_radius
        ball_speed_y = -ball_speed_y
        brick_rects = [pygame.Rect(brick[0], brick[1], brick_width, brick_height) for brick in bricks]
for i, brick_rect in enumerate(brick_rects):
    if brick_rect.collidepoint(ball_x, ball_y):
        bricks.pop(i)  # Удаление кирпича
        ball_speed_y = -ball_speed_y  # Изменение направления мяча
        break  # Выход после уничтожения одного кирпича, чтобы не удалять несколько за один кадр

# Столкновение с платформой
    if paddle_x <= ball_x <= paddle_x + paddle_width and paddle_y <= ball_y + ball_radius <= paddle_y + paddle_height:
        ball_speed_y = -ball_speed_y

# Очистка экрана
    screen.fill(BLACK)
    for brick in bricks:
        pygame.draw.rect(screen, WHITE, pygame.Rect(brick[0], brick[1], brick_width, brick_height))

# Рисование объектов
    pygame.draw.rect(screen, WHITE, (paddle_x, paddle_y, paddle_width, paddle_height))
    pygame.draw.circle(screen, BLUE, (ball_x, ball_y), ball_radius)

# Обновление экрана
    pygame.display.flip()

# Контроль ФПС
    clock.tick(fps)
pygame.quit()
sys.exit()