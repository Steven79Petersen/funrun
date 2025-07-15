import pygame
from pygame import Vector2
from config import COLORS, font_small

class Player:
    """Represents a player in the game."""
    def __init__(self, player_id, color_idx):
        """Initialize a Player with an ID and color index."""
        self.id = player_id
        self.color = COLORS['player_colors'][color_idx]
        self.position = 0
        self.drinks = 0
        self.skip_turn = False

    def draw(self, fields, screen):
        """Draw the player on the provided screen at their current field position."""
        if self.position >= len(fields):
            return
        field = fields[self.position]
        center = Vector2(field.rect.center)
        pygame.draw.circle(screen, (30, 30, 30), (center.x + 3, center.y + 3), 18)
        pygame.draw.circle(screen, self.color, center, 16)
        pygame.draw.circle(screen, (255, 255, 255), center, 16, 2)
        pygame.draw.circle(
            screen,
            (min(self.color[0] + 60, 255), min(self.color[1] + 60, 255), min(self.color[2] + 60, 255)),
            (center.x - 4, center.y - 4), 6
        )
        text = font_small.render(str(self.id + 1), True, COLORS['text_dark'])
        screen.blit(text, (center.x - text.get_width() // 2, center.y - text.get_height() // 2))
