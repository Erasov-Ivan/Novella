import pygame
import time
from generator.generator import ChapterGenerator
from utils import *


class Chapter:
    def __init__(
            self, screen: pygame.Surface, font: pygame.font.Font, path: str, stats: dict = {}
    ):
        self.stats = stats
        self.path = path
        self.chapter = ChapterGenerator()
        self.chapter.load(self.path)
        self.background = Background(screen=screen)
        self.screen = screen
        self.font = font

        self.current_position = self.chapter.labels.get('start', None)
        self.current_text_position = 0
        if self.current_position is None:
            raise ValueError("No start point")

        self.current_text = None
        self.repeat = 0

    def start(self):
        #self.update_dairy()
        self.update_current_text()
        self.update_current_background()

    def next(self):
        #if len(self.choices.buttons) > 0:
        #    return

        if self.repeat > 0:
            self.repeat -= 1
            self.update_current_position()
            return

        texts = self.current_position.texts
        if texts is not None:
            self.current_text_position += 1
            if self.current_text_position < len(texts):
                #self.update_dairy()
                self.update_current_text()
                #self.update_current_choices()
                return
        if (next_key := self.current_position.next) is not None:
            #self.update_dairy()
            self.current_text_position = 0
            self.current_position = self.chapter.labels.get(next_key)
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
                    screen=self.screen
                )

    def update_current_background(self):
        background = self.current_position.background
        if background is not None:
            image = background.image
            if image is not None:
                self.background.update(image=f'{self.path}/{image}')
            else:
                self.background.update(color=background.color)

    def update_current_position(self):
        if self.current_position is not None:
            self.update_current_background()
            self.update_current_text()
            #self.update_current_choices()
            #self.choices.draw_current_buttons()


    def process_button_click(self, mouse_position: tuple[int, int]):
        index = self.choices.is_button_clicked(mouse_position=mouse_position)
        if index is not None:
            self.choices.buttons = []
            result = self.current_position['texts'][self.current_text_position]['choices'][index]
            self.current_position['texts'][self.current_text_position]['choices'][index]['done'] = True

            plot = result.get('plot', {})
            tasks = result.get('tasks', {})
            theory = result.get('theory', {})
            self.dairy.update(plot=plot, tasks=tasks, theory=theory)

            if (stats := result.get('stats', None)) is not None:
                for key, value in stats.items():
                    if key not in self.stats.keys():
                        self.stats[key] = value
                    else:
                        self.stats[key] += value
                    self.drawer.update_current_text(
                        words=f'{key}: {f"+{value}" if value >= 0 else value}',
                        centered=True,
                        delay=0.01
                    )
                    self.drawer.show_current_text_appearance_animation()
                    time.sleep(1)
            if result.get('words', None) is not None:
                self.drawer.update_current_text(
                    words=result.get('words', ''),
                    character=result.get('character', None),
                    title=result.get('title', None),
                    centered=result.get('centered', False),
                    delay=result.get('delay', None)
                )
                self.drawer.show_current_text_appearance_animation()
                if result.get('repeat', False):
                    self.repeat += 1
            elif (next_key := result.get('label', None)) is not None:
                self.current_position = self.chapter.get(next_key)
                self.current_text_position = 0
                if self.current_position is not None:
                    self.update_current_position()
        else:
            if self.dairy.dairy_button.is_clicked(mouse_position=mouse_position):
                self.dairy.open_dairy()

    def update_dairy(self):
        texts = self.current_position.get('texts')
        if texts is not None:
            if self.current_text_position < len(texts):
                plot = texts[self.current_text_position].get('plot', {})
                tasks = texts[self.current_text_position].get('tasks', {})
                theory = texts[self.current_text_position].get('theory', {})
                self.dairy.update(plot=plot, tasks=tasks, theory=theory)

