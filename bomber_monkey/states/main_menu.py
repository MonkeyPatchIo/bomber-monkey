import math
import time
from enum import IntEnum
from typing import Tuple, Any

import pygame
import pygameMenu

from bomber_monkey.features.display.image import Image
from bomber_monkey.game_config import GameConfig, BLUE_MONKEY_COLOR, BLACK_COLOR, WHITE_COLOR, RED_COLOR
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


class MainMenuState(AppState):

    def __init__(self, conf: GameConfig, screen):
        super().__init__()
        self.conf = conf
        self.screen = screen
        self.allow_quit_time = 0
        self.start_time = -1

        font_title = pygame.font.Font(pygameMenu.font.FONT_8BIT, TITLE_FONT_SIZE)
        font_subtitle = pygame.font.Font(pygameMenu.font.FONT_8BIT, SUBTITLE_FONT_SIZE)
        font_main_text = pygame.font.Font(pygameMenu.font.FONT_8BIT, MAIN_TEXT_FONT_SIZE)
        self.font_credit_text = pygame.font.Font(pygameMenu.font.FONT_8BIT, CREDIT_FONT_SIZE)

        self.rendered_title = font_title.render(TITLE, 1, BLUE_MONKEY_COLOR)
        self.title_pos = Vector.create(conf.pixel_size.x / 2 - (len(TITLE) * TITLE_FONT_SIZE) / 2, MARGIN)

        self.rendered_subtitle = font_subtitle.render(SUBTITLE_PREFIX, 1, BLUE_MONKEY_COLOR)
        self.monkeypatch = pygame.transform.scale(
            conf.graphics_cache.get_image(Image(conf.media_path("monkeypatch.png"))),
            SUBTITLE_PICTURE_SIZE.as_ints())
        self.subtitle_pos = Vector.create(conf.pixel_size.x / 2 - SUBTITLE_SIZE.x / 2, MARGIN * 2 + TITLE_FONT_SIZE)
        self.subtitle_text_pos = self.subtitle_pos \
                                 + Vector.create(0, SUBTITLE_PICTURE_SIZE.y - SUBTITLE_FONT_SIZE - SUBTITLE_TEXT_OFFSET)
        self.subtitle_pic_pos = self.subtitle_pos + Vector.create((len(SUBTITLE_PREFIX)) * SUBTITLE_FONT_SIZE, 0)

        self.rendered_main_text1_prefix = font_main_text.render(MAIN_TEXT1_PREFIX, 1, WHITE_COLOR)
        self.rendered_main_text1_key = font_main_text.render(MAIN_TEXT1_KEY, 1, RED_COLOR)
        self.rendered_main_text2 = font_main_text.render(MAIN_TEXT2, 1, WHITE_COLOR)
        main_text1_prefix_width = len(MAIN_TEXT1_PREFIX) * MAIN_TEXT_FONT_SIZE
        main_text1_key_width = len(MAIN_TEXT1_KEY) * MAIN_TEXT_FONT_SIZE
        main_text2_width = len(MAIN_TEXT2) * MAIN_TEXT_FONT_SIZE
        main_text1_width = main_text1_prefix_width + main_text1_key_width
        self.main_text1_prefix_pos = Vector.create(conf.pixel_size.x / 2 - main_text1_width / 2,
                                                   conf.pixel_size.y / 2 - (2 * MAIN_TEXT_FONT_SIZE + MARGIN) / 2)
        self.main_text1_key_pos = self.main_text1_prefix_pos + Vector.create(main_text1_prefix_width, 0)
        self.main_text2_pos = Vector.create(conf.pixel_size.x / 2 - main_text2_width / 2,
                                            self.main_text1_prefix_pos.y + MARGIN + MAIN_TEXT_FONT_SIZE)

        self.rendered_credits_title = self.font_credit_text.render(CREDIT_TITLE, 1, WHITE_COLOR)
        credits_height = 2 * MARGIN + 2 * CREDIT_FONT_SIZE
        self.credits_title_pos = Vector.create(conf.pixel_size.x / 2 - len(CREDIT_TITLE) * CREDIT_FONT_SIZE / 2,
                                               conf.pixel_size.y - credits_height)
        self.credits_name_base_pos = Vector.create(conf.pixel_size.x / 2,
                                                   self.credits_title_pos.y + CREDIT_FONT_SIZE + MARGIN)

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

        self.screen.fill(BLACK_COLOR, pygame.rect.Rect((0, 0), self.conf.pixel_size.as_ints()))
        self.screen.blit(self.rendered_title, self.title_pos.as_ints())
        self.screen.blit(self.rendered_subtitle, self.subtitle_text_pos.as_ints())
        self.screen.blit(self.monkeypatch, self.subtitle_pic_pos.as_ints())

        self.screen.blit(self.rendered_main_text1_prefix, self.main_text1_prefix_pos.as_ints())
        if elapsed_time % (BLINK_ON_TIME + BLINK_OFF_TIME) < BLINK_OFF_TIME:
            self.screen.blit(self.rendered_main_text1_key, self.main_text1_key_pos.as_ints())
        self.screen.blit(self.rendered_main_text2, self.main_text2_pos.as_ints())

        self.screen.blit(self.rendered_credits_title, self.credits_title_pos.as_ints())

        ratio = elapsed_time % ((2 * CREDIT_SLIDE_TIME + CREDIT_STAY_TIME) * len(CREDIT_NAMES))
        name = CREDIT_NAMES[int(ratio / len(CREDIT_NAMES))]
        credits_name_pos = self.credits_name_base_pos - Vector.create(len(name) * CREDIT_FONT_SIZE / 2, 0)
        rendered_name = self.font_credit_text.render(name, 1, WHITE_COLOR)
        ratio2 = ratio % len(CREDIT_NAMES)
        if ratio2 < CREDIT_SLIDE_TIME:
            offset = CREDIT_FONT_SIZE * math.sin((1 + (ratio2 / CREDIT_SLIDE_TIME)) * math.pi / 2)
        elif ratio2 > CREDIT_STAY_TIME + CREDIT_STAY_TIME:
            offset = CREDIT_FONT_SIZE * math.sin(((ratio2 - CREDIT_STAY_TIME - CREDIT_STAY_TIME) / CREDIT_SLIDE_TIME) * math.pi / 2)
        else:
            offset = 0
        if offset > 0:
            credits_name_pos += Vector.create(0, offset)
            rendered_name = rendered_name.subsurface(0, 0, rendered_name.get_width(), rendered_name.get_height() - offset)
        self.screen.blit(rendered_name, credits_name_pos.as_ints())

        pygame.display.flip()
