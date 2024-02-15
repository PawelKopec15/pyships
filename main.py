import pygame
import sys
import math
from enum import Enum

from draw_wizard import *

from animated_sprite import AnimatedSprite
from animated_sprite import TILESET_PATH

from battleship import BattleShip
from battleship import BSOrientation

from board import Board

class GameState(Enum):
    TITLE = 0
    SHIP_SETUP = 1
    PLAYER_TURN = 2
    ENEMY_TURN = 3
    END = 4
    
class GameSubState(Enum):
    TRANSITION_ANIMATION = 0
    WAITING_FOR_INPUT = 1
    AFTER_INPUT_ANIMATION = 2
    AFTER_INPUT_RESULT = 3

background = pygame.image.load("assets/background2.png")

clock = pygame.time.Clock()

# Gameplay setup
board_width = 11
board_height = 9
board = Board((board_width, board_height))

ship_list = [ BattleShip(4), BattleShip(3), BattleShip(3), BattleShip(2), BattleShip(2) ]
ship_i = 0

game_state = GameState.TITLE
game_sub_state = GameSubState.WAITING_FOR_INPUT

first_coords_x = 99999
first_coords_y = 99999

# Main loop
while True:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_x //= GLOBAL_SCALE
    mouse_y //= GLOBAL_SCALE
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:            
            # Check which mouse button was clicked
            if event.button == 1:  # Left mouse button
                
                pos = math.floor((mouse_x-first_coords_x)/TILE_SIZE), math.floor((mouse_y-first_coords_y)/TILE_SIZE)
                
                if game_state == GameState.PLAYER_TURN and game_sub_state == GameSubState.WAITING_FOR_INPUT:
                    if first_coords_x <= mouse_x <= (first_coords_x + board_width*TILE_SIZE) and first_coords_y <= mouse_y <= (first_coords_y + board_height*TILE_SIZE):
                        board.shoot_at_p2(pos)
                elif game_state == GameState.SHIP_SETUP and game_sub_state == GameSubState.WAITING_FOR_INPUT:
                    if(board.add_ship(1, ship_list[ship_i], pos)):
                        ship_i += 1
                        if(ship_i >= len(ship_list)):
                            game_sub_state = GameSubState.AFTER_INPUT_RESULT
                    
            elif event.button == 3:  # Right mouse button
                if game_state == GameState.SHIP_SETUP and game_sub_state == GameSubState.WAITING_FOR_INPUT:
                    ship_list[ship_i].rotate_clockwise()
    
    delta = clock.tick(20)    

    # Updating all animated sprites
    update_all_animated_sprites(delta)
    
    ## DRAWING
    # Backgrounds
    draw_scaled(screen, background, (0, 0), pygame.Rect(0, 0, background.get_width(), background.get_height()))
    
    if game_state == GameState.SHIP_SETUP or  game_state == GameState.ENEMY_TURN:
        first_coords_x, first_coords_y = board.draw_bottom(screen, delta)
    elif game_state == GameState.PLAYER_TURN:
        first_coords_x, first_coords_y = board.draw_top(screen)
        
    # Ship in hand
    if game_state == GameState.SHIP_SETUP and game_sub_state == GameSubState.WAITING_FOR_INPUT:
        ship_list[ship_i].draw_self(screen, (mouse_x-8, mouse_y-8))
    
    # Pin in hand
    if game_state == GameState.PLAYER_TURN and game_sub_state == GameSubState.WAITING_FOR_INPUT:
        draw_scaled(screen, ui_pin.get_sprite_sheet(), (mouse_x-8, mouse_y-24), ui_pin.get_frame_rect())
    
    

    # Update the display
    pygame.display.flip()