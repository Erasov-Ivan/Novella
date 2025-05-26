import pygame
from pygame.color import Color
import re
import time

BASIC_BUTTON_COLOR = Color('grey40')
BASIC_BUTTON_HOVER_COLOR = Color('grey60')
BASIC_BUTTON_TEXT_COLOR = Color('black')
BASIC_BUTTON_BORDER_COLOR = Color('black')
BASIC_TEXT_COLOR = Color('white')
BASIC_TEXT_OVERLAY_COLOR = (0, 0, 0, 200)


class BasicSurface:
    def __init__(self, x: int, y: int, width: int, height: int, fill_color: Color = Color(0, 0, 0, 0)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.parent = None
        self.children = []
        self.fill_color = fill_color

    def fill(self):
        self.surface.fill(self.fill_color)

    def draw(self, dest: pygame.Surface):
        dest.blit(
            source=self.surface,
            dest=(self.x, self.y)
        )


class Block(BasicSurface):
    def __init__(
            self, x: int, y: int, width: int, height: int,
            fill_color: Color, parent: BasicSurface | None
    ):
        super().__init__(x=x, y=y, width=width, height=height, fill_color=fill_color)
        self.parent = parent

    def is_hovered(self, mouse_x, mouse_y) -> bool:
        mouse_x = mouse_x - self.parent.x
        mouse_y = mouse_y - self.parent.y
        parent = self.parent
        while (parent := parent.parent) is not None:
            mouse_x = mouse_x - parent.x
            mouse_y = mouse_y - parent.y
        return self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height


class BasicText(Block):
    def __init__(
            self, text: str, font: pygame.font.Font,  text_color: Color = BASIC_TEXT_COLOR,
            background_color: Color = Color(0, 0, 0, 0),
            x: int = 0, y: int = 0, width: int = 0, height: int = 0, parent: BasicSurface | None = None
    ):
        super().__init__(x=x, y=y, width=width, height=height, parent=parent, fill_color=background_color)
        self.text = text
        self.text_color = text_color
        self.font = font
        self.start_offset_from_middle = self.font.size(self.text[:(len(self.text) + 1) // 2])[0]

    def draw(self, dest: pygame.Surface):
        text = self.font.render(self.text, True, self.text_color)
        text_rect = text.get_rect(
            midleft=(dest.get_width() / 2 - self.start_offset_from_middle, dest.get_height() / 2)
        )
        dest.blit(
            source=text,
            dest=text_rect
        )


class GameText:
    def __init__(
            self, words: str, character: str | None, title: str | None,
            font: pygame.font.Font, screen: pygame.Surface, centered: bool | None,
            text_color: Color = BASIC_TEXT_COLOR,
            background_color: Color = BASIC_TEXT_OVERLAY_COLOR, background_size_mul: float = 1/6,
            delay: float | None = 0.005
    ):
        if character is not None:
            words = f'{character}: {words}'
        if delay is None:
            self.delay = 0.005
        else:
            self.delay = delay
        self.text = words
        self.cleared_text = re.sub(r'\{.*?}', '', self.text)
        self.text_color = text_color
        self.font = font
        self.background_color = background_color
        self.background_size_mul = background_size_mul
        self.start_offset_from_middle = self.font.size(self.cleared_text[:len(self.cleared_text) // 2 + 1])[0]
        overlay_height = int(screen.get_height() * self.background_size_mul)
        if centered:
            y = (screen.get_height() - overlay_height) // 2
        else:
            y = screen.get_height() - overlay_height
        self.overlay = BasicSurface(
            x=0,
            y=y,
            width=screen.get_width(),
            height=overlay_height,
            fill_color=self.background_color
        )
        self.overlay.fill()
        self.screen = screen
        self.animation_done = False

        self.letter = -1
        self.cleared_words_index = 0
        self.cleared_words_len = len(self.cleared_text)
        self.cleared_words = self.cleared_text

    def draw_overlay(self):
        self.overlay.draw(dest=self.screen)

    def draw_text(self):
        text = self.font.render(self.cleared_text, True, self.text_color)
        text_rect = text.get_rect(
            midleft=(self.screen.get_width() / 2 - self.start_offset_from_middle, self.overlay.y + self.overlay.height / 2)
        )
        self.screen.blit(source=text, dest=text_rect)

    def draw(self):
        self.draw_overlay()
        if self.animation_done:
            self.draw_text()
        else:
            self.continue_animation()

    def continue_animation(self):
        if self.cleared_words_index <= self.cleared_words_len:
            if self.text[self.letter] == '{':
                command = ''
                self.letter += 1
                while self.text[self.letter] != '}':
                    command += self.text[self.letter]
                    self.letter += 1
                command_params = command.split()
                if command_params[0] == 'sleep':
                    time.sleep(float(command_params[1]))
            self.cleared_text = self.cleared_words[:self.cleared_words_index]
            self.draw_text()
            self.letter += 1
            self.cleared_words_index += 1
            time.sleep(self.delay)
        else:
            self.animation_done = True
            self.draw_text()


class Button(Block):
    def __init__(
            self, x: int, y: int, width: int, height: int, parent: BasicSurface | None,
            text: str, callback: str, font: pygame.font.Font,
            fill_color: Color = BASIC_BUTTON_COLOR, hover_color: Color = BASIC_BUTTON_HOVER_COLOR,
            text_color: Color = BASIC_BUTTON_TEXT_COLOR, border_color: Color = BASIC_BUTTON_BORDER_COLOR,
            border_size: int = 2
    ):
        super().__init__(x=x, y=y, width=width, height=height, fill_color=fill_color, parent=parent)
        self.parent = parent
        self.text = BasicText(text=text, font=font, text_color=text_color)
        self.hover_color = hover_color
        self.hovered = False
        self.callback = callback
        self.boarder = BasicSurface(
            x=x-border_size, y=y-border_size,
            width=width+border_size * 2, height=height + border_size*2,
            fill_color=border_color
        )
        self.boarder.fill()
        self.fill()

    def draw(self, dest: pygame.Surface):
        self.boarder.draw(dest=dest)
        self.text.draw(
            dest=self.surface
        )
        dest.blit(
            source=self.surface,
            dest=(self.x, self.y)
        )

    def check_hover(self, mouse_x: int, mouse_y: int):
        if self.is_hovered(mouse_x=mouse_x, mouse_y=mouse_y) and not self.hovered:
            self.fill_color, self.hover_color = self.hover_color, self.fill_color
            self.hovered = True
        elif not self.is_hovered(mouse_x=mouse_x, mouse_y=mouse_y) and self.hovered:
            self.fill_color, self.hover_color = self.hover_color, self.fill_color
            self.hovered = False


class ButtonsList(Block):
    def __init__(
            self, area: BasicSurface,
            font: pygame.font.Font, text_color: Color = BASIC_BUTTON_TEXT_COLOR,
            buttons_color: Color = BASIC_BUTTON_COLOR, buttons_hover_color: Color = BASIC_BUTTON_HOVER_COLOR,
            height_interval: int = 10, button_height: int | None = None,
            border_color: Color = BASIC_BUTTON_BORDER_COLOR, border_size: int = 2
    ):
        super().__init__(
            x=0,
            y=0,
            width=area.width,
            height=area.height,
            fill_color=area.fill_color,
            parent=area
        )
        if button_height is None:
            self.button_height = font.get_height() + 10
        else:
            self.button_height = button_height
        self.font = font
        self.text_color = text_color
        self.buttons_color = buttons_color
        self.buttons_hover_color = buttons_hover_color
        self.height_interval = height_interval
        self.border_size = border_size
        self.border_color = border_color

    def update_buttons(self, buttons: list[tuple[str, str]]):
        """buttons: list[(caption, callback)]"""
        self.children = []
        if len(buttons) == 0:
            return
        for i in range(len(buttons)):
            caption, callback = buttons[i]
            self.children.append(
                Button(
                    x=self.border_size,
                    y=(self.button_height + self.height_interval) * i + self.border_size,
                    width=self.width - self.border_size * 2,
                    height=self.button_height - self.border_size * 2,
                    text=caption,
                    text_color=self.text_color,
                    font=self.font,
                    callback=callback,
                    fill_color=self.buttons_color,
                    hover_color=self.buttons_hover_color,
                    border_color=self.border_color,
                    border_size=self.border_size,
                    parent=self
                )
            )

    def check_hovers(self, mouse_x: int, mouse_y: int):
        for button in self.children:
            button.check_hover(mouse_x=mouse_x, mouse_y=mouse_y)


class Background:
    def __init__(self, screen: pygame.Surface, default: Color | pygame.Surface = Color('black')):
        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()
        self.default = default
        self.current_background = default

    def update(self, image: str = None, color: str = None):
        if image is None and color is None:
            self.current_background = self.default
        elif color is not None:
            self.current_background = color
        else:
            background = pygame.image.load(image)
            self.current_background = pygame.transform.scale(
                surface=background, size=(self.screen_width, self.screen_height)
            )

    def draw(self):
        if type(self.current_background) is pygame.Surface:
            self.screen.blit(source=self.current_background, dest=(0, 0))
        elif type(self.current_background) is str:
            self.fill(self.current_background)
        else:
            self.fill()

    def fill(self, color: Color = None):
        if color is None:
            self.screen.fill(self.default)
        else:
            self.screen.fill(color)


def draw_surface(source: BasicSurface, dest: pygame.Surface):
    source.fill()
    for child in source.children:
        draw_surface(source=child, dest=source.surface)
    source.draw(dest=dest)

