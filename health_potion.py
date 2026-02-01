import random,os,sys,pygame

class HealthPotion:
    def __init__(self,x,y):
        self.x=random.randrange(100, x-100)
        self.y=random.randrange(100, y-100)
        self.image = pygame.transform.scale(
            pygame.image.load("assets/Images/health.png").convert_alpha(),
            (100, 100)
        )
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
