import pygame
import time
from choices import Choices
from dairy import Dairy
from generator import ChapterGenerator
from question import Form
from utils import *


class Chapter:
    def __init__(
            self, screen: pygame.Surface, font: pygame.font.Font, path: str,
            dairy: Dairy,
            stats: dict = {},
            text_overlay_height_mul: float = 1/6
    ):
        self.stats = stats
        self.dairy = dairy
        self.path = path
        self.chapter = ChapterGenerator()
        self.chapter.load(f'{self.path}/chapter.json')
        self.background = Background(screen=screen)
        self.screen = screen
        self.font = font
        self.text_overlay_height_mul = text_overlay_height_mul

        self.current_position = self.chapter.labels.get('start', None)
        self.current_text_position = 0
        if self.current_position is None:
            raise ValueError("No start point")
        self.current_text: GameText = None
        self.repeat = 0

        self.choices: Choices = None

    def start(self):
        self.update_dairy()
        self.update_current_text()
        self.update_current_background()
        self.update_current_choices()

    def next(self):
        if self.choices is not None and len(self.choices.buttons.children) > 0:
            return

        if (q := self.current_position.texts[self.current_text_position].question) is not None:
            form = Form(screen=self.screen, font=self.font, question=q.question, answer=q.answer)
            res = form.start()
            if res:
                self.current_position = self.chapter.labels.get(q.right_label)
            else:
                self.current_position = self.chapter.labels.get(q.wrong_label)
            if self.current_position is not None:
                self.current_text_position = 0
                self.update_dairy()
                self.update_current_position()
                return

        if self.repeat > 0:
            self.repeat -= 1
            self.update_current_position()
            return

        texts = self.current_position.texts
        if texts is not None:
            self.current_text_position += 1
            if self.current_text_position < len(texts):
                self.update_dairy()
                self.update_current_text()
                self.update_current_choices()
                return
        if (next_key := self.current_position.next) is not None:
            self.current_text_position = 0
            self.current_position = self.chapter.labels.get(next_key)
            self.update_dairy()
            self.update_current_position()
        else:
            return

    def update_current_text(self):
        texts = self.current_position.texts
        if texts is None:
            return
        else:
            if len(texts) <= self.current_text_position:
                return
            else:
                text = texts[self.current_text_position]
                self.current_text = GameText(
                    words=text.words,
                    character=text.character,
                    title=text.title,
                    delay=text.delay,
                    centered=text.centered,
                    font=self.font,
                    screen=self.screen,
                    background_size_mul=self.text_overlay_height_mul
                )

    def update_current_background(self):
        background = self.current_position.background
        if background is not None:
            image = background.image
            if image is not None:
                self.background.update(image=f'{self.path}/{image}')
            else:
                self.background.update(color=background.color)

    def update_current_choices(self):
        if self.current_position.texts[self.current_text_position].choices is not None:
            self.choices = Choices(
                screen_width=self.screen.get_width(), screen_height=self.screen.get_height(), font=self.font,
                text_overlay_height_mul=self.text_overlay_height_mul,
                text_centered=self.current_position.texts[self.current_text_position].centered
            )
            self.choices.update_buttons(choices=self.current_position.texts[self.current_text_position].choices)

    def update_current_position(self):
        if self.current_position is not None:
            self.update_current_background()
            self.update_current_text()
            self.update_current_choices()

    def draw(self):
        self.background.draw()
        self.current_text.draw()
        if self.choices is not None:
            self.choices.draw(dest=self.screen)

    def process_button_click(self, mouse_position: tuple[int, int]):
        if self.choices is not None:
            callback = self.choices.check_mouse_click(mouse_position=mouse_position)
            if callback is not None:
                index = int(callback)
                self.choices = None
                self.current_position.texts[self.current_text_position].choices[index].done = True
                choice = self.current_position.texts[self.current_text_position].choices[index]
                self.dairy.update(plot=choice.plot, tasks=choice.tasks, theory=choice.theory)

                if (stats := choice.stats) is not None:
                    for key, value in stats.items():
                        if key not in self.stats.keys():
                            self.stats[key] = value
                        else:
                            self.stats[key] += value
                        #self.update_current_text(text=f'{key}: {f"+{value}" if value >= 0 else value}', centered=True)

                if choice.words is not None:
                    self.current_text = GameText(
                        words=choice.words,
                        character=choice.character,
                        title=choice.title,
                        centered=choice.centered,
                        font=self.font,
                        screen=self.screen,
                        background_size_mul=self.text_overlay_height_mul
                    )
                    if choice.repeat:
                        self.repeat += 1
                elif (next_key := choice.label) is not None:
                    self.current_position = self.chapter.labels.get(next_key)
                    self.current_text_position = 0
                    if self.current_position is not None:
                        self.update_current_position()
        else:
            if self.dairy.dairy_button.is_hovered(*mouse_position):
                self.dairy.open_dairy()

    def update_dairy(self):
        texts = self.current_position.texts
        if texts is not None:
            if self.current_text_position < len(texts):
                plot = texts[self.current_text_position].plot
                tasks = texts[self.current_text_position].tasks
                theory = texts[self.current_text_position].theory
                self.dairy.update(plot=plot, tasks=tasks, theory=theory)

