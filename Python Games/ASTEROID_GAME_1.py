import pygame
import random
import sys

pygame.init()

width = 800
height = 600

red = (255,0,0)
blue = (0,0,255)
yellow = (255,255,0)
background = (0,0,0)

player_sizex = 70
player_sizey = 10
player_size = 40
player_posi = [width/2, height-2*player_sizey]
player_speed = 11

enemy_size = 50
enemy_posi = [random.randint(0,width-enemy_size), 0]
enemy_total = [enemy_posi]

blue_speed = 10

screen = pygame.display.set_mode((width, height))

game_over = False


clock = pygame.time.Clock()

myfont = pygame.font.SysFont('8-Bit-Madness', 25)

def enemy_set(enemy_total):
        delay = random.random()
        if len(enemy_total) < 10 and delay < 0.1:
                xpos = random.randint(0,width-enemy_size)
                ypos = 0
                enemy_total.append([xpos, ypos])

def draw_enemies(enemy_total):
        for enemy_posi in enemy_total:
                pygame.draw.rect(screen, blue, (enemy_posi[0], enemy_posi[1], enemy_size, enemy_size))

def update_enemy_positions(enemy_total):
        for idx, enemy_posi in enumerate(enemy_total):
                if enemy_posi[1] >= 0 and enemy_posi[1] < height:
                        enemy_posi[1] += blue_speed
                else:
                        enemy_total.pop(idx)
                        

while not game_over:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
                player_posi[0]-=player_speed
                
        if keys[pygame.K_RIGHT]:
                player_posi[0]+=player_speed
        

        screen.fill(background)

        enemy_set(enemy_total)

        update_enemy_positions(enemy_total)
            
        draw_enemies(enemy_total)

        pygame.draw.rect(screen, red, (player_posi[0], player_posi[1], player_size, player_sizey))

        clock.tick(30)

        pygame.display.update()
