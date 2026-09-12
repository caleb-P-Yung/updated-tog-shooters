import random,pygame,os,sys,math
class powerup:
    def resource_path(self,path):
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.abspath("./")

        return os.path.join(base_path, path)
    def __init__(self, maxx, maxy,type,potions):
        if potions:
            self.x = random.randint(0+10, maxx-10)
            self.y = random.randint(0+10, maxy-100)
        else:
            self.x = random.randint(0+10, maxx-10)
            self.y = random.randint(0+10, maxy-290)
        self.types = types=["st","s","h","sp","bo"]
        self.type=type
    def gettype(self):
        for i in self.types:return i
    def draw(self, screen):
        if self.type == "s":
            screen.blit(pygame.transform.scale(pygame.image.load(self.resource_path("assets/Images/strengh.png")).convert_alpha(), (50, 50)), (self.x, self.y))
        if self.type == "st":
            screen.blit(pygame.transform.scale(pygame.image.load(self.resource_path("assets/Images/stun.png")).convert_alpha(), (50, 50)), (self.x, self.y))
        if self.type == "h":
            screen.blit(pygame.transform.scale(pygame.image.load(self.resource_path("assets/Images/health.png")).convert_alpha(), (50, 50)), (self.x, self.y))
        if self.type == "sp":
            screen.blit(pygame.transform.scale(pygame.image.load(self.resource_path("assets/Images/speed.png")).convert_alpha(), (50, 50)), (self.x, self.y))
        if self.type == "bo":
            screen.blit(pygame.transform.scale(pygame.image.load(self.resource_path("assets/Images/boom.png")).convert_alpha(), (50, 50)), (self.x, self.y))
    # Source - https://stackoverflow.com/a/55580166
# Posted by Rabbid76, modified by community. See post 'Timeline' for change history
# Retrieved 2026-09-12, License - CC BY-SA 4.0

    def chase(self,enemies,bosses):
        if self.type=="bo":
            pos = pygame.math.Vector2(self.x, self.y)
            enemy = min([e for e in enemies], key=lambda e: pos.distance_to(pygame.math.Vector2(e.x, e.y)))
            boss = min([e for e in bosses], key=lambda e: pos.distance_to(pygame.math.Vector2(e.x, e.y)))
                
            enemy.health -= math.floor(enemy.health/2)
            boss.health -= math.floor(boss.health/2)
