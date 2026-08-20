import pygame
from game_systems.data import *
from misc_widgets.txtview import *


def teto_end(screen,clock,font_name):
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True

        draw_text(screen,"彩蛋结局",WIDTH/2-30,30,(255,255,255),50,font_name)
        draw_text(screen,"▽^v^▽  你直接那钻头给学校干爆了^v^",WIDTH/2-50,HEIGHT-45,(255,255,255),30,font_name)

        clock.tick(FPS)
        pygame.display.flip()
        screen.fill((0,0,0))