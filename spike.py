import random,os,sys,pygame

class Spikes:
    def resource_path(self,path):
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.abspath("./")

        return os.path.join(base_path, path)
    def __init__(self,x,y):
        self.x=random.randrange(100, x-100)
        self.y=random.randrange(100, y-100)
        self.image = pygame.transform.scale(
            pygame.image.load(self.resource_path("assets/Images/spike.png")).convert_alpha(),
            (100, 100)
        )
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
