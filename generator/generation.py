from generator import ChapterGenerator, Label, Text, Choice, Background, Tasks, Plot, Theory, Question
from generator import COLOR_BLACK, MAIN_CHARACTER

generator = ChapterGenerator()
# Подгружаем сюда текущий файл главы чтобы прописывать его дальше
generator.load(filename='../chapters/chapter_1/old.json')
PERSON_FUSS = 'Фусс'

generator.labels['прощаемся с Фуссом'] = Label(
    texts=[
        Text(
            character=PERSON_FUSS,
            words='Теперь отправляйтесь дальше. На сегодня мы с вами попрощаемся'
        ),
        Text(
            character=MAIN_CHARACTER,
            words=' Спасибо вам'
        )
    ],
    next='К кому пойти'
)
generator.labels['К кому пойти'] = Label(
    background=Background(
        color='black'
    ),
    texts=[
        Text(
            words='Теперь пришло время выбирать. Я пойду к…',
            choices=[
                Choice(
                    caption='Иоганну Бернулли',
                    label='пойти к бернулли'
                ),
                Choice(
                    caption='Якобу Герману',
                    label='пойти к герману'
                ),
                Choice(
                    caption='Андрею Лекселю',
                    label='пойти к лекселю'
                )
            ]
        )
    ],
    next='идём к эйлеру'
)

generator.labels['пойти к бернулли'] = Label(
    background=Background(
        image='images/12.webp'
    ),
    texts=[
        Text(
            words='Карта привела нас на границу города, где уже закончились многоэтажные здания.',
            centered=True
        ),
        Text(
            words='Теперь друг друга сменяли похожие домики с разноцветными крышами.',
            centered=True
        ),
        Text(
            words='Подойдя к чуть накренившимся забору, вы позвонили в колокольчик около калитки',
            centered=True
        ),
        Text(
            words='Мелодичный звон, казалось, разлетелся на всю округу.',
            centered=True
        )
    ],
    next='встреча с бернулли'
)

generator.save(filename='chapter.json')
