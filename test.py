import pygame
import random
import numpy as np

WIDTH, HEIGHT = 800, 600
ALIEN_WIDTH = 40
ALIEN_HEIGHT = 25
ALIEN_SPEED = 2
WHITE = (255, 255, 255)

class Bloom:
    def __init__(self, threshold=80, blur_iterations=5, blur_radius=80):
        self.threshold = threshold
        self.blur_iterations = blur_iterations
        self.blur_radius = blur_radius

    def apply_bloom(self, input_surface):
        # Convert the input surface to an array
        input_array = pygame.surfarray.array3d(input_surface)

        # Create a mask to identify bright pixels
        bright_pixels = np.sum(input_array, axis=2) > self.threshold

        # Blur the bright pixels horizontally
        for _ in range(self.blur_iterations):
            self._box_blur_horizontal(bright_pixels)

        # Blur the result vertically
        for _ in range(self.blur_iterations):
            self._box_blur_vertical(bright_pixels)

        # Create a new surface for the bloom effect
        bloom_surface = pygame.Surface(input_surface.get_size())
        bloom_surface.set_alpha(0)  # Set alpha to 0 to blend the bloom effect

        # Blend the original image with the bloom
        bloom_array = np.zeros_like(input_array)
        bloom_array[bright_pixels] = input_array[bright_pixels]
        pygame.surfarray.blit_array(bloom_surface, bloom_array)

        return bloom_surface

    def _box_blur_horizontal(self, pixels):
        for y in range(pixels.shape[0]):
            row = pixels[y, :]
            blurred_row = np.convolve(row, np.ones(self.blur_radius) / self.blur_radius, mode='same')
            pixels[y, :] = blurred_row > 0.5

    def _box_blur_vertical(self, pixels):
        for x in range(pixels.shape[1]):
            col = pixels[:, x]
            blurred_col = np.convolve(col, np.ones(self.blur_radius) / self.blur_radius, mode='same')
            pixels[:, x] = blurred_col > 0.5

class Alien(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load the alien sprite image
        # Initialize the surface and rect
        self.image = pygame.image.load("./sprites/alien.png").convert_alpha()
        self.image.set_colorkey(WHITE)  
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = 0 - ALIEN_HEIGHT
        
        self.speed = ALIEN_SPEED

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > HEIGHT:
            self.kill()


aliens = pygame.sprite.Group()

# Example usage
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Create a sample surface
sample_surface = pygame.Surface((WIDTH, HEIGHT))
pygame.draw.circle(sample_surface, (255, 255, 255), (400, 300), 50)

# Create a Bloom instance
bloom_effect = Bloom()

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if random.random() < 0.02:  # Add an alien with 2% probability each frame
        print("Adding an alien!")
        alien = Alien()
        aliens.add(alien)
    aliens.update()
    
    # Apply bloom effect
    bloom_surface = bloom_effect.apply_bloom(sample_surface)

    # Clear the screen
    screen.fill((0, 0, 0))

    # Blit the original surface
    screen.blit(sample_surface, (0, 0))

    # Blit the aliens
    aliens.draw(screen)

    # Blit the bloom effect
    screen.blit(bloom_surface, (0, 0), special_flags=pygame.BLEND_ADD)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()