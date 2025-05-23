from chapter_1_old import chapter1
from generator import ChapterGenerator, Label, Text, Choice, Background, Tasks, Plot, Theory
from generator import COLOR_BLACK, MAIN_CHARACTER

generator = ChapterGenerator()
# Подгружаем сюда текущий файл главы чтобы прописывать его дальше
generator.load(data=chapter1)

# Ну и просто через append добавляем метки
generator.labels.append(
    Label(
        label='монетная площадь',
        background=Background(image='images/5.webp'),
        texts=[
            Text(
                words='Монетная площадь',
            ),
            Text(
                words='Монетная площадь по праву считалась сердцем Кёнинсберга и находилась между северной стеной замка и замковым прудом',
            ),
            Text(
                words='Это было необычайной красоты место и казалось, что весь грязный город, который попадался до этого, совершенно с другой планеты.',
            ),
            Text(
                words='Осмотревшись, вы заметили сам гаштет и снующих между лавками девушек в передниках и подносами с пивом',
            )
        ],
        next='вход в гаштет'
    )
)
generator.labels.append(
    Label(
        label='вход в гаштет',
        background=Background(color=COLOR_BLACK),
        texts=[
            Text(
                words='Подойдя ближе вы остановились перед вывеской “Augustusburg” и уверенно зашли внутр',
                centered=True
            )
        ],
        next='входим в гаштет'
    )
)
generator.labels.append(
    Label(
        label='входим в гаштет',
        background=Background(image='images/6.webp'),
        texts=[
            Text(
                words='Внутри пахло хмелем и копченостями',
                centered=True
            ),
            Text(
                words='То и дело раздавались крики подвыпивших гостей, где-то в углу началась потасовка, которую быстро разогнал трактирщик',
                centered=True
            )
        ],
        next='к кому подойти в гаштете'
    )
)
generator.labels.append(
    Label(
        label='к кому подойти в гаштете',
        background=Background(image='images/6.webp'),
        texts=[
            Text(
                words='Вы осмотрели присутствующих и решили подойти к…',
                centered=True,
                choices=[
                    Choice(
                        caption='трактирщику',
                        label='трактирщик в гаштете'
                    ),
                    Choice(
                        caption='мужчине в углу',
                        label='мужчина в гаштете'
                    ),
                    Choice(
                        caption='интересной даме',
                        label='дама в гаштете'
                    )
                ]
            )
        ]
    )
)
generator.labels.append(
    Label(
        label='мужчина в гаштете',
        background=Background(image='images/7.webp'),
        texts=[
            Text(
                character=MAIN_CHARACTER,
                words='Здравствуйте, господин! Не знаете ли вы мистера Леонарда Эйлера?'
            ),
            Text(
                character='пьяница',
                words='Сначала угости, потом спрашивай!',
                choices=[
                    Choice(
                        caption='угостить',
                        label='угостили пьяницу пивом'
                    ),
                    Choice(
                        caption='не угощать',
                        label='не угостили пьяницу пивом'
                    )
                ]
            )
        ]
    )
)
generator.labels.append(
    Label(
        label='угостили пьяницу пивом',
        texts=[
            Text(
                words='Мужчина жадно приложился к кружке пиво и только когда осушил стакан промямлил',
                centered=True
            ),
            Text(
                character='пьяница',
                words='Не знаю такого… Ик…'
            ),
            Text(
                words='Вы сделали неверный выбор. Попробуйте снова!',
                centered=True
            )
        ],
        next='к кому подойти в гаштете'
    )
)
generator.labels.append(
    Label(
        label='не угостили пьяницу пивом',
        texts=[
            Text(
                character='пьяница',
                words='Ну и иди к черту!'
            ),
            Text(
                words='Вы сделали неверный выбор. Попробуйте снова!',
                centered=True
            )
        ],
        next='к кому подойти в гаштете'
    )
)

# Сохраняем в новый файл чтоб если косяк то не перезаписать старый
generator.save(filename='new.json')

