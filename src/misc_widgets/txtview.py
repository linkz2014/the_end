import pygame

class DialogBox:
    def __init__(self, screen, font, dialog_list,
                 draw_box=True, box_rect=(40, 220, 720, 140),
                 text_offset_x=60, text_offset_y=240, line_height=36,
                 type_speed=0.06, text_color=(255,255,255),
                 box_color=(0,0,0)):
        """
        :param screen: pygame主画布
        :param font: pygame字体对象
        :param dialog_list: 对话列表 [文本1,文本2...]
        :param draw_box: 是否绘制对话框 True/False
        :param box_rect: 对话框矩形 (x,y,w,h)
        :param text_offset_x: 文字距离框左侧偏移
        :param text_offset_y: 第一行文字y坐标
        :param line_height: 行间距
        :param type_speed: 打字速度(秒)
        :param text_color: 文字颜色
        :param box_color: 对话框颜色（黑色）
        """
        self.screen = screen
        self.font = font
        self.dialog_list = dialog_list
        self.draw_box = draw_box
        self.text_offset_x = text_offset_x
        self.text_offset_y = text_offset_y
        self.line_height = line_height
        self.type_speed = type_speed
        self.text_color = text_color
        
        self.box_rect = box_rect
        self.box_color = box_color

        # 运行状态变量
        self.dialog_index = 0
        self.full_text = self.dialog_list[self.dialog_index]
        self.display_text = ""
        self.char_index = 0
        self.timer = 0.0
        self.is_finish = False

    def reset(self):
        """重置对话从头开始"""
        self.dialog_index = 0
        self._load_current_text()

    def _load_current_text(self):
        self.full_text = self.dialog_list[self.dialog_index]
        self.display_text = ""
        self.char_index = 0
        self.timer = 0.0
        self.is_finish = False

    def handle_event(self, event):
        """传入事件，处理回车交互
        返回 True = 所有对话播放完毕
        """
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            if not self.is_finish:
                # 打字中：立刻显示全部文字
                self.display_text = self.full_text
                self.char_index = len(self.full_text)
                self.is_finish = True
            else:
                # 切换下一段对话
                if self.dialog_index + 1 < len(self.dialog_list):
                    self.dialog_index += 1
                    self._load_current_text()
                else:
                    # 全部对话结束
                    return True
        return False

    def update(self, dt):
        """dt: 帧间隔时间(秒)，更新打字动画"""
        if not self.is_finish:
            self.timer += dt
            if self.timer >= self.type_speed and self.char_index < len(self.full_text):
                self.display_text += self.full_text[self.char_index]
                self.char_index += 1
                self.timer = 0
            if self.char_index >= len(self.full_text):
                self.is_finish = True

    def draw(self):
        """绘制对话框与文字"""
        # 绘制黑色矩形对话框
        if self.draw_box:
            x, y, w, h = self.box_rect
            pygame.draw.rect(self.screen, self.box_color, (x, y, w, h))

        # 绘制多行文字
        lines = self.display_text.split("\n")
        y_pos = self.text_offset_y
        for line in lines:
            surf = self.font.render(line, True, self.text_color)
            self.screen.blit(surf, (self.text_offset_x, y_pos))
            y_pos += self.line_height

def load_font(font_file: str, size: int):
    """
    加载自定义ttf字体
    :param font_file: 字体文件路径
    :param size: 字体大小
    """
    return pygame.font.Font(font_file, size)

def draw_text(screen,text,x,y,color,size,font_name,bold=False):
    font = load_font(font_name,size)
    font.set_bold(bold)
    texts = font.render(text,True,color)
    text_rect = texts.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    screen.blit(texts,text_rect)

def draw_cmd_text(screen,text,x,y,color,size,font_name,bold=False):
    font = load_font(font_name,size)
    font.set_bold(bold)
    texts = font.render(text,True,color)
    text_rect = texts.get_rect()
    text_rect.left = x
    text_rect.top = y
    screen.blit(texts,text_rect)