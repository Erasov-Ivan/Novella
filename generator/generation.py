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
                right_label='fuss_right_answer',
                wrong_label='fuss_wrong_answer'
            )
        )
    ]
)
generator.labels['fuss_right_answer'] = Label(
    texts=[
        Text(
            character=PERSON_FUSS,
            words='Отлично! Я так и знал что вы отгадаете.'
        ),
        Text(
            character=PERSON_FUSS,
            words='Первая часть пароля: “Именно математика дает…”'
        )
    ]
)

generator.labels['fuss_wrong_answer'] = Label(
    texts=[
        Text(
            character=PERSON_FUSS,
            words='Хмм.. Так и быть, я дам вам первую часть пароля'
        ),
        Text(
            character=PERSON_FUSS,
            words='Но учтите, это только потому что я очень хочу помочь вам'
        ),
        Text(
            character=PERSON_FUSS,
            words='Запоминайте: “Именно математика дает…”'
        )
    ]
)

# Сохраняем в новый файл чтоб если косяк то не перезаписать старый
generator.save(filename='chapter.json')

