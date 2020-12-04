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


player_sizey = 10
player_sizex = 50
player_posi = [width/2, height-2*player_sizey]
player_speed = 11

enemy_size = 50
enemy_posi = [random.randint(0,width-enemy_size), 0]
enemy_total = [enemy_posi]

blue_speed = 10

screen = pygame.display.set_mode((width, height))

game_over = False

score = 0

clock = pygame.time.Clock()

myfont = pygame.font.SysFont('8-Bit-Madness', 25)

def set_level(score, blue_speed):
        if score < 20:
                blue_speed = 5
        elif score < 40:
                blue_speed = 8
        elif score < 60:
                blue_speed = 12
        else:
                blue_speed = 15
        return blue_speed
        # SPEED = score/5 + 1


def enemy_set(enemy_total):
        delay = random.random()
        if len(enemy_total) < 10 and delay < 0.1:
                xpos = random.randint(0,width-enemy_size)
                ypos = 0
                enemy_total.append([xpos, ypos])

def draw_enemies(enemy_total):
        for enemy_posi in enemy_total:
                pygame.draw.rect(screen, blue, (enemy_posi[0], enemy_posi[1], enemy_size, enemy_size))

def update_enemy_positions(enemy_total, score):
        for idx, enemy_posi in enumerate(enemy_total):
                if enemy_posi[1] >= 0 and enemy_posi[1] < height:
                        enemy_posi[1] += blue_speed
                else:
                        enemy_total.pop(idx)
                        score += 1
        return score

def collision_check(enemy_total, player_posi):
        for enemy_posi in enemy_total:
                if detect_collision(enemy_posi, player_posi):
                        return True
        return False

def detect_collision(player_posi, enemy_posi):
        px = player_posi[0]
        py = player_posi[1]

        ex = enemy_posi[0]
        ey = enemy_posi[1]

        if (ex >= px and ex < (px + player_sizex)) or (px >= ex and px < (ex+enemy_size)):
                if (ey >= py and ey < (py + player_sizey)) or (py >= ey and py < (ey+enemy_size)):
                        return True
        return False

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
        score = update_enemy_positions(enemy_total, score)
        blue_speed = set_level(score, blue_speed)

        text = "Score:" + str(score)
        label = myfont.render(text, 1, yellow)
        screen.blit(label, (width-200, height-40))

        if collision_check(enemy_total, player_posi):
                game_over = True
                break
                
              
            

        draw_enemies(enemy_total)

        pygame.draw.rect(screen, red, (player_posi[0], player_posi[1], player_sizex, player_sizey))

        clock.tick(30)

        pygame.display.update()
