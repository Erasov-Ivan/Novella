import pygame
import time
from drawer import Drawer, Button


class Chapter:
    def __init__(self, drawer: Drawer, chapter: dict, path: str):
        self.drawer = drawer
        self.chapter = chapter
        self.path = path

        self.current_position = self.chapter.get('start', None)
        self.current_text_position = 0
        if self.current_position is None:
            raise ValueError("No start point")
        self.current_choice: list[Button] = []

    def start(self):
        pass

    def next(self):
        if len(self.current_choice) > 0:
            return

        texts = self.current_position.get('texts')
        if texts is not None:
            self.current_text_position += 1
            if self.current_text_position < len(texts):
                self.show_current_position()
                return
        if (next_key := self.current_position.get('next')) is not None:
            self.current_text_position = 0
            self.current_position = self.chapter.get(next_key)
            background = self.current_position.get('background', None)
            if background is not None:
                image = background.get('image', None)
                if image is not None:
                    self.drawer.update_background(image=f'{self.path}/{image}')
                else:
                    self.drawer.update_background(color=background.get('color', None))
            if self.current_position is None:
                return
            else:
                self.show_current_position()
        else:
            return

    def show_current_position(self):
        texts = self.current_position.get('texts')
        if texts is None:
            return
        else:
            if len(texts) <= self.current_text_position:
                return
            else:
                words = texts[self.current_text_position].get('words', '')
                character = texts[self.current_text_position].get('character', None)
                title = texts[self.current_text_position].get('title', None)
                if title is not None and character is not None:
                    words = f'{character}: {words}'
                centered = texts[self.current_text_position].get('centered', False)
                delay = texts[self.current_text_position].get('delay', None)
                if delay is None:
                    delay = 0.005

                self.drawer.show_text_appearance_animation(
                    words=words, character=character, title=title, centered=centered, delay=delay
                )


