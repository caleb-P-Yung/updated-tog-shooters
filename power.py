import random
import pygame
class powerup:
    def __init__(self, maxx, maxy,type):
        self.x = random.randint(0+10, maxx-10)
        self.y = random.randint(0+10, maxy-100)
        self.types = types=["st","s"]
        self.type=type
    def gettype(self):
        for i in self.types:return i
    def draw(self, screen):
        if self.type == "s":
            screen.blit(pygame.transform.scale(pygame.image.load("assets/Images/strengh.png").convert_alpha(), (50, 50)), (self.x, self.y))
        if self.type == "st":
            screen.blit(pygame.transform.scale(pygame.image.load("assets/Images/stun.png").convert_alpha(), (50, 50)), (self.x, self.y))
        if self.type == "h":
            screen.blit(pygame.transform.scale(pygame.image.load("assets/Images/health.png").convert_alpha(), (50, 50)), (self.x, self.y))