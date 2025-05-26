import pygame
from utils import *


class Question:
    def __init__(self, screen: pygame.Surface, font: pygame.font.Font, question: str, answer: str):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.font = font
        self.question = question
        self.answer = answer

        self.surface = BasicSurface(
            x=self.screen_width // 6,
            y=self.screen_height // 4,
            width=self.screen_width // 6 * 4,
            height=self.screen_height // 2,
            fill_color=Color('grey')
        )
        self.label = Button(
            x=0,
            y=self.surface.height // 7,
            width=self.surface.width,
            height=self.surface.height // 7,
            fill_color=Color(0, 0, 0, 0),
            border_color=Color(0, 0, 0, 0),
            text=self.question,
            font=self.font,
            parent=self.surface,
            callback=''
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

    def start(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            mouse_position = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if self.input_box.handle_event(event):
                    print("1 Отправлен ответ:", self.input_box.text.text)

               #if event.type == pygame.MOUSEBUTTONDOWN:
               #     if submit_button.collidepoint(event.pos):
               #         print("2 Отправлен ответ (кнопка):", input_box.text)

            self.submit_button.check_hover(*mouse_position)
            self.input_box.update()
            self.draw()

            #pygame.draw.rect(screen, LIGHT_BLUE, submit_button)
            #self.screen.blit(button_text, (submit_button.x + 50, submit_button.y + 10))

            pygame.display.flip()
            clock.tick(60)
