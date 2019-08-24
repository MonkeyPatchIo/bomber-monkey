import time

import pygame as pg
import pygameMenu
from pygame.surface import Surface

from bomber_monkey.features.display.image import Image
from bomber_monkey.features.player.players_config import PlayersConfig
from bomber_monkey.game_config import GameConfig, BLUE_MONKEY_COLOR, BLACK_COLOR
from bomber_monkey.game_scores import GameRoundResult
from bomber_monkey.utils.vector import Vector

TITLE_FONT_SIZE = 50
TITLE_BOTTOM_MARGIN = 50
MESSAGE_FONT_SIZE = 35
BOX_PADDING = 30
PLAYER_MESSAGE_PREFIX = "Player "
SCORE_LINE_HEIGHT = 80
SCORE_SLOT_MARGIN = 10
SCORE_SLOT_SIZE = Vector.create(64, 64)
SCORE_SLOT_SPACING = 10
MONKEY_BLINK_ON_TIME = .4
MONKEY_BLINK_OFF_TIME = .2
MONKEY_MAX_BLINK_TIME = 5
MONKEY_FLIP_TIME = .5

SCORE_SLOT_OFFSET_Y = SCORE_LINE_HEIGHT / 2 - SCORE_SLOT_SIZE.y / 2
SCORE_SLOT_OFFSET_X = SCORE_SLOT_SIZE.x + SCORE_SLOT_SPACING


class ScoreBoard:

    def __init__(self, conf: GameConfig, screen: Surface, players_config: PlayersConfig, result: GameRoundResult, title: str):
        self.conf = conf
        self.screen = screen
        self.players_config = players_config
        self.result = result
        self.title = title
        self.graphics_cache = conf.graphics_cache
        self.start_time = time.time()

        self.monkey_placeholder = conf.graphics_cache.get_image(Image(
            self.conf.media_path('monkey_placeholder.png'),
            display_size=SCORE_SLOT_SIZE))
        self.monkeys = [
            conf.graphics_cache.get_image(Image(
                self.conf.media_path('monkey_player.png'),
                display_size=SCORE_SLOT_SIZE,
                color_tint=slot.color))
            for slot in players_config.slots
        ]

    def draw_scores(self):
        messages_size_y = self.players_config.nb_players * SCORE_LINE_HEIGHT
        box_size_y = BOX_PADDING + TITLE_FONT_SIZE + TITLE_BOTTOM_MARGIN + messages_size_y + BOX_PADDING
        box_size = Vector.create(self.conf.pixel_size.x / 1.3, box_size_y)
        box_pos = self.conf.pixel_size / 2 - (box_size / 2)
        self.screen.fill(BLACK_COLOR, pg.rect.Rect(box_pos.as_ints(), box_size.as_ints()))

        font_title = pg.font.Font(pygameMenu.font.FONT_8BIT, TITLE_FONT_SIZE)
        font_message = pg.font.Font(pygameMenu.font.FONT_8BIT, MESSAGE_FONT_SIZE)
        text = font_title.render(self.title, 1, BLUE_MONKEY_COLOR)
        self.screen.blit(text, (box_pos + Vector.create(BOX_PADDING, BOX_PADDING)).as_ints())

        messages_relative_pos = Vector.create(BOX_PADDING, BOX_PADDING + TITLE_FONT_SIZE + TITLE_BOTTOM_MARGIN)
        messages_pos = box_pos + messages_relative_pos

        score_relative_offset_x = (len(PLAYER_MESSAGE_PREFIX) + 1) * MESSAGE_FONT_SIZE + SCORE_SLOT_MARGIN

        for player_id in range(self.players_config.nb_players):
            color = self.players_config.slots[player_id].color
            score = self.result.scores.scores[player_id]
            text = font_message.render(PLAYER_MESSAGE_PREFIX + str(player_id + 1), 1, color)
            pos_score_line = messages_pos + Vector.create(0, SCORE_LINE_HEIGHT) * player_id
            pos_player_title = pos_score_line + Vector.create(0, SCORE_LINE_HEIGHT / 2 - MESSAGE_FONT_SIZE / 2)
            self.screen.blit(text, pos_player_title.as_ints())

            for i in range(self.conf.winning_score):
                pos_score_slot = pos_score_line + Vector.create(score_relative_offset_x + i * SCORE_SLOT_OFFSET_X, SCORE_SLOT_OFFSET_Y)
                monkey = self.monkey_placeholder if self.should_show_placeholder(i, score, player_id) else self.monkeys[player_id]
                if self.should_flip(i, score, player_id):
                    monkey = pg.transform.flip(monkey, True, False)
                self.screen.blit(monkey, pos_score_slot.as_ints())

            score_value_pos_x = messages_pos.x + box_size.x - 2 * BOX_PADDING - MESSAGE_FONT_SIZE
            text = font_message.render(str(self.result.scores.scores[player_id]), 1, color)
            self.screen.blit(text, (score_value_pos_x, pos_player_title.y))

    def should_show_placeholder(self, i: int, score: int, player_id: int):
        if i < score - 1:
            return False
        if i >= score:
            return True
        if self.result.winner_id != player_id:
            return False
        elapsed_time = time.time() - self.start_time
        if elapsed_time > MONKEY_MAX_BLINK_TIME:
            return False
        ratio = elapsed_time % (MONKEY_BLINK_OFF_TIME + MONKEY_BLINK_ON_TIME)
        return ratio < MONKEY_BLINK_OFF_TIME

    def should_flip(self, i: int, score: int, player_id: int):
        if self.result.winner_id != player_id or self.conf.winning_score != score or i >= score:
            return False
        elapsed_time = time.time() - self.start_time
        return int(elapsed_time / MONKEY_FLIP_TIME) % 2 == 0

