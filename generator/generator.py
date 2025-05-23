import json

MAIN_CHARACTER = 'ГГ'
WORDS = 'words'
TEXTS = 'texts'
BACKGROUND = 'background'
NEXT = 'next'
CHARACTER = 'character'
CENTERED = 'centered'
TITLE = 'title'
DELAY = 'delay'
CHOICES = 'choices'
CAPTION = 'caption'
LABEL = 'label'
REPEAT = 'repeat'
STATS = 'stats'
COLOR = 'color'
IMAGE = 'image'
CHAPTER = 'chapter'
ADD = 'add'
REMOVE = 'remove'
TASKS = 'tasks'
PLOT = 'plot'
THEORY = 'theory'

COLOR_BLACK = 'black'


class Tasks:
    def __init__(
            self,
            add: dict | None = None,
            remove: list[str] | None = None
    ):
        self.add = add
        self.remove = remove

    def __dict__(self):
        return {
            ADD: self.add,
            REMOVE: self.remove
        }


class Plot:
    def __init__(
            self,
            chapter: str,
            add: list[str]
    ):
        self.chapter = chapter
        self.add = add

    def __dict__(self):
        return {
            CHAPTER: self.chapter,
            ADD: self.add
        }


class Theory:
    def __init__(
            self,
            smth: str | None = None
    ):
        self.smth = smth

    def __dict__(self):
        return {}


class Choice:
    def __init__(
            self,
            caption: str,
            character: str | None = None,
            title: str | None = None,
            label: str | None = None,
            words: str | None = None,
            repeat: bool | None = None,
            stats: dict | None = None,
            tasks: Tasks | None = None,
            plot: Plot | None = None,
            theory: Theory | None = None
    ):
        self.caption = caption
        self.character = character
        self.title = title
        self.label = label
        self.words = words
        self.repeat = repeat
        self.stats = stats
        self.tasks = tasks
        self.plot = plot
        self.theory = theory

    def __dict__(self):
        if self.label is not None and self.words is not None:
            raise ValueError(f'Choice "{self.caption}" has label and words')
        result = {}
        if self.caption is not None: result[CAPTION] = self.caption
        if self.character is not None: result[CHARACTER] = self.character
        if self.title is not None: result[TITLE] = self.title
        if self.label is not None: result[LABEL] = self.label
        if self.words is not None: result[WORDS] = self.words
        if self.repeat is not None: result[REPEAT] = self.repeat
        if self.stats is not None: result[STATS] = self.stats
        if self.tasks is not None: result[TASKS] = self.tasks.__dict__()
        if self.plot is not None: result[PLOT] = self.plot.__dict__()
        if self.theory is not None: result[THEORY] = self.theory.__dict__()
        return result


class Text:
    def __init__(
            self,
            words: str,
            character: str | None = None,
            title: str | None = None,
            centered: bool | None = None,
            delay: float | None = None,
            choices: list[Choice] | None = None,
            tasks: Tasks | None = None,
            plot: Plot | None = None,
            theory: Theory | None = None
    ):
        self.words = words
        self.character = character
        self.title = title
        self.centered = centered
        self.delay = delay
        self.choices = choices
        self.tasks = tasks
        self.plot = plot
        self.theory = theory

    def __dict__(self):
        result = {WORDS: self.words}
        if self.character is not None: result[CHARACTER] = self.character
        if self.title is not None: result[TITLE] = self.title
        if self.centered is not None: result[CENTERED] = self.centered
        if self.delay is not None: result[DELAY] = self.delay
        if self.choices is not None: result[CHOICES] = list(map(lambda choice: choice.__dict__(), self.choices))
        if self.tasks is not None: result[TASKS] = self.tasks.__dict__()
        if self.plot is not None: result[PLOT] = self.plot.__dict__()
        if self.theory is not None: result[THEORY] = self.theory.__dict__()
        return result


class Background:
    def __init__(
            self,
            image: str | None = None,
            color: str | None = None
    ):
        self.image = image
        self.color = color

    def __dict__(self):
        if self.color is not None and self.image is not None:
            raise ValueError('Background can only be one from: image, color')
        result = {}
        if self.image is not None: result[IMAGE] = self.image
        if self.color is not None: result[COLOR] = self.color
        return result


class Label:
    def __init__(
            self,
            label: str,
            texts: list[Text],
            next: str | None = None,
            background: Background | None = None
    ):
        self.label = label
        self.texts = texts
        self.next = next
        self.background = background

    def __dict__(self):
        result = {}
        if self.background is not None:
            result[BACKGROUND] = self.background.__dict__()
        result[TEXTS] = list(map(lambda text: text.__dict__(), self.texts))

        if self.next is not None:
            result[NEXT] = self.next
        return result


class ChapterGenerator:
    def __init__(self):
        self.labels: list[Label] = []

    def save(self, filename: str) -> None:
        result = {}
        for label in self.labels:
            result[label.label] = label.__dict__()
        with open(filename, 'w', encoding='utf-8-sig') as f:
            f.write(json.dumps(result, ensure_ascii=False))

    def load(self, filename: str | None = None, data: dict | None = None) -> None:
        if filename is None and data is None:
            raise ValueError('Nothing provided')
        if filename is not None:
            with open(filename, 'r', encoding='utf-8-sig', errors='ignore') as f:
                data = json.load(f)

        for label, label_value in data.items():
            next_label = label_value.get(NEXT, None)
            background_raw = label_value.get(BACKGROUND, None)
            if background_raw is not None:
                background = Background(
                    image=background_raw.get(IMAGE, None),
                    color=background_raw.get(COLOR, None)
                )
            else:
                background = None
            texts_raw: list[dict] = label_value.get(TEXTS, [])
            texts = []
            for t in texts_raw:
                choices_raw = t.get(CHOICES, [])
                if len(choices_raw) == 0:
                    choices = None
                else:
                    choices = []
                    for choice in choices_raw:
                        if (tasks_raw := choice.get(TASKS, None)) is not None:
                            tasks = Tasks(
                                add=tasks_raw.get(ADD, None),
                                remove=tasks_raw.get(REMOVE, None)
                            )
                        else:
                            tasks = None
                        if (plot_raw := choice.get(PLOT, None)) is not None:
                            plot = Plot(
                                chapter=plot_raw.get(CHAPTER, None),
                                add=plot_raw.get(ADD, [])
                            )
                        else:
                            plot = None
                        if (theory := choice.get(THEORY, None)) is not None:
                            theory = Theory()
                        else:
                            theory = None
                        choices.append(
                            Choice(
                                caption=choice.get(CAPTION),
                                character=choice.get(CHARACTER, None),
                                title=choice.get(TITLE, None),
                                label=choice.get(LABEL, None),
                                words=choice.get(WORDS, None),
                                repeat=choice.get(REPEAT, None),
                                stats=choice.get(STATS, None),
                                tasks=tasks,
                                plot=plot,
                                theory=theory
                            )
                        )

                if (tasks_raw := t.get(TASKS, None)) is not None:
                    tasks = Tasks(
                        add=tasks_raw.get(ADD, None),
                        remove=tasks_raw.get(REMOVE, None)
                    )
                else:
                    tasks = None
                if (plot_raw := t.get(PLOT, None)) is not None:
                    plot = Plot(
                        chapter=plot_raw.get(CHAPTER, None),
                        add=plot_raw.get(ADD, [])
                    )
                else:
                    plot = None
                if (theory_raw := t.get(THEORY, None)) is not None:
                    theory = Theory()
                else:
                    theory = None
                text = Text(
                    words=t.get(WORDS),
                    character=t.get(CHARACTER, None),
                    title=t.get(TITLE, None),
                    centered=t.get(CENTERED, None),
                    delay=t.get(DELAY, None),
                    choices=choices,
                    tasks=tasks,
                    plot=plot,
                    theory=theory
                )
                texts.append(text)
            self.labels.append(
                Label(
                    label=label,
                    background=background,
                    texts=texts,
                    next=next_label
                )
            )
