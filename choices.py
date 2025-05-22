import pygame
from pygame.colordict import THECOLORS


class Button:
    def __init__(
            self, x: int, y: int, width: int, height: int, text: str, action: dict,
            font: pygame.font.Font, text_color: str = 'white',
            color: str = 'gray40', hover_color: str = 'gray20', border_color: str = 'black'
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.action = action
        try:
            self.text_color = THECOLORS[text_color]
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

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def check_hover(self, mouse_position: tuple[float, float]):
        self.is_hovered = self.rect.collidepoint(mouse_position)
        return self.is_hovered

    def is_clicked(self, mouse_pos, mouse_click):
        return self.rect.collidepoint(mouse_pos) and mouse_click


class Choices:
    def __init__(
            self, screen: pygame.Surface,
            text_area_height: int, font: pygame.font.Font,
            height_interval: int = 10, borders_interval: int = 10, right_interval: int = 100
    ):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

        self.text_area_height = text_area_height
        self.font = font
        self.height_interval = height_interval
        self.borders_interval = borders_interval
        self.right_interval = right_interval
        self.height_size = self.font.get_height() + borders_interval * 2
        self.buttons: list[Button] = []

    def update_buttons(self, buttons: list[dict], text_centered: bool):
        self.buttons = []
        if len(buttons) == 0:
            return
        captions = list(map(lambda b: b.get('caption', ''), buttons))
        max_width = max(map(lambda c: self.font.size(c)[0], captions)) + 5
        if text_centered:
            start_x = self.screen_width // 2 - (max_width // 2)
            start_y = self.screen_height // 2 + self.text_area_height // 2
        else:
            start_x = self.screen_width - max_width - self.right_interval
            start_y = (self.screen_height - self.text_area_height) // 2 - (
                    len(buttons) * (self.height_size + self.height_interval) // 2)
        for button in buttons:
            caption = button.get('caption', '')
            self.buttons.append(
                Button(
                    text=caption,
                    x=start_x,
                    y=start_y,
                    width=max_width + self.borders_interval * 2,
                    height=self.height_size,
                    action=button,
                    font=self.font
                )
            )
            start_y += self.height_size + self.height_interval

    def draw_current_buttons(self):
        for button in self.buttons:
            button.draw(surface=self.screen)

    def check_hover(self, mouse_position: tuple[int, int]):
        for button in self.buttons:
            button.check_hover(mouse_position=mouse_position)




