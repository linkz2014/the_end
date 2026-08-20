import pygame
import random

# 全局画布宽高由外部传入，不写死在模块内
def draw_crt_lines(surface, screen_width, screen_height, line_gap=4, alpha=40):
    """绘制CRT显示器扫描线遮罩"""
    overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    for y in range(0, screen_height, line_gap):
        pygame.draw.line(overlay, (0, 0, 0, alpha), (0, y), (screen_width, y))
    surface.blit(overlay, (0, 0))


def add_horizontal_glitch(src_surface, screen_width, screen_height, glitch_strength=0.3):
    """添加横向花屏故障特效"""
    buf_surf = src_surface.copy()
    bar_height_range = (15, 90)
    bar_count = int(glitch_strength * 12)
    for _ in range(bar_count):
        h = random.randint(*bar_height_range)
        y = random.randint(0, screen_height - h)
        offset_x = random.randint(-60, 60) if random.random() < 0.4 else 0
        # 黑色故障横条
        pygame.draw.rect(buf_surf, (0, 0, 0), (0, y, screen_width, h))
        if offset_x != 0:
            strip = src_surface.subsurface((0, y, screen_width, h))
            buf_surf.blit(strip, (offset_x, y))
    return buf_surf
