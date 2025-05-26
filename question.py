import pygame
from utils import *


class Form:
    def __init__(self, screen: pygame.Surface, font: pygame.font.Font, question: str, answer: str):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.font = font
        self.question = question
        self.answer = answer.replace(' ', '')

        text_width = self.font.size(self.question)[0]
        self.surface = BasicSurface(
            x=(self.screen_width - text_width) // 2 - 20,
            y=self.screen_height // 4,
            width=text_width + 20,
            height=self.screen_height // 2,
            fill_color=Color('grey')
        )
        self.label = Button(
            x=10,
            y=self.surface.height // 7,
            width=self.surface.width,
            height=self.surface.height // 7,
            fill_color=Color(0, 0, 0, 0),
            border_color=Color(0, 0, 0, 0),
            text=self.question,
            font=self.font,
            parent=self.surface,
            callback='',
            text_position='left'
        )
        self.surface.children.append(self.label)

        self.input_box = InputBox(
            x=self.surface.width // 4,
            y=self.surface.height // 7 * 3,
            width=self.surface.width // 2,
            height=self.font.get_height() + 5,
            font=self.font,
            parent=self.surface,
            text_color=Color('black')
        )
        self.surface.children.append(self.input_box)

        self.submit_button = Button(
            x=self.surface.width // 4,
            y=self.input_box.y + self.input_box.height + self.surface.height // 7,
            width=self.surface.width // 2,
            height=self.surface.height // 7,
            text='Ответить',
            callback='',
            parent=self.surface,
            font=self.font
        )
        self.surface.children.append(self.submit_button)

    def draw(self):
        draw_surface(source=self.surface, dest=self.screen)

    def start(self) -> bool:
        clock = pygame.time.Clock()
        running = True
        while running:
            mouse_position = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if self.input_box.handle_event(event):
                    return self.input_box.text.text.replace(' ', '') == self.answer

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.submit_button.is_hovered(*event.pos):
                        return self.input_box.text.text.replace(' ', '') == self.answer

            self.submit_button.check_hover(*mouse_position)
            self.input_box.update()
            self.draw()

            pygame.display.flip()
            clock.tick(60)
