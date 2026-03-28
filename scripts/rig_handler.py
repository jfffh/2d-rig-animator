import pygame
import math
from scripts.rig_element import rig_element

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from scripts.globals import global_vars

class rig_handler:
    def __init__(self, globals:"global_vars"):
        self.globals = globals
        self.rig_elements:list[rig_element] = []
        self.element = 0

    def add_element(self, element:rig_element):
        self.rig_elements.append(element)

    def draw_skeleton(self, screen:pygame.Surface, camera:pygame.Vector2):
        lines = []
        for i, element in enumerate(self.rig_elements):
            lines.append((element.start_position - camera, element.end_position - camera, element.layer, i == self.element))
        
        def sort_key(element:tuple):
            return element[2]

        lines.sort(key=sort_key)

        bone_colors = self.globals.configs["bone_colors"]
        bone_thickness = self.globals.configs["bone_thickness"]
        bone_highlight_color = self.globals.configs["bone_highlight_color"]
        bone_highlight = bone_thickness + self.globals.configs["bone_highlight"] * 2
        for i, line in enumerate(lines):
            if line[3]:
                pygame.draw.line(screen, bone_highlight_color, line[0], line[1], bone_highlight)
            pygame.draw.line(screen, bone_colors[i % len(bone_colors)], line[0], line[1], bone_thickness)
    
    def update(self, use_mouse:bool):
        if self.globals.keymap.check_if_key_pressed(pygame.K_TAB):
            self.element += 1
            if self.element >= len(self.rig_elements):
                self.element = 0
        
        element = self.rig_elements[self.element]

        if use_mouse:
            if self.globals.cursor.left_click:
                if element.parent == None:
                    mid_point = (element.start_position - element.end_position) / 2
                    element.start_position.xy = pygame.Vector2(self.globals.cursor.x + self.globals.camera.x, self.globals.cursor.y + self.globals.camera.y) + mid_point
            if self.globals.cursor.right_click:
                if element.parent == None:
                    element.relative_direction = math.atan2(self.globals.cursor.y + self.globals.camera.y - element.start_position.y, self.globals.cursor.x + self.globals.camera.x - element.start_position.x)
                else:
                    element.relative_direction = math.atan2(self.globals.cursor.y + self.globals.camera.y - element.start_position.y, self.globals.cursor.x + self.globals.camera.x - element.start_position.x) - element.parent.direction

        for element in self.rig_elements:
            element.update_position()

    def draw(self, screen:pygame.Surface, camera:pygame.Vector2):
        surfaces = []
        for element in self.rig_elements:
            if element.sprite != None:
                surface = pygame.transform.rotate(element.sprite, -math.degrees(element.direction))
                mid_point = (element.start_position - element.end_position) / 2
                surfaces.append((surface, element.start_position - mid_point - camera, element.layer))
        
        def sort_key(element:tuple):
            return element[2]

        surfaces.sort(key=sort_key)

        for surface in surfaces:
            screen.blit(surface[0], surface[0].get_rect(center = surface[1]))
    
    def fetch_export_data(self):
        x_positions = []; y_positions = []
        for element in self.rig_elements:
            x_positions.append(element.start_position.x)
            x_positions.append(element.end_position.x)
            
            y_positions.append(element.start_position.y)
            y_positions.append(element.end_position.y)

        max_x = max(x_positions) + self.globals.configs["export_padding"][0]
        min_x = min(x_positions) - self.globals.configs["export_padding"][0]
        max_y = max(y_positions) + self.globals.configs["export_padding"][1]
        min_y = min(y_positions) - self.globals.configs["export_padding"][1]

        return min_x, min_y, max_x, max_y
    
    def export(self, surface_size:tuple, min_position:pygame.Vector2):
        export_surface = pygame.Surface(surface_size)

        surfaces = []
        for element in self.rig_elements:
            if element.sprite != None:
                surface = pygame.transform.rotate(element.sprite, -math.degrees(element.direction))
                mid_point = (element.start_position - element.end_position) / 2
                surfaces.append((surface, element.start_position - mid_point - min_position, element.layer))
        
        def sort_key(element:tuple):
            return element[2]

        surfaces.sort(key=sort_key)

        for surface in surfaces:
            export_surface.blit(surface[0], surface[0].get_rect(center = surface[1]))

        return export_surface

    def fetch_save_data(self):
        save_data = {}
        for element in self.rig_elements:
            save_data[element.name] = element.save()
        return save_data
    
    def load_data(self, data:dict):
        for element_name, element_data in data.items():
            for element in self.rig_elements:
                if element.name == element_name:
                    element.load(element_data[0], element_data[1])