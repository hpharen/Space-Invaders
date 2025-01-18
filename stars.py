import pygame
import random

class Star:
    def __init__(self, x, y, yspeed):
        self.colour = (255, 255, 255)
        self.radius = 2
        self.x = x
        self.y = y
        self.yspeed = yspeed

    def draw(self, screen):
        pygame.draw.circle(screen, self.colour, (self.x, self.y), self.radius)

    def fall(self):
        self.y += self.yspeed

    def check_if_i_should_reappear_on_top(self, height):
        if self.y >= height:
            self.y = 0

class StarManager:
    def __init__(self, width, height, num_stars, yspeed):
        self.stars = []
        for _ in range(num_stars):
            x = random.randint(1, width - 1)
            y = random.randint(1, height - 1)
            self.stars.append(Star(x, y, yspeed))
        self.height = height

    def update_and_draw(self, screen):
        for star in self.stars:
            star.draw(screen)
            star.fall()
            star.check_if_i_should_reappear_on_top(self.height)
