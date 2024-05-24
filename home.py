import pygame
import random

# Инициализация Pygame
pygame.init()

# Параметры окна
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Space Impact')

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Загрузка изображений
player_image = pygame.image.load('hero.png').convert_alpha()
enemy_image = pygame.image.load('enemy.png').convert_alpha()
boss_image = pygame.image.load('boss.png').convert_alpha()

# Шрифты
font = pygame.font.SysFont(None, 55)


# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.center = (100, SCREEN_HEIGHT // 2)
        self.speed_y = 0

    def update(self):
        self.speed_y = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.speed_y = -5
        if keys[pygame.K_DOWN]:
            self.speed_y = 5
        self.rect.y += self.speed_y

        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def shoot(self):
        bullet = Bullet(self.rect.right, self.rect.centery)
        all_sprites.add(bullet)
        bullets.add(bullet)


# Класс пули
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.left = x
        self.speed_x = 10

    def update(self):
        self.rect.x += self.speed_x
        if self.rect.left > SCREEN_WIDTH:
            self.kill()


# Класс врага
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = random.randrange(SCREEN_HEIGHT - self.rect.height)
        self.speed_x = random.randrange(3, 8)

    def update(self):
        self.rect.x -= self.speed_x
        if self.rect.right < 0:
            self.kill()


# Класс босса
class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = boss_image
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = SCREEN_HEIGHT // 2 - self.rect.height // 2
        self.speed_x = 2
        self.health = 10  # Увеличено количество здоровья до 10

    def update(self):
        self.rect.x -= self.speed_x
        if self.rect.right < 0:
            self.kill()

    def hit(self):
        self.health -= 1
        if self.health <= 0:
            self.kill()


# Создание групп спрайтов
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
bosses = pygame.sprite.Group()

# Создание игрока
player = Player()
all_sprites.add(player)

# Основной цикл игры
running = True
shooting = False
shoot_delay = 250  # Задержка между выстрелами в миллисекундах
last_shot = pygame.time.get_ticks()
clock = pygame.time.Clock()
enemy_kills = 0
boss_kills = 0
boss_spawned = False


def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)


while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                shooting = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                shooting = False

    # Автоматическая стрельба
    if shooting:
        now = pygame.time.get_ticks()
        if now - last_shot >= shoot_delay:
            player.shoot()
            last_shot = now

    # Создание новых врагов, если босс не на экране
    if not boss_spawned and random.random() < 0.02:
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Проверка на столкновение пуль с врагами
    hits = pygame.sprite.groupcollide(bullets, enemies, True, True)
    if hits:
        enemy_kills += len(hits)

    # Спавн босса каждые 25 уничтоженных врагов
    if enemy_kills >= 25 and not boss_spawned:
        boss = Boss()
        all_sprites.add(boss)
        bosses.add(boss)
        boss_spawned = True
        enemy_kills = 0  # Сброс количества убийств врагов

    # Урон боссу при попадании пули
    boss_hits = pygame.sprite.groupcollide(bullets, bosses, True, False)
    for boss in boss_hits:
        boss.hit()
        if boss.health <= 0:
            boss_spawned = False
            boss_kills += 1
            running = False  # Игра заканчивается при уничтожении босса

    # Обновление всех спрайтов
    all_sprites.update()

    # Проверка на столкновение игрока с врагами и боссами
    if pygame.sprite.spritecollide(player, enemies, False) or pygame.sprite.spritecollide(player, bosses, False):
        running = False

    # Отрисовка всех спрайтов
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Отображение сообщения "BOSS" при появлении босса
    if boss_spawned:
        draw_text(screen, '-=BOSS=-', 72, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    pygame.display.flip()

pygame.quit()
