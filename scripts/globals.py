import pygame
from scripts.inputs import keymap, cursor
from scripts.rig_handler import rig_handler
from scripts.ui import element_selector, frame_selector, button_pannel
from scripts.frame import frame_handler

class global_vars:
    def __init__(self, configs:dict, rig_data:dict):
        self.configs = configs
        self.rig_data = rig_data

        self.keymap = keymap()
        self.cursor = cursor()

        self.frame_handler = frame_handler(self)
        self.element_selector = element_selector(self, 640 - 60, 120)

        self.delta_time = 0

        self.camera = pygame.Vector2(-320, -180)

        self.frame_selector = frame_selector(self)

        self.button_pannel = button_pannel(self)