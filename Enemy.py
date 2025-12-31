# Enemy.py
import os,sys,pygame
def resource_path(path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".//")

    return os.path.join(base_path, path)

class Enemy:
    def __init__(self, x, y, speed=0.6, health=100):
        self.x = x
        self.y = y
        self.speed = speed
        self.health = health
        self.image = pygame.transform.scale(
            pygame.image.load(resource_path("assets/Images/Ememy.png")).convert_alpha(),
            (100, 100)
        )

    def move_toward(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        dist = (dx*dx + dy*dy) ** 0.5
        if dist != 0:
            self.x += self.speed * dx / dist
            self.y += self.speed * dy / dist

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
