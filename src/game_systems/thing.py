import pygame

class Character(pygame.sprite.Sprite):
    def __init__(self,x:int,y:int,C_id:int,img:pygame.surface.Surface):
        """x,y:起始坐标 \n id:人物的编号 \n img:图像"""
        super().__init__()
        self.image = img
        self.C_id = C_id
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

class Player(Character):
    def __init__(self,x:int,y:int,img):
        """x,y:起始坐标 \n img:图像"""
        super().__init__(x,y,-1,img)
        self.speed = 5
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed
