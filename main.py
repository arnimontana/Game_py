from os import listdir
import pygame
import random
from pygame.constants import QUIT, K_DOWN, K_UP, K_RIGHT, K_LEFT

pygame.init()

FPS = pygame.time.Clock()

screen = width, height = 800, 600

BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
GREEN = 0, 255, 0
BLUE = 0, 0, 255

font = pygame.font.SysFont('Verdana', 20)

main_surface = pygame.display.set_mode(screen)

IMGS_PATH = 'goose'

# player = pygame.Surface((20, 20))
#player.fill(WHITE)
player_imgs = [pygame.image.load(IMGS_PATH + '/' + file).convert_alpha() for file in listdir(IMGS_PATH)]
player = player_imgs [0]
player_rect = player.get_rect()
player_speed = 10

def create_enemy():
    #enemy = pygame.Surface((20, 20))
    #enemy.fill(RED)
    
    enemy = pygame.image.load ('enemy.png').convert_alpha()
        
    enemy_rect = pygame.Rect(width, random.randint(0, height), *enemy.get_size())
    enemy_speed = random.randint(2, 5)
    return [enemy, enemy_rect, enemy_speed]

def create_bonus():
    #bonus = pygame.Surface((20, 20))
    #bonus.fill(GREEN)
    
    bonus = pygame.image.load('bonus.png').convert_alpha()
    
    bonus_rect = pygame.Rect(random.randint(0, width), -bonus.get_height(), *bonus.get_size())
    bonus_speed = random.randint(4, 6)
    return [bonus, bonus_rect, bonus_speed]

bg = pygame.image.load ('background.png').convert()
bgX = 0
bgX2 = bg.get_width()
bg_speed = 3

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 2500)

CHANGE_IMG = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMG, 125)

img_index = 0

scores = 0

enemies = []
bonuses = []

is_working = True

while is_working:

    FPS.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False

        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())

        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())

        if event.type == CHANGE_IMG:
            img_index += 1
            if img_index == len(player_imgs):
                img_index = 0
            player = player_imgs[img_index]
            
        
        pressed_keys = pygame.event.get_pressed()

    #main_surface.fill(BLACK)

    #main_surface.blit(bg, (0, 0))

    bgX -= bg_speed
    bgX2 -= bg_speed

    if bgX < bg.get_width():
        bgX = bg.get_width()

    if bgX2 < -bg.get_width():
        bgX2 = bg.get_width()

    #main_surface.blit(ball, ball_rect)

    main_surface.blit(font.render(str(scores), True, WHITE), (width - 30, 0))
    
    main_surface.blit(font.render(str(scores), True, WHITE), width - 30, 0)

    for enemy in enemies:
        enemy[1] = enemy[1].move(-enemy[2],0)
        main_surface.blit(enemy[0], enemy_rect[1])

        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

        if ball_rect.colliderect(enemy[1]):
            is_working = False

    for bonus in bonuses:
        bonus [1] = bonus[1].move(0, bonus[2])
        main_surface.blit(bonus[0], bonus[1])

        if bonus[1].bottom >= height:
            bonuses.pop(bonuses.index(bonus))

        if ball_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            scores += 1

    if pressed_keys[K_DOWN] and not ball_rect.bottom >= height:
        ball_rect = ball_rect.move(0, ball_speed)

    if pressed_keys[K_UP] and not ball_rect.top >= height:
        ball_rect = ball_rect.move(0, -ball_speed)
        
    if pressed_keys[K_RIGHT] and not ball_rect.left >= width:
        ball_rect = ball_rect.move(ball_speed, 0)
        
    if pressed_keys[K_LEFT] and not ball_rect.right >= width:
        ball_rect = ball_rect.move(-ball_speed, 0)

    enemy_rect = enemy_rect.move(-enemy_speed, 0)

pygame.display.flip()