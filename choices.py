from utils import *
from generator import Choice


class Choices:
    def __init__(
            self, font: pygame.font.Font,
            x: int, y: int, width: int, height: int
    ):
        self.font = font
        self.buttons_surface = BasicSurface(
            x=x, y=y, width=width, height=height
        )
        self.buttons = ButtonsList(
            area=self.buttons_surface,
            font=self.font
        )
        self.buttons_surface.children.append(self.buttons)

    def update_buttons(self, choices: list[Choice]):
        buttons = []
        for i in range(len(choices)):
            if not choices[i].done:
                buttons.append((choices[i].caption, str(i)))
        self.buttons.update_buttons(buttons=buttons)

    def draw(self, dest: pygame.Surface):
        draw_surface(source=self.buttons_surface, dest=dest)

    def check_hover(self, mouse_position: tuple[int, int]):
        self.buttons.check_hovers(*mouse_position)

    def check_mouse_click(self, mouse_position: tuple[int, int]) -> str | None:
        for button in self.buttons.children:
            if button.is_hovered(*mouse_position):
                return button.callback
        return None






