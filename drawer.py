import pygame
from pygame.colordict import THECOLORS


class Drawer:
    def __init__(
            self, screen: pygame.Surface,
            text_area_height: int, font: pygame.font.Font,
            text_color: str = 'white', text_background_darkness: int = 200,
            default_background: str = 'black'
    ):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

        self.text_area_height = text_area_height
        self.font = font
        if text_color not in THECOLORS.keys():
            raise ValueError(f'Unknown color: {text_color}')
        self.text_color = text_color

        if text_background_darkness < 0:
            text_background_darkness = 0
        elif text_background_darkness > 255:
            text_background_darkness = 255
        self.text_background_darkness = text_background_darkness

        if default_background not in THECOLORS.keys():
            raise ValueError(f'Unknown color: {default_background}')
        self.default_background = default_background

        self.text_overlay_surface = pygame.Surface((self.screen_width, self.text_area_height), pygame.SRCALPHA)
        self.text_overlay_surface.fill((0, 0, 0, self.text_background_darkness))

        self.current_background: pygame.Surface | str = self.default_background

    def draw_text_title(self, title: str, centered: bool = False):
        text_surface = self.font.render(title, True, THECOLORS[self.text_color])
        if centered:
            text_rect = text_surface.get_rect(center=(self.screen_width / 2, self.screen_height / 2 - self.font.get_height()))
        else:
            text_rect = text_surface.get_rect(
                center=(self.screen_width / 2, self.screen_height - self.text_area_height / 2 - self.font.get_height()))
        self.screen.blit(text_surface, text_rect)

    def draw_text(self, text: str, centered: bool = False):
        text_surface = self.font.render(text, True, THECOLORS[self.text_color])
        if centered:
            text_rect = text_surface.get_rect(center=(self.screen_width / 2, self.screen_height / 2))
            text_overlay_react = self.text_overlay_surface.get_rect(
                center=(self.screen_width / 2, self.screen_height / 2)
            )
        else:
            text_rect = text_surface.get_rect(center=(self.screen_width / 2, self.screen_height - self.text_area_height / 2))
            text_overlay_react = self.text_overlay_surface.get_rect(
                center=(self.screen_width / 2, self.screen_height - self.text_area_height / 2)
            )
        self.screen.blit(self.text_overlay_surface, text_overlay_react)
        self.screen.blit(text_surface, text_rect)

    def update_background(self, image: str = None, color: str = None):
        if image is None and color is None:
            self.current_background = self.default_background
        elif color is not None:
            self.current_background = color
        else:
            background = pygame.image.load(image)
            self.current_background = pygame.transform.scale(
                surface=background, size=(self.screen_width, self.screen_height)
            )

    def draw_current_background(self):
        if type(self.current_background) is pygame.Surface:
            self.screen.blit(source=self.current_background, dest=(0, 0))
        elif type(self.current_background) is str:
            self.fill_background(color=self.current_background)
        else:
            self.fill_background()

    def fill_background(self, color: str = None):
        if color is None:
            self.screen.fill(THECOLORS[self.default_background])
        else:
            try:
                self.screen.fill(THECOLORS[color])
            except KeyError:
                self.screen.fill(THECOLORS[self.default_background])

