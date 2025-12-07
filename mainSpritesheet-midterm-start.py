import pygame
from player import Character

pygame.init()

screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Sprite Animation Test")

clock = pygame.time.Clock()
player = Character((300, 350))

run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    player.handle_keys(keys)

    screen.fill((100, 100, 100))
    screen.blit(player.image, player.rect)
    pygame.display.flip()

pygame.quit()
