from generator import ChapterGenerator, Label, Text, Choice, Background, Tasks, Plot, Theory
from generator import COLOR_BLACK, MAIN_CHARACTER

generator = ChapterGenerator()
# Подгружаем сюда текущий файл главы чтобы прописывать его дальше
generator.load(filename='../chapters/chapter_1/old.json')
PERSON_FUSS = 'Фусс'

generator.labels.append(
    Label(
        label='вход в квартиру Фусса',
        background=Background(color=COLOR_BLACK),
        texts=[
            Text(
                words='Следуя всем указаниям вы добираетесь к дому мистера Николая Фусса',
                centered=True
            ),
            Text(
                words='Стук в дверь, недолгое ожидание и дверь открывает мужчина средних лет.',
                centered=True
            )
        ],
        next='разговор с фуссом'
    )
)

generator.labels.append(
    Label(
        label='разговор с фуссом',
        background=Background(
            image='images/10.webp'
        ),
        texts=[
            Text(
                words='Он стоял расслабленно, в домашнем красном халате с растянутыми карманами, чуть покосившимися круглыми очками на носу и вопросом во взгляде'
            ),
            Text(
                character=PERSON_FUSS,
                words='Что вы хотели?',
                choices=[
                    Choice(
                        caption='Я прибыл из будущего!',
                        stats={'Решительность': 1},
                        label='прибыл из будущего'
                    ),
                    Choice(
                        caption='Меня сюда направил ваш знакомый…',
                        stats={'Осторожность': 1},
                        label='направил знакомый'
                    )
                ]
            ),
        ]
    )
)

generator.labels.append(
    Label(
        label='прибыл из будущего',
        texts=[
            Text(
                character=MAIN_CHARACTER,
                words='Я прилетела сюда из будущего и ищу Леонарда Эйлера!'
            ),
            Text(
                character=MAIN_CHARACTER,
                words='Мне кажется, что с его помощью я могу вернуться домой.'
            ),
            Text(
                words='Глаза математика округлились и он погрузился в какие-то свои мысли',
                centered=True
            ),
            Text(
                words='Немного подумав, он распахнул перед нежданным гостем дверь и быстро зашептал',
                centered=True
            ),
            Text(
                character=PERSON_FUSS,
                words='Пожалуйста, потише, об этом не нужно так громко кричать.'
            ),
            Text(
                character=PERSON_FUSS,
                words='Заходите внутрь и мы познакомимся с вами поближе. Кажется, нам есть что обсудить'
            ),
            Text(
                character='Мысли',
                words='Удивительно, кто угодно бы подумал, что у меня не все дома, а этот джентльмен даже внутрь пригласил!',
                centered=True
            )
        ],
        next='квартира Фусса'
    )
)

generator.labels.append(
    Label(
        label='направил знакомый',
        texts=[
            Text(
                character=MAIN_CHARACTER,
                words='Меня сюда направил ваш знакомый по одному очень деликатному поручению!'
            ),
            Text(
                character=PERSON_FUSS,
                words='Да что вы говорите…{sleep 0.5} И что же вас направил?'
            ),
            Text(
                character=MAIN_CHARACTER,
                words='Меня направил к вам Леонард Эйлер'
            ),
            Text(
                character=PERSON_FUSS,
                words='Вы так молоды, а уже нагло врете в глаза!'
            ),
            Text(
                character=PERSON_FUSS,
                words='Лео не имеет здесь знакомых кроме своих друзей и молочника, а вот его в лицо я уж точно знаю!'
            ),
            Text(
                character=PERSON_FUSS,
                words='Сейчас же говорите правду или проваливайте с моего порога!'
            ),
            Text(
                words=' Фусс явно попытался сделать угрожающий вид. С его добрым взглядом, это получилось даже забавно',
                centered=True
            ),
            Text(
                character=MAIN_CHARACTER,
                words='Простите, мы действительно с ним не знакомы, но он то мне и нужен.'
            ),
            Text(
                character=MAIN_CHARACTER,
                words='Видите ли, я из будущего и ищу того, кто сможет мне помочь.'
            ),
            Text(
                character=PERSON_FUSS,
                words='Слабо верится, после вашего выступления!'
            ),
            Text(
                words='Не растерявшись, вы достаете прилетевший с вами смартфон из кармана и показываете его Николаю.',
                centered=True
            ),
            Text(
                character=MAIN_CHARACTER,
                words='Видите, я не вру. Это наши современные технологии.',
            ),
            Text(
                character=MAIN_CHARACTER,
                words='Тут и книга, и фотоальбом и калькулятор в одном кирпичике!'
            ),
            Text(
                words='Он повертел протянутый предмет, потыкал кнопки и шепнул.',
                centered=True
            ),
            Text(
                character=PERSON_FUSS,
                words='Заходите, я вам верю…'
            )
        ],
        next='квартира Фусса'
    )
)

generator.labels.append(
    Label(
        label='квартира Фусса',
        background=Background(
            color=COLOR_BLACK
        ),
        texts=[
            Text(
                words='Спустя несколько часов рассказов о всех предшествующих событиях, и не менее 5 чашек чая, монолог был закончен.',
                centered=True
            )
        ],
        next='разговариаем в Фуссом'
    )
)
generator.labels.append(
    Label(
        label='разговариаем в Фуссом',
        background=Background(
            image='images/11.jpg'
        ),
        texts=[
            Text(
                character=PERSON_FUSS,
                words=' Да…{sleep 0.3} Да! Кто знал…{sleep 0.3} Кто знал, что все так обернется!'
            ),
            Text(
                words='Фусс вскочил и тут же уселся обратно в кресло.'
            ),
            Text(
                character=PERSON_FUSS,
                words='Об этом точно надо подумать…'
            ),
            Text(
                character=MAIN_CHARACTER,
                words='О чем?'
            ),
            Text(
                character=PERSON_FUSS,
                words='Это сейчас не так важно…{sleep 0.3} Гораздо важнее другое!'
            ),
            Text(
                character=PERSON_FUSS,
                words='Вам обязательно нужно познакомиться с моими коллегами, они будут просто в восторге…'
            ),
            Text(
                character=PERSON_FUSS,
                words='Не просто в восторге, они будут вне себя от радости! А знаете что…'
            ),
            Text(
                words='Он вспомнил, что находится не один в комнате и посмотрел на вас.',
                centered=True
            ),
            Text(
                character=PERSON_FUSS,
                words='Вам нужно познакомиться с моими друзьями'
            ),
            Text(
                character=PERSON_FUSS,
                words='Только знаете, у нас не все так просто. Они не имеют склонности разговаривать с незнакомцами'
            ),
            Text(
                character=MAIN_CHARACTER,
                words='И что же мне делать? Почему я не могу сразу обратиться к Эйлеру?'
            ),
            Text(
                character=PERSON_FUSS,
                words='Знаете, это некий тест, который сначала нужно пройти у нас.'
            ),
            Text(
                character=PERSON_FUSS,
                words='Для начала дайте карту, я отмечу на ней, кто где живет.'
            ),
            Text(
                words='Вы протягиваете ему свернутый лист и он быстро помечает на нем несколько крестиков.',
                centered=True
            ),
            Text(
                character=PERSON_FUSS,
                words='Здесь отмечены три адреса: дом Иоганна Бернулли, Якоба Германа и Андрея Лекселя.'
            ),
            Text(
                character=PERSON_FUSS,
                words='Вам обязательно нужно заглянуть к каждому!'
            ),
            Text(
                character=PERSON_FUSS,
                words='Эйлер не любит подпускать к себе невесть кого, поэтому придумал специальный пароль.'
            ),
            Text(
                character=PERSON_FUSS,
                words='Только после его произношения, он заговорит с вами'
            ),
            Text(
                character=PERSON_FUSS,
                words='Каждый из трех задаст вам вопрос. Только дав верный ответ, вы получите часть пароля'
            ),
            Text(
                character=PERSON_FUSS,
                words='Всё понятно?',
                centered=True,
                choices=[
                    Choice(
                        caption='да',
                        words='Отлично!'
                    ),
                    Choice(
                        caption='нет',
                        title='Ваша задача разгадать загадки моих друзей.',
                        words='Разгадали - поговорите с Эйлером, в ином случае - застрянете здесь навсегда'
                    )
                ],
            ),
            Text(
                character=PERSON_FUSS,
                words='Вы получите первую часть пароля, если отгадаете мою загадку.'
            ),
            Text(
                character=PERSON_FUSS,
                words='Мельник пошел на мельницу и увидел в каждом углу по 3 кошки. Сколько ног на мельнице?',
                centered=True
            )
        ]
    )
)

# Сохраняем в новый файл чтоб если косяк то не перезаписать старый
generator.save(filename='chapter.json')

