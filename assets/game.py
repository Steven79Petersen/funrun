import random
import sys
import pygame
from pygame import Vector2
from card import Card
from field import Field
from config import COLORS, BOARD_POS, FIELD_SIZE, DICE_POS, CARD_POS, CARD_SIZE, font_small, font_large, font_medium, screen_width, screen_height
from player import Player

clock = pygame.time.Clock()

def create_neon_background():
    """Create and return a neon-styled background surface."""
    background = pygame.Surface((screen_width, screen_height))
    background.fill(COLORS['background'])
    for i in range(3, 0, -1):
        glow = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        pygame.draw.rect(glow, (100, 50, 150, 5 * i),
                        (50 - i * 10, 50 - i * 10, screen_width - 100 + i * 20, screen_height - 100 + i * 20),
                        border_radius=20 + i * 5)
        background.blit(glow, (0, 0))
    for _ in range(50):
        x, y = random.randint(0, screen_width), random.randint(0, screen_height)
        size = random.randint(1, 3)
        brightness = random.randint(200, 255)
        pygame.draw.circle(background, (brightness, brightness, brightness), (x, y), size)
    return background

class Game:
    """Main game logic and state management."""
    def __init__(self, num_players, screen, tasks):
        """Initialize the game with the given number of players, screen, and tasks."""
        self.players = [Player(i, i % len(COLORS['player_colors'])) for i in range(num_players)]
        self.current_player = 0
        self.dice_value = 0
        self.fields = []
        self.create_board()
        self.screen = screen
        self.deck = [Card(task) for task in tasks]
        for i, card in enumerate(self.deck):
            card.card_number = i + 1
        random.shuffle(self.deck)
        self.current_card = None
        self.message = ""
        self.message_time = 0
        self.waiting_for_card = False
        self.game_over = False
        self.moving = False
        self.move_steps = 0
        self.target_position = 0
        self.winner = None
        self.neon_background = create_neon_background()

    def create_board(self):
        """Create the game board fields and assign their types."""
        positions = []
        for col in range(13):
            positions.append(Vector2(BOARD_POS.x + col * FIELD_SIZE, BOARD_POS.y))
        for col in range(13):
            positions.append(Vector2(BOARD_POS.x + (12 - col) * FIELD_SIZE, BOARD_POS.y + FIELD_SIZE))
        for col in range(13):
            positions.append(Vector2(BOARD_POS.x + col * FIELD_SIZE, BOARD_POS.y + 2 * FIELD_SIZE))
        for col in range(13):
            positions.append(Vector2(BOARD_POS.x + (12 - col) * FIELD_SIZE, BOARD_POS.y + 3 * FIELD_SIZE))
        for col in range(13):
            positions.append(Vector2(BOARD_POS.x + col * FIELD_SIZE, BOARD_POS.y + 4 * FIELD_SIZE))
        for i, pos in enumerate(positions):
            field = Field(pos, i)
            if i == 0:
                field.type = 'start'
            elif i == 61:
                field.type = 'finish'
            elif i % 3 == 0:
                field.type = 'card'
            elif i % 5 == 0:
                field.type = 'drink'
            elif i % 7 == 0:
                field.type = 'back'
            self.fields.append(field)

    def roll_dice(self):
        """Handle dice rolling and initiate player movement."""
        if self.dice_value == 0 and not self.waiting_for_card and not self.game_over and not self.moving:
            self.dice_value = random.randint(1, 3)
            player = self.players[self.current_player]
            if not player.skip_turn:
                self.target_position = min(player.position + self.dice_value, len(self.fields) - 1)
                self.move_steps = self.dice_value
                self.moving = True
            else:
                player.skip_turn = False
                self.show_message(f"Spieler {self.current_player + 1} setzt aus!")
                self.current_player = (self.current_player + 1) % len(self.players)

    def update_movement(self):
        """Update player movement animation."""
        if self.moving:
            player = self.players[self.current_player]
            if player.position < self.target_position and self.move_steps > 0:
                player.position += 1
                self.move_steps -= 1
                pygame.time.delay(200)
            else:
                self.moving = False
                self.handle_field_action()

    def handle_field_action(self):
        """Handle the action when a player lands on a field."""
        player = self.players[self.current_player]
        field = self.fields[player.position]
        if field.type == 'back':
            player.position = max(0, player.position - 2)
            self.show_message(f"Spieler {self.current_player + 1} geht 2 Felder zurück!")
            pygame.time.delay(500)
        elif field.type == 'drink':
            player.drinks += 1
            self.show_message(f"Spieler {self.current_player + 1} muss trinken!")
        elif field.type == 'card':
            if self.deck:
                self.current_card = self.deck.pop()
                self.current_card.visible = True
                self.waiting_for_card = True
                self.show_message(f"Spieler {self.current_player + 1} zieht eine Karte!")
                return
        if player.position >= 61:
            player.position = 61
            self.game_over = True
            self.winner = self.current_player
            self.show_message(f"Spieler {self.current_player + 1} hat gewonnen!")
        elif not self.waiting_for_card and not self.game_over:
            self.current_player = (self.current_player + 1) % len(self.players)
            self.dice_value = 0

    def show_message(self, msg):
        """Display a message to the players."""
        self.message = msg
        self.message_time = pygame.time.get_ticks()

    def draw_dice(self):
        """Draw the dice on the screen."""
        pygame.draw.rect(self.screen, (200, 200, 230), (DICE_POS.x, DICE_POS.y, 80, 80), border_radius=10)
        pygame.draw.rect(self.screen, (230, 230, 255), (DICE_POS.x, DICE_POS.y, 80, 80), 3, border_radius=10)
        dot_color = (40, 40, 60)
        center = DICE_POS + Vector2(40, 40)
        if self.dice_value > 0:
            if self.dice_value == 1:
                pygame.draw.circle(self.screen, dot_color, center, 8)
            elif self.dice_value == 2:
                pygame.draw.circle(self.screen, dot_color, center + Vector2(-20, -20), 6)
                pygame.draw.circle(self.screen, dot_color, center + Vector2(20, 20), 6)
            elif self.dice_value == 3:
                pygame.draw.circle(self.screen, dot_color, center + Vector2(-20, -20), 6)
                pygame.draw.circle(self.screen, dot_color, center, 6)
                pygame.draw.circle(self.screen, dot_color, center + Vector2(20, 20), 6)
        else:
            text = font_small.render("WÜRFELN", True, dot_color)
            self.screen.blit(text, (center.x - text.get_width() // 2, center.y - text.get_height() // 2))

    def draw_game_over(self):
        """Draw the game over screen and winner announcement."""
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        winner_text = font_large.render(f"Spieler {self.winner + 1} hat gewonnen!", True, COLORS['player_colors'][self.winner])
        self.screen.blit(winner_text, (screen_width // 2 - winner_text.get_width() // 2, 200))
        buttons = [
            {"text": "Neustart", "pos": Vector2(screen_width // 2 - 120, 350), "color": COLORS['button_restart']},
            {"text": "Hauptmenü", "pos": Vector2(screen_width // 2 + 120, 350), "color": COLORS['button_menu']}
        ]
        for button in buttons:
            text = font_medium.render(button["text"], True, COLORS['text_light'])
            button_rect = pygame.Rect(button["pos"].x - 100, button["pos"].y - 25, 200, 50)
            pygame.draw.rect(self.screen, button["color"], button_rect, border_radius=10)
            pygame.draw.rect(self.screen, COLORS['button_border'], button_rect, 3, border_radius=10)
            self.screen.blit(text, (button["pos"].x - text.get_width() // 2, button["pos"].y - text.get_height() // 2))
        pygame.display.flip()

    def handle_game_over_events(self):
        """Handle events on the game over screen."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if (screen_width // 2 - 120 - 100 <= x <= screen_width // 2 - 120 + 100 and 325 <= y <= 375):
                    return "restart"
                elif (screen_width // 2 + 120 - 100 <= x <= screen_width // 2 + 120 + 100 and 325 <= y <= 375):
                    return "menu"
        return None

    def draw(self):
        """Draw the entire game state to the screen."""
        self.screen.blit(self.neon_background, (0, 0))
        pygame.draw.rect(self.screen, (0, 0, 0, 120), (50, 50, screen_width - 100, screen_height - 100), border_radius=20)
        pygame.draw.rect(self.screen, COLORS['table'], (50, 50, screen_width - 100, screen_height - 100), border_radius=20)
        for field in self.fields:
            field.draw(self.screen)
        for player in self.players:
            player.draw(self.fields, self.screen)
        if self.current_card:
            self.current_card.draw(CARD_POS, self.screen)
        else:
            pygame.draw.rect(self.screen, (30, 25, 50), (CARD_POS.x, CARD_POS.y, CARD_SIZE.x, CARD_SIZE.y), border_radius=10)
            pygame.draw.rect(self.screen, COLORS['card'], (CARD_POS.x, CARD_POS.y, CARD_SIZE.x, CARD_SIZE.y), 2, border_radius=10)
            if len(self.deck) > 0:
                text = font_small.render(f"{len(self.deck)}", True, COLORS['text_light'])
                self.screen.blit(text, (CARD_POS.x + CARD_SIZE.x - 20, CARD_POS.y + 10))
        self.draw_dice()
        if not self.game_over:
            player = self.players[self.current_player]
            text = font_medium.render(f"Spieler {self.current_player + 1} ist dran", True, player.color)
            self.screen.blit(text, (70, 70))
        if pygame.time.get_ticks() - self.message_time < 3000:
            text = font_medium.render(self.message, True, COLORS['text_light'])
            pygame.draw.rect(self.screen, (0, 0, 0, 160), (screen_width // 2 - text.get_width() // 2 - 20, 70, text.get_width() + 40, text.get_height() + 20), border_radius=10)
            pygame.draw.rect(self.screen, (100, 50, 150, 100), (screen_width // 2 - text.get_width() // 2 - 20, 70, text.get_width() + 40, text.get_height() + 20), 2, border_radius=10)
            self.screen.blit(text, (screen_width // 2 - text.get_width() // 2, 80))
        pygame.display.flip()

    def handle_events(self):
        """Handle all in-game events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (DICE_POS.x <= event.pos[0] <= DICE_POS.x + 80 and DICE_POS.y <= event.pos[1] <= DICE_POS.y + 80):
                    self.roll_dice()
                if self.current_card and (CARD_POS.x <= event.pos[0] <= CARD_POS.x + CARD_SIZE.x and CARD_POS.y <= event.pos[1] <= CARD_SIZE.y + CARD_POS.y):
                    self.current_card.visible = not self.current_card.visible
                    if not self.current_card.visible:
                        self.current_card = None
                        self.waiting_for_card = False
                        if not self.game_over:
                            self.current_player = (self.current_player + 1) % len(self.players)
                            self.dice_value = 0

    def run(self):
        """Main game loop."""
        while True:
            if self.game_over:
                self.draw_game_over()
                action = self.handle_game_over_events()
                if action == "restart":
                    return "restart"
                elif action == "menu":
                    return "menu"
            else:
                self.handle_events()
                self.update_movement()
                self.draw()
                clock.tick(10)
