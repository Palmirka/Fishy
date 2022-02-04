import pygame
import sys


class Button:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.size_x = 300
        self.size_y = 64
        self.img = pygame.transform.scale(img, (self.size_x, self.size_y))

    def display_text(self, screen, text):
        my_font = pygame.font.SysFont('Comic Sans MS', 30)
        text_surf = my_font.render(text, True, (0, 0, 0))
        screen.blit(self.img, (self.x, self.y))
        screen.blit(text_surf, (self.x+5, self.y+5))
        pygame.display.update()

    def display(self, screen):
        screen.blit(self.img, (self.x, self.y))

    def mouse_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if self.y < y < self.y + self.size_y and self.x < x < self.x + self.size_x:
                return 1
        return 0


name = 'Player'
start_pic = pygame.image.load('images/start_button.png')
scores_pic = pygame.image.load('images/scores_button.png')
exit_pic = pygame.image.load('images/exit_button.png')
input_pic = pygame.image.load('images/input.png')
buttons = [Button(350, 350, start_pic), Button(350, 500, scores_pic), Button(350, 650, exit_pic),
           Button(350, 200, input_pic)]


def get_name():
    return name


def set_name(x):
    global name
    name = x


def start_menu(screen):
    for i in buttons:
        i.display(screen)
    buttons[3].display_text(screen, name)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or buttons[2].mouse_click(event):
            pygame.quit()
            sys.exit()
        if buttons[0].mouse_click(event):
            return 0
        if buttons[1].mouse_click(event):
            return 2
        if buttons[3].mouse_click(event):
            x = True
            while x:
                for e in pygame.event.get():
                    if e.type == pygame.KEYDOWN:
                        if e.key == pygame.K_BACKSPACE:
                            if len(get_name()) > 0:
                                set_name(get_name()[:-1])
                        elif len(get_name()) < 12:
                            set_name(get_name()+e.unicode)
                        buttons[3].display_text(screen, get_name())
                    elif e.type == pygame.MOUSEBUTTONDOWN:
                        x = False
                    elif e.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

    pygame.display.update()
    return 1
