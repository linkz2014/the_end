import pygame
#import pathlib
#pahts = pathlib.Path(__file__).parent/"_internal"

WIDTH,HEIGHT = 1000,500
FPS = 60

#文件名
font_name = "fot\\JhenaHei.ttf"
player_save_name = "save\\player_info.endio"
copy_save_name = "save\\copy.endio"
revoke_delete_name = "save\\revoke_delete.endio"
people_img = pygame.transform.scale(pygame.image.load("pic\\人占位符.png"),(215,300))
class_paper_img = pygame.transform.scale(pygame.image.load("pic\\items\\class_paper.png"),(300,300))
#关于存档
def write_data(content:str):
    with open(player_save_name,"a",encoding="utf-8") as file:
        file.write(content)

def get_data_len():
    with open(player_save_name,"r",encoding="utf-8") as f:
        return len(f.read())

def delete_all_data():
    with open(player_save_name,"r",encoding="utf-8") as f:
        delete__data = f.read()
    with open(revoke_delete_name,"w",encoding="utf-8") as f:
        f.write(delete__data)
    open(player_save_name,"w",encoding="utf-8").close()

def copy_data():
    with open(player_save_name,"r",encoding="utf-8") as f:
        player_data = f.read()
    with open(copy_save_name,"w",encoding="utf-8") as f:
        f.write(player_data)

def rstore_data():
    try:
        with open(copy_save_name,"r",encoding="utf-8") as f:
            copy_player_data = f.read()
        with open(player_save_name,"w",encoding="utf-8") as f:
            f.write(copy_player_data)
    except FileNotFoundError:
        print("文件不存在")

def revoke_delete():
    with open(revoke_delete_name,"r",encoding="utf-8") as f:
        revoke_data = f.read()
    with open(player_save_name,"w",encoding="utf-8") as f:
        f.write(revoke_data)