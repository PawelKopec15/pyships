import pygame
import sys

from animated_sprite import AnimatedSprite
from animated_sprite import TILESET_PATH

GLOBAL_SCALE = 4
TILE_SIZE = 16

BOARD_X_OFFSET = 10
BOARD_MARGIN = 5

pygame.init()

# Set up the screen
screen_width = 300
screen_height = 180
screen = pygame.display.set_mode((screen_width * GLOBAL_SCALE, screen_height * GLOBAL_SCALE))
pygame.display.set_caption("PyShips")

board_top = pygame.image.load("assets/board_top.png").convert_alpha()
board_bottom = pygame.transform.flip(board_top, False, True)

tile_water = AnimatedSprite(TILESET_PATH, pygame.Rect(32, 0, 16, 16), 8, 4500 )
tile_missed_bullet = AnimatedSprite(TILESET_PATH, pygame.Rect(0, 80, 16, 16), 2, 800 )

tile_sonar = AnimatedSprite(TILESET_PATH, pygame.Rect(0, 96, 16, 16), 7, 4300 )
tile_pin_white = AnimatedSprite(TILESET_PATH, pygame.Rect(0, 112, 16, 16), 7, 4300 )
tile_pin_red = AnimatedSprite(TILESET_PATH, pygame.Rect(0, 128, 16, 16), 7, 4300 )
tile_pin_glowing = AnimatedSprite(TILESET_PATH, pygame.Rect(0, 144, 16, 16), 7, 4300 )

ui_grid = AnimatedSprite(TILESET_PATH, pygame.Rect(0, 0, 16, 16), 2, 1000 )
ui_pin = AnimatedSprite(TILESET_PATH, pygame.Rect(48, 64, 16, 32), 1 , 1000)

effect_splash = AnimatedSprite(TILESET_PATH, pygame.Rect(64, 64, 16, 16), 5, 6000 )
effect_explosion = AnimatedSprite(TILESET_PATH, pygame.Rect(64, 80, 16, 16), 5, 10000 )

def update_all_animated_sprites(delta):
    tile_water.tick(delta)
    tile_missed_bullet.tick(delta)
    tile_sonar.tick(delta)
    tile_pin_white.tick(delta)
    tile_pin_red.tick(delta)
    tile_pin_glowing.tick(delta)
    ui_grid.tick(delta)
    effect_splash.tick(delta)
    effect_explosion.tick(delta)

def draw_scaled(screen, sprite_sheet, pos, frame_rect, scale=GLOBAL_SCALE):
    scaled_image = pygame.transform.scale(sprite_sheet, (sprite_sheet.get_width() * scale, sprite_sheet.get_height() * scale))
    screen.blit(scaled_image, (pos[0]*scale, pos[1]*scale), pygame.Rect(frame_rect.left*scale, frame_rect.top*scale, frame_rect.width*scale, frame_rect.height*scale))
    
def draw_grid(screen, ui_grid, pos, size):
    grid_width = ui_grid.get_frame_rect().width
    grid_height = ui_grid.get_frame_rect().height
    for y in range(size[1]):
        for x in range(size[0]):
            draw_scaled(screen, ui_grid.get_sprite_sheet(), (x*grid_width+pos[0], y*grid_height+pos[1]), ui_grid.get_frame_rect())
    
def draw_water(screen, tile_water, pos, size):
    water_width = tile_water.get_frame_rect().width
    water_height = tile_water.get_frame_rect().height
    for y in range(size[1]):
        for x in range(size[0]):
            draw_scaled(screen, tile_water.get_sprite_sheet(), (x*water_width+pos[0], y*water_height+pos[1]), tile_water.get_frame_rect())

def draw_board_top_only(screen, y, board_size, color):
    draw_scaled(screen, board_top, (BOARD_X_OFFSET, y), pygame.Rect(0, 0, board_top.get_width(), board_top.get_height()))
    
    background_x = max ( board_top.get_width()//5*2 - (board_size[0]*TILE_SIZE//2), BOARD_X_OFFSET+BOARD_MARGIN )
    background_y = board_top.get_height()//2 - (board_size[1]*TILE_SIZE//2 + BOARD_MARGIN) + y
    background_width = board_size[0]*TILE_SIZE+2
    background_height = board_size[1]*TILE_SIZE+2
    
    background_surface = pygame.Surface((background_width, background_height))
    background_surface.fill(color)
    
    screen.blit(pygame.transform.scale(background_surface, (background_width*GLOBAL_SCALE,background_height*GLOBAL_SCALE)), (background_x*GLOBAL_SCALE, background_y*GLOBAL_SCALE))
    
    return background_x+1, background_y+1
 
def draw_board_top(screen, board_size, p2_board, p2_ships):
    
    first_coord_x, first_coord_y = draw_board_top_only(screen, 0, board_size, (99, 199, 77))
    
    for ship in p2_ships:
        coords = ship[1].get_all_coords(ship[0])
        for i in range( len(coords) ):
            if ship[1].is_segment_on_fire(i):
                if ship[1].wrecked():
                    draw_scaled(screen, tile_pin_red.get_sprite_sheet(), (first_coord_x+TILE_SIZE*coords[i][0], first_coord_y+TILE_SIZE*coords[i][1]), tile_pin_red.get_frame_rect())
                else:
                    draw_scaled(screen, tile_pin_glowing.get_sprite_sheet(), (first_coord_x+TILE_SIZE*coords[i][0], first_coord_y+TILE_SIZE*coords[i][1]), tile_pin_glowing.get_frame_rect())
            else:
                draw_scaled(screen, tile_sonar.get_sprite_sheet(), (first_coord_x+TILE_SIZE*coords[i][0], first_coord_y+TILE_SIZE*coords[i][1]), tile_sonar.get_frame_rect())
    
    for y in range( board_size[1] ):
        for x in range( board_size[0] ):
            current_pos = (first_coord_x+TILE_SIZE*x, first_coord_y+TILE_SIZE*y)
            
            if(p2_board[y][x] == None):
                draw_scaled(screen, tile_sonar.get_sprite_sheet(), current_pos, tile_sonar.get_frame_rect())
            elif(p2_board[y][x] == -1):
                draw_scaled(screen, tile_pin_white.get_sprite_sheet(), current_pos, tile_pin_white.get_frame_rect())
                
            draw_scaled(screen, ui_grid.get_sprite_sheet(), current_pos, ui_grid.get_frame_rect())
            
    return first_coord_x, first_coord_y

def draw_board_bottom_only(screen, y, board_size, color):
    draw_scaled(screen, board_bottom, (BOARD_X_OFFSET, y), pygame.Rect(0, 0, board_bottom.get_width(), board_bottom.get_height()))
    
    background_x = max ( board_bottom.get_width()//5*2 - (board_size[0]*TILE_SIZE//2), BOARD_X_OFFSET+BOARD_MARGIN )
    background_y = board_bottom.get_height()//2 - (board_size[1]*TILE_SIZE//2 - BOARD_MARGIN) + y
    background_width = board_size[0]*TILE_SIZE+2
    background_height = board_size[1]*TILE_SIZE+2
    
    background_surface = pygame.Surface((background_width, background_height))
    background_surface.fill(color)
    
    screen.blit(pygame.transform.scale(background_surface, (background_width*GLOBAL_SCALE,background_height*GLOBAL_SCALE)), (background_x*GLOBAL_SCALE, background_y*GLOBAL_SCALE))
    
    return background_x+1, background_y+1
            
def draw_board_bottom(screen, board_size, p1_board, p1_ships, delta):
    
    first_coord_x, first_coord_y = draw_board_bottom_only(screen, 0, board_size, (192, 203, 220))
    
    for ship in p1_ships:
        ship[1].tick(delta)
        ship[1].draw_self(screen, ( first_coord_x + ship[0][0] * TILE_SIZE, first_coord_y + ship[0][1] * TILE_SIZE ))
    
    for y in range( board_size[1] ):
        for x in range( board_size[0] ):
            current_pos = (first_coord_x+TILE_SIZE*x, first_coord_y+TILE_SIZE*y)
            
            if(p1_board[y][x] == None):
                draw_scaled(screen, tile_water.get_sprite_sheet(), current_pos, tile_water.get_frame_rect())
            elif(p1_board[y][x] == -1):
                draw_scaled(screen, tile_missed_bullet.get_sprite_sheet(), current_pos, tile_missed_bullet.get_frame_rect())
                
            draw_scaled(screen, ui_grid.get_sprite_sheet(), current_pos, ui_grid.get_frame_rect())
            
    return first_coord_x, first_coord_y

def draw_both_boards_only(screen, y, board_size):
    draw_board_top_only(screen, y-board_bottom.get_size()[1], board_size, (62, 137, 72))
    draw_board_bottom_only(screen, y, board_size, (44, 232, 245))