import pygame
import sys
import math

from draw_wizard import *

from animated_sprite import AnimatedSprite
from animated_sprite import TILESET_PATH

from battleship import BattleShip
from battleship import BSOrientation

from board import Board

background = pygame.image.load("assets/background2.png")
            
pygame.init()

# Set up the screen
screen_width = 300
screen_height = 180
screen = pygame.display.set_mode((screen_width * GLOBAL_SCALE, screen_height * GLOBAL_SCALE))
pygame.display.set_caption("PyShips")

clock = pygame.time.Clock()

# Gameplay setup
board_width = 11
board_height = 9
board = Board((board_width, board_height))
board.add_ship(1, BattleShip(4), (2, 4))

first_coords_x = 99999
first_coords_y = 99999

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get the position of the mouse when clicked
            mouse_x, mouse_y = pygame.mouse.get_pos()
            mouse_x //= GLOBAL_SCALE
            mouse_y //= GLOBAL_SCALE
            # Check which mouse button was clicked
            if event.button == 1:  # Left mouse button
                if first_coords_x <= mouse_x <= (first_coords_x + board_width*TILE_SIZE) and first_coords_y <= mouse_y <= (first_coords_y + board_height*TILE_SIZE):
                    pos = math.floor((mouse_x-first_coords_x)/TILE_SIZE), math.floor((mouse_y-first_coords_y)/TILE_SIZE)
                    board.shoot_at_p1(pos)
                    
            elif event.button == 3:  # Right mouse button
                pass
    
    delta = clock.tick(60)

    # Clear the screen
    # screen.fill((0, 0, 0))
    draw_scaled(screen, background, (0, 0), pygame.Rect(0, 0, background.get_width(), background.get_height()))

    # Updating all animated sprites
    update_all_animated_sprites(delta)
    
    first_coords_x, first_coords_y = board.draw_bottom(screen, delta)

    # Update the display
    pygame.display.flip()