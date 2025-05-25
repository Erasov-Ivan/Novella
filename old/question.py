import pygame
from utils import TextLabel


class Question:
    def __init__(self, screen: pygame.Surface, font: pygame.font.Font, question: str, answer: str):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.font = font
        self.question = question
        self.answer = answer

        self.surface_color = 'grey'
        self.surface = pygame.Surface(
            (self.screen_width // 2, self.screen_height // 2)
        )
        self.rect = self.surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2))

        self.label = TextLabel(
            screen=self.surface,
            x=self.rect.width // 5,
            y=self.rect.height // 5,
            width=self.rect.width // 5 * 3,
            height=self.rect.height // 5,
            font=self.font
        )

    def draw(self):
        self.surface.fill(self.surface_color)
        self.label.draw()
        self.screen.blit(self.surface, self.rect)

    def start(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if self.label.handle_event(event):
                    print("1 Отправлен ответ:", self.label.text)

               #if event.type == pygame.MOUSEBUTTONDOWN:
               #     if submit_button.collidepoint(event.pos):
               #         print("2 Отправлен ответ (кнопка):", input_box.text)

            self.label.update()
            self.draw()

            #pygame.draw.rect(screen, LIGHT_BLUE, submit_button)
            #self.screen.blit(button_text, (submit_button.x + 50, submit_button.y + 10))

            pygame.display.flip()
            clock.tick(60)
