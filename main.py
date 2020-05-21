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
character = pygame.sprite.Sprite()
character.image = pygame.image.load(os.path.join(asset_path, "character.png")).convert_alpha()
character_size = character.image.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_xpos = screen_width/2 - character_width/2 # 캐릭터 실제 위치
character_ypos = screen_height - stage_height - character_height
# character move
character_to_x = 0  # 캐릭터 이동 속도
character_speed = 7 # 캐릭터 이동 속력


# weapon
weapon = pygame.sprite.Sprite()
weapon.image = pygame.image.load(os.path.join(asset_path, "weapon.png")).convert_alpha()
weapon_size = weapon.image.get_rect().size
weapon_width = weapon_size[0]
# 무기는 여러번 발사 가능
weapons = []
# weapon speed
weapon_speed = 10

# ball
ball = pygame.sprite.Sprite()

ball_images = [
    pygame.image.load(os.path.join(asset_path, "ball1.png")).convert_alpha(),
    pygame.image.load(os.path.join(asset_path, "ball2.png")).convert_alpha(),
    pygame.image.load(os.path.join(asset_path, "ball3.png")).convert_alpha(),
    pygame.image.load(os.path.join(asset_path, "ball4.png")).convert_alpha()
]
# 공 크기에 따른 속력
ball_speed_y = [-19, -16, -13, -10]

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

# text
game_font = pygame.font.Font(None, 40)

total_time = 60
start_tick = pygame.time.get_ticks()

game_result = ""

left_pressed = False    # 버그 해결 : 키 중복 입력 시 캐릭터 이동 제한
right_pressed = False
#####################################################################################
# event loop
running = True  

while running:
    dt = clock.tick(30) # set FPS

    #####################################################################################
    # 3. event(keyboard, mouse)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):    # quit game
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                left_pressed = True
            elif event.key == pygame.K_RIGHT:
                right_pressed = True
            elif event.key == pygame.K_SPACE:
                weapon_xpos = character_xpos + character_width/2 - weapon_width/2
                weapon_ypos = character_ypos
                weapons.append([weapon_xpos, weapon_ypos])
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                left_pressed = False
                character_to_x = 0
            elif event.key == pygame.K_RIGHT:
                right_pressed = False
                character_to_x = 0

        if left_pressed and right_pressed:
            character_to_x = 0
        else:
            if left_pressed:
                character_to_x = 0 - character_speed
            if right_pressed:
                character_to_x = 0 + character_speed


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
            ball_val["to_y"] += 0.6

        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]
            # bug fix: 캐릭터의 이동이 원활하지 않는 버그 수정
    #####################################################################################
    # 5. collision

    # character rect update
    character.rect = character.image.get_rect()
    character.rect.left = character_xpos
    character.rect.top = character_ypos
    character.mask = pygame.mask.from_surface(character.image)


    for ball_idx, ball_val in enumerate(balls):
        ball_xpos = ball_val["pos_x"]
        ball_ypos = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]
        # ball rect update
        ball.rect = ball_images[ball_img_idx].get_rect()
        ball.rect.left = ball_xpos
        ball.rect.top = ball_ypos
        ball.mask = pygame.mask.from_surface(ball_images[ball_img_idx])


        # collision between character and ball
        if(pygame.sprite.collide_mask(character, ball)):
            running = False
            game_result = "Game Over"
            break

        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_xpos = weapon_val[0]
            weapon_ypos = weapon_val[1]
            # weapon rect update
            weapon.rect = weapon.image.get_rect()
            weapon.rect.left = weapon_xpos
            weapon.rect.top = weapon_ypos

            # collision between ball and weapons
            if(pygame.sprite.collide_mask(weapon, ball)):
                weapon_to_remove = weapon_idx
                ball_to_remove = ball_idx

                if ball_img_idx < 3:    # 공 나누기

                    ball_width = ball.rect.size[0]
                    ball_height = ball.rect.size[1]

                    small_ball_rect = ball_images[ball_img_idx + 1].get_rect()
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]

                    # left
                    balls.append({
                        "pos_x" : ball_xpos + ball_width/2 - small_ball_width/2,   
                        "pos_y" : ball_ypos + ball_height/2 - small_ball_height/2,
                        "img_idx" : ball_img_idx+1,
                        "to_x" : -3,     
                        "to_y" : -6,
                        "init_speed_y" : ball_speed_y[ball_img_idx+1]
                    })
                    # right
                    balls.append({
                        "pos_x" : ball_xpos + ball_width/2 - small_ball_width/2,   
                        "pos_y" : ball_ypos + ball_height/2 - small_ball_height/2,
                        "img_idx" : ball_img_idx+1,
                        "to_x" : 3,     
                        "to_y" : -6,
                        "init_speed_y" : ball_speed_y[ball_img_idx+1]
                    })

                break
        else:           
            continue
        break
    ###################### bug fix: 중첩 for일 경우 의도한 대로 break를 실행 (중첩 for문 동시 탈출)
    
    if ball_to_remove > -1:
        del balls[ball_to_remove]
        ball_to_remove = -1
    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1

    if len(balls) == 0:
        game_result = "Stage Clear"
        running = False
        
    #####################################################################################
    # 7. draw in screen

    screen.blit(background,(0, 0))
    for weapon_xpos, weapon_ypos in weapons:
        screen.blit(weapon.image, (weapon_xpos, weapon_ypos))
    for idx, val in enumerate(balls):
        ball_xpos = val["pos_x"]
        ball_ypos = val["pos_y"]
        ball_img_idx = val["img_idx"] 
        screen.blit(ball_images[ball_img_idx], (ball_xpos, ball_ypos))

    screen.blit(stage, (0, screen_height-stage_height))
    screen.blit(character.image, (character_xpos, character_ypos))

    elapsed_time = (pygame.time.get_ticks() - start_tick) / 1000
    timer = game_font.render("Time : {}".format(int(total_time - elapsed_time)), True, (255,255,255))
    screen.blit(timer, (10, 10))


    if total_time - elapsed_time <= 0:
        game_result = "Time Out"
        running = False


    pygame.display.update() # display update


# quit
msg = game_font.render(game_result, True, (0,0,0))
msg_rect = msg.get_rect(center=(int(screen_width/2), int(screen_height/2)))
screen.blit(msg, msg_rect)
pygame.display.update()

pygame.time.delay(1000)
pygame.quit()   