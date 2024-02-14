import pygame
import sys
from animated_sprite import AnimatedSprite

GLOBAL_SCALE = 4

tile_water = AnimatedSprite("assets\\tileset.png", pygame.Rect(32, 0, 16, 16), 8, 5 )
tile_missed_bullet = AnimatedSprite("assets\\tileset.png", pygame.Rect(64, 48, 16, 16), 2, 1 )
ui_grid = AnimatedSprite("assets\\tileset.png", pygame.Rect(0, 0, 16, 16), 2, 1 )
effect_splash = AnimatedSprite("assets\\tileset.png", pygame.Rect(64, 64, 16, 16), 6, 6 )

def draw_scaled(sprite_sheet, pos, frame_rect, scale=GLOBAL_SCALE):
    scaled_image = pygame.transform.scale(sprite_sheet, (sprite_sheet.get_width() * scale, sprite_sheet.get_height() * scale))
    screen.blit(scaled_image, (pos[0]*scale, pos[1]*scale), pygame.Rect(frame_rect.left*scale, frame_rect.top*scale, frame_rect.width*scale, frame_rect.height*scale))
    
def draw_grid(pos, size):
    grid_width = ui_grid.get_frame_rect().width
    grid_height = ui_grid.get_frame_rect().height
    for y in range(size[1]):
        for x in range(size[0]):
            draw_scaled(ui_grid.get_sprite_sheet(), (x*grid_width+pos[0], y*grid_height+pos[1]), ui_grid.get_frame_rect())
    
def draw_water(pos, size):
    water_width = tile_water.get_frame_rect().width
    water_height = tile_water.get_frame_rect().height
    for y in range(size[1]):
        for x in range(size[0]):
            draw_scaled(tile_water.get_sprite_sheet(), (x*water_width+pos[0], y*water_height+pos[1]), tile_water.get_frame_rect())
            

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
    screen.fill((0, 0, 0))

    # Updating all animated sprites
    tile_water.tick(delta)
    tile_missed_bullet.tick(delta)
    ui_grid.tick(delta)
    effect_splash.tick(delta)
    
    draw_water((10, 10), (11, 9))
    
    draw_scaled(tile_missed_bullet.get_sprite_sheet(), (26, 26), tile_missed_bullet.get_frame_rect())
    
    #draw_grid((10, 10), (11, 9))

    # Update the display
    pygame.display.flip()