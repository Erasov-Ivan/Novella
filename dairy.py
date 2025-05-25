from utils import *
from generator.generator import *


class Dairy:
    def __init__(
            self, screen: pygame.Surface, font: pygame.font.Font,
            button_size: int = 40,
    ):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.font = font

        self.dairy_button = Button(
            x=self.screen_width - button_size - 40,
            y=40,
            width=button_size,
            height=button_size,
            text='Д',
            font=font,
            callback='',
            parent=None
        )

        self.surface = BasicSurface(
            x=self.screen_width // 3,
            y=self.screen_height // 10,
            width=self.screen_width // 3,
            height=self.screen_height // 10 * 8,
            fill_color=Color('grey')
        )
        self.titles_surface = Block(
            x=0, y=0, width=self.surface.width, height=self.surface.height // 10,
            parent=self.surface, fill_color=Color(0, 0, 0, 0)
        )
        self.surface.children.append(self.titles_surface)
        self.titles_surface.children.append(
            Button(
                x=0, y=0,
                width=self.titles_surface.width // 3, height=self.titles_surface.height,
                text='Текущие цели', callback='tasks', font=self.font, parent=self.titles_surface
            )
        )
        self.titles_surface.children.append(
            Button(
                x=self.titles_surface.width // 3, y=0,
                width=self.titles_surface.width // 3, height=self.titles_surface.height,
                text='Обзор сюжета', callback='plot', font=self.font, parent=self.titles_surface
            )
        )
        self.titles_surface.children.append(
            Button(
                x=self.titles_surface.width // 3 * 2, y=0,
                width=self.titles_surface.width // 3, height=self.titles_surface.height,
                text='Теория', callback='theory', font=self.font, parent=self.titles_surface
            )
        )
        self.data_surface = Block(
            x=self.titles_surface.height, y=0,
            width=self.surface.width, height=self.surface.height - self.titles_surface.height,
            fill_color=Color(0, 0, 0, 0), parent=self.surface
        )
        self.surface.children.append(self.data_surface)

    def open_dairy(self):
        running = True
        while running:
            mouse_position = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        #self.check_titles_click(mouse_position=mouse_position)
                        #self.check_chapters_buttons(mouse_position=mouse_position)
                        if self.dairy_button.is_hovered(*mouse_position):
                            running = False

            self.dairy_button.check_hover(*mouse_position)
            draw_surface(source=self.surface, dest=self.screen)
            pygame.display.flip()

    def update(self, plot: Plot, tasks: Tasks, theory: Theory):
        return



