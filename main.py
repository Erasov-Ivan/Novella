import pygame
from menu import MainMenu
from saves import Saver
from chapter import Chapter
from dairy import Dairy
import time

pygame.init()

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
FPS = 60

FONT = pygame.font.SysFont('Arial', 24)
screen = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Курсач")
clock = pygame.time.Clock()

saver = Saver()
buttons = saver.get_chapters_buttons()

main_menu = MainMenu(
    screen=screen,
    font=FONT,
    buttons=buttons
)

chapter_key = main_menu.chose_chapter()
if chapter_key is None:
    exit()
path = saver.get_chapter_path(key=chapter_key)
chapter = Chapter(
    screen=screen,
    font=FONT,
    path=f'chapters/{path}',
    dairy=Dairy(
        screen=screen,
        font=FONT
    ),
    stats=saver.stats,
    current_label=saver.current_label,
    current_text_position=saver.current_text_position
)
start_time = time.time()
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

    if time.time() - start_time > 5:
        start_time = time.time()
        saver.update(
            current_label=chapter.current_position.label,
            current_text_position=chapter.current_text_position,
            stats=chapter.stats
        )
saver.save()
pygame.quit()

