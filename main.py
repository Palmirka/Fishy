import game
import menu
import pygame
import leaderboard

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1000, 800))
    pygame.display.set_caption('Fishy')
    icon = pygame.image.load('images/icon.ico')
    pygame.display.set_icon(icon)

    bg = pygame.image.load("images/bg.jpg")
    bg = pygame.transform.scale(bg, (1000, 800))

    # State of game [menu, game, leaderboard]
    state = 'menu'
    while True:
        screen.blit(bg, (0, 0))
        if state == 'game':
            state = game.gameplay(screen)
        elif state == 'menu':
            game.restart()
            state = menu.start_menu(screen)
        elif state == 'leaderboard':
            state = leaderboard.show_results(screen) or state
