import pygame
from pygame.colordict import THECOLORS


class Button:
    def __init__(
            self, x: int, y: int, width: int, height: int,
            color: str = 'gray40', hover_color: str = 'gray20', border_color: str = 'black'
    ):
        self.rect = pygame.Rect(x, y, width, height)
        try:
            self.color = THECOLORS[color]
            self.hover_color = THECOLORS[hover_color]
            self.border_color = THECOLORS[border_color]
        except KeyError:
            raise ValueError(f'Unknown color: {color}, {hover_color}, {border_color}')
        self.is_hovered = False

    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        pygame.draw.rect(surface, self.border_color, self.rect, 2, border_radius=5)

    def check_hover(self, mouse_position: tuple[float, float]):
        self.is_hovered = self.rect.collidepoint(mouse_position)
        return self.is_hovered

    def is_clicked(self, mouse_position: tuple[float, float]) -> bool:
        return self.rect.collidepoint(mouse_position)


class TextButton(Button):
    def __init__(
            self, x: int, y: int, width: int, height: int, text: str, index: str,
            font: pygame.font.Font, text_color: str = 'white',
            color: str = 'gray40', hover_color: str = 'gray20'
    ):
        super().__init__(
            x=x, y=y, width=width, height=height, color=color, hover_color=hover_color, border_color=hover_color
        )
        self.text = text
        self.font = font
        self.index = index
        try:
            self.text_color = THECOLORS[text_color]
        except KeyError:
            raise ValueError(f'Unknown color: {text_color}')

    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        pygame.draw.rect(surface, self.border_color, self.rect, 2, border_radius=5)

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)


class TextLabel:
    def __init__(
            self, x: int, y: int, width: int, height: int, screen: pygame.Surface,
            font: pygame.font.Font, text_color: str = 'white',
            color: str = 'gray40', active_color: str = 'gray60', text: str = '',
    ):
        self.screen = screen
        self.font = font
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.active_color = active_color
        self.text = text
        self.text_color = text_color
        self.text_surface = self.font.render(text, True, self.text_color)
        self.active = False
        self.cursor_visible = True
        self.cursor_timer = 0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = self.active_color if self.active else self.color

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                print("3 Пользователь ввел:", self.text)
                return True  # Возвращаем True при нажатии Enter
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

            self.text_surface = self.font.render(self.text, True, self.text_color)

    def update(self):
        self.cursor_timer += 1
        if self.cursor_timer > 30:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
        pygame.draw.rect(self.screen, 'black', self.rect, 2)

        self.screen.blit(self.text_surface, (self.rect.x + 5, self.rect.y + 5))

        if self.active and self.cursor_visible:
            cursor_x = self.rect.x + 5 + self.text_surface.get_width()
            pygame.draw.line(
                self.screen, self.text_color,
                (cursor_x, self.rect.y + 5),
                (cursor_x, self.rect.y + self.rect.height - 5),
                2
            )
