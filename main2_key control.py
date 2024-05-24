import pygame
pygame.init()

window_size = (1280, 1024)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Test project")

image = pygame.image.load("picPygame.png")
image_rect = image.get_rect()

speed = 5

run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        image_rect.x -= speed
    if keys[pygame.K_RIGHT]:
        image_rect.x += speed
    if keys[pygame.K_UP]:
        image_rect.y -= speed
    if keys[pygame.K_DOWN]:
        image_rect.y += speed

    screen.fill((255, 255, 255))
    screen.blit(image, image_rect)
    pygame.display.flip()

pygame.quit()