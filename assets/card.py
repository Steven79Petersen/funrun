import pygame
from config import COLORS, CARD_SIZE, font_medium, font_small, font_cursive

class Card:
    """Represents a task card in the game."""
    def __init__(self, task):
        """Initialize a Card with a task description."""
        self.task = task
        self.visible = False

    def draw(self, pos, screen):
        """Draw the card at the given position on the provided screen."""
        if self.visible:
            # Draw card front
            pygame.draw.rect(screen, (20, 15, 30), (pos.x, pos.y, CARD_SIZE.x, CARD_SIZE.y), border_radius=10)
            pygame.draw.rect(screen, COLORS['card'], (pos.x, pos.y, CARD_SIZE.x, CARD_SIZE.y), 3, border_radius=10)
            words = self.task.split(' ')
            lines = []
            current_line = []
            for word in words:
                test_line = ' '.join(current_line + [word])
                if font_medium.size(test_line)[0] < CARD_SIZE.x - 30:
                    current_line.append(word)
                else:
                    lines.append(' '.join(current_line))
                    current_line = [word]
            lines.append(' '.join(current_line))
            for i, line in enumerate(lines):
                text_shadow = font_medium.render(line, True, (0, 0, 0, 150))
                screen.blit(text_shadow, (pos.x + CARD_SIZE.x // 2 - text_shadow.get_width() // 2 + 2,
                                          pos.y + 40 + i * 30 + 2))
                text = font_medium.render(line, True, COLORS['text_light'])
                screen.blit(text, (pos.x + CARD_SIZE.x // 2 - text.get_width() // 2,
                                   pos.y + 40 + i * 30))
        else:
            pygame.draw.rect(screen, COLORS['card_back'], (pos.x, pos.y, CARD_SIZE.x, CARD_SIZE.y), border_radius=10)
            pygame.draw.rect(screen, COLORS['card'], (pos.x, pos.y, CARD_SIZE.x, CARD_SIZE.y), 3, border_radius=10)
            for i in range(3, 0, -1):
                glow = font_cursive.render("FunRun", True, (220, 220, 255, i * 60))
                screen.blit(glow, (pos.x + CARD_SIZE.x // 2 - glow.get_width() // 2,
                                   pos.y + CARD_SIZE.y // 2 - glow.get_height() // 2))
            title = font_cursive.render("FunRun", True, (240, 240, 255))
            screen.blit(title, (pos.x + CARD_SIZE.x // 2 - title.get_width() // 2,
                                pos.y + CARD_SIZE.y // 2 - title.get_height() // 2))
            if hasattr(self, 'card_number'):
                text = font_small.render(f"#{self.card_number}", True, (240, 240, 255))
                screen.blit(text, (pos.x + 10, pos.y + 10))
            pygame.draw.line(screen, (180, 180, 220, 100), (pos.x + 30, pos.y + 50),
                             (pos.x + CARD_SIZE.x - 30, pos.y + 50), 2)
            pygame.draw.line(screen, (180, 180, 220, 100), (pos.x + 30, pos.y + CARD_SIZE.y - 50),
                             (pos.x + CARD_SIZE.x - 30, pos.y + CARD_SIZE.y - 50), 2)
