import pygame
import pygame.gfxdraw

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_GRAY = (192, 192, 192)
GRAY = (128, 128, 128)
DARK_GRAY = (45, 45, 45)
GREEN = (12, 160, 12)

TOP_LEFT = 0
TOP_RIGHT = 1


def draw_line(grid, cell_dimensions, fromcoo, tocoo, color, width):
    x, y, w, h = cell_dimensions
    pygame.draw.line(
        grid.screen,
        color,
        (x + w * fromcoo[0] // 100, y + h * fromcoo[1] // 100),
        (x + w * tocoo[0] // 100, y + h * tocoo[1] // 100),
        w * width // 100,
    )


def draw_circle(grid, cell_dimensions, pos, radius, color=DARK_GRAY):
    x, y, w, h = cell_dimensions
    pygame.gfxdraw.aacircle(grid.screen, x + w * pos[0] // 100, y + h * pos[1] // 100, w * radius // 200, color)
    pygame.gfxdraw.filled_circle(grid.screen, x + w * pos[0] // 100, y + h * pos[1] // 100, w * radius // 200, color)


def draw_rect(grid, cell_dimensions, lefttop, rightbottom, color):
    x, y, w, h = cell_dimensions
    pygame.draw.rect(
        grid.screen,
        color,
        (
            x + w * lefttop[0] // 100,
            y + h * lefttop[1] // 100,
            w * (rightbottom[0] - lefttop[0]) // 100,
            h * (rightbottom[1] - lefttop[1]) // 100,
        ),
    )


def draw_text(grid, cell_dimensions, text, pos, size, color):
    x, y, w, h = cell_dimensions
    font = pygame.font.Font(grid.font, h * size // 100)
    text = font.render(text, True, WHITE)
    text_rect = text.get_rect()
    text_rect.center = (x + w * pos[0] // 100, y + h * pos[1] // 100)
    grid.screen.blit(text, text_rect)


# Specific drawing routines


def draw_target(grid, cell_dimensions):
    draw_circle(grid, cell_dimensions, (50, 50), 20, GREEN)


def draw_hero(grid, cell_dimensions):
    HAT = (200, 0, 0)
    SKIN = (190,160,60)
    SUIT = (20,20,120)
    draw_circle(grid, cell_dimensions, (50, 15), 20, HAT)  # Hat
    draw_circle(grid, cell_dimensions, (50, 60), 60, SUIT)  # Body
    draw_circle(grid, cell_dimensions, (50, 25), 35, SKIN)  # Head
    draw_circle(grid, cell_dimensions, (45, 25), 7, GRAY)  # Eyes
    draw_circle(grid, cell_dimensions, (55, 25), 7, GRAY)  # Eyes
    draw_line(grid, cell_dimensions, (50, 50), (65, 98), SUIT, 20) # legs
    draw_line(grid, cell_dimensions, (50, 50), (35, 98), SUIT, 20)
    draw_circle(grid, cell_dimensions, (10, 25), 15, SKIN)  # Hands
    draw_circle(grid, cell_dimensions, (90, 25), 15, SKIN)
    draw_line(grid, cell_dimensions, (50, 50), (10, 25), SUIT, 20) # arms
    draw_line(grid, cell_dimensions, (50, 50), (90, 25), SUIT, 20)


def draw_general_box(grid, cell_dimensions, back_color, fore_color):
    draw_rect(grid, cell_dimensions, (10, 10), (90, 90), back_color)
    for x in range(10, 91, 18):
        draw_line(grid, cell_dimensions, (x, 20), (x, 80), fore_color, 5)
    draw_line(grid, cell_dimensions, (20, 20), (75, 75), back_color, 20)
    draw_line(grid, cell_dimensions, (30, 20), (75, 65), fore_color, 5)
    draw_line(grid, cell_dimensions, (20, 30), (65, 75), fore_color, 5)
    draw_line(grid, cell_dimensions, (10, 20), (85, 20), fore_color, 5)
    draw_line(grid, cell_dimensions, (10, 80), (85, 80), fore_color, 5)


def draw_box(grid, cell_dimensions):
    draw_general_box(grid, cell_dimensions, (200, 150, 70), (100, 70, 30))


def draw_box_on_goal(grid, cell_dimensions):
    draw_general_box(grid, cell_dimensions, (100, 75, 35), (50, 35, 15))


def draw_brick(grid, cell_dimensions):
    BRICK_COLOR = (180, 160, 50)
    ADD_COLOR = (100, 70, 30)
    draw_rect(grid, cell_dimensions, (0, 0), (100, 100), BRICK_COLOR)
    for y in (0, 25, 50, 75, 100):
        draw_line(grid, cell_dimensions, (0, y), (100, y), ADD_COLOR, 5)
    for x in (0, 50, 100):
        draw_line(grid, cell_dimensions, (x, 0), (x, 25), ADD_COLOR, 5)
        draw_line(grid, cell_dimensions, (x, 50), (x, 75), ADD_COLOR, 5)
    for x in (25, 75):
        draw_line(grid, cell_dimensions, (x, 25), (x, 50), ADD_COLOR, 5)
        draw_line(grid, cell_dimensions, (x, 75), (x, 100), ADD_COLOR, 5)


def full_screen_message(grid, color, message):
    play_area_dimensions = grid.cell_dimensions(0, 0, grid.width, grid.height)
    pygame.draw.rect(grid.screen, color, play_area_dimensions)
    draw_text(grid, play_area_dimensions, message, (50, 50), 12, WHITE)
    pygame.display.flip()


def blit_text(grid, text, font, color, coo, adjust):
    sx, sy, sw, sh = grid.get_sidebar_dimensions()
    x = sx + sw * coo[0] // 100
    y = sy + sh * coo[1] // 100
    rendered = font.render(text, True, color)
    text_rect = rendered.get_rect()
    if adjust == TOP_LEFT:
        text_rect.topleft = (x, y)
    elif adjust == TOP_RIGHT:
        text_rect.topright = (x, y)
    grid.screen.blit(rendered, text_rect)
    return text_rect


def sidebar_message(grid, coo, text):
    grid.clear_sidebar(DARK_GRAY)
    font = pygame.font.Font(grid.font, 18)
    blit_text(grid, text, font, WHITE, coo, TOP_LEFT)
    pygame.display.flip()


class LevelButton(pygame.sprite.Sprite):
    def __init__(self, grid, level, color):
        # Call the parent class (Sprite) constructor
        super().__init__()
        self.grid = grid
        self.level = level
        self.font = pygame.font.Font(pygame.font.get_default_font(), 12)
        self.color = color
        self.x = 48 + 1.7 * ((level - 1) % 30)
        self.y = 10 + ((level - 1) // 30) * 50

    def show(self):
        self.rect = blit_text(self.grid, str(self.level), self.font, self.color, (self.x, self.y), TOP_RIGHT)


def level_buttons(grid, curlevel):
    buttons = pygame.sprite.Group()
    for l in range(60):
        level = l + 1
        color = LIGHT_GRAY if level <= curlevel else GRAY
        button = LevelButton(grid, level, color)
        buttons.add(button)
    return buttons


def show_levels(grid, level):
    buttons = level_buttons(grid, level)
    font = pygame.font.Font(grid.font, 12)
    blit_text(grid, 'choose', font, GRAY, (46, 10), TOP_RIGHT)
    blit_text(grid, 'a level', font, GRAY, (46, 60), TOP_RIGHT)
    for button in buttons:
        button.show()
    pygame.display.flip()
    return buttons
