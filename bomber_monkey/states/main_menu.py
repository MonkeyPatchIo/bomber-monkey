import math
import time
from enum import IntEnum
from typing import Tuple, Any

import pygame
import pygameMenu
from pygame.rect import Rect
from pygame.surface import Surface

from bomber_monkey.features.board.board import Board, fill_board
from bomber_monkey.features.board.board_display_system import TileSet, draw_empty, draw_tiles
from bomber_monkey.features.display.image import Image
from bomber_monkey.game_config import GameConfig, BLUE_MONKEY_COLOR, WHITE_COLOR, ORANGE_COLOR, BLACK_COLOR
from bomber_monkey.game_scores import GameScores
from bomber_monkey.states.app_state import AppState, AppTransitions
from bomber_monkey.utils.vector import Vector

TITLE_FONT_SIZE = 70
TITLE = "Bomber Monkey"
MARGIN = 10
SUBTITLE_FONT_SIZE = 40
SUBTITLE_PREFIX = "by "
SUBTITLE_PICTURE_SIZE = Vector.create(460, 92)
SUBTITLE_SIZE = Vector.create((len(SUBTITLE_PREFIX)) * SUBTITLE_FONT_SIZE, 0) + SUBTITLE_PICTURE_SIZE
SUBTITLE_TEXT_OFFSET = 10

MAIN_TEXT_FONT_SIZE = 50
MAIN_TEXT1_PREFIX = "Hit "
MAIN_TEXT1_KEY = "ENTER"
MAIN_TEXT2 = "to start a game"
BLINK_ON_TIME = .7
BLINK_OFF_TIME = .3

CREDIT_FONT_SIZE = 30
CREDIT_TITLE = "Crafted by"
CREDIT_NAMES = [
    "Logan",
    "Florent",
    "Nicolas"
]
CREDIT_SLIDE_TIME = 1
CREDIT_STAY_TIME = 1

SHADOW_OFFSET = Vector.create(5, 5)


class MainMenuState(AppState):

    def __init__(self, conf: GameConfig, screen: Surface):
        super().__init__()
        self.conf = conf
        self.screen = screen
        self.allow_quit_time = 0
        self.start_time = -1

        self.buffer = screen.copy()
        self.draw_board(self.buffer)
        self.draw_header(self.buffer)
        self.draw_main_text(self.buffer)
        self.draw_credits(self.buffer)

    def draw_board(self, buffer: Surface):
        board = Board(tile_size=self.conf.tile_size, grid_size=self.conf.grid_size)
        fill_board(board)
        tile_set = TileSet(self.conf)
        draw_empty(board, buffer, self.conf, tile_set)
        draw_tiles(board, buffer, self.conf, tile_set)

    def draw_shadow_text(self, buffer: Surface, font, text: str, color, pos: Vector, subsurface: int = 0):
        rendered = font.render(text, 1, color)
        rendered_shadow = font.render(text, 1, BLACK_COLOR)
        if subsurface > 0:
            crop = Rect((0, 0), (rendered.get_width(), rendered.get_height() - subsurface))
            rendered = rendered.subsurface(crop)
            rendered_shadow = rendered_shadow.subsurface(crop)
        shadow_pos = pos + SHADOW_OFFSET
        buffer.blit(rendered_shadow, shadow_pos.as_ints())
        buffer.blit(rendered, pos.as_ints())

    def draw_header(self, buffer: Surface):
        buffer.fill(BLACK_COLOR, Rect(0, 0, self.conf.pixel_size.x,
                                      MARGIN + TITLE_FONT_SIZE + MARGIN + SUBTITLE_PICTURE_SIZE.y + MARGIN))

        font_title = pygame.font.Font(pygameMenu.font.FONT_8BIT, TITLE_FONT_SIZE)
        rendered_title = font_title.render(TITLE, 1, BLUE_MONKEY_COLOR)
        title_pos = Vector.create(self.conf.pixel_size.x / 2 - (len(TITLE) * TITLE_FONT_SIZE) / 2, MARGIN)
        buffer.blit(rendered_title, title_pos.as_ints())

        font_subtitle = pygame.font.Font(pygameMenu.font.FONT_8BIT, SUBTITLE_FONT_SIZE)
        rendered_subtitle = font_subtitle.render(SUBTITLE_PREFIX, 1, BLUE_MONKEY_COLOR)
        subtitle_pos = Vector.create(self.conf.pixel_size.x / 2 - SUBTITLE_SIZE.x / 2, MARGIN * 2 + TITLE_FONT_SIZE)
        subtitle_text_pos = subtitle_pos \
                            + Vector.create(0, SUBTITLE_PICTURE_SIZE.y - SUBTITLE_FONT_SIZE - SUBTITLE_TEXT_OFFSET)
        buffer.blit(rendered_subtitle, subtitle_text_pos.as_ints())

        monkeypatch = pygame.transform.scale(
            self.conf.graphics_cache.get_image(Image(self.conf.media_path("monkeypatch.png"))),
            SUBTITLE_PICTURE_SIZE.as_ints())
        subtitle_pic_pos = subtitle_pos + Vector.create((len(SUBTITLE_PREFIX)) * SUBTITLE_FONT_SIZE, 0)
        buffer.blit(monkeypatch, subtitle_pic_pos.as_ints())

    def draw_main_text(self, buffer: Surface):
        text1_prefix_width = len(MAIN_TEXT1_PREFIX) * MAIN_TEXT_FONT_SIZE
        text1_key_width = len(MAIN_TEXT1_KEY) * MAIN_TEXT_FONT_SIZE
        text1_width = text1_prefix_width + text1_key_width

        self.font_main_text = pygame.font.Font(pygameMenu.font.FONT_8BIT, MAIN_TEXT_FONT_SIZE)
        text1_prefix_pos = Vector.create(self.conf.pixel_size.x / 2 - text1_width / 2,
                                         self.conf.pixel_size.y / 2 - (2 * MAIN_TEXT_FONT_SIZE + MARGIN) / 2)
        self.draw_shadow_text(buffer, self.font_main_text, MAIN_TEXT1_PREFIX, WHITE_COLOR, text1_prefix_pos)

        self.main_text1_key_pos = text1_prefix_pos + Vector.create(text1_prefix_width, 0)

        text2_width = len(MAIN_TEXT2) * MAIN_TEXT_FONT_SIZE
        text2_pos = Vector.create(self.conf.pixel_size.x / 2 - text2_width / 2,
                                  text1_prefix_pos.y + MARGIN + MAIN_TEXT_FONT_SIZE)
        self.draw_shadow_text(buffer, self.font_main_text, MAIN_TEXT2, WHITE_COLOR, text2_pos)

    def blink_key(self, elapsed_time: float):
        if elapsed_time % (BLINK_ON_TIME + BLINK_OFF_TIME) > BLINK_OFF_TIME:
            self.draw_shadow_text(self.screen, self.font_main_text, MAIN_TEXT1_KEY, ORANGE_COLOR,
                                  self.main_text1_key_pos)

    def draw_credits(self, buffer: Surface):
        self.font_credit = pygame.font.Font(pygameMenu.font.FONT_8BIT, CREDIT_FONT_SIZE)
        credits_height = 2 * MARGIN + 2 * CREDIT_FONT_SIZE
        credits_title_pos = Vector.create(self.conf.pixel_size.x / 2 - len(CREDIT_TITLE) * CREDIT_FONT_SIZE / 2,
                                          self.conf.pixel_size.y - credits_height)
        self.draw_shadow_text(buffer, self.font_credit, CREDIT_TITLE, WHITE_COLOR, credits_title_pos)
        self.credits_name_base_pos = Vector.create(self.conf.pixel_size.x / 2,
                                                   credits_title_pos.y + CREDIT_FONT_SIZE + MARGIN)

    def slide_credit_name(self, elapsed_time: float):
        ratio = elapsed_time % ((2 * CREDIT_SLIDE_TIME + CREDIT_STAY_TIME) * len(CREDIT_NAMES))
        name = CREDIT_NAMES[int(ratio / len(CREDIT_NAMES))]
        credits_name_pos = self.credits_name_base_pos - Vector.create(len(name) * CREDIT_FONT_SIZE / 2, 0)
        ratio2 = ratio % len(CREDIT_NAMES)
        if ratio2 < CREDIT_SLIDE_TIME:
            offset = CREDIT_FONT_SIZE * math.sin((1 + (ratio2 / CREDIT_SLIDE_TIME)) * math.pi / 2)
        elif ratio2 > CREDIT_STAY_TIME + CREDIT_STAY_TIME:
            offset = CREDIT_FONT_SIZE * math.sin(
                ((ratio2 - CREDIT_STAY_TIME - CREDIT_STAY_TIME) / CREDIT_SLIDE_TIME) * math.pi / 2)
        else:
            offset = 0
        if offset > 0:
            credits_name_pos += Vector.create(0, offset)
        self.draw_shadow_text(self.screen, self.font_credit, name, WHITE_COLOR, credits_name_pos, offset)

    def run(self) -> Tuple[IntEnum, Any]:
        if self.start_time < 0:
            self.start_time = time.time()
        elapsed_time = time.time() - self.start_time
        events = pygame.event.get()
        if elapsed_time > self.conf.score_board_min_display_time:
            for event in events:
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
                    self.start_time = -1
                    return AppTransitions.NEW_GAME, GameScores(self.conf)

        self.screen.blit(self.buffer, (0, 0))
        self.blink_key(elapsed_time)
        self.slide_credit_name(elapsed_time)
        pygame.display.flip()
