import pygame
import math
import json
from enum import Enum, auto

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from scripts.globals import global_vars

pygame.font.init()

FONT = pygame.Font("data/consolas.ttf", 10)
FONT.align = pygame.FONT_LEFT

class element_selector:
    class selector:
        class states(Enum):
            unselected = auto()
            hovered_over = auto()
            selected = auto()

        def __init__(self, name:str, width:int, text_color:tuple, background_color:tuple):
            self.name = name
            self.text_surface = FONT.render(self.name, False, text_color, wraplength=width)
            self.background_surface = pygame.Surface((width, self.text_surface.height + 4))
            self.background_surface.fill(background_color)
            self.position = pygame.Vector2((0, 0))
            self.rect = self.background_surface.get_rect()

            self.state = element_selector.selector.states.unselected

        def set_position(self, x:int, y:int):
            self.position.xy = x, y
            self.rect.center = self.position.xy

    def __init__(self, globals:"global_vars", x:int, width:int):
        self.globals = globals
        self.x = x
        self.width = width

    def generate_selectors(self):
        text_color = self.globals.configs["text_color"]
        background_color = self.globals.configs["ui_background_color"]

        self.selectors:list[element_selector.selector] = []
        for element in self.globals.frame_handler.frame.rig_handler.rig_elements:
            self.selectors.append(element_selector.selector(
                element.name,
                self.width,
                text_color,
                background_color
            ))
        
        if len(self.selectors) > 0:
            self.selectors[0].set_position(self.x, self.selectors[0].background_surface.height / 2)
            for i, selector in enumerate(self.selectors[1:]):
                selector.set_position(self.x, self.selectors[i].position.y + self.selectors[i].background_surface.height / 2 + selector.background_surface.height / 2)
    
    def update(self):
        for i, selector in enumerate(self.selectors):
            selector.state = selector.states.unselected
            if i == self.globals.frame_handler.frame.rig_handler.element:
                selector.state = selector.states.selected
            if selector.rect.collidepoint(self.globals.cursor.position):
                selector.state = selector.states.hovered_over
                if self.globals.cursor.new_left_click:
                    selector.state = selector.states.selected
                    self.globals.frame_handler.frame.rig_handler.element = i
        
        if self.globals.cursor.x > self.x - (self.width / 2):
            return True
        return False

    def draw(self, screen:pygame.Surface):
        surface = pygame.Surface((self.width, screen.height))
        surface.fill(self.globals.configs["ui_background_color"])
        surface.set_alpha(25)
        screen.blit(surface, surface.get_rect(centerx = self.x))

        for selector in self.selectors:
            surface = selector.background_surface
            if selector.state == selector.states.unselected:
                surface.set_alpha(75)
            else:
                surface.set_alpha(200)
            screen.blit(surface, surface.get_rect(center = selector.position))
            surface = selector.text_surface
            screen.blit(surface, surface.get_rect(center = selector.position))

class button:
    def __init__(self, text:str, globals:"global_vars", center_left:pygame.Vector2):
        self.globals = globals
        self.text_surface = FONT.render(text, False, globals.configs["text_color"])
        self.background_surface = pygame.Surface((self.text_surface.width + 4, self.text_surface.height + 4))
        self.background_surface.fill(globals.configs["ui_background_color"])
        self.rect = self.background_surface.get_rect()
        self.rect.left = center_left.x
        self.rect.centery = center_left.y
        self.position = pygame.Vector2(self.rect.center)

        self.hovered_over = False
        self.clicked = False

    def update(self):
        self.hovered_over = False
        if self.rect.collidepoint(self.globals.cursor.position):
            self.hovered_over = True
            if self.globals.cursor.left_click and self.clicked == False:
                self.clicked = True
                return True
            elif self.globals.cursor.left_click == False:
                self.clicked = False
        else:
            self.clicked = False
        return False
    
    def draw(self, screen:pygame.Surface):
        surface = self.background_surface
        surface.set_alpha(75 if self.hovered_over == False else 200)
        screen.blit(surface, surface.get_rect(center = self.position))
        surface = self.text_surface
        screen.blit(surface, surface.get_rect(center = self.position))

class frame_selector:
    def __init__(self, globals:"global_vars"):
        self.globals = globals

        self.previous_frame_button = button("<", self.globals, pygame.Vector2(4, 360 - 12))
        self.next_frame_button = button(">", self.globals, pygame.Vector2(self.previous_frame_button.rect.right + 4, 360 - 12))
        self.insert_frame_before_button = button("insert frame before", self.globals, pygame.Vector2(self.next_frame_button.rect.right + 4, 360 - 12))
        self.insert_frame_after_button = button("insert frame after", self.globals, pygame.Vector2(self.insert_frame_before_button.rect.right + 4, 360 - 12))
        self.duplicate_frame_button = button("duplicate frame", self.globals, pygame.Vector2(self.insert_frame_after_button.rect.right + 4, 360 - 12))
        self.delete_frame_button = button("delete frame", self.globals, pygame.Vector2(self.duplicate_frame_button.rect.right + 4, 360 - 12))

        self.rect = pygame.FRect(0, 360 - 44, self.delete_frame_button.rect.right + 4, 44)

        self.text_box = pygame.Surface((self.rect.width - 8, 16))
        self.text_box.fill((255, 255, 255))
        self.text_box.set_alpha(75)
        self.text_box_rect = pygame.FRect(4, 360 - 44 + 4, self.rect.width - 8, 16)

    def update(self):
        if self.previous_frame_button.update():
            self.globals.frame_handler.previous_frame()
        if self.next_frame_button.update():
            self.globals.frame_handler.next_frame()
        if self.insert_frame_before_button.update():
            self.globals.frame_handler.insert_frame_before_current_frame()
        if self.insert_frame_after_button.update():
            self.globals.frame_handler.insert_frame_after_current_frame()
        if self.duplicate_frame_button.update():
            self.globals.frame_handler.duplicate_current_frame()
        if self.delete_frame_button.update():
            self.globals.frame_handler.delete_current_frame()

        if self.rect.collidepoint(self.globals.cursor.position):
            return True
        return False

    def draw(self, screen:pygame.Surface):
        surface = pygame.Surface(self.rect.size)
        surface.fill(self.globals.configs["ui_background_color"])
        surface.set_alpha(25)
        screen.blit(surface, self.rect)

        self.next_frame_button.draw(screen)
        self.previous_frame_button.draw(screen)
        self.insert_frame_before_button.draw(screen)
        self.insert_frame_after_button.draw(screen)
        self.duplicate_frame_button.draw(screen)
        self.delete_frame_button.draw(screen)

        screen.blit(self.text_box, self.text_box_rect)
        surface = FONT.render(f"frame: {self.globals.frame_handler.frame_hash + 1} / {len(self.globals.frame_handler.frames)}", False, self.globals.configs["text_color"])
        screen.blit(surface, surface.get_rect(left = self.text_box_rect.left, centery = self.text_box_rect.centery))

class button_pannel:
    def __init__(self, globals:"global_vars"):
        self.globals = globals

        self.show_bone_button = button("show bones", globals, pygame.Vector2(4, 12))
        self.hide_bone_button = button("hide bones", globals, pygame.Vector2(4, self.show_bone_button.rect.bottom + 14))
        self.show_sprite_button = button("show sprites", globals, pygame.Vector2(self.show_bone_button.rect.right + 4, 12))
        self.hide_sprite_button = button("hide sprites", globals, pygame.Vector2(self.hide_bone_button.rect.right + 4, self.show_sprite_button.rect.bottom + 14))
        self.export_button = button("export", globals, pygame.Vector2(self.show_sprite_button.rect.right + 4, 12))
        self.save_button = button("save", globals, pygame.Vector2(self.hide_sprite_button.rect.right + 4, self.export_button.rect.bottom + 14))

        self.rect = pygame.FRect(0, 0, self.export_button.rect.right + 4, self.save_button.rect.bottom + 4)

        self.show_bones = True
        self.show_sprites = True

    def update(self):
        if self.show_bone_button.update():
            self.show_bones = True
        if self.hide_bone_button.update():
            self.show_bones = False
        if self.show_sprite_button.update():
            self.show_sprites = True
        if self.hide_sprite_button.update():
            self.show_sprites = False
        
        if self.export_button.update():
            export_data = []
            for frame in self.globals.frame_handler.frames:
                export_data.append(frame.rig_handler.fetch_export_data())
            
            def min_x_key(element:tuple):
                return element[0]
            
            def min_y_key(element:tuple):
                return element[1]
            
            def max_x_key(element:tuple):
                return element[2]
            
            def max_y_key(element:tuple):
                return element[3]
            
            min_x = math.floor(min(export_data, key=min_x_key)[0])
            min_y = math.floor(min(export_data, key=min_y_key)[1])
            max_x = math.ceil(max(export_data, key=max_x_key)[2])
            max_y = math.ceil(max(export_data, key=max_y_key)[3])

            export_surface_size = (max_x - min_x, max_y - min_y)
            min_position = (min_x, min_y)

            print(f"exporting with a size of {export_surface_size}...")

            for i, frame in enumerate(self.globals.frame_handler.frames):
                print(f"exporting frame {i}...")
                export_surface = frame.rig_handler.export(export_surface_size, min_position)
                if self.globals.configs["export_tag"] == None:
                    pygame.image.save(export_surface, f"user_data/exports/{self.globals.configs["rig_name"]}-frame-{i}.png")
                else:
                    pygame.image.save(export_surface, f"user_data/exports/{self.globals.configs["rig_name"]}-{self.globals.configs["export_tag"]}-frame-{i}.png")

            print("done exporting!")

        if self.save_button.update():
            if self.globals.configs["save_path"] != None:
                save_data = {}
                for i, frame in enumerate(self.globals.frame_handler.frames):
                    save_data[str(i)] = frame.rig_handler.fetch_save_data()
                
                file = open(self.globals.configs["save_path"], "w")
                json.dump(save_data, file)
                file.close()

        if self.rect.collidepoint(self.globals.cursor.position):
            return True
        return False

    def draw(self, screen:pygame.Surface):
        surface = pygame.Surface(self.rect.size)
        surface.fill(self.globals.configs["ui_background_color"])
        surface.set_alpha(25)
        screen.blit(surface, self.rect)

        self.show_bone_button.draw(screen)
        self.hide_bone_button.draw(screen)
        self.show_sprite_button.draw(screen)
        self.hide_sprite_button.draw(screen)
        self.export_button.draw(screen)
        self.save_button.draw(screen)