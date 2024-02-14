import pygame
import sys

from animated_sprite import AnimatedSprite

GLOBAL_SCALE = 4

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