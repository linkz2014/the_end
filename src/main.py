import pygame
from game_systems.data import *
from game_systems.start_ui import *
from game_systems.thing import *
from game_systems.end_ui import *

pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("结局")

#设置项
game_settings = {import pygame
from game_systems.data import *
from game_systems.start_ui import *
from game_systems.thing import *
from game_systems.end_ui import *

pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("结局")

#设置项
game_settings = {
    "volume": 0.6
}

running = True
show = {
    "loading":True,
    "choice_role":True,
    "start_plot":True
}
start = draw_start_screen(screen,font_name,clock,game_settings)
if start:
    running = False
    show = {key:False for key in show}

if get_data_len() != 0:
    show = {key:False for key in show}
    
if show["loading"]:
    loading = draw_loading_screen(screen,clock,font_name)
    if loading:
        running = False
        show = {key:False for key in show}

if show["choice_role"]:
    choice = draw_choice_screen(screen,clock,font_name,player_save_name)
    if type(choice) == str:
        running = False
        show = {key:False for key in show}
        if "developer" in choice:
            developer_end(screen,clock,font_name)

    if choice:
        running = False
        show = {key:False for key in show}

if show["start_plot"]:
    start_plot = draw_start_plot_screen(screen,clock,font_name)
    if start_plot:
        running = False

all_sprites = pygame.sprite.Group()
player = Player(50,50,pygame.Surface((50,50)))
all_sprites.add(player)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
    
    clock.tick(FPS)
    pygame.display.flip()
    screen.fill((255,0,0))
    player.move()
    all_sprites.draw(screen)
    
pygame.quit()
    "volume": 0.6
}

running = True
show = {
    "loading":True,
    "choice_role":True,
    "start_plot":True
}
start = draw_start_screen(screen,font_name,clock,game_settings)
if start:
    running = False
    show = {key:False for key in show}

if get_data_len() != 0:
    show = {key:False for key in show}
    
if show["loading"]:
    loading = draw_loading_screen(screen,clock,font_name)
    if loading:
        running = False
        show = {key:False for key in show}

if show["choice_role"]:
    choice = draw_choice_screen(screen,clock,font_name,player_save_name)
    if type(choice) == str:
        running = False
        show = {key:False for key in show}
        if "teto" in choice:
            teto_end(screen,clock,font_name)

    if choice:
        running = False
        show = {key:False for key in show}

if show["start_plot"]:
    start_plot = draw_start_plot_screen(screen,clock,font_name)
    if start_plot:
        running = False

all_sprites = pygame.sprite.Group()
player = Player(50,50,pygame.Surface((50,50)))
all_sprites.add(player)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
    
    clock.tick(FPS)
    pygame.display.flip()
    screen.fill((255,0,0))
    player.move()
    all_sprites.draw(screen)
    
pygame.quit()
