from generator import ChapterGenerator, Label, Text, Choice, Background, Tasks, Plot, Theory
from generator import COLOR_BLACK, MAIN_CHARACTER

generator = ChapterGenerator()
# Подгружаем сюда текущий файл главы чтобы прописывать его дальше
generator.load(filename='../chapters/chapter_1/chapter.json')


# Сохраняем в новый файл чтоб если косяк то не перезаписать старый
generator.save(filename='new.json')

