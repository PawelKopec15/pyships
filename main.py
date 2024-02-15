import pygame
import sys
import math
import copy
import time
from enum import Enum

from draw_wizard import *
from enemy_ai import *

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
    
def check_winning_condition(board):
    if(board.check_winner_p1()):
        text = font.render("You win!!!", True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (screen_width*GLOBAL_SCALE // 2, screen_height*GLOBAL_SCALE // 2)

        screen.blit(text, text_rect)
        pygame.display.flip()
        time.sleep(2)
        sys.exit(0)
    elif(board.check_winner_p2()):
        text = font.render("You lose :(.", True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (screen_width*GLOBAL_SCALE // 2, screen_height*GLOBAL_SCALE // 2)

        screen.blit(text, text_rect)
        pygame.display.flip()
        time.sleep(2)
        sys.exit(0)

background = pygame.image.load("assets/background2.png")

clock = pygame.time.Clock()

# Load the font
font_path = "assets/c64esque.ttf"
font_size = 56
font = pygame.font.Font(font_path, font_size)

# Gameplay setup
board_width = 11
board_height = 9
board = Board((board_width, board_height))

ship_list = [ BattleShip(4), BattleShip(3), BattleShip(3), BattleShip(2), BattleShip(2) ]
enemy_ship_list = [ BattleShip(4), BattleShip(3), BattleShip(3), BattleShip(2), BattleShip(2) ]
ship_i = 0

game_state = GameState.TITLE
game_sub_state = GameSubState.WAITING_FOR_INPUT
transition_animation_current_y = -screen_height
transition_animation_current_target = 0
transition_delay = 0

enemy_rocket_y = -16
enemy_rocket_dest = (0, 0)
enemy_chances = 2

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
                        if not board.shoot_at_p2(pos):
                            game_sub_state = GameSubState.TRANSITION_ANIMATION
                            transition_delay = 1000
                            transition_animation_current_target = 0
                            transition_animation_current_y = screen_height
                
                elif game_state == GameState.SHIP_SETUP and game_sub_state == GameSubState.WAITING_FOR_INPUT:
                    if(board.add_ship(1, copy.copy(ship_list[ship_i]), pos)):
                        ship_i += 1
                        if(ship_i >= len(ship_list)):
                            ai_place_ships(board, (board_width, board_height), enemy_ship_list)
                            game_state = GameState.PLAYER_TURN
                            game_sub_state = GameSubState.TRANSITION_ANIMATION
                            transition_animation_current_target = screen_height
                            
                elif game_state == GameState.TITLE:
                    game_state = GameState.SHIP_SETUP
                    game_sub_state = GameSubState.TRANSITION_ANIMATION
                    transition_animation_current_target = 0
                    
            elif event.button == 3:  # Right mouse button
                if game_state == GameState.SHIP_SETUP and game_sub_state == GameSubState.WAITING_FOR_INPUT:
                    ship_list[ship_i].rotate_clockwise()
    
    delta = clock.tick(30)    

    # Updating all animated sprites
    update_all_animated_sprites(delta)
           
    
    ## DRAWING
    # Backgrounds
    draw_scaled(screen, background, (0, 0), pygame.Rect(0, 0, background.get_width(), background.get_height()))
    
    if game_sub_state != GameSubState.TRANSITION_ANIMATION or transition_delay>0:
        if game_state == GameState.SHIP_SETUP or  game_state == GameState.ENEMY_TURN:
            first_coords_x, first_coords_y = board.draw_bottom(screen, delta)
        elif game_state == GameState.PLAYER_TURN:
            first_coords_x, first_coords_y = board.draw_top(screen)
    
    # Transition animation
    if game_sub_state == GameSubState.TRANSITION_ANIMATION:
        if transition_delay > 0:
            transition_delay -= delta
            
            if transition_delay < 0:
                check_winning_condition(board)
                if game_state == GameState.PLAYER_TURN:
                    game_state = GameState.ENEMY_TURN
                    enemy_chances = 2
                    enemy_rocket_y = -16
                else:
                    game_state = GameState.PLAYER_TURN
            
        else:
            board.draw_both_for_animation(screen, transition_animation_current_y)
            direction = math.copysign(1, transition_animation_current_target-transition_animation_current_y)
            transition_animation_current_y += delta * direction / 8
            if(math.copysign(1, transition_animation_current_target-transition_animation_current_y) != direction):
                game_sub_state = GameSubState.WAITING_FOR_INPUT
        
    # Ship in hand
    if game_state == GameState.SHIP_SETUP and game_sub_state == GameSubState.WAITING_FOR_INPUT:
        ship_list[ship_i].draw_self(screen, (mouse_x-8, mouse_y-8))
    
    # Pin in hand
    if game_state == GameState.PLAYER_TURN and game_sub_state == GameSubState.WAITING_FOR_INPUT:
        draw_scaled(screen, ui_pin.get_sprite_sheet(), (mouse_x-8, mouse_y-24), ui_pin.get_frame_rect())
        
    # Start screen
    if game_state == GameState.TITLE:
        text = font.render("Welcome to PyShips! Click anywhere to begin.", True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (screen_width*GLOBAL_SCALE // 2, screen_height*GLOBAL_SCALE // 2)

        screen.blit(text, text_rect)
    
    ## Enemy turn
    if game_state == GameState.ENEMY_TURN and game_sub_state == GameSubState.WAITING_FOR_INPUT:
        
        if enemy_rocket_y > screen_height * 2:
            enemy_rocket_y = -16
        
        if enemy_rocket_y == -16:
            if enemy_chances > 0:
                enemy_rocket_dest = ai_take_a_shot(board)
                enemy_chances -= 1
            else:
                game_sub_state = GameSubState.TRANSITION_ANIMATION
                transition_delay = 1000
                transition_animation_current_target = screen_height
                transition_animation_current_y = 0
                enemy_rocket_y = -32
            
        elif enemy_rocket_dest[1]*TILE_SIZE+first_coords_x < enemy_rocket_y < screen_height:
            if board.shoot_at_p1(enemy_rocket_dest):
                enemy_chances += 1
            enemy_rocket_y = screen_height+16        
            
        enemy_rocket_y += delta / 8
        draw_scaled(screen, effect_bomb.get_sprite_sheet(), (enemy_rocket_dest[0]*TILE_SIZE + first_coords_x, enemy_rocket_y), effect_bomb.get_frame_rect())
    

    # Update the display
    pygame.display.flip()