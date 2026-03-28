from copy import deepcopy
from scripts.rig_handler import rig_handler
from scripts.rig_loader import load_rig

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from scripts.globals import global_vars

class frame:
    def __init__(self, globals:"global_vars"):
        self.globals = globals
        self.rig_handler = rig_handler(globals)
        load_rig(globals.rig_data, self.rig_handler)

    def copy(self):
        new_frame = frame(self.globals)
        new_frame.rig_handler = deepcopy(self.rig_handler)
        new_frame.rig_handler.globals = self.globals
        return new_frame

class frame_handler:
    def __init__(self, globals:"global_vars"):
        self.globals = globals
        self.frames = []
        self.frame_hash = 0

    def add_frame(self):
        self.frames.append(frame(self.globals))
        self.globals.element_selector.generate_selectors()

    @property
    def frame(self):
        return self.frames[self.frame_hash]
    
    def next_frame(self):
        self.frame_hash += 1
        if self.frame_hash >= len(self.frames):
            self.frame_hash = 0

    def previous_frame(self):
        self.frame_hash -= 1
        if self.frame_hash < 0:
            self.frame_hash = len(self.frames) - 1
    
    def insert_frame_before_current_frame(self):
        self.frames.insert(self.frame_hash, frame(self.globals))
        self.frame_hash += 1
        self.globals.element_selector.generate_selectors()

    def insert_frame_after_current_frame(self):
        self.frames.insert(self.frame_hash + 1, frame(self.globals))
        self.globals.element_selector.generate_selectors()

    def duplicate_current_frame(self):
        self.frames.insert(self.frame_hash + 1, self.frames[self.frame_hash].copy())
        self.globals.element_selector.generate_selectors()

    def delete_current_frame(self):
        if len(self.frames) > 1:
            self.frames.pop(self.frame_hash)
            if self.frame_hash >= len(self.frames):
                self.frame_hash = 0
    
    def clear(self):
        self.frames.clear()
        self.frame_hash = 0