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

# ball
ball_images = [
    pygame.image.load(os.path.join(asset_path, "ball1.png")),
    pygame.image.load(os.path.join(asset_path, "ball2.png")),
    pygame.image.load(os.path.join(asset_path, "ball3.png")),
    pygame.image.load(os.path.join(asset_path, "ball4.png"))
]
# 공 크기에 따른 속력
ball_speed_y = [-14, -11, -8 -5]

balls = []

balls.append({
    "pos_x" : 50,   # 초기 위치
    "pos_y" : 50,
    "img_idx" : 0,
    "to_x" : 3,     # 초기 이동 속도
    "to_y" : -6,
    "init_speed_y" : ball_speed_y[0]
})

# 사라질 무기와 공 저장 변수
weapon_to_remove = -1
ball_to_remove = -1

# font
game_font = pygame.font.Font(None, 40)

#####################################################################################
# event loop
running = True  
game_over = False
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
   
    # weapon move ***
    weapons = [ [w[0], w[1]-weapon_speed] for w in weapons ]
    weapons = [ [w[0], w[1]] for w in weapons if w[1] > 0]

    # ball move
    for ball_idx, ball_val in enumerate(balls):
        ball_xpos = ball_val["pos_x"]
        ball_ypos = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        # set ball boundary X
        if ball_xpos < 0 or ball_xpos > screen_width-ball_width:
            ball_val["to_x"] = ball_val["to_x"] * -1

        # set ball boundary Y
        if ball_ypos >= screen_height-stage_height-ball_height: # bouncing at stage first
            ball_val["to_y"] = ball_val["init_speed_y"]
        else:   # speed down
            ball_val["to_y"] += 0.4

        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]

    #####################################################################################
    # 5. collision

    # character rect update
    character_rect = character.get_rect()
    character_rect.left = character_xpos
    character_rect.top = character_ypos

    for ball_idx, ball_val in enumerate(balls):
        ball_xpos = ball_val["pos_x"]
        ball_ypos = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]
        # ball rect update
        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.left = ball_xpos
        ball_rect.top = ball_ypos
        
        # collision between character and ball
        if character_rect.colliderect(ball_rect):
            running = False
            game_over = True
            break

        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_xpos = weapon_val[0]
            weapon_ypos = weapon_val[1]
            # weapon rect update
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_xpos
            weapon_rect.top = weapon_ypos

            # collision between ball and weapons
            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_idx
                ball_to_remove = ball_img_idx
                break
    
    if ball_to_remove > -1:
        del balls[ball_to_remove]
        ball_to_remove = -1
    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1


    #####################################################################################
    # 6. timer

    #####################################################################################
    # 7. draw in screen

    screen.blit(background,(0, 0))
    for weapon_xpos, weapon_ypos in weapons:
        screen.blit(weapon, (weapon_xpos, weapon_ypos))
    for idx, val in enumerate(balls):
        ball_xpos = val["pos_x"]
        ball_ypos = val["pos_y"]
        ball_img_idx = val["img_idx"] 
        screen.blit(ball_images[ball_img_idx], (ball_xpos, ball_ypos))

    screen.blit(stage, (0, screen_height-stage_height))
    screen.blit(character, (character_xpos, character_ypos))

    if game_over:
        screen.blit(game_font.render("Game Over", True, (0,0,0)), (screen_width/2-70, 100))

    pygame.display.update() # display update


# quit
pygame.time.delay(1000)
pygame.quit()