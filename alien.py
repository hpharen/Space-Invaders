import pygame

class Alien:
    def __init__(self, x, y, image):
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (70, 60))  # Scale aliens to fit better
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

class AlienGrid:
    def __init__(self, rows=3, cols=8, spacing=20):
        self.aliens = []
        alien_images = ["sprites/alien1.png", "sprites/alien2.png", "sprites/alien3.png"]
        start_x, start_y = 100, 100  # Starting position of the alien grid
        
        for row in range(rows):
            for col in range(cols):
                x = start_x + col * (80 + spacing)
                y = start_y + row * (80 + spacing)
                alien = Alien(x, y, alien_images[row % len(alien_images)])
                self.aliens.append(alien)

    def draw(self, screen):
        for alien in self.aliens:
            alien.draw(screen)
