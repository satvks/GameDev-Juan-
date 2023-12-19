import os
import sys
import math
import random
import pygame

import ParticleTypes.particles as particles
# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 30
ALIEN_WIDTH = 40
ALIEN_HEIGHT = 25
BULLET_WIDTH = 5
BULLET_HEIGHT = 15
PLAYER_SPEED = 8
BULLET_SPEED = 15
ALIEN_SPEED = 2
ALIEN_SPAWN_RATE = 0.0018

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invader")

# Classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./sprites/player.png").convert_alpha()
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 40))
        self.dx = 0
        self.dy = 0

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.dx = -PLAYER_SPEED
        elif keys[pygame.K_d]:
            self.dx = PLAYER_SPEED
        else:
            self.dx = 0

        self.rect.move_ip(self.dx, self.dy)
        self.rect.clamp_ip(screen.get_rect())  # Keep player inside the screen

class Alien(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load the alien sprite image
        self.image = pygame.image.load("./sprites/alien.png").convert_alpha()
        self.image.set_colorkey(WHITE)
        #self.surf.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = 0 - ALIEN_HEIGHT
        
        self.speed = ALIEN_SPEED

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.surf = pygame.Surface((BULLET_WIDTH, BULLET_HEIGHT))
        self.surf.fill(GREEN)
        self.rect = self.surf.get_rect(center=(x, y))

    def update(self):
        self.rect.move_ip(0, -BULLET_SPEED)
        if self.rect.bottom < 0:
            self.kill()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.surf = pygame.Surface((POWER_UP_SIZE, POWER_UP_SIZE))
        self.surf.fill(YELLOW)
        self.rect = self.surf.get_rect(center=(x, y))
        self.speed = 1

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# Helper Methods
def screen_shake(shake=False):
    if shake:
        shake_offset_x = random.randint(-10, 10)
        shake_offset_y = random.randint(-10, 10)
        for sprite in shake_sprites:
            screen.blit(sprite.image, (sprite.rect.x - shake_offset_x, sprite.rect.y - shake_offset_y))
        

# Additional constants
LIVES = 3
POWER_UP_SIZE = 25
POWER_UP_DROP_RATE = 0.003

# Colors
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

player_lives = LIVES
level = 1
power_ups = pygame.sprite.Group()

font = pygame.font.SysFont('Arial', 30)

# Main Loop
player = Player()
bullets = pygame.sprite.Group()
aliens = pygame.sprite.Group()
shake_sprites = pygame.sprite.Group()
ptics = particles.ParticleEmitter()

score = 0
shake_countdown = 0

clock = pygame.time.Clock()


ptics.create_particles(-1,-1,25,1)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = Bullet(player.rect.centerx, player.rect.top)
                bullets.add(bullet)

     # Screen clear and drawing
    screen.fill(BLACK)

    # Draw the score and lives on the screen
    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {player_lives}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)

    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 40))
    screen.blit(level_text, (SCREEN_WIDTH - 120, 10))

    player.move()
    screen.blit(player.image, player.rect)
    shake_sprites.add(player)

    if random.random() < ALIEN_SPAWN_RATE:  # Add an alien with 2% probability each frame
        alien = Alien()
        aliens.add(alien)
        shake_sprites.add(alien)
    
    bullets.update()
    aliens.update()

    # Collisions
    for bullet in bullets:
        screen.blit(bullet.surf, bullet.rect)

    bullet_alien_collisions = pygame.sprite.groupcollide(aliens, bullets, True, True)
    for alien in bullet_alien_collisions:
        ptics.create_particles(alien.rect.x,alien.rect.y)
        score += 10
    
    player_alien_collisions = pygame.sprite.spritecollide(player, aliens, True)
    if player_alien_collisions:
        player_alien_collisions[0].kill()
        player_lives -= 1
        if player_lives <= 0:
            running = False
        shake_countdown = 15
    if shake_countdown > 0:
        screen_shake(True)
        shake_countdown -= 1
    else:
        aliens.draw(screen)
    
    # Spawn power-ups occasionally
    if random.random() < POWER_UP_DROP_RATE:
        power_up = PowerUp(random.randint(0, SCREEN_WIDTH), 0)
        power_ups.add(power_up)

    power_ups.update()

    for power_up in power_ups:
        screen.blit(power_up.surf, power_up.rect)

    player_powerup_collisions = pygame.sprite.spritecollide(player, power_ups, True)
    for power_up in player_powerup_collisions:
        if(ALIEN_SPAWN_RATE < 0.0031):
            ALIEN_SPAWN_RATE += 0.0001875
        if(PLAYER_SPEED < 10):
            ALIEN_SPEED += 0.5
            PLAYER_SPEED += 1
        # For example, you can change this to other benefits

    # Check for level up
    if score > level * 50:
        level += 1

    for particle in ptics.particles:
            particle.update()
            ptics.update()
            screen.blit(particle.surf, particle.rect)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
