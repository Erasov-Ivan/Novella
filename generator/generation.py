from generator import ChapterGenerator, Label, Text, Choice, Background, Tasks, Plot, Theory, Question
from generator import COLOR_BLACK, MAIN_CHARACTER

generator = ChapterGenerator()
# Подгружаем сюда текущий файл главы чтобы прописывать его дальше
#generator.load(filename='../chapters/chapter_1/old.json')
PERSON_FUSS = 'Фусс'

generator.labels['test'] = Label(
    texts=[
        Text(
            words='Вы получите первую часть пароля, если отгадаете мою загадку.',
            character=PERSON_FUSS,
            centered=True,
            question=Question(
                question='Мельник пошел на мельницу и увидел в каждом углу по 3 кошки. Сколько ног на мельнице?',
                answer='50',
                right_label='',
                wrong_label=''
            )
        )
    ]
)

# Сохраняем в новый файл чтоб если косяк то не перезаписать старый
generator.save(filename='chapter.json')

