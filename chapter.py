import pygame
import time
from drawer import Drawer
from choices import Choices


class Chapter:
    def __init__(self, drawer: Drawer, choices: Choices, chapter: dict, path: str, stats: dict = {}):
        self.drawer = drawer
        self.choices = choices
        self.chapter = chapter
        self.stats = stats
        self.path = path

        self.current_position = self.chapter.get('start', None)
        self.current_text_position = 0
        if self.current_position is None:
            raise ValueError("No start point")

        self.repeat = 0

    def start(self):
        self.update_current_text()
        self.update_current_background()
        self.drawer.show_current_text_appearance_animation()

    def next(self):
        if len(self.choices.buttons) > 0:
            return

        if self.repeat > 0:
            self.repeat -= 1
            self.update_current_position()
            return

        texts = self.current_position.get('texts')
        if texts is not None:
            self.current_text_position += 1
            if self.current_text_position < len(texts):
                self.update_current_text()
                self.drawer.show_current_text_appearance_animation()
                self.update_current_choices()
                self.choices.draw_current_buttons()
                return
        if (next_key := self.current_position.get('next')) is not None:
            self.current_text_position = 0
            self.current_position = self.chapter.get(next_key)
            self.update_current_position()
        else:
            return

    def update_current_text(self):
        texts = self.current_position.get('texts')
        if texts is None:
            return
        else:
            if len(texts) <= self.current_text_position:
                return
            else:
                self.drawer.update_current_text(
                    words=texts[self.current_text_position].get('words', ''),
                    character=texts[self.current_text_position].get('character', None),
                    title=texts[self.current_text_position].get('title', None),
                    centered=texts[self.current_text_position].get('centered', False),
                    delay=texts[self.current_text_position].get('delay', None)
                )

    def update_current_background(self):
        background = self.current_position.get('background', None)
        if background is not None:
            image = background.get('image', None)
            if image is not None:
                self.drawer.update_current_background(image=f'{self.path}/{image}')
            else:
                self.drawer.update_current_background(color=background.get('color', None))

    def update_current_choices(self):
        texts = self.current_position.get('texts')
        if texts is not None:
            if self.current_text_position < len(texts):
                choices = texts[self.current_text_position].get('choices', [])
                centered = texts[self.current_text_position].get('centered', False)
                self.choices.update_buttons(
                    buttons=choices,
                    text_centered=centered
                )

    def update_current_position(self):
        if self.current_position is not None:
            self.update_current_background()
            self.update_current_text()
            self.drawer.show_current_text_appearance_animation()
            self.update_current_choices()
            self.choices.draw_current_buttons()

    def show_current_state(self):
        self.drawer.draw_current_background()
        self.drawer.show_current_text()
        self.choices.draw_current_buttons()

    def process_button_click(self, mouse_position: tuple[int, int]):
        index = self.choices.is_button_clicked(mouse_position=mouse_position)
        if index is not None:
            self.choices.buttons = []
            result = self.current_position['texts'][self.current_text_position]['choices'][index]
            self.current_position['texts'][self.current_text_position]['choices'][index]['done'] = True
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
                if self.current_position is not None:
                    self.update_current_position()




