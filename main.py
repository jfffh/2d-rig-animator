import pygame
import math
from scripts.globals import global_vars
from scripts.rig_loader import load_rig, load_rig_data, load_rig_from_save
from scripts.configs import load_configs

screen = pygame.display.set_mode((640, 360), pygame.SRCALPHA)
clock = pygame.time.Clock()

def main():
    configs = load_configs("config.json")
    globals = global_vars(
        load_configs("config.json"),
        load_rig_data(configs["rig_path"])
    )

    if globals.configs["load_save_on_boot"] and globals.configs["save_path"] != None:
        if globals.configs["save_path"] != None:
            load_rig_from_save(globals)
    else:
        globals.frame_handler.add_frame()

    run = True

    while run:
        globals.delta_time = clock.tick(60) / 1000

        globals.keymap.set_keys([pygame.K_TAB], False)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            globals.keymap.update_keys(event)
        
        globals.cursor.update(globals.delta_time)

        if globals.keymap.check_if_key_pressed(pygame.K_UP):
            globals.camera.y -= 500 * globals.delta_time
        if globals.keymap.check_if_key_pressed(pygame.K_DOWN):
            globals.camera.y += 500 * globals.delta_time
        if globals.keymap.check_if_key_pressed(pygame.K_LEFT):
            globals.camera.x -= 500 * globals.delta_time
        if globals.keymap.check_if_key_pressed(pygame.K_RIGHT):
            globals.camera.x += 500 * globals.delta_time

        use_mouse = True
        if globals.element_selector.update():
            use_mouse = False
        if globals.frame_selector.update():
            use_mouse = False
        if globals.button_pannel.update():
            use_mouse = False
        
        globals.frame_handler.frame.rig_handler.update(use_mouse)

        screen.fill(globals.configs["background_color"])

        columns = math.floor(screen.width / globals.configs["grid_size"][0]) + 1
        rows = math.floor(screen.height / globals.configs["grid_size"][1]) + 1

        start_x = math.floor(globals.camera.x / globals.configs["grid_size"][0]) * globals.configs["grid_size"][0]
        start_y = math.floor(globals.camera.y / globals.configs["grid_size"][1]) * globals.configs["grid_size"][1]

        for xi in range(columns):
            x = start_x + (xi * globals.configs["grid_size"][0]) - globals.camera.x
            pygame.draw.line(screen, globals.configs["grid_color"], (x, 0), (x, 360), 2)

        for yi in range(rows):
            y = start_y + (yi * globals.configs["grid_size"][1]) - globals.camera.y
            pygame.draw.line(screen, globals.configs["grid_color"], (0, y), (640, y), 2)

        if globals.button_pannel.show_sprites:
            globals.frame_handler.frame.rig_handler.draw(screen, globals.camera)
        if globals.button_pannel.show_bones:
            globals.frame_handler.frame.rig_handler.draw_skeleton(screen, globals.camera)

        globals.element_selector.draw(screen)
        globals.frame_selector.draw(screen)
        globals.button_pannel.draw(screen)

        pygame.display.update()

main()