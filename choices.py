from utils import *
from generator.generator import Choice


class Choices:
    def __init__(
            self, font: pygame.font.Font, buttons_surface: BasicSurface
    ):
        self.font = font
        self.buttons_surface = buttons_surface
        self.buttons = ButtonsList(
            area=buttons_surface,
            font=font
        )

    def update_buttons(self, choices: list[Choice]):
        buttons = []
        for i in range(len(choices)):
            buttons.append((choices[i].caption, str(i)))
        self.buttons.update_buttons(buttons=buttons)

    def draw_current_buttons(self, dest: pygame.Surface):
        draw_surface(source=self.buttons_surface, dest=dest)

    def check_hover(self, mouse_position: tuple[int, int]):
        self.buttons.check_hovers(*mouse_position)






