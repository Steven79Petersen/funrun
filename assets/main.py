"""Main entry point for the FunRun game."""
import json
import pygame
from game import Game, create_neon_background
import func
from config import MENU, GAME, get_screen_size

pygame.init()

try:
    with open('tasks.json', 'r', encoding='utf-8') as f:
        tasks = json.load(f)
except FileNotFoundError:
    print("tasks.json not found")
    tasks = [
        "Saufi Saufi"
    ]

screen_width, screen_height = get_screen_size()
screen = pygame.display.set_mode((screen_width, screen_height))
screen.fill((0, 0, 0))
pygame.display.set_caption("FUNRUN - Das ultimative Partyspiel")
clock = pygame.time.Clock()

state = MENU
game = None
background = create_neon_background()

while True:
    if state == MENU:
        func.draw_menu(screen, background)
        game, state = func.handle_menu_events(state, game, screen, tasks)
    elif state == GAME:
        result = game.run()
        if result == "restart":
            game = Game(len(game.players), screen, tasks)
        elif result == "menu":
            state = MENU
    clock.tick(60)