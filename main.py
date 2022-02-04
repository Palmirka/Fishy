import game
import menu
import pygame
import leaderboard

pygame.init()
screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption('Fishy')
icon = pygame.image.load('images/icon.ico')
pygame.display.set_icon(icon)

bg = pygame.image.load("images/bg.jpg")
bg = pygame.transform.scale(bg, (1000, 800))

# State of game [menu, game, leaderboards]
state = 1
while True:
    screen.blit(bg, (0, 0))
    if state == 0:
        state = game.gameplay(screen)
    elif state == 1:
        game.restart()
        state = menu.start_menu(screen)
    elif state == 2:
        leaderboard.show_results(screen)
