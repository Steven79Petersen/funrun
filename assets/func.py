import sys
import pygame
from pygame.math import Vector2
from game import Game, create_neon_background
from config import COLORS, GAME, font_large, font_medium, screen_width, screen_height, state

def draw_menu(screen, neon_background):
    """Draw the main menu on the provided screen with a neon background."""
    screen.blit(neon_background, (0, 0))

    # Titel
    title = font_large.render("FUNRUN", True, (255, 120, 120))
    subtitle = font_medium.render("Das ultimative Partyspiel", True, (200, 220, 255))

    # Titel-Glow
    for i in range(4, 0, -1):
        glow_surf = pygame.Surface((title.get_width() + i * 15, title.get_height() + i * 15), pygame.SRCALPHA)
        glow_title = font_large.render("FUNRUN", True, (255, 100, 100, i * 20))
        glow_surf.blit(glow_title, (i * 8, i * 8))
        screen.blit(glow_surf, (screen_width // 2 - title.get_width() // 2 - i * 8, 100 - i * 8))

    screen.blit(title, (screen_width // 2 - title.get_width() // 2, 100))
    screen.blit(subtitle, (screen_width // 2 - subtitle.get_width() // 2, 160))

    # Menübuttons
    buttons = [
        {"text": "Allein zu Hause", "pos": Vector2(screen_width // 2, 250), "color": (255, 180, 100)},
        {"text": "Gruppen-Therapie", "pos": Vector2(screen_width // 2, 350), "color": (180, 255, 100)}
    ]

    for button in buttons:
        text = font_medium.render(button["text"], True, button["color"])
        text_width = text.get_width()
        text_height = text.get_height()

        button_width = text_width + 40
        button_height = text_height + 20
        button_rect = pygame.Rect(button["pos"].x - button_width // 2, button["pos"].y - button_height // 2,
                                  button_width, button_height)

        pygame.draw.rect(screen, COLORS['button'], button_rect, border_radius=15)
        pygame.draw.rect(screen, button["color"], button_rect, 3, border_radius=15)
        screen.blit(text, (button["pos"].x - text_width // 2, button["pos"].y - text_height // 2))

    # Vorschau-Spielfeld
    preview_pos = Vector2(screen_width // 2 - 100, 450)
    pygame.draw.rect(screen, (40, 30, 70), (preview_pos.x, preview_pos.y, 200, 100), border_radius=10)

    # Mini-Spielfeld
    for row in range(2):
        for col in range(6):
            color = COLORS['normal']
            if row == 0 and col == 0:
                color = COLORS['start']
            elif row == 1 and col == 5:
                color = COLORS['finish']
            elif (row + col) % 3 == 0:
                color = COLORS['card']
            elif (row + col) % 4 == 0:
                color = COLORS['drink']

            pygame.draw.rect(screen, color, (preview_pos.x + 20 + col * 25, preview_pos.y + 20 + row * 35, 20, 25))
            pygame.draw.rect(screen, COLORS['field_border'],
                             (preview_pos.x + 20 + col * 25, preview_pos.y + 20 + row * 35, 20, 25), 1)

    # Spieler-Chips
    for i in range(3):
        pygame.draw.circle(screen, COLORS['player_colors'][i],
                           (preview_pos.x + 40 + i * 40, preview_pos.y + 80), 8)

    pygame.display.flip()

def handle_menu_events(state, game, screen, tasks):
    """Handle menu events and return the updated game and state."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if (screen_width // 2 - 120 <= x <= screen_width // 2 + 120 and 230 <= y <= 270):
                game = Game(2, screen, tasks)
                state = GAME
            elif (screen_width // 2 - 120 <= x <= screen_width // 2 + 120 and 330 <= y <= 370):
                game = Game(4, screen, tasks)
                state = GAME
    return game, state