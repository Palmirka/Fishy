import threading
import leaderboard
import menu
import random
import pygame
import sys

speed = 0.05
start_size_x = 64
start_size_y = 36


class Enemy:
    """Enemy"""
    def __init__(self, left, y, enemy_speed, size, bigger):
        self.size = size
        if bigger:
            self.img = pygame.image.load('images/enemyImg.png')
        else:
            self.img = pygame.image.load('images/smallEnemyImg.png')
        self.img = pygame.transform.scale(self.img, (size, size))
        self.left = left
        self.y = y
        self.speed = enemy_speed
        if left:
            self.x = 1000
        else:
            self.img = pygame.transform.flip(self.img, True, False)
            self.x = -start_size_x

    def move(self, screen):
        if self.left:
            self.x -= self.speed
        else:
            self.x += self.speed
        screen.blit(self.img, (self.x, self.y))


class Player:
    """Player"""
    def __init__(self, x=500, y=400):
        self.img = pygame.image.load('images/playerImg.png')
        self.original_img = self.img
        self.left = True
        self.x = x
        self.y = y
        self.size_x = start_size_x
        self.size_y = start_size_y

    def turn(self, side):
        """Turn player"""
        if side != self.left:
            self.left = not self.left
            self.img = pygame.transform.flip(self.img, True, False)

    def move(self, screen):
        """Move player"""
        screen.blit(self.img, (self.x, self.y))

    def set_position(self, x, y):
        """Set position"""
        if -1 < x < 921:
            self.x = x
        if -1 < y < 721:
            self.y = y

    def resize(self, points):
        """Resize"""
        self.size_x += points
        self.size_y += points*0.5625
        self.img = pygame.transform.scale(self.original_img, (self.size_x, self.size_y))
        if not self.left:
            self.img = pygame.transform.flip(self.img, True, False)


def move_enemies(enemy, screen):
    """Move enemies"""
    for i in enemy:
        i.move(screen)
        if (-1)*i.size > i.x or i.x > 1000 + i.size:
            enemy.remove(i)


def catch_keys(player):
    """Handle keyword actions"""
    keys = pygame.key.get_pressed()  # checking pressed keys
    if keys[pygame.K_UP]:
        player.set_position(-1, player.y - speed)
    if keys[pygame.K_DOWN]:
        player.set_position(-1, player.y + speed)
    if keys[pygame.K_RIGHT]:
        player.turn(False)
        player.set_position(player.x + speed, -1)
    if keys[pygame.K_LEFT]:
        player.turn(True)
        player.set_position(player.x - speed, -1)


def spawn_enemy(enemy, player):
    """Spawn enemy"""
    if not random.randint(0, 200):
        left = random.randint(0, 2)
        enemy_speed = random.randint(0, 60) / 100 + 0.3
        enemy_size = random.randint(int(start_size_x * 0.3), start_size_x * 4)
        y = random.randint(0, 800 - enemy_size)
        enemy.append(Enemy(left, y, enemy_speed, enemy_size, enemy_size > player.size_x))


def check_collisions(player, enemy):
    """Check collision"""
    x = player.x
    y = player.y
    size_x = player.size_x
    size_y = player.size_y
    for i in enemy:
        if i.y + i.size * 0.25 < y + size_y < i.y + i.size * 0.75 or i.y + i.size * 0.25 < y < i.y + i.size * 0.75 \
                or y < i.y + i.size * 0.75 < y + size_y or y < i.y + i.size * 0.25 < y + size_y:
            if i.x < x + size_x < i.x + i.size or i.x < x < i.x + i.size \
                    or x < i.x + i.size < x + size_x or x < i.x < x + size_x:
                if size_x >= i.size:
                    player.resize(i.size*0.1)
                    enemy.remove(i)
                else:
                    return 1
    return 0


class Game:
    """Game data"""
    state = 'game'
    first = True


players = Player()
enemies = []
threads = []
game = Game()


def restart():
    """Restart game"""
    game.state = 'game'
    game.first = True
    enemies.clear()
    players.set_position(500, 400)
    players.resize(64-players.size_x)


def player_thread(player, screen, enemy):
    """Player thread"""
    while not check_collisions(players, enemy):
        catch_keys(player)
        player.move(screen)
    leaderboard.add(menu.name, player.size_x - 64)
    game.state = 'menu'


def gameplay(screen):
    """Gameplay"""
    if game.first:
        threads.clear()
        threads.append(threading.Thread(target=player_thread, args=(players, screen, enemies)))
        for thread in threads:
            thread.start()
        game.first = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    spawn_enemy(enemies, players)
    move_enemies(enemies, screen)
    pygame.display.update()
    return game.state
