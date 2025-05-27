from utils import *


class MainMenu:
    def __init__(self, screen: pygame.Surface, font: pygame.font, buttons: list[tuple[str, str]]):
        self.screen = screen
        self.font = font

        self.surface = BasicSurface(
            x=self.screen.get_width() // 4,
            y=self.screen.get_height() // 10,
            width=self.screen.get_width() // 2,
            height=self.screen.get_height() // 10 * 8,
            fill_color=Color('grey')
        )
        self.buttons_surface = Block(
            x=self.surface.width // 10,
            y=self.surface.height // 3,
            width=self.surface.width // 10 * 8,
            height=self.surface.height // 2,
            parent=self.surface,
            fill_color=Color(0, 0, 0, 0)
        )
        self.surface.children.append(self.buttons_surface)

        self.text_label = Button(
            text='Выбирите главу',
            x=self.surface.width // 4,
            y=self.surface.width // 10,
            width=self.surface.width // 2,
            height=self.surface.height // 10,
            parent=self.surface,
            font=self.font,
            callback=''
        )
        self.surface.children.append(self.text_label)

        self.chapters_list = ButtonsList(
            area=self.buttons_surface,
            font=self.font
        )
        self.buttons_surface.children.append(self.chapters_list)
        self.chapters_list.update_buttons(buttons=buttons)

    def check_chapter_click(self, mouse_position: tuple[int, int]) -> str | None:
        for button in self.chapters_list.children:
            if button.is_hovered(*mouse_position):
                return button.callback

    def chose_chapter(self) -> str:
        running = True
        while running:
            mouse_position = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        res = self.check_chapter_click(mouse_position=mouse_position)
                        if res is not None and res != '':
                            return res

            self.chapters_list.check_hovers(*mouse_position)
            self.screen.fill(Color('black'))
            draw_surface(source=self.surface, dest=self.screen)
            pygame.display.flip()

    def update_buttons(self, buttons: list[tuple[str, str]]):
        self.chapters_list.update_buttons(buttons=buttons)
