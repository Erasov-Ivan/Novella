from utils import *
from generator import *


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
            text='D',
            font=font,
            callback='',
            parent=None
        )

        self.plot = {}
        self.tasks = {}
        self.theory = {}

        self.surface = BasicSurface(
            x=self.screen_width // 4,
            y=self.screen_height // 10,
            width=self.screen_width // 2,
            height=self.screen_height // 10 * 8,
            fill_color=Color('grey')
        )
        self.titles_surface = Block(
            x=0, y=0, width=self.surface.width, height=self.surface.height // 10,
            parent=self.surface, fill_color=Color(0, 0, 0, 0)
        )
        self.surface.children.append(self.titles_surface)
        self.tasks_button = Button(
            x=0, y=0,
            width=self.titles_surface.width // 3, height=self.titles_surface.height,
            text='Текущие цели', callback='tasks', font=self.font, parent=self.titles_surface
        )
        self.titles_surface.children.append(self.tasks_button)
        self.plot_button =  Button(
            x=self.titles_surface.width // 3, y=0,
            width=self.titles_surface.width // 3, height=self.titles_surface.height,
            text='Обзор сюжета', callback='plot', font=self.font, parent=self.titles_surface
        )
        self.titles_surface.children.append(self.plot_button)
        self.theory_button = Button(
            x=self.titles_surface.width // 3 * 2, y=0,
            width=self.titles_surface.width // 3, height=self.titles_surface.height,
            text='Теория', callback='theory', font=self.font, parent=self.titles_surface
        )
        self.titles_surface.children.append(self.theory_button)
        self.data_surface = Block(
            x=0, y=self.titles_surface.height,
            width=self.surface.width, height=self.surface.height - self.titles_surface.height,
            fill_color=Color(0, 0, 0, 0), parent=self.surface
        )
        self.surface.children.append(self.data_surface)
        self.plot_headers_surface = Block(
            x=self.data_surface.width // 4,
            y=0,
            width=self.data_surface.width // 2,
            height=self.data_surface.height // 10,
            parent=self.data_surface,
            fill_color=Color(0, 0, 0, 0)
        )
        self.plot_headers_button_left = Button(
            x=0, y=0,
            width=self.plot_headers_surface.width // 4, height=self.plot_headers_surface.height,
            parent=self.plot_headers_surface, text='<', callback='plot_left', font=self.font
        )
        self.plot_headers_surface.children.append(self.plot_headers_button_left)

        self.plot_headers_caption = Button(
            x=self.plot_headers_surface.width // 4, y=0,
            width=self.plot_headers_surface.width // 2, height=self.plot_headers_surface.height,
            parent=self.plot_headers_surface, text='', callback='None', font=self.font
        )
        self.plot_headers_surface.children.append(self.plot_headers_caption)

        self.plot_headers_button_right = Button(
            x=self.plot_headers_surface.width // 4 * 3, y=0,
            width=self.plot_headers_surface.width // 4, height=self.plot_headers_surface.height,
            parent=self.plot_headers_surface, text='>', callback='plot_right', font=self.font
        )
        self.plot_headers_surface.children.append(self.plot_headers_button_right)
        self.plot_text_surface = BasicSurface(
            x=0, y=self.plot_headers_surface.height,
            width=self.data_surface.width, height=self.data_surface.height - self.plot_headers_surface.height
        )
        self.plot_chapter_index = 0
        self.plot_text_offset = 0
        self.theory_chapter_index = 0
        self.theory_text_offset = 0

    def check_titles_click(self, mouse_position: tuple[int, int]):
        for title in self.titles_surface.children:
            if title.is_hovered(*mouse_position):
                title.check_hover(*mouse_position)
                for t in self.titles_surface.children:
                    t.check_hover(*mouse_position)

    def draw_current_tasks(self):
        self.data_surface.children = []
        current_y = self.data_surface.height // 10
        for task in self.tasks.values():
            block = Block(
                x=self.data_surface.width // 10,
                y=current_y,
                width=self.data_surface.width - self.data_surface.width // 5,
                height=self.font.get_height() + 5,
                parent=self.data_surface,
                fill_color=Color(0, 0, 0, 0)
            )
            block.children.append(
                BasicText(
                    text=task, text_color=Color('black'), font=self.font, position='left'
                )
            )
            self.data_surface.children.append(block)
            current_y = current_y + self.font.get_height() + 5

    def draw_plot(self):
        self.data_surface.children = []
        self.plot_text_surface.children = []
        if len(self.plot.keys()) == 0:
            chapter = ''
            texts = ['Тут пока ничего нет']
        else:
            chapter = list(self.plot.keys())[self.plot_chapter_index]
            texts = self.plot[chapter]
        self.plot_headers_caption.text.text = chapter
        current_y = self.plot_text_surface.height // 20
        for text in texts:
            block = Block(
                x=self.plot_text_surface.width // 10,
                y=current_y + self.plot_text_offset,
                width=self.plot_text_surface.width - self.plot_text_surface.width // 5,
                height=self.font.get_height() + 5,
                parent=self.plot_text_surface,
                fill_color=Color(0, 0, 0, 0)
            )
            block.children.append(
                BasicText(
                    text=text, text_color=Color('black'), font=self.font, position='left'
                )
            )
            self.plot_text_surface.children.append(block)
            current_y = current_y + self.font.get_height() + 5
        self.data_surface.children.append(self.plot_headers_surface)
        self.data_surface.children.append(self.plot_text_surface)

    def check_plot_buttons_click(self, mouse_position: tuple):
        if self.plot_headers_button_right.is_hovered(*mouse_position):
            self.plot_chapter_index += 1
            self.plot_text_offset = 0
        if self.plot_headers_button_left.is_hovered(*mouse_position):
            self.plot_chapter_index -= 1
            self.plot_text_offset = 0
        if self.plot_chapter_index < 0:
            self.plot_chapter_index = 0
        if self.plot_chapter_index >= len(self.plot.keys()):
            self.plot_chapter_index = len(self.plot.keys()) - 1

    def draw_theory(self):
        self.data_surface.children = []
        self.plot_text_surface.children = []
        if len(self.theory.keys()) == 0:
            chapter = ''
            texts = ['Тут пока ничего нет']
        else:
            chapter = list(self.theory.keys())[self.theory_chapter_index]
            texts = self.theory[chapter]
        self.plot_headers_caption.text.text = chapter
        current_y = self.plot_text_surface.height // 20
        for text in texts:
            block = Block(
                x=self.plot_text_surface.width // 10,
                y=current_y + self.theory_text_offset,
                width=self.plot_text_surface.width - self.plot_text_surface.width // 5,
                height=self.font.get_height() + 5,
                parent=self.plot_text_surface,
                fill_color=Color(0, 0, 0, 0)
            )
            block.children.append(
                BasicText(
                    text=text, text_color=Color('black'), font=self.font, position='left'
                )
            )
            self.plot_text_surface.children.append(block)
            current_y = current_y + self.font.get_height() + 5
        self.data_surface.children.append(self.plot_headers_surface)
        self.data_surface.children.append(self.plot_text_surface)

    def draw_data(self):
        for title in self.titles_surface.children:
            if title.hovered:
                match title.callback:
                    case 'plot':
                        self.draw_plot()
                    case 'tasks':
                        self.draw_current_tasks()
                    case 'theory':
                        self.draw_theory()

    def open_dairy(self):
        running = True
        while running:
            mouse_position = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.check_titles_click(mouse_position=mouse_position)
                        self.check_plot_buttons_click(mouse_position=mouse_position)
                        if self.dairy_button.is_hovered(*mouse_position):
                            running = False
                if event.type == pygame.MOUSEWHEEL:
                    if self.plot_button.hovered:
                        self.plot_text_offset += event.y * 30
                    elif self.theory_button.hovered:
                        self.theory_text_offset += event.y * 30

            self.dairy_button.check_hover(*mouse_position)
            self.plot_headers_button_right.check_hover(*mouse_position)
            self.plot_headers_button_left.check_hover(*mouse_position)
            draw_surface(source=self.surface, dest=self.screen)
            self.draw_button()
            self.draw_data()
            pygame.display.flip()

    def update(self, plot: Plot | None = None, tasks: Tasks | None = None, theory: Theory | None = None):
        if plot is not None:
            title = plot.chapter
            if title is not None and plot.add is not None:
                for text in plot.add:
                    if title in self.plot.keys():
                        self.plot[title].append(text)
                    else:
                        self.plot[title] = [text]

        if tasks is not None:
            if tasks.add is not None:
                for key, value in tasks.add.items():
                    self.tasks[key] = value

            if tasks.remove is not None:
                for key in tasks.remove:
                    self.tasks.pop(key, None)

        if theory is not None:
            title = theory.chapter
            if title is not None and theory.add is not None:
                for text in theory.add:
                    if title in self.theory.keys():
                        self.theory[title].append(text)
                    else:
                        self.theory[title] = [text]

    def draw_button(self):
        self.dairy_button.fill()
        self.dairy_button.draw(dest=self.screen)



