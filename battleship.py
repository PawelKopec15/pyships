import pygame
from enum import IntEnum
from typing import NamedTuple

from animated_sprite import AnimatedSprite
from animated_sprite import TILESET_PATH

from draw_wizard import draw_scaled
from draw_wizard import TILE_SIZE

class BSOrientation(IntEnum):
    RIGHT = 0
    UP = 1
    LEFT = 2
    DOWN = 3
    
class BSPartType(IntEnum):
    BOW = 0
    MIDDLE = 1
    REAR = 2

class BSPart(NamedTuple):
    part: BSPartType
    burning: bool

class BattleShip:
    
    def __init__ (self, size):
        self.size = max(size, 2)
        self.orientation = BSOrientation.RIGHT
        
        self.parts = [ BSPart( BSPartType.REAR, False ) ]
        for _ in range(1, size-1):
            self.parts.append( BSPart( BSPartType.MIDDLE, False ))
        self.parts.append( BSPart( BSPartType.BOW, False ) )
        
        ## Initializing animated tiles in a list where
        ## rows (outer list)     - orientation
        ## columns (inner lists) - part type
        ANIMATION_SPEED = 1200
        
        self.tiles = [
            [ AnimatedSprite(TILESET_PATH, pygame.Rect(128, 32, 16, 16), 2, ANIMATION_SPEED ),
              AnimatedSprite(TILESET_PATH, pygame.Rect(96, 32, 16, 16), 2, ANIMATION_SPEED ),
              AnimatedSprite(TILESET_PATH, pygame.Rect(64, 32, 16, 16), 2, ANIMATION_SPEED ),],
            
            [ AnimatedSprite(TILESET_PATH, pygame.Rect(0, 16, 16, 16), 2, ANIMATION_SPEED ),
              AnimatedSprite(TILESET_PATH, pygame.Rect(0, 32, 16, 16), 2, ANIMATION_SPEED ),
              AnimatedSprite(TILESET_PATH, pygame.Rect(0, 48, 16, 16), 2, ANIMATION_SPEED ),],
            
            [ AnimatedSprite(TILESET_PATH, pygame.Rect(64, 16, 16, 16), 2, ANIMATION_SPEED ),
              AnimatedSprite(TILESET_PATH, pygame.Rect(96, 16, 16, 16), 2, ANIMATION_SPEED ),
              AnimatedSprite(TILESET_PATH, pygame.Rect(128, 16, 16, 16), 2, ANIMATION_SPEED ),],
            
            [ AnimatedSprite(TILESET_PATH, pygame.Rect(32, 48, 16, 16), 2, ANIMATION_SPEED ),
              AnimatedSprite(TILESET_PATH, pygame.Rect(32, 32, 16, 16), 2, ANIMATION_SPEED ),
              AnimatedSprite(TILESET_PATH, pygame.Rect(32, 16, 16, 16), 2, ANIMATION_SPEED ),],
            ]
        
        self.sprite_fire = AnimatedSprite(TILESET_PATH, pygame.Rect(0, 64, 16, 16), 3, 3000)
        self.tile_wreckage = AnimatedSprite(TILESET_PATH, pygame.Rect(64, 48, 16, 16), 6, 4000)
    
    def tick(self, delta):
        for l in self.tiles:
            for i in l:
                i.tick(delta)
        
        self.sprite_fire.tick(delta)
        self.tile_wreckage.tick(delta)
        
    def set_orientation(self, val):
        self.orientation = val
        
    def set_segment_on_fire(self, segment, val):
        if segment > self.size:
            return
    
        self.parts[segment] = BSPart(self.parts[segment].part, val)
        
    def get_indexes_of_segments_on_fire(self):
        to_ret = []
        for i in range(self.size):
            if self.parts[i].burning:
                to_ret.append(i)
        return to_ret
        
    def wrecked(self):
        for p in self.parts:
            if not p.burning:
                return False
        return True
    
    def get_dimentions(self):
        if(self.orientation == BSOrientation.DOWN or BSOrientation.UP):
            return (TILE_SIZE, TILE_SIZE*self.size)
        return(TILE_SIZE*self.size, TILE_SIZE)
    
    def get_all_coords(self, pos):
        coords = []
        current_pos = pos
        
        for _ in range(self.size):
            coords.append(current_pos)
            if(self.orientation == BSOrientation.RIGHT):
                current_pos = (current_pos[0] + 1, current_pos[1])
            elif(self.orientation == BSOrientation.UP):
                current_pos = (current_pos[0], current_pos[1] - 1)
            elif(self.orientation == BSOrientation.LEFT):
                current_pos = (current_pos[0] - 1, current_pos[1])
            elif(self.orientation == BSOrientation.DOWN):
                current_pos = (current_pos[0], current_pos[1] + 1)
        
        return coords
        
    def draw_self(self, screen, pos):
        
        positions_list = []
        current_pos = pos
        
        for _ in range(self.size):
            positions_list.append(current_pos)
            if(self.orientation == BSOrientation.RIGHT):
                current_pos = (current_pos[0] + TILE_SIZE, current_pos[1])
            elif(self.orientation == BSOrientation.UP):
                current_pos = (current_pos[0], current_pos[1] - TILE_SIZE)
            elif(self.orientation == BSOrientation.LEFT):
                current_pos = (current_pos[0] - TILE_SIZE, current_pos[1])
            elif(self.orientation == BSOrientation.DOWN):
                current_pos = (current_pos[0], current_pos[1] + TILE_SIZE)
        
        if not self.wrecked():
            for i in range(self.size):
                draw_scaled(screen, self.tiles[self.orientation][self.parts[i].part].get_sprite_sheet(), positions_list[i], self.tiles[self.orientation][self.parts[i].part].get_frame_rect() )
                if self.parts[i].burning:
                    draw_scaled(screen, self.sprite_fire.get_sprite_sheet(), positions_list[i], self.sprite_fire.get_frame_rect())     
        
        else:
            for p in positions_list:
                draw_scaled(screen, self.tile_wreckage.get_sprite_sheet(), p, self.tile_wreckage.get_frame_rect())
            