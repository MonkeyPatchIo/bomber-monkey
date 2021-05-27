import sys

import pygame
import pygame_menu

from bomber_monkey.features.player.player_action import PlayerAction
from bomber_monkey.features.player.players_config import PlayersConfig, menu_wait
from bomber_monkey.game_config import BLACK_COLOR, GameConfig, WHITE_COLOR, GREEN_COLOR, RED_COLOR
from bomber_monkey.game_inputs import refresh_game_inputs
from bomber_monkey.utils.vector import Vector

CONFIG_FONT = pygame_menu.font.FONT_MUNRO
FONT_SIZE = 30
MARGIN = 20
MENU_FPS = 60  # this will drive the time left to capture the key pressure


class ControllersConfigurator:

    def __init__(self):
        self.conf = GameConfig()
        self.players_config = PlayersConfig()

        self.nb_controllers = len(self.players_config.descriptors)

        self.clock = pygame.time.Clock()

        font = pygame.font.Font(CONFIG_FONT, FONT_SIZE)

        blits = []

        self.rendered_names_pos_y = []
        max_descriptor_name_size = 0
        line_pos = Vector.create(MARGIN, FONT_SIZE + 2 * MARGIN)
        for descriptor in self.players_config.descriptors:
            rendered_name: pygame.Surface = font.render(descriptor.name, False, WHITE_COLOR)
            max_descriptor_name_size = max(max_descriptor_name_size, rendered_name.get_size()[0])
            blits.append((rendered_name, line_pos.as_ints()))
            self.rendered_names_pos_y.append(line_pos.y)
            line_pos += Vector.create(0, FONT_SIZE + MARGIN)

        self.rendered_cols_pos_x = []
        self.rendered_cols_width = []
        col_pos = Vector.create(MARGIN + max_descriptor_name_size + MARGIN, MARGIN)
        rendered_col: pygame.Surface = font.render("Unassigned", False, WHITE_COLOR)
        blits.append((rendered_col, col_pos.as_ints()))
        self.rendered_cols_pos_x.append(col_pos.x)
        rendered_width = rendered_col.get_size()[0]
        self.rendered_cols_width.append(rendered_width)
        col_pos += Vector.create(rendered_width + MARGIN, 0)
        self.nb_slot = min(4, self.nb_controllers)
        for i in range(self.nb_slot):
            rendered_col: pygame.Surface = font.render("Player #" + str(i + 1), False, WHITE_COLOR)
            blits.append((rendered_col, col_pos.as_ints()))
            self.rendered_cols_pos_x.append(col_pos.x)
            rendered_width = rendered_col.get_size()[0]
            self.rendered_cols_width.append(rendered_width)
            col_pos += Vector.create(rendered_width + MARGIN, 0)

        self.rendered_X: pygame.Surface = font.render("X", False, GREEN_COLOR)
        self.rendered_X_bad: pygame.Surface = font.render("X", False, RED_COLOR)
        self.rendered_X_width = self.rendered_X.get_size()[0]

        self.bindings = [0] * self.nb_controllers
        self.bindings[0] = 1
        self.bindings[1] = 2

        window_size = (col_pos.x + MARGIN, line_pos.y + MARGIN)
        self.screen = pygame.display.set_mode(window_size)
        self.buffer = self.screen.copy()
        self.buffer.fill(BLACK_COLOR, pygame.rect.Rect((0, 0), window_size))
        for blit in blits:
            self.buffer.blit(*blit)

    def run(self):
        while True:
            inputs = refresh_game_inputs()
            if inputs.quit:
                sys.exit()
            config_ok = self.is_config_ok()
            for player_id, action in menu_wait(self.players_config):
                if action & PlayerAction.MAIN_ACTION and config_ok:
                    self.set_players_config()
                    return
                if action & PlayerAction.MOVE_LEFT:
                    self.handle_left(player_id)
                if action & PlayerAction.MOVE_RIGHT:
                    self.handle_right(player_id)

            self.screen.blit(self.buffer, (0, 0))

            for i in range(self.nb_controllers):
                binding = self.bindings[i]
                x = self.rendered_cols_pos_x[binding] + int(
                    self.rendered_cols_width[binding] / 2 - self.rendered_X_width / 2)
                y = self.rendered_names_pos_y[i]
                self.screen.blit(self.rendered_X if config_ok else self.rendered_X_bad, (x, y))

            pygame.display.flip()
            self.clock.tick(MENU_FPS)

    def handle_left(self, i):
        player = self.bindings[i]
        if player > 0:
            self.bindings[i] = player - 1

    def handle_right(self, i):
        player = self.bindings[i]
        if player < self.nb_slot:
            self.bindings[i] = player + 1

    def is_config_ok(self):
        players = set()
        for i in range(self.nb_controllers):
            player = self.bindings[i]
            if player > 0:
                # check that a player can have only one controller
                if player in players:
                    return False
                players.add(player)

        # At least two players
        if len(players) < 2:
            return False

        return True

    def set_players_config(self):
        player_descriptor_bindings = []
        for i in range(self.nb_controllers):
            player = self.bindings[i]
            if player > 0:
                player_descriptor_bindings.append((player, self.players_config.descriptors[i]))
        # sort by player id
        player_descriptor_bindings = sorted(player_descriptor_bindings,
                                            key=lambda player_descriptor: player_descriptor[0])
        # do set the players_config
        self.players_config.active_descriptors = [player_descriptor[1] for player_descriptor in
                                                  player_descriptor_bindings]
