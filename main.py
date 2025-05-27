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

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
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
            saver=saver,
            stats=saver.stats,
            current_label=saver.current_label,
            current_text_position=saver.current_text_position
        )
        chapter.start()
        saver.save()
        buttons = saver.get_chapters_buttons()
        main_menu.update_buttons(buttons=buttons)

pygame.quit()

