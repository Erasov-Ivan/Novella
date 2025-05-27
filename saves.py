import json


class Saver:
    def __init__(self):
        try:
            with open('save.json', 'r', encoding='utf-8-sig', errors='ignore') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}

        self.current_chapter = data.get('current_chapter', 'start')
        self.current_label = data.get('current_label', 'start')
        self.current_text_position = data.get('current_text_position', 0)
        self.stats = data.get('stats', {})

        with open('chapters/config.json', 'r', encoding='utf-8-sig', errors='ignore') as f:
            self.config = json.load(f)

    def save(self):
        with open('save.json', 'w', encoding='utf-8-sig', errors='ignore') as f:
            result = {
                'current_chapter': self.current_chapter,
                'current_label': self.current_label,
                'current_text_position': self.current_text_position,
                'stats': self.stats
            }
            f.write(json.dumps(result))

    def get_chapters_buttons(self) -> list[tuple[str, str]]:
        already_done = True
        buttons = []
        next_key = 'start'
        while next_key is not None:
            chapter = self.config.get(next_key, None)
            if chapter is None:
                break
            if next_key == self.current_chapter:
                already_done = False
                buttons.append((chapter.get('title') + ' - Продолжить', next_key))
            else:
                if already_done:
                    buttons.append((chapter.get('title') + ' - Выполнено', next_key))
                else:
                    buttons.append((chapter.get('title'), ''))
            next_key = chapter.get('next', None)
        return buttons

    def get_chapter_path(self, key: str) -> str:
        return self.config.get(key, {}).get('path')

    def finish_chapter(self):
        self.current_chapter = self.config.get(self.current_chapter, {}).get('next')

    def update(
            self,
            current_chapter: str | None = None,
            current_label: str | None = None,
            current_text_position: int | None = None,
            stats: dict | None = None
    ):
        if current_chapter is not None:
            self.current_chapter = current_chapter
        if current_label is not None:
            self.current_label = current_label
        if current_text_position is not None:
            self.current_text_position = current_text_position
        if stats is not None:
            self.stats = stats
