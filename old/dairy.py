import pygame
from utils import TextButton, Button


class Plot:
    def __init__(self, plot: dict, font: pygame.font.Font, text_color: str, data_surface: pygame.Surface):
        self.plot = plot
        self.text_color = text_color
        self.font = font
        self.current_page = 0
        data_surface = data_surface

        self.title_surface = pygame.Surface((data_surface.get_width() // 3 * 2, data_surface.get_height() // 10))
        self.title_rect = self.title_surface.get_rect(
            center=(data_surface.get_width() // 2, data_surface.get_height() // 20)
        )

        self.left_button = TextButton(
            x=0, y=0, width=self.title_surface.get_width() // 5, height=self.title_surface.get_height(),
            text='<-', text_color=self.text_color, index='left', font=self.font
        )
        self.right_button = TextButton(
            x=self.title_surface.get_width() // 5 * 4, y=0, width=self.title_surface.get_width() // 5,
            height=self.title_surface.get_height(), text='->', text_color=self.text_color, index='right', font=self.font
        )

    def draw_title(self, title: str, surface: pygame.Surface):
        title_button = TextButton(
            x=self.title_surface.get_width() // 5, y=0, width=self.title_surface.get_width() // 5 * 3,
            height=self.title_surface.get_height(), text=title, text_color=self.text_color, index='title',
            font=self.font
        )
        self.left_button.draw(self.title_surface)
        self.right_button.draw(self.title_surface)
        title_button.draw(self.title_surface)
        surface.blit(self.title_surface, self.title_rect)

    def draw(self, surface):
        if self.plot == {}:
            title = ''
            lines = ['Тут пока ничего нет']
        else:
            title = list(self.plot.keys())[self.current_page]
            lines = self.plot[title]

        self.draw_title(title=title, surface=surface)
        current_y = self.title_surface.get_height() * 2
        for line in lines:
            text_surface = self.font.render(line, True, self.text_color)
            text_rect = text_surface.get_rect(
                midleft=(
                    surface.get_width() // 10, current_y
                )
            )
            surface.blit(text_surface, text_rect)
            current_y += self.font.get_height()

    def add(self, title: str, text: str):
        if title in self.plot.keys():
            self.plot[title].append(text)
        else:
            self.plot[title] = [text]


class CurrentTasks:
    def __init__(self, current_tasks: dict, font: pygame.font.Font, text_color: str):
        self.current_tasks = current_tasks
        self.text_color = text_color
        self.font = font

    def draw(self, surface: pygame.Surface):
        current_y = surface.get_height() // 10
        tasks = self.current_tasks.values()
        if len(tasks) == 0:
            tasks = ['Тут пока ничего нет']
        for task in tasks:
            text_surface = self.font.render(f'- {task}', True, self.text_color)
            text_rect = text_surface.get_rect(
                midleft=(
                    surface.get_width() // 10, current_y
                )
            )
            surface.blit(text_surface, text_rect)
            current_y += self.font.get_height() * 2

    def add(self, key: str, value: str):
        self.current_tasks[key] = value

    def remove(self, key: str):
        self.current_tasks.pop(key, None)


class Theory:
    def __init__(self, theory: dict):
        self.theory = theory


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
            height=button_size
        )

        self.surface_color = 'grey'
        self.surface = pygame.Surface(
            (self.screen_width - self.screen_width // 3, self.screen_height - self.screen_height // 10)
        )
        self.rect = self.surface.get_rect(center=(self.screen_width//2, self.screen_height//2))

        self.titles_surface = pygame.Surface(
            (self.surface.get_width(), self.surface.get_height() // 10)
        )
        self.titles_rect = self.titles_surface.get_rect(
            center=(self.surface.get_width() // 2, self.surface.get_height() // 20)
        )

        self.titles: list[TextButton] = [
            TextButton(
                text='Текущие цели',
                x=0,
                y=0,
                width=self.titles_surface.get_width() // 3,
                height=self.titles_surface.get_height(),
                font=self.font,
                index='tasks',
                hover_color=self.surface_color
            ),
            TextButton(
                text='Обзор сюжета',
                x=self.titles_surface.get_width() // 3,
                y=0,
                width=self.titles_surface.get_width() // 3,
                height=self.titles_surface.get_height(),
                font=self.font,
                index='plot',
                hover_color=self.surface_color
            ),
            TextButton(
                text='Теория',
                x=self.titles_surface.get_width() // 3 * 2,
                y=0,
                width=self.titles_surface.get_width() // 3,
                height=self.titles_surface.get_height(),
                font=self.font,
                index='theory',
                hover_color=self.surface_color
            )
        ]

        self.data_surface = pygame.Surface(
            (self.surface.get_width(), self.surface.get_height() - self.titles_surface.get_height())
        )
        self.data_rect = self.data_surface.get_rect(
            center=(self.surface.get_width() // 2, (self.surface.get_height() + self.titles_surface.get_height()) // 2)
        )

        self.plot = Plot(
            plot={},
            font=self.font, text_color='black', data_surface=self.data_surface
        )
        self.theory = Theory(theory={})
        self.tasks = CurrentTasks(
            current_tasks={},
            font=self.font, text_color='black'
        )

    def draw_button(self):
        self.dairy_button.draw(surface=self.screen)

    def draw_titles(self):
        for title in self.titles:
            title.draw(surface=self.titles_surface)
        self.surface.blit(self.titles_surface, self.titles_rect)

    def draw_data(self):
        self.data_surface.fill(self.surface_color)
        for title in self.titles:
            if title.is_hovered:
                match title.index:
                    case 'tasks':
                        self.tasks.draw(surface=self.data_surface)
                        break
                    case 'plot':
                        self.plot.draw(surface=self.data_surface)
                        break
        self.surface.blit(self.data_surface, self.data_rect)

    def draw_dairy(self):
        self.surface.fill(self.surface_color)
        self.draw_button()
        self.draw_titles()
        self.draw_data()
        self.screen.blit(self.surface, self.rect)

    def check_titles_click(self, mouse_position: tuple[int, int]):
        relative_mouse_pos = (
            mouse_position[0] - self.rect.x,
            mouse_position[1] - self.rect.y
        )
        for title in self.titles:
            if title.is_clicked(mouse_position=relative_mouse_pos):
                title.is_hovered = True
                for other_title in self.titles:
                    if other_title.index != title.index:
                        other_title.is_hovered = False
                break

    def check_chapters_buttons(self, mouse_position: tuple[int, int]):
        relative_mouse_pos = (
            mouse_position[0] - self.rect.x - self.data_rect.x - self.plot.title_rect.x,
            mouse_position[1] - self.rect.y - self.data_rect.y - self.plot.title_rect.y
        )
        if self.plot.left_button.is_clicked(mouse_position=relative_mouse_pos):
            self.plot.current_page -= 1
        elif self.plot.right_button.is_clicked(mouse_position=relative_mouse_pos):
            self.plot.current_page += 1
        if self.plot.current_page < 0:
            self.plot.current_page = len(self.plot.plot.keys()) - 1
        elif self.plot.current_page >= len(self.plot.plot.keys()):
            self.plot.current_page = 0

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
                        self.check_chapters_buttons(mouse_position=mouse_position)
                        if self.dairy_button.is_clicked(mouse_position=mouse_position):
                            running = False

            self.dairy_button.check_hover(mouse_position=mouse_position)
            self.draw_dairy()
            pygame.display.flip()

    def update(self, plot: dict, tasks: dict, theory: dict):
        title = plot.get('chapter', None)
        if title is not None:
            for text in plot.get('add', []):
                self.plot.add(title=title, text=text)

        for key, value in tasks.get('add', {}).items():
            self.tasks.add(key=key, value=value)

        for key in tasks.get('remove', []):
            self.tasks.remove(key=key)


