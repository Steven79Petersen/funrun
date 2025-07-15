import pygame
from config import COLORS, FIELD_SIZE, font_small

class Field:
    """Represents a field on the game board."""
    def __init__(self, pos, index):
        """Initialize a Field with a position and index."""
        self.pos = pos
        self.index = index
        self.rect = pygame.Rect(pos.x, pos.y, FIELD_SIZE, FIELD_SIZE)
        self.type = 'normal'

    def draw(self, screen):
        """Draw the field on the provided screen."""
        pygame.draw.rect(screen, COLORS[self.type], self.rect)
        pygame.draw.rect(screen, COLORS['field_border'], self.rect, 2)
        text = font_small.render(str(self.index), True, COLORS['text_dark'])
        screen.blit(text, (self.pos.x + FIELD_SIZE // 2 - text.get_width() // 2,
                           self.pos.y + FIELD_SIZE // 2 - text.get_height() // 2))
