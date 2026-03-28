import json
import math
import pygame

from scripts.rig_element import rig_element
from scripts.rig_handler import rig_handler

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from scripts.globals import global_vars

def load_rig_data(rig_path:str):
    file = open(rig_path)
    data = json.load(file)
    file.close()
    return data

def load_rig(rig_data:dict[dict], rig_handler:rig_handler):
    rig_data = rig_data.copy()

    elements = {}
    parents = [None]
    elements_with_parent = []

    while len(rig_data) > 0:
        for element_name, element in rig_data.items():
            if element["parent"] in parents:
                elements_with_parent.append(element_name)
        
        parents.clear()

        for element_name in elements_with_parent:
            element = rig_data[element_name]
            elements[element_name] = rig_element(
                    element_name,
                    element["length"],
                    math.radians(-element.get("direction", 0)),
                    elements[element["parent"]] if element["parent"] != None else None,
                    element.get("bind_to_end", True),
                    element.get("layer", 0),
                    pygame.image.load(surface_file).convert_alpha() if (surface_file := element.get("sprite")) != None else None
            )

            del rig_data[element_name]

            if element_name not in parents:
                parents.append(element_name)
        
        elements_with_parent = []
    
    for element in elements.values():
        rig_handler.add_element(element)

def load_rig_from_save(globals:"global_vars"):
    file = open(globals.configs["save_path"])
    save_data = json.load(file)
    file.close()

    frames = len(save_data)

    globals.frame_handler.clear()
    for i in range(frames):
        globals.frame_handler.add_frame()
        globals.frame_handler.frames[i].rig_handler.load_data(save_data[str(i)])


            