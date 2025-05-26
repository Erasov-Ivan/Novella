import pygame
from chapter import Chapter
from dairy import Dairy
from generator import Tasks

pygame.init()

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
FPS = 60

FONT = pygame.font.SysFont('Arial', 24)
screen = pygame.display.set_mode(size=(SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Курсач")
clock = pygame.time.Clock()


dairy = Dairy(
    screen=screen,
    font=FONT
)
dairy.update(
    tasks=Tasks(
        add={
            '1': 'task 1',
            '2': 'task 2',
            '3': 'very very very long task number three'
        }
    )
)

chapter = Chapter(
    screen=screen,
    font=FONT,
    path='chapters/chapter_1',
    dairy=dairy
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

    dairy.dairy_button.check_hover(*mouse_position)
    dairy.draw_button()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

