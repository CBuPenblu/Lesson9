import pygame
pygame.init()
import time

window_size = (1280, 1024)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Test project")

image1 = pygame.image.load("picPygame.png")
image_rect1 = image1.get_rect()

image2 = pygame.image.load("picPython.png")
image_rect2 = image2.get_rect()

run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEMOTION:
            mouseX, mouseY = pygame.mouse.get_pos()
            image_rect1.x = mouseX - 250
            image_rect1.y = mouseY - 250

    if image_rect1.colliderect(image_rect2):
        print("Objects hit each other")
        time.sleep(1)


    screen.fill((255, 255, 255))
    screen.blit(image1, image_rect1)
    screen.blit(image2, image_rect2)
    pygame.display.flip()

pygame.quit()