import pygame
from chapter import Chapter
from drawer import Drawer
import time

pygame.init()

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900

FONT = pygame.font.SysFont('Arial', 24)
screen = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Курсач")

drawer = Drawer(
    screen=screen,
    text_area_height=100,
    font=FONT,
)

chapter1 = {
    'start': {
        'texts': [
            {
                'words': 'Придя в себя после головокружительного путешествия, вы оглядываетесь по сторонам',
                'centered': True
            }
        ],
        'background': {
            'color': 'black'
        },
        'next': 1
    },
    1: {
        'texts': [
            {'words': 'Узкие улочки и дома, сверху донизу выложенные камни, журчащие по тем же улицам ручейки сточных труб'},
            {'words': 'По дороге не спеша идут знатные дамы, одеты в роскошные платья 18 века и их кавалеры'},
            {'words': 'Мимо проезжают кареты, запряженные лошадьми'},
            {'words': 'По теневой стороны улице мимо снуют обычные горожане, которые явно торопятся по поручениям своих господ'},
            {
                'character': 'Мысли',
                'words': 'Какая очевидная разница… Прислуга и знать. Идут по одной дороге, но живут совершенно разными жизнями.',
                'centered': True
            },
        ],
        'background': {
            'image': '1.webp'
        }
    }
}

chapter = Chapter(
    drawer=drawer,
    chapter=chapter1,
    path='images'
)


chapter.show_current_position()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            chapter.next()

pygame.quit()

