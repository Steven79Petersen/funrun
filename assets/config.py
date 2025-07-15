"""Configuration and constants for the FunRun game."""
from pygame.math import Vector2
import pygame

# Farbpalette
COLORS = {
    'background': (15, 10, 25),
    'table': (30, 25, 50),
    'field_border': (220, 220, 220),
    'start': (100, 255, 100),
    'finish': (255, 215, 0),
    'normal': (80, 70, 120),
    'back': (255, 100, 100),
    'drink': (255, 175, 0),
    'card': (180, 180, 200),
    'neon_grid': (40, 30, 70),
    'player_colors': [
        (255, 80, 80), (80, 210, 255), (255, 225, 80),
        (80, 255, 110), (210, 80, 255), (80, 255, 255),
        (255, 160, 60), (160, 60, 255)
    ],
    'text_light': (240, 240, 250),
    'text_dark': (30, 30, 40),
    'button': (40, 30, 70),
    'button_border': (180, 180, 220),
    'card_back': (80, 70, 150),  # Helleres Blau für bessere Sichtbarkeit
    'button_restart': (100, 200, 100),
    'button_menu': (200, 100, 100)
}

# Spielfeldkonfiguration
BOARD_ROWS = 5
BOARD_COLS = 13
FIELD_SIZE = 35
BOARD_POS = Vector2(120, 120)
DICE_POS = Vector2(700, 500)
CARD_POS = Vector2(650, 250)
CARD_SIZE = Vector2(180, 220)

# Spielzustände
MENU = 0
GAME = 1
GAME_OVER = 2
state = MENU

# Fonts
pygame.font.init()
font_large = pygame.font.Font(None, 48)
font_medium = pygame.font.Font(None, 28)
font_small = pygame.font.Font(None, 20)  # Kleinere Schrift für Würfel
font_cursive = pygame.font.Font(None, 36)
font_cursive.set_italic(True)

def get_screen_size():
    """Return the default screen size as a tuple (width, height)."""
    return 900, 650

screen_width, screen_height = get_screen_size() 