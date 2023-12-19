import pygame
import sys
import random

LIMIT = 255

class Particle:
    def __init__(self, x, y):
        self.surf = pygame.Surface((random.randint(2, 8), random.randint(2, 8)))
        self.color = (random.randint(100, 255), random.randint(50, 200), 10)
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect(center=(x, y))
        self.lifetime = random.randint(40, 100)
        self.velocity = (random.uniform(-2, 2), random.uniform(-2, 2))

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        self.surf.set_alpha(((self.lifetime - 20)/20)*255)
        self.lifetime -= 1

class Star:
    def __init__(self):
        self.lifetime = 1
        self.pos = pygame.math.Vector2(random.randint(0, 800), random.randint(0, 600))
        self.up = False
        self.adder = random.randint(0, 200)
        # create a variable for size/mass that is normally distributed where the mean is 3
        # and the standard deviation is 0.5
        # size = random.normalvariate(6, 2)
        self.mass = pygame.math.Vector2(random.uniform(1, 10.0)  , random.uniform(1, 10.0)  )
        inverse_mass = 1.0 / (self.mass.x * self.mass.y)
        min_speed = 5.0
        max_speed = 10.0
        self.speed = min_speed + (max_speed - min_speed) * (inverse_mass - 1.0) / (9.0) # speed depends on size depends on normal distribution probability
        self.color = pygame.math.Vector3(random.randint(185, 255),random.randint(165, 255),random.randint(205, 255))

        self.surf = pygame.Surface(self.mass.xy, pygame.SRCALPHA)
        self.rect = self.surf.get_rect(center=self.pos.xy)
        self.surf.fill(self.color)

        if random.randint(1, 2) == 2:
            self.up = False
        else:
            self.up = True

    def update(self):
        if self.up:
            self.adder += 0.75 
            if self.adder >= LIMIT-1: 
                self.up = False
        else:
            self.adder -= 1
            if self.adder < 1:
                self.up = True
        self.rect.y += (self.speed)
        if(self.rect.y > 610):
            self.rect.y = -10;
        self.surf.set_alpha(self.adder)



# Particle Emitter class
class ParticleEmitter:
    def __init__(self):
        self.particles = []
        self.clock = pygame.time.Clock()
        self.update_interval = 40  # Update every 40 milliseconds (25 FPS)

    def create_particles(self, x, y, count=15, type=0):
        for _ in range(count):
            if type == 0:
                particle = Particle(x, y)
            else:
                particle = Star()
            self.particles.append(particle)

    def update(self):
        if self.clock.get_time() >= self.update_interval:
            for particle in self.particles:
                particle.update()
                if particle.lifetime <= 0:
                    self.particles.remove(particle)
            self.clock.tick()