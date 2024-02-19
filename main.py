import math

import pygame
import random
from pygame import mixer


pygame.init()

screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)
background = pygame.image.load("bg.jpg")


# mixer.music.load("music.wav")
# mixer.music.play(-1)

playerIMG = pygame.image.load("player.png")
playerX = 400 - 32
playerY = 480
playerX_change = 0
speedP = 0.3

enemyIMG = pygame.image.load("enemy.png")

enemies = []


def add_enemy(enemyX, enemyY, speedE, direction, enemyY_move):
    enemy = {"enemyX": enemyX,
             "enemyY": enemyY,
             "speedE": speedE,
             "enemyX_change": speedE if direction == "left" else -speedE,
             "enemyY_move": enemyY_move}
    enemies.append(enemy)


add_enemy(random.randint(0, 800-64), 50, 0.3, "right", 40)

bulletIMG = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 0
speedB = 0.5
firing = False


def is_collided(x1, y1, x2, y2):
    return math.sqrt((math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2))) < 27


def draw_player(x, y):
    screen.blit(playerIMG, (x, y))


def draw_enemy(x, y):
    screen.blit(enemyIMG, (x, y))


def fire(x, y):
    global firing
    firing = True
    screen.blit(bulletIMG, (x, y))


score_value = 0
level = 1

font = pygame.font.Font("freesansbold.ttf", 26)


def show_score_and_level():
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (10, 10))
    score = font.render("Level : " + str(level), True, (255, 255, 255))
    screen.blit(score, (10, 40))


def game_over():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.fill((32, 32, 32))
        over_font = pygame.font.Font("freesansbold.ttf", 64)
        over_text = over_font.render("GAME OVER", True, (255, 255, 255))
        score_text = over_font.render("Score : " + str(score_value), True, (255, 255, 255))
        screen.blit(score_text, (200, 350))
        level_text = over_font.render("Level : " + str(level), True, (255, 255, 255))
        screen.blit(level_text, (200, 450))
        screen.blit(over_text, (200, 250))

        pygame.display.update()


running = True
while running:
    # screen.fill((32, 32, 32))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -speedP
            if event.key == pygame.K_RIGHT:
                playerX_change = speedP
            if event.key == pygame.K_SPACE:
                bulletX = playerX + 16
                bulletY = playerY
                fire(bulletX, bulletY)
                # bullet_sound = mixer.Sound("fire.wav")
                # bullet_sound.play()
        if event.type == pygame.KEYUP:
            playerX_change = 0

    draw_player(playerX, playerY)
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 800 - 64:
        playerX = 800 - 64

    for e in enemies:
        if is_collided(e["enemyX"], e["enemyY"], bulletX, bulletY) and firing:
            firing = False
            score_value += 1
            enemies.remove(e)
            if score_value < 5:
                add_enemy(random.randint(0, 800-64), 50, 0.3, "right", 40)
            elif score_value < 7:
                level += 1
                add_enemy(random.randint(0, 800 - 64), 80, 0.3, "right", 40)
                add_enemy(random.randint(0, 800 - 64), 80, 0.4, "left", 40)
            elif score_value < 10:
                add_enemy(random.randint(0, 800 - 64), 80, 0.3, "left", 40)
            elif score_value < 12:
                level += 1
                add_enemy(random.randint(0, 800 - 64), 80, 0.4, "right", 60)
                add_enemy(random.randint(0, 800 - 64), 80, 0.3, "left", 60)
            elif score_value < 15:
                add_enemy(random.randint(0, 800 - 64), 100, 0.3, "left", 60)
            elif score_value < 17:
                level += 1
                add_enemy(random.randint(0, 800 - 64), 100, 0.4, "right", 60)
                add_enemy(random.randint(0, 800 - 64), 100, 0.3, "left", 60)
            elif score_value < 20:
                add_enemy(random.randint(0, 800 - 64), 80, 0.4, "right", 40)
            elif score_value < 22:
                level += 1
                add_enemy(random.randint(0, 800 - 64), 80, 0.3, "right", 60)
                add_enemy(random.randint(0, 800 - 64), 100, 0.4, "left", 60)
                add_enemy(random.randint(0, 800 - 64), 120, 0.3, "right", 40)
            elif score_value > 22:
                level += 1
                add_enemy(random.randint(0, 800 - 64), 120, 0.3, "left", 60)
                add_enemy(random.randint(0, 800 - 64), 100, 0.4, "right", 60)
        elif e["enemyY"] >= 460 - 64:
            running = False
            game_over()
        else:
            if e["enemyX"] <= 0:
                e["enemyX_change"] = e["speedE"]
                e["enemyY"] += e["enemyY_move"]
            elif e["enemyX"] >= 800 - 64:
                e["enemyX_change"] = -e["speedE"]
                e["enemyY"] += e["enemyY_move"]
            e["enemyX"] += e["enemyX_change"]
            draw_enemy(e["enemyX"], e["enemyY"])

    if firing:
        bulletY -= speedB
        if bulletY <= 0:
            firing = False
        fire(bulletX, bulletY)

    rectangle = pygame.Rect(0, 460, 800, 5,)
    pygame.draw.rect(screen, (255, 255, 255), rectangle)
    show_score_and_level()
    pygame.display.update()
