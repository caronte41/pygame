import pygame
import random
from circleshape import CircleShape
from constants import *

score = 0

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt
    def split(self):
        global score
        score += 1
        print(f"split{score}")
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return []
        random_angle = random.uniform(20,50)   
        v1 = self.velocity.rotate(random_angle)
        v2 = self.velocity.rotate(-random_angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        ast1 = Asteroid(self.position.x, self.position.y, new_radius)
        ast2 = Asteroid(self.position.x, self.position.y, new_radius)
        ast1.velocity = v1 * 1.2
        ast2.velocity = v2 * 1.2

        return [ast1, ast2] 


