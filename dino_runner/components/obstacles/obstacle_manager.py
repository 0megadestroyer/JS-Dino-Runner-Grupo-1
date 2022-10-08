from random import randint
import random
import pygame
from dino_runner.components.obstacles.bird import Bird
from dino_runner.utils.constants import BIRD, LARGE_CACTUS, SMALL_CACTUS
from .cactus import SmallCactus, LargeCactus


class ObstacleManager:
    def __init__(self):
        self.obstacles = []

    def update(self, game_speed, player, on_death):
        obstacle_random = random.randint(0,2)
        if len(self.obstacles) == 0:
            if obstacle_random == 0:
                self.obstacles.append(SmallCactus(SMALL_CACTUS))
            elif obstacle_random == 1:
                self.obstacles.append(LargeCactus(LARGE_CACTUS))
            else:
                self.obstacles.append(Bird(BIRD))

        for obstacle in self.obstacles:
            obstacle.update(game_speed, self.obstacles)
            if player.dino_rect.colliderect(obstacle.rect):
                if on_death():
                    self.obstacles.remove(obstacle)
                else:
                    break

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)

    def reset_obstacles(self):
        self.obstacles = []
