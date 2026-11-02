import os
from collections import deque

import pygame

import drawing
from mazerunner import MazeRunner

LEVEL_FILE = 'lastlevel.txt'
SAVE_FILE = 'savegame.txt'


def cooadd(coo, dxdy):
    return (coo[0] + dxdy[0], coo[1] + dxdy[1])


def cell_symbol(cell: list[str]) -> str:
    """Stack of items on a grid cell to its Sokoban level symbol."""
    return {'.@': '+', '.$': '*'}.get(''.join(cell), cell[-1] if cell else ' ')


class Game:
    def __init__(self, grid):
        self.grid = grid
        self.active = False
        if os.path.isfile(LEVEL_FILE):
            with open(LEVEL_FILE) as f:
                self.level = int(f.read())
        else:
            self.level = 1
        self.move_path = []

    def start_level(self, set='', level=-1):
        if not set:
            set = self.last_set
        self.last_set = set
        self.level = level if level > -1 else self.level
        self.load_level()
        self.init_level()
        self.states = deque()

    def load_level(self):
        self.grid.update_automatic = False
        self.grid.load(f'levels/{self.last_set}/level{self.level:003}.txt', resize=True)
        pygame.display.set_caption(f'Sokoban - {self.last_set} - level {self.level}')
        self.grid.update_automatic = True
        self.grid.redraw()
        with open(LEVEL_FILE, 'w') as f:
            f.write(str(self.level))

    def retrace_state(self):
        """Backup a move"""
        if not self.states:
            return
        state = self.states.pop()
        self.grid.update_automatic = False
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                self.grid.clear((x, y))
                for item in state.grid[y][x]:
                    self.grid.push((x, y), item)
                if self.grid[x, y] == '@':
                    self.hero_pos = (x, y)
        self.grid.update_automatic = True
        self.grid.redraw()

    def init_level(self):
        # Scan the newly loaded level and set game state accordingly
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                if self.grid[x, y] == '@':
                    self.hero_pos = (x, y)
                    self.grid[x, y] = ' '
                    self.grid.push((x, y), '@')
                elif self.grid[x, y] == '+':  # Hero on goal
                    self.hero_pos = (x, y)
                    self.grid[x, y] = '.'
                    self.grid.push((x, y), '@')
                elif self.grid[x, y] == '-':
                    self.grid.clear((x, y))
                elif self.grid[x, y] == '$':  # Box
                    self.grid[x, y] = ' '
                    self.grid.push((x, y), '$')
                elif self.grid[x, y] == '*':  # Box on goal
                    self.grid[x, y] = '.'
                    self.grid.push((x, y), '$')
        self.active = True

    def abs_move(self, pos):
        self.grid.pop(self.hero_pos)
        self.hero_pos = pos
        self.grid.push(pos, '@')

    def rel_move(self, dxdy):
        self.abs_move(cooadd(self.hero_pos, dxdy))

    def move_hero(self, dxdy):

        if not self.active:
            return

        target = self.grid[cooadd(self.hero_pos, dxdy)]

        # empty or earth -> move
        if target in (' ', '.'):
            self.rel_move(dxdy)

        # pushing a crate
        elif target in ('$', '*'):
            first_pos = cooadd(self.hero_pos, dxdy)
            second_pos = cooadd(first_pos, dxdy)
            if self.grid[second_pos] in (' ', '.'):
                self.states.append(self.grid.snapshot())  # Save state for undoing
                self.grid.pop(first_pos)
                self.grid.push(second_pos, '$')
                self.rel_move(dxdy)

        self.check_win()

    def move_to_pos(self, endpos):
        mr = MazeRunner(self.grid)
        path = mr.find_path(self.hero_pos, endpos)
        if path:
            self.move_path = path
            self.active = False  # First let the hero move to the new spot

    def timer_step(self):
        if not self.move_path:
            return
        self.abs_move(self.move_path[0])
        self.move_path = self.move_path[1:]
        if not self.move_path:
            self.active = True  # Finished moving

    def check_win(self):
        for x in range(self.grid.width):
            for y in range(self.grid.height):
                if self.grid[x, y, 0] == '.':
                    if self.grid[x, y] != '$':
                        return False
        drawing.full_screen_message(self.grid, drawing.GREEN, 'Level complete!')
        self.level += 1
        self.active = False

    def save_state(self):
        if not self.active:
            return
        with open(SAVE_FILE, 'w') as f:
            f.write(self.board_text())

    def board_text(self) -> str:
        """Current board in standard Sokoban text notation."""
        return ''.join(''.join(cell_symbol(cell) for cell in row) + '\n' for row in self.grid.grid)

    def load_state(self):
        if not os.path.isfile(SAVE_FILE):
            return
        self.grid.update_automatic = False
        self.grid.load(SAVE_FILE, resize=True)
        self.grid.update_automatic = True
        self.init_level()
        self.states = deque()
        self.grid.redraw()
