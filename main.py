import pygame

pygame.init()   # initialize

# set frame size
screen_width = 480
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))

# set game title
pygame.display.set_caption("test")

# event loop
running = True  
while running:
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            running = False

# quit
pygame.quit()