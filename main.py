import pygame
from chapter import Chapter
from drawer import Drawer
from chapter_1.chapter_1 import chapter1

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


chapter = Chapter(
    drawer=drawer,
    chapter=chapter1,
    path='chapter_1'
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

