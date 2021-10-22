import time
import sys

import pygame
import pygame_menu

from bomber_monkey.features.controller.controller_descriptor import ControllerDescriptor
from bomber_monkey.features.player.player_action import PlayerAction
from bomber_monkey.features.player.players_config import PlayersConfig, MAX_PLAYER_NUMBER
from bomber_monkey.game_config import BLACK_COLOR, GameConfig, WHITE_COLOR, GREEN_COLOR, RED_COLOR, GREY_COLOR
from bomber_monkey.game_inputs import refresh_game_inputs, get_game_inputs
from bomber_monkey.utils.vector import Vector

CONFIG_FONT = pygame_menu.font.FONT_MUNRO
FONT_SIZE = 30
HELP_FONT_SIZE = 20
MARGIN = 20
MENU_FPS = 60  # this will drive the time left to capture the key pressure
BLINK_DURATION = 1.0


class ControllersConfigurator:

    def __init__(self):
        self.conf = GameConfig()
        self.players_config = PlayersConfig()
        self.clock = pygame.time.Clock()
        self.rendered_names_pos_y = []

        self.rendered_cols_pos_x = []
        self.rendered_cols_width = []

        self.rendered_X: pygame.Surface = None
        self.rendered_X_bad: pygame.Surface = None
        self.rendered_X_width = None
        self.bindings = []
        self.screen = None
        self.buffer = None

        self.time = time.time()
        self.reset()

    @property
    def nb_controllers(self):
        return len(self.players_config.descriptors)

    def reset(self):
        self.conf = GameConfig()
        self.players_config = PlayersConfig()

        font = pygame.font.Font(CONFIG_FONT, FONT_SIZE)
        help_font = pygame.font.Font(CONFIG_FONT, HELP_FONT_SIZE)

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

        self.rendered_ia_names = {}
        self.rendered_ia_names_length = {}

        for key, template in self.players_config.ia_templates.items():
            name, factory = template
            rendered_name: pygame.Surface = font.render(f"IA {name} ", False, WHITE_COLOR)
            self.rendered_ia_names[name] = rendered_name
            max_descriptor_name_size = max(max_descriptor_name_size, rendered_name.get_size()[0])
            self.rendered_ia_names_length[name] = rendered_name.get_size()[0]

        for _ in range(MAX_PLAYER_NUMBER):
            self.rendered_names_pos_y.append(line_pos.y)
            line_pos += Vector.create(0, FONT_SIZE + MARGIN)

        lines = [
            "Press:",
            "- Up/Down: select the focused controller",
            "- Left/Right: to select the focused controller slot",
            "- Escape: to reset",
            "- Return: to validate",
            *[
                f'- {str(chr(key)).upper()}: to add the IA "{name}"'
                for key, (name, factory) in self.players_config.ia_templates.items()
            ]
        ]

        for line in lines:
            rendered_line: pygame.Surface = help_font.render(line, False, GREY_COLOR)
            blits.append((rendered_line, line_pos.as_ints()))
            line_pos += Vector.create(0, HELP_FONT_SIZE + int(MARGIN / 2))

        self.rendered_cols_pos_x = []
        self.rendered_cols_width = []
        col_pos = Vector.create(MARGIN + max_descriptor_name_size + MARGIN, MARGIN)
        rendered_col: pygame.Surface = font.render("Unassigned", False, WHITE_COLOR)
        blits.append((rendered_col, col_pos.as_ints()))
        self.rendered_cols_pos_x.append(col_pos.x)
        rendered_width = rendered_col.get_size()[0]
        self.rendered_cols_width.append(rendered_width)
        col_pos += Vector.create(rendered_width + MARGIN, 0)
        for i in range(MAX_PLAYER_NUMBER):
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
            for player_id, action in player_menu_wait(self.players_config):
                if action & PlayerAction.CANCEL:
                    self.reset()
                if action & PlayerAction.MAIN_ACTION and config_ok:
                    self.set_players_config()
                    return
                if action & PlayerAction.MOVE_LEFT:
                    self.handle_left(player_id)
                if action & PlayerAction.MOVE_RIGHT:
                    self.handle_right(player_id)

            for key, (name, factory) in self.players_config.ia_templates.items():
                if key in inputs.keyboard.up:
                    self.add_ia(ControllerDescriptor(name, factory))

            self.screen.blit(self.buffer, (0, 0))

            for i in range(len(self.players_config.descriptors) + len(self.players_config.ia_descriptors)):
                if i == self.players_config.focused_controller\
                        and (time.time() - self.time) % BLINK_DURATION < BLINK_DURATION / 3:
                    continue
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
        if player < MAX_PLAYER_NUMBER:
            self.bindings[i] = player + 1

    def is_config_ok(self):
        players = set()
        for i in range(self.nb_controllers + len(self.players_config.ia_descriptors)):
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
        for i in range(self.nb_controllers + len(self.players_config.ia_descriptors)):
            player = self.bindings[i]
            if player > 0:
                if i >= self.nb_controllers:
                    player_descriptor_bindings.append((player, self.players_config.ia_descriptors[i - self.nb_controllers]))
                else:
                    player_descriptor_bindings.append((player, self.players_config.descriptors[i]))

        # sort by player id
        player_descriptor_bindings = sorted(player_descriptor_bindings,
                                            key=lambda player_descriptor: player_descriptor[0])
        # do set the players_config
        self.players_config.active_controllers = [
            player_descriptor[1]
            for player_descriptor in player_descriptor_bindings
        ]

    def add_ia(self, descriptor: ControllerDescriptor):
        nb_ia = len(self.players_config.ia_descriptors)
        if nb_ia >= MAX_PLAYER_NUMBER:
            return

        rendered_name = self.rendered_ia_names[descriptor.name]
        pos_y = self.rendered_names_pos_y[self.nb_controllers + nb_ia]
        self.buffer.blit(rendered_name, (MARGIN, pos_y))
        self.bindings.append(0)
        self.players_config.ia_descriptors.append(descriptor)


def player_menu_wait(players_config: PlayersConfig):
    limit = len(players_config.descriptors) + len(players_config.ia_descriptors)

    focus = players_config.focused_controller
    inputs = get_game_inputs()

    if pygame.K_DOWN in inputs.keyboard.up:
        players_config.focused_controller += 1
        players_config.focused_controller %= limit
        yield focus, PlayerAction.MOVE_DOWN

    if pygame.K_UP in inputs.keyboard.up:
        players_config.focused_controller += limit - 1
        players_config.focused_controller %= limit
        yield focus, PlayerAction.MOVE_UP

    if pygame.K_LEFT in inputs.keyboard.up:
        yield focus, PlayerAction.MOVE_LEFT

    if pygame.K_RIGHT in inputs.keyboard.up:
        yield focus, PlayerAction.MOVE_RIGHT

    if pygame.K_RETURN in inputs.keyboard.up:
        yield focus, PlayerAction.MAIN_ACTION

    if pygame.K_ESCAPE in inputs.keyboard.up:
        yield focus, PlayerAction.CANCEL

    return None
