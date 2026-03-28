import pygame
import math

class rig_element:
    def __init__(self, name:str, length:int, direction:float = 0, parent:object|None = None, bind_to_end:bool = True, layer:int = 0, sprite:pygame.Surface|None = None):
        self.name = name
        
        self.length = length
        self.relative_direction = direction

        self.parent = parent

        self.start_position = pygame.Vector2(0, 0)
        self.end_position = pygame.Vector2(math.cos(self.relative_direction) * self.length, math.sin(self.relative_direction) * self.length)

        self.bind_to_end = bind_to_end 

        self.update_position()

        self.layer = layer
        self.sprite = sprite

    def update_position(self):
        if self.parent != None:
            if self.bind_to_end:
                self.start_position.x = self.parent.start_position.x + math.cos(self.parent.direction) * self.parent.length
                self.start_position.y = self.parent.start_position.y + math.sin(self.parent.direction) * self.parent.length
            else:
                self.start_position.xy = self.parent.start_position.xy
        self.end_position.xy = (self.start_position.x + math.cos(self.direction) * self.length, self.start_position.y + math.sin(self.direction) * self.length)

    @property
    def direction(self):
        if self.parent == None:
            return self.relative_direction
        else:
            return self.parent.direction + self.relative_direction

    def load(self, start_position:pygame.Vector2, relative_direction:float):
        self.start_position.xy = start_position
        self.relative_direction = relative_direction
        self.update_position()
    
    def save(self):
        return tuple(self.start_position.xy), self.relative_direction