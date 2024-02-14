import pygame

TILESET_PATH = "assets\\tileset.png"
class AnimatedSprite:
    
    def __init__(self, image_path, first_frame_rect, num_of_frames, millis_per_frame):
        self.sprite_sheet = pygame.image.load(image_path)
        self.frame_rect = first_frame_rect
        self.first_frame_x = first_frame_rect.left
        self.num_of_frames = num_of_frames
        self.fps = millis_per_frame
        self.frame = 0
        self.timer = 0
        self.looped_once = False
        
    def tick(self, delta):
        
        self.timer += delta
        
        time_per_frame = 1000000 // self.fps
        if self.timer // time_per_frame > self.frame:
            
            self.frame += 1
            if(self.frame >= self.num_of_frames):
                self.frame = 0
                self.timer -= time_per_frame * self.num_of_frames
                self.looped_once = True
        
        self.frame_rect.x = self.frame * self.frame_rect.width + self.first_frame_x
        
    def reset(self):
        self.timer = 0
        self.tick(0)
    
    def repeated(self):
        return self.looped_once
        
    def get_sprite_sheet(self):
        return self.sprite_sheet
    
    def get_frame_rect(self):
        return self.frame_rect