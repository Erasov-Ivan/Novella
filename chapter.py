from saves import Saver
from choices import Choices
from dairy import Dairy
from generator import ChapterGenerator
from question import Form
from utils import *


class Chapter:
    def __init__(
            self,
            screen: pygame.Surface,
            font: pygame.font.Font,
            path: str,
            dairy: Dairy,
            saver: Saver,
            stats: dict = {},
            text_overlay_height_mul: float = 1/6,
            current_label: str = 'start',
            current_text_position: int = 0
    ):
        self.stats = stats
        self.dairy = dairy
        self.saver = saver
        self.path = path
        self.chapter = ChapterGenerator()
        self.chapter.load(f'{self.path}/chapter.json')
        self.background = Background(screen=screen)
        self.screen = screen
        self.font = font
        self.text_overlay_height_mul = text_overlay_height_mul

        self.current_position = self.chapter.labels.get(current_label, None)
        self.current_text_position = current_text_position
        if self.current_position is None:
            raise ValueError("No start point")
        self.current_text: GameText = None
        self.repeat = 0

        self.choices: Choices = None
        self.stats_shower = StatsShower(
            screen=self.screen, font=self.font, text_overlay_height_mul=self.text_overlay_height_mul
        )

    def next(self) -> None | bool:
        if self.choices is not None and len(self.choices.buttons.children) > 0:
            return

        if (q := self.current_position.texts[self.current_text_position].question) is not None:
            form = Form(screen=self.screen, font=self.font, question=q.question, answer=q.answer)
            res = form.start()
            if res:
                self.current_position = self.chapter.labels.get(q.right_label)
                if (stats := q.stats) is not None:
                    self.update_stats(stats=stats)
            else:
                self.current_position = self.chapter.labels.get(q.wrong_label)
            if self.current_position is not None:
                self.current_text_position = 0
                self.update_dairy()
                self.update_current_position()
                return

        if self.repeat > 0:
            self.repeat -= 1
            self.update_current_position()
            return

        texts = self.current_position.texts
        if texts is not None:
            self.current_text_position += 1
            if self.current_text_position < len(texts):
                self.update_dairy()
                self.update_current_text()
                self.update_current_choices()
                return
        if (next_key := self.current_position.next) is not None:
            if next_key == 'end':
                return True
            self.current_text_position = 0
            self.current_position = self.chapter.labels.get(next_key)
            self.update_dairy()
            self.update_current_position()
        else:
            return

    def update_current_text(self):
        texts = self.current_position.texts
        if texts is None:
            return
        else:
            if len(texts) <= self.current_text_position:
                return
            else:
                text = texts[self.current_text_position]
                self.current_text = GameText(
                    words=text.words,
                    character=text.character,
                    title=text.title,
                    delay=text.delay,
                    centered=text.centered,
                    font=self.font,
                    screen=self.screen,
                    background_size_mul=self.text_overlay_height_mul
                )

    def update_current_background(self):
        background = self.current_position.background
        if background is not None:
            image = background.image
            if image is not None:
                self.background.update(image=f'{self.path}/{image}')
            else:
                self.background.update(color=background.color)

    def update_current_choices(self):
        if self.current_position.texts[self.current_text_position].choices is not None:
            unclicked_choices = []
            for choice in self.current_position.texts[self.current_text_position].choices:
                if not choice.done:
                    unclicked_choices.append(choice)
            if len(unclicked_choices) == 0:
                self.next()
                return
            self.choices = Choices(
                screen_width=self.screen.get_width(), screen_height=self.screen.get_height(), font=self.font,
                text_overlay_height_mul=self.text_overlay_height_mul,
                text_centered=self.current_position.texts[self.current_text_position].centered
            )
            self.choices.update_buttons(choices=unclicked_choices)

    def update_current_position(self):
        if self.current_position is not None:
            self.update_current_background()
            self.update_current_text()
            self.update_current_choices()

    def draw(self):
        self.background.draw()
        self.current_text.draw()
        if self.choices is not None:
            self.choices.draw(dest=self.screen)
        self.stats_shower.draw()

    def process_button_click(self, mouse_position: tuple[int, int]):
        if self.choices is not None:
            callback = self.choices.check_mouse_click(mouse_position=mouse_position)
            if callback is not None:
                index = int(callback)
                self.choices = None
                self.current_position.texts[self.current_text_position].choices[index].done = True
                choice = self.current_position.texts[self.current_text_position].choices[index]
                self.dairy.update(plot=choice.plot, tasks=choice.tasks, theory=choice.theory)

                if (stats := choice.stats) is not None:
                    self.update_stats(stats=stats)

                if choice.words is not None:
                    self.current_text = GameText(
                        words=choice.words,
                        character=choice.character,
                        title=choice.title,
                        centered=choice.centered,
                        font=self.font,
                        screen=self.screen,
                        background_size_mul=self.text_overlay_height_mul
                    )
                    if choice.repeat:
                        self.repeat += 1
                elif (next_key := choice.label) is not None:
                    self.current_position = self.chapter.labels.get(next_key)
                    self.current_text_position = 0
                    if self.current_position is not None:
                        self.update_current_position()
        else:
            if self.dairy.dairy_button.is_hovered(*mouse_position):
                self.dairy.open_dairy()

    def update_dairy(self):
        texts = self.current_position.texts
        if texts is not None:
            if self.current_text_position < len(texts):
                plot = texts[self.current_text_position].plot
                tasks = texts[self.current_text_position].tasks
                theory = texts[self.current_text_position].theory
                self.dairy.update(plot=plot, tasks=tasks, theory=theory)

    def update_stats(self, stats: dict):
        for key, value in stats.items():
            self.stats_shower.show(text=f'{key}: {f"+{value}" if value >= 0 else value}')
            if key not in self.stats.keys():
                self.stats[key] = value
            else:
                self.stats[key] += value

    def start(self):
        self.update_dairy()
        self.update_current_text()
        self.update_current_background()
        self.update_current_choices()
        start_time = time.time()
        clock = pygame.time.Clock()
        FPS = 60
        running = True
        while running:
            mouse_position = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    ended = self.next()
                    if ended:
                        self.saver.finish_chapter()
                        running = False
                        break

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.process_button_click(mouse_position=mouse_position)

            if self.choices is not None:
                self.choices.check_hover(mouse_position=mouse_position)
            self.draw()

            self.dairy.dairy_button.check_hover(*mouse_position)
            self.dairy.draw_button()
            pygame.display.flip()
            clock.tick(FPS)

            if time.time() - start_time > 5:
                start_time = time.time()
                self.saver.update(
                    current_label=self.current_position.label,
                    current_text_position=self.current_text_position,
                    stats=self.stats
                )
