import pygame
from constants import *
from player import Player
from asteroid import *

from shot import Shot
from astreoidfield import AsteroidField



def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)

    asteroid_field = AsteroidField()

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    dt = 0

    def draw_score(screen):
        font = pygame.font.SysFont('Arial', 30)
       
        score_text = font.render(f'Score: {score}', True, (255, 255, 255))
        screen.blit(score_text, (20, 20))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        updatable.update(dt)
        for asteroid in asteroids:
            for shot in shots:
                hit = asteroid.collisions(shot)
                if hit:
                    shot.kill()
                    new_asteroids = asteroid.split()
                    asteroids.add(*new_asteroids) 

             
            t = asteroid.collisions(player)
            if t:
                pygame.quit()


        screen.fill("black")

        for obj in drawable:
            obj.draw(screen)

        draw_score(screen)
        pygame.display.flip()

        # limit the framerate to 60 FPS
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
