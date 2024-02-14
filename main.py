import pygame
import sys

from draw_wizard import *

from animated_sprite import AnimatedSprite
from animated_sprite import TILESET_PATH

from battleship import BattleShip
from battleship import BSOrientation

background = pygame.image.load("assets/background2.png")

tile_water = AnimatedSprite(TILESET_PATH, pygame.Rect(32, 0, 16, 16), 8, 4500 )
tile_missed_bullet = AnimatedSprite(TILESET_PATH, pygame.Rect(0, 80, 16, 16), 2, 800 )
ui_grid = AnimatedSprite(TILESET_PATH, pygame.Rect(0, 0, 16, 16), 2, 1000 )
effect_splash = AnimatedSprite(TILESET_PATH, pygame.Rect(64, 64, 16, 16), 5, 6000 )
effect_explosion = AnimatedSprite(TILESET_PATH, pygame.Rect(64, 80, 16, 16), 5, 10000 )
            
pygame.init()

# Set up the screen
screen_width = 260
screen_height = 180
screen = pygame.display.set_mode((screen_width * GLOBAL_SCALE, screen_height * GLOBAL_SCALE))
pygame.display.set_caption("Gaym")


clock = pygame.time.Clock()

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    delta = clock.tick(60)

    # Clear the screen
    # screen.fill((0, 0, 0))
    draw_scaled(screen, background, (0, 0), pygame.Rect(0, 0, background.get_width(), background.get_height()))

    # Updating all animated sprites
    tile_water.tick(delta)
    tile_missed_bullet.tick(delta)
    ui_grid.tick(delta)
    effect_splash.tick(delta)

    
    draw_water(screen, tile_water, (10, 10), (11, 9))
    
    #draw_grid(screen, ui_grid, (10, 10), (11, 9))

    # Update the display
    pygame.display.flip()