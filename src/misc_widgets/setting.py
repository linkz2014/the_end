import pygame
import sys
from game_systems.data import delete_all_data,copy_data,rstore_data,revoke_delete
import os

# 全局配色，外部可直接覆盖修改
COLORS = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "gray": (225, 225, 225),
    "light_gray": (250, 250, 250),
    "dark_gray": (160, 160, 160),   # 新增：按下时暗色
    "blue": (50, 150, 255),
    "red": (220, 60, 60),
    "bg": (0, 0, 0)
}

# 滑块组件
class Slider:
    def __init__(self, x, y, w, h, min_val, max_val, start_val, track_color=None, fill_color=None, knob_color=None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.min_val = min_val
        self.max_val = max_val
        self.value = start_val
        self.dragging = False
        self.track_color = track_color or COLORS["gray"]
        self.fill_color = fill_color or COLORS["blue"]
        self.knob_color = knob_color or COLORS["white"]
        self.circle_x = self.x + (self.value - self.min_val)/(self.max_val-self.min_val)*self.w

    def draw(self, surf):
        pygame.draw.rect(surf, self.track_color, (self.x, self.y, self.w, self.h))
        pygame.draw.rect(surf, self.fill_color, (self.x, self.y, self.circle_x - self.x, self.h))
        pygame.draw.circle(surf, self.knob_color, (int(self.circle_x), self.y+self.h//2), 10)

    def update(self, mouse_pos, mouse_down):
        mx, my = mouse_pos
        if mouse_down:
            if self.x <= mx <= self.x+self.w and self.y-15 <= my <= self.y+self.h+15:
                self.dragging = True
        else:
            self.dragging = False
        if self.dragging:
            self.circle_x = max(self.x, min(mx, self.x+self.w))
            ratio = (self.circle_x - self.x) / self.w
            self.value = self.min_val + ratio*(self.max_val - self.min_val)

# 按钮组件【修改此处：增加pressed状态，点击时变暗】
class Button:
    def __init__(self, x, y, w, h, text, font, radius=6):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = font
        self.radius = radius
        self.hover = False
        self.pressed = False   # 新增按下状态

    def draw(self, surf):
        if self.pressed:
            base_color = COLORS["dark_gray"]
        elif self.hover:
            base_color = COLORS["light_gray"]
        else:
            base_color = COLORS["gray"]
        pygame.draw.rect(surf, base_color, self.rect, border_radius=self.radius)
        pygame.draw.rect(surf, COLORS["black"], self.rect, 2, border_radius=self.radius)
        txt_surf = self.font.render(self.text, True, COLORS["black"])
        surf.blit(txt_surf, txt_surf.get_rect(center=self.rect.center))

    def check_hover(self, mouse_pos):
        self.hover = self.rect.collidepoint(mouse_pos)

    def is_click(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
    
    # 新增：更新按下状态，传入鼠标位置+鼠标左键是否按下
    def update_pressed(self, mouse_pos, mouse_left_down):
        if self.hover and mouse_left_down:
            self.pressed = True
        else:
            self.pressed = False

# 设置页面管理类，所有配置可外部传入自定义
class SettingScreen:
    def __init__(self, screen, clock, font, small_font, font_path, settings):
        self.screen = screen
        self.clock = clock
        self.font = font
        self.small_font = small_font
        self.font_path = font_path
        self.settings = settings
        self.running = True
        self._build_widgets()

    def _build_widgets(self):
        # 仅保留音量滑块、返回按钮
        self.volume_slider = Slider(300, 120, 350, 8, 0, 1, self.settings["volume"])
        self.buttons = {
            "delete":Button(200, 210, 200, 50, "删除存档", self.font),
            "revoke_delete":Button(400, 210, 200, 50, "撤销删除", self.font),
            "btn_back":Button(300, 350, 200, 50, "返回游戏", self.font),
            "copy":Button(200, 280, 200, 50, "备份存档", self.font),
            "rstore":Button(400, 280, 200, 50, "恢复备份", self.font)
        }

    def run(self):
        screen_width, screen_height = self.screen.get_size()
        while self.running:
            mouse_pos = pygame.mouse.get_pos()
            mouse_down = pygame.mouse.get_pressed()[0]
            self.screen.fill(COLORS["bg"])

            # 标题
            title = self.font.render("设置", True, COLORS["white"])
            self.screen.blit(title, title.get_rect(center=(screen_width//2, 50)))

            # 音量调节
            vol_text = self.font.render(f"音量：{int(self.settings['volume']*100)}%", True, COLORS["white"])
            self.screen.blit(vol_text, (100, 110))
            self.volume_slider.update(mouse_pos, mouse_down)
            self.volume_slider.draw(self.screen)
            self.settings["volume"] = self.volume_slider.value

            # 返回按钮
            for key in self.buttons:
                btn = self.buttons[key]
                btn.check_hover(mouse_pos)
                btn.update_pressed(mouse_pos, mouse_down) # 新增这一行更新按下状态
                btn.draw(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.buttons["btn_back"].is_click(mouse_pos):
                        self.running = False
                    elif self.buttons["delete"].is_click(mouse_pos):
                        delete_all_data()
                    elif self.buttons["copy"].is_click(mouse_pos):
                        copy_data()
                    elif self.buttons["rstore"].is_click(mouse_pos):
                        rstore_data()
                    elif self.buttons["revoke_delete"].is_click(mouse_pos):
                        revoke_delete()

            pygame.display.flip()
            self.clock.tick(60)
        return self.settings
