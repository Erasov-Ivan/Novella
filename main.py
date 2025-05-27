import pygame
from menu import MainMenu
import json
from chapter import Chapter
from dairy import Dairy

pygame.init()

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
FPS = 60

FONT = pygame.font.SysFont('Arial', 24)
screen = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Курсач")
clock = pygame.time.Clock()


def save(current_chapter: str, current_label: str, current_text_position: int, stats: dict):
    with open('save.json', 'w', encoding='utf-8-sig', errors='ignore') as f:
        result = {
            'current_chapter': current_chapter,
            'current_label': current_label,
            'current_text_position': current_text_position,
            'stats': stats
        }
        f.write(json.dumps(result))


try:
    with open('save.json', 'r', encoding='utf-8-sig', errors='ignore') as f:
        data = json.load(f)
except FileNotFoundError:
    data = {}

current_chapter = data.get('current_chapter', 'start')
current_label = data.get('current_label', 'start')
current_text_position = data.get('current_text_position', 0)
stats = data.get('stats', {})


with open('chapters/config.json', 'r', encoding='utf-8-sig', errors='ignore') as f:
    config = json.load(f)

already_done = True
buttons = []
next_key = 'start'
while next_key is not None:
    chapter = config.get(next_key, None)
    if chapter is None:
        break
    if next_key == current_chapter:
        already_done = False
        buttons.append((chapter.get('title') + ' - Продолжить', next_key))
    else:
        if already_done:
            buttons.append((chapter.get('title') + ' - Выполнено', next_key))
        else:
            buttons.append((chapter.get('title'), ''))
    next_key = chapter.get('next', None)


main_menu = MainMenu(
    screen=screen,
    font=FONT,
    buttons=buttons
)

chapter_key = main_menu.chose_chapter()
path = config.get(chapter_key, {}).get('path')
chapter = Chapter(
    screen=screen,
    font=FONT,
    path=f'chapters/{path}',
    dairy=Dairy(
        screen=screen,
        font=FONT
    ),
    stats=stats,
    current_label=current_label,
    current_text_position=current_text_position
)
chapter.start()
running = True
while running:
    mouse_position = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            chapter.next()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                chapter.process_button_click(mouse_position=mouse_position)

    if chapter.choices is not None:
        chapter.choices.check_hover(mouse_position=mouse_position)
    chapter.draw()

    chapter.dairy.dairy_button.check_hover(*mouse_position)
    chapter.dairy.draw_button()
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

