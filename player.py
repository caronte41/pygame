from circleshape import CircleShape
from shot import Shot
import pygame
import random
from constants import *

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.speed = 0  # Current speed (can be positive or negative)
        self.shot_timer = 0
        
    def triangle(self):
        forward = pygame.Vector2(0, -1).rotate(-self.rotation)  # Up is forward
        right = pygame.Vector2(1, 0).rotate(-self.rotation) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
        
    def draw(self, screen):
        pygame.draw.polygon(screen, (255, 255, 255), self.triangle(), 2)
    def shoot(self):
        if self.shot_timer > 0:
            return
        forward = pygame.Vector2(0, -1).rotate(-self.rotation)
        shot_position = self.position + forward * self.radius
        shot = Shot(shot_position.x, shot_position.y, self.radius)
        shot.velocity = forward * PLAYER_SHOOT_SPEED
        self.shot_timer = PLAYER_SHOOT_COOLDOWN

        
    def update(self, dt):
        self.shot_timer -= dt
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            self.shoot()
        
        # Rotation - A turns left, D turns dright
        if keys[pygame.K_a]:
            self.rotation += PLAYER_TURN_SPEED * dt  # Subtract for counterclockwise
        if keys[pygame.K_d]:
            self.rotation -= PLAYER_TURN_SPEED * dt  # Add for clockwise
        
        # Acceleration - W accelerates forward, S brakes/reverses
        if keys[pygame.K_w]:
            self.speed += PLAYER_ACCELERATION * dt
            if self.speed > PLAYER_MAX_SPEED:
                self.speed = PLAYER_MAX_SPEED
        elif keys[pygame.K_s]:
            self.speed -= PLAYER_ACCELERATION * dt
            if self.speed < -PLAYER_MAX_REVERSE_SPEED:  # Limit reverse speed
                self.speed = -PLAYER_MAX_REVERSE_SPEED
        else:
            # Deceleration when no keys are pressed
            if self.speed > 0:
                self.speed -= PLAYER_DECELERATION * dt
                if self.speed < 0:
                    self.speed = 0
            elif self.speed < 0:
                self.speed += PLAYER_DECELERATION * dt
                if self.speed > 0:
                    self.speed = 0
        
        # Movement based on current direction and speed
        if self.speed != 0:
            # Up is forward in pygame coordinates (-y)
            forward = pygame.Vector2(0, -1).rotate(-self.rotation)
            self.position += forward * self.speed * dt