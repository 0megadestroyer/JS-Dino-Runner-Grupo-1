from dino_runner.utils.constants import BIRD
from.obstacle import Obstacle

class Bird(Obstacle):
    def __init__(self, image):
        self.image = BIRD[0]
        self.bird_rect = self.image.get_rect()
        self.step_index = 0
        self.type = 0
        self.fly = True
        super().__init__(image,self.type)
        self.rect.y = 250
    def fly(self):
        self.image = BIRD[0] if self.step_index < 5 else BIRD[1]
        self.bird_rect = self.image.get_rect()
        self.step_index += 1

    def draw(self, screen):
        screen.blit(self.images[self.type], (self.rect.x, self.rect.y))
