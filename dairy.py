import pygame
from utils import Button


class Plot:
    def __init__(self, plot: dict):
        self.plot = plot


class CurrentTasks:
    def __init__(self, current_tasks: dict):
        self.current_tasks = current_tasks


class Theory:
    def __init__(self, theory: dict):
        self.theory = theory


class Dairy:
    def __init__(
            self, screen: pygame.Surface,  font: pygame.font.Font,
            button_size: int = 40,
    ):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.font = font

        self.dairy_button = Button(
            x=self.screen_width - button_size - 40,
            y=40,
            width=button_size,
            height=button_size
        )

    def draw_button(self):
        self.dairy_button.draw(surface=self.screen)

    def open_dairy(self):
        print('openning dairy')





