import pygame

#for handling key presses
class keymap:
    __slots__ = ("keys")
    def __init__(self):
        self.keys = {}

    def update_keys(self, event:pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            self.keys[event.key] = True
        if event.type == pygame.KEYUP:
            self.keys[event.key] = False

    def set_keys(self, keys:int|list, state:bool):
        if type(keys) == int:
            self.keys[keys] = state
        else:
            for key in keys:
                self.keys[key] = state

    def check_if_key_pressed(self, key_code:int):
        if key_code in self.keys:
            return self.keys[key_code]
        else:
            return False

#for handling mouse interactions
class cursor:
    __slots__ = ("left_click", "right_click", "left_click_time", "right_click_time", "left_click_registered", "right_click_registered")
    def __init__(self):
        self.left_click = False
        self.right_click = False

        self.left_click_time = 0
        self.right_click_time = 0

        self.left_click_registered = False
        self.right_click_registered = False

    def update(self, delta_time:float):
        buttons = pygame.mouse.get_pressed()
        self.left_click = buttons[0]
        self.right_click = buttons[2]

        if self.left_click:
            self.left_click_time += 1000 * delta_time
        else:
            self.left_click_time = 0
            self.left_click_registered = False

        if self.right_click:
            self.right_click_time += 1000 * delta_time
        else:
            self.right_click_time = 0
            self.right_click_registered = False
        
    @property
    def clicked(self):
        return self.right_click_time > 0 or self.left_click_time > 0
    
    @property
    def position(self):
        return (self.x, self.y)
    
    @property
    def x(self):
        return pygame.mouse.get_pos()[0]
    
    @property
    def y(self):
        return pygame.mouse.get_pos()[1]
    
    def register_left_click(self):
        self.left_click_registered = True

    def register_right_click(self):
        self.right_click_registered = True

    @property
    def new_left_click(self):
        return self.left_click and self.left_click_registered == False
    
    @property
    def new_right_click(self):
        return self.right_click and self.right_click_registered == False
