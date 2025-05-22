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
