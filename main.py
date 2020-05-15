import os
import pygame

#####################################################################################
# 1. default init

pygame.init()   # initialize#

screen_width = 640
screen_height = 480

# set frame size
screen = pygame.display.set_mode((screen_width, screen_height))

# set game title
pygame.display.set_caption("PANG")

# FPS
clock = pygame.time.Clock()

#####################################################################################
# 2. user game init (background, character, enemy, font, timer, speed...)

current_path = os.path.dirname(__file__)    # 현재파일 위치
asset_path = os.path.join(current_path, "asset")    # asset 폴더 위치

# background
background = pygame.image.load(os.path.join(asset_path, "background.png"))
# stage
stage = pygame.image.load(os.path.join(asset_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1]

# character
character = pygame.image.load(os.path.join(asset_path, "character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_xpos = screen_width/2 - character_width/2 # 캐릭터 실제 위치
character_ypos = screen_height - stage_height - character_height
# character move
character_to_x = 0  # 캐릭터 이동 속도
character_speed = 5 # 캐릭터 이동 속력

# weapon
weapon = pygame.image.load(os.path.join(asset_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]
# 무기는 여러번 발사 가능
weapons = []
# weapon speed
weapon_speed = 10


#####################################################################################
# event loop
running = True  
while running:
    dt = clock.tick(60) # set FPS

    #####################################################################################
    # 3. event(keyboard, mouse)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):    # quit game
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE:
                weapon_xpos = character_xpos + character_width/2 - weapon_width/2
                weapon_ypos = character_ypos
                weapons.append([weapon_xpos, weapon_ypos])
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0


    #####################################################################################
    # 4. position move

    # character move
    character_xpos += character_to_x

    if character_xpos < 0:
        character_xpos = 0
    elif character_xpos > screen_width-character_width:
        character_xpos = screen_width-character_width
   
    # weapon move
    weapons = [ [w[0], w[1]-weapon_speed] for w in weapons ]

    weapons = [ [w[0], w[1]] for w in weapons if w[1] > 0]

    #####################################################################################
    # 5. collision
   
    #####################################################################################
    # 6. timer

    #####################################################################################
    # 7. draw in screen

    screen.blit(background,(0, 0))
    for weapon_xpos, weapon_ypos in weapons:
        screen.blit(weapon, (weapon_xpos, weapon_ypos))
    screen.blit(stage, (0, screen_height-stage_height))
    screen.blit(character, (character_xpos, character_ypos))


    pygame.display.update() # display update


# quit
pygame.time.delay(1000)
pygame.quit()