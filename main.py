import pygame
from chapter import Chapter
from drawer import Drawer
from choices import Choices
from dairy import Dairy
from chapters.chapter_1.chapter_1 import chapter1

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

choices = Choices(
    screen=screen,
    text_area_height=100,
    font=FONT
)

dairy = Dairy(
    screen=screen,
    font=FONT
)

chapter = Chapter(
    drawer=drawer,
    choices=choices,
    dairy=dairy,
    chapter=chapter1,
    path='chapters/chapter_1'
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
    chapter.choices.check_hover(mouse_position=mouse_position)
    dairy.dairy_button.check_hover(mouse_position=mouse_position)
    chapter.show_current_state()
    pygame.display.flip()


pygame.quit()

