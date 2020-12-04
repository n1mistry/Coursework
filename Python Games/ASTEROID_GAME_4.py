import pygame
import random
import sys
pygame.init()

width = 800    #screen size
height = 600

red = (255,0,0)       #colours
blue = (0,0,255)
yellow = (255,255,0)
start = (50,64,84)
background = (77, 7, 0)
green = (7,240,15)
white = (255,255,255)

spaceship = pygame.image.load('tiefighter.png')  #loading images
asteroid = pygame.image.load('Asteroid.png')
goldcoin = pygame.image.load('goldcoin.png')

player_sizey = 50
player_sizex = 50
player_posi = [width/2, height-2*player_sizey]
player_speed = 11
lives = 3

asteroid_size = 50
asteroid_posi = [random.randint(0,width-asteroid_size), 0]
asteroid_total = [asteroid_posi]
asteroid_speed = 6

goldcoin_size = 50
goldcoin_posi = [random.randint(0,width-asteroid_size), 0]
goldcoin_total = [goldcoin_posi]
goldcoin_speed = 5

star_size = 5
star_posi = [random.randint(0,width-asteroid_size), 0]
star_total = [star_posi]
star_speed = 3

beamX = 0
beamY = 480
beamX_change = 0
beamY_change = 50
beam_state = "ready"

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Space Game")
pygame.display.set_icon(spaceship)

game_over = False

score = 0

clock = pygame.time.Clock()

myfont = pygame.font.SysFont('8-Bit-Madness', 25)

#asteroids functions
def asteroid_level(score, asteroid_speed):
        if score < 20:
                asteroid_speed = 6
               
        elif score < 40:
                asteroid_speed = 9
                           
        elif score < 60:
                asteroid_speed = 13
                
        else:
                asteroid_speed = 16                        
        return asteroid_speed

def asteroid_set(asteroid_total):
        delay = random.random()
        if len(asteroid_total) < 10 and delay < 0.1:
                xpos = random.randint(0,width-asteroid_size)
                ypos = 0
                asteroid_total.append([xpos, ypos])

def draw_asteroid(asteroid_total):
        for asteroid_posi in asteroid_total:
                screen.blit(asteroid, (asteroid_posi[0],asteroid_posi[1]))

def update_asteroid_positions(asteroid_total, score):
        for idx, asteroid_posi in enumerate(asteroid_total):
                if asteroid_posi[1] >= 0 and asteroid_posi[1] < height:
                        asteroid_posi[1] += asteroid_speed
                else:
                        asteroid_total.pop(idx)
                        score += 1
                px = player_posi[0]
                py = player_posi[1]
                ex = asteroid_posi[0]
                ey = asteroid_posi[1]

                if (ex >= px and ex < (px + player_sizex)) or (px >= ex and px < (ex+asteroid_size)):
                        if (ey >= py and ey < (py + player_sizey)) or (py >= ey and py < (ey+asteroid_size)):
                                print("HIT")
                                asteroid_total.pop(idx)
                                global lives
                                lives=lives-1
                                global game_over
                                if lives == 0:
                                        game_over = True
        return score

def asteroid_collision_check(asteroid_total, player_posi):
        for asteroid_posi in asteroid_total:
                if detect_asteroid_collision(asteroid_posi, player_posi):
                        lives=lives-1
                        return True
        return False



#functions for goldcoins blocks
def goldcoin_level(score, goldcoin_speed):
        if score < 20:
                goldcoin_speed = 5
               
        elif score < 40:
                goldcoin_speed = 8
                           
        elif score < 60:
                goldocoin_speed = 12
                
        else:
                goldcoin_speed = 15                       
        return goldcoin_speed

def goldcoin_set(goldcoin_total):
        delay = random.random()
        if len(goldcoin_total) < 5 and delay < 0.1:
                xposi = random.randint(0,width-asteroid_size)
                yposi = 0
                goldcoin_total.append([xposi, yposi])

def draw_goldcoins(goldcoin_total):
        for goldcoin_posi in goldcoin_total:
                screen.blit(goldcoin, (goldcoin_posi[0],goldcoin_posi[1]))

def update_goldcoin_positions(goldcoin_total, score):
        for idx, goldcoin_posi in enumerate(goldcoin_total):
                px = player_posi[0]
                py = player_posi[1]

                ptx = goldcoin_posi[0]
                pty = goldcoin_posi[1]
                if goldcoin_posi[1] >= 0 and goldcoin_posi[1] < height:
                                goldcoin_posi[1] += goldcoin_speed
                else:
                        goldcoin_total.pop(idx)
                if (ptx >= px and ptx < (px + player_sizex)) or (px >= ptx and px < (ptx+goldcoin_size)):
                        if (pty >= py and pty < (py + player_sizey)) or (py >= pty and py < (pty+goldcoin_size)):
                                goldcoin_total.pop(idx)
                                score+=1      
        return score

#Background Stars
def star_level(score, star_speed):
        if score < 20:
                star_speed = 4
               
        elif score < 40:
                star_speed = 7
                           
        elif score < 60:
                star_speed = 11
                
        else:
                star_speed = 14                        
        return star_speed

def star_set(star_total):
        delay = random.random()
        if len(star_total) < 100 and delay < 0.5:
                xposi = random.randint(0,width-star_size) 
                yposi = 0
                star_total.append([xposi, yposi])

def draw_star(star_total):
        for star_posi in star_total:
                pygame.draw.rect(screen, white, (star_posi[0], star_posi[1], star_size, star_size))

def update_star_positions(star_total):
        for idx, star_posi in enumerate(star_total):
                if star_posi[1] >= 0 and star_posi[1] < height:
                        star_posi[1] += star_speed
                else:
                        star_total.pop(idx)

#Beams
def firebeam(beamX,beamY):
        global beam_state
        beam_state = "fire"
        pygame.draw.rect(screen, red, (beamX+30, beamY+10, 10, 32))

def beam_collision(asteroid_total):
        for idx, asteroid_posi in enumerate(asteroid_total):
                if (beamX+50 >= asteroid_posi[0] and beamX+50 < (asteroid_posi[0] + 100)):
                        if (beamY >= asteroid_posi[1] and beamY < (asteroid_posi[1] + asteroid_size)):
                                asteroid_total.pop(idx)
                                
#main game loop
while not game_over:

        screen.fill(background) 
        
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        sys.exit()
        keys = pygame.key.get_pressed()     #movement of player and boundaries of player
        if keys[pygame.K_LEFT] and player_posi[0]>0:
                player_posi[0]-=player_speed
        if keys[pygame.K_RIGHT] and player_posi[0]<width-player_sizex:
                player_posi[0]+=player_speed
        if keys[pygame.K_UP] and player_posi[1]>0:
                player_posi[1]-=player_speed
        if keys[pygame.K_DOWN] and player_posi[1]<height-player_sizey:
                player_posi[1]+=player_speed
        if keys[pygame.K_SPACE]:
                if beam_state is "ready":
                        beamX = player_posi[0]
                        beamY = player_posi[1]
                        firebeam(beamX,beamY)

        #beam movement
        if beamY <= 0:
                beamY = 480
                beam_state = "ready"
        
        if beam_state is "fire":
                firebeam(beamX,beamY)
                beamY -= beamY_change

        star_set(star_total)
        asteroid_set(asteroid_total)
        goldcoin_set(goldcoin_total)

        draw_star(star_total)
        screen.blit(spaceship, (player_posi[0],player_posi[1]))
        draw_goldcoins(goldcoin_total)
        draw_asteroid(asteroid_total)
        
        update_star_positions(star_total)
        score = update_asteroid_positions(asteroid_total, score)
        score = update_goldcoin_positions(goldcoin_total, score)

        asteroid_speed = asteroid_level(score, asteroid_speed)
        goldcoin_speed = goldcoin_level(score, goldcoin_speed)
        star_speed = star_level(score, star_speed)

        beam_collision(asteroid_total)

        text = "Score:" + str(score)     #drawing score
        label = myfont.render(text, 1, yellow)
        screen.blit(label, (width-100, height-40))

        text2 = "lives:" + str(lives)
        label = myfont.render(text2, 1, yellow)
        screen.blit(label, (width-300, height-40))
                            
        

        clock.tick(30)

        pygame.display.update()
