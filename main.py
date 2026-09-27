import sys
from functools import partial

import pygame
from gridworld.grid import Grid

import drawing
from game_logic import Game

# TODO:
# - Pack and level chooser


def key_action(key, game):
    if key == pygame.K_q:
        sys.exit()
    elif key == pygame.K_s:
        game.save_state()
    elif key == pygame.K_l:
        game.load_state()
    elif key == pygame.K_BACKSPACE:
        game.retrace_state()
    elif key == pygame.K_r or not (game.active or game.move_path):
        game.start_level()
    else:
        moves = {
            pygame.K_LEFT: (-1, 0),
            pygame.K_RIGHT: (1, 0),
            pygame.K_UP: (0, -1),
            pygame.K_DOWN: (0, 1),
            pygame.K_SPACE: (0, 0),
        }
        movement = moves.get(key)
        if movement:
            game.move_hero(movement)


def cell_click(pos, game):
    game.move_to_pos(pos)


# def mouse_click(pos, game):
#    for button in game.level_buttons:
#        if button.rect.collidepoint(*pos):
#            game.start_level(button.level)


def setup_grid():
    grid = Grid(
        10,
        10,
        33,
        33,
        title='Sokoban',
        cellcolor=drawing.LIGHT_GRAY,
        framerate=60,
        full_screen=False,
    )
    grid.update_fullscreen = False  # Only update the changed bits
    grid.set_drawaction('_', partial(grid.draw_background, color=(60, 60, 60)))
    grid.set_drawaction('#', drawing.draw_brick)
    grid.set_drawaction('.', drawing.draw_target)
    grid.set_drawaction('$', drawing.draw_box)
    grid.set_drawaction('*', drawing.draw_box_on_goal)
    grid.set_drawaction('@', drawing.draw_hero)

    return grid


if __name__ == '__main__':
    grid = setup_grid()
    game = Game(grid)

    grid.set_timer_action(partial(game.timer_step))
    grid.set_key_action(partial(key_action, game=game))
    grid.set_cell_click_action(partial(cell_click, game=game))
    # grid.set_mouse_click_action(partial(mouse_click, game=game))
    # grid.set_update_sidebar_action(game.update_sidebar)
    pygame.key.set_repeat(100, 60)
    game.start_level('sasquatch1')
    grid.run()
