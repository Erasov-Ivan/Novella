import pygame
from pygame.colordict import THECOLORS
import time
import re


class Button:
    def __init__(
            self, x: int, y: int, width: int, height: int, text: str, action: dict,
            font: pygame.font.Font, text_color: str = 'white',
            color: str = 'gray66', hover_color: str = 'gray85', border_color: str = 'black'
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

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        return self.is_hovered

    def is_clicked(self, mouse_pos, mouse_click):
        return self.rect.collidepoint(mouse_pos) and mouse_click


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
        if title is None:
            return
        text_surface = self.font.render(title, True, THECOLORS[self.text_color])
        if centered:
            text_rect = text_surface.get_rect(
                center=(self.screen_width / 2, self.screen_height / 2 - self.font.get_height()))
        else:
            text_rect = text_surface.get_rect(
                center=(self.screen_width / 2, self.screen_height - self.text_area_height / 2 - self.font.get_height()))
        self.screen.blit(text_surface, text_rect)

    def draw_text(self, text: str, start_offset_from_middle: int, centered: bool = False):
        text_surface = self.font.render(text, True, THECOLORS[self.text_color])
        if centered:
            text_rect = text_surface.get_rect(
                midleft=(self.screen_width / 2 - start_offset_from_middle, self.screen_height / 2)
            )
            text_overlay_react = self.text_overlay_surface.get_rect(
                center=(self.screen_width / 2, self.screen_height / 2)
            )
        else:
            text_rect = text_surface.get_rect(
                midleft=(self.screen_width / 2 - start_offset_from_middle, self.screen_height - self.text_area_height / 2)
            )
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

    def show_text_appearance_animation(
            self, words: str, title: str, character: str, centered: bool, delay: float = 0.005
    ):
        if title is not None and character is not None:
            words = f'{character}: {words}'
        elif title is None and character is not None:
            title = character
        cleared_words = re.sub(r'\{.*?}', '', words)
        cleared_words_len = len(cleared_words)
        words_len = len(words)
        start_offset_from_middle = self.font.size(words[:len(cleared_words) // 2])[0]
        letter = -1
        cleared_words_index = 0
        while cleared_words_index <= cleared_words_len:
            if words[letter] == '{':
                command = ''
                letter += 1
                while words[letter] != '}':
                    command += words[letter]
                    letter += 1
                command_params = command.split()
                if command_params[0] == 'sleep':
                    time.sleep(float(command_params[1]))
            self.draw_current_background()
            self.draw_text(
                text=cleared_words[:cleared_words_index],
                centered=centered,
                start_offset_from_middle=start_offset_from_middle
            )
            self.draw_text_title(title=title, centered=centered)
            letter += 1
            cleared_words_index += 1

            time.sleep(delay)
            pygame.display.flip()
