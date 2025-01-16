# Interstellar Attackers

import pygame
import random

WIDTH = 1366
HEIGHT = 768
stars = []

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1366, 768))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

# Load the spaceship image once (outside the loop for efficiency)
spaceship_image = pygame.image.load("spaceship.png")
spaceship_image = pygame.transform.scale(spaceship_image, (100, 100))

# Banking variables
bank_angle = 0  # Current bank angle
bank_speed = 200  # Speed of banking in degrees per second
max_bank_angle = 20  # Maximum tilt angle for banking

yspeed = 8
x = 1
y = 1

class Star(object):
    def __init__(self, x, y, yspeed):
        self.colour = (255, 255, 255)
        self.radius = 2
        self.x = x
        self.y = y
        self.yspeed = yspeed

    def draw(self):
        pygame.draw.circle(screen, self.colour, (self.x, self.y), self.radius)

    def fall(self):
        self.y += self.yspeed

    def check_if_i_should_reappear_on_top(self):
        if self.y >= HEIGHT:
            self.y = 0

for i in range(100):
    x = random.randint(1, WIDTH - 1)
    y = random.randint(1, HEIGHT - 1)
    stars.append(Star(x, y, yspeed))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    for star in stars:
        star.draw()
        star.fall()
        star.check_if_i_should_reappear_on_top()

    # WASD for movement
    keys = pygame.key.get_pressed()

    # Determine movement direction
    if keys[pygame.K_w]:
        player_pos.y -= 450 * dt
    if keys[pygame.K_s]:
        player_pos.y += 450 * dt

    # Determine banking direction
    if keys[pygame.K_a] and keys[pygame.K_d]:
        # Neutral banking if both A and D are pressed
        if bank_angle > 0:
            bank_angle -= bank_speed * dt
            bank_angle = max(0, bank_angle)  # Avoid overshooting
        elif bank_angle < 0:
            bank_angle += bank_speed * dt
            bank_angle = min(0, bank_angle)  # Avoid overshooting
    elif keys[pygame.K_a]:
        # Bank left
        player_pos.x -= 450 * dt
        bank_angle += bank_speed * dt
    elif keys[pygame.K_d]:
        # Bank right
        player_pos.x += 450 * dt
        bank_angle -= bank_speed * dt
    else:
        # Gradually return to neutral position when no A or D key is pressed
        if bank_angle > 0:
            bank_angle -= bank_speed * dt
            bank_angle = max(0, bank_angle)  # Avoid overshooting
        elif bank_angle < 0:
            bank_angle += bank_speed * dt
            bank_angle = min(0, bank_angle)  # Avoid overshooting

    if keys[pygame.K_ESCAPE]:
        break

    # Clamp the bank angle to the maximum limits
    bank_angle = max(-max_bank_angle, min(max_bank_angle, bank_angle))

    # Rotate the spaceship image for banking effect
    rotated_spaceship = pygame.transform.rotate(spaceship_image, bank_angle)

    # Adjust position to keep the rotation centered (avoid jitter)
    rotated_rect = rotated_spaceship.get_rect(center=(round(player_pos.x), round(player_pos.y)))

    # Draw the rotated spaceship
    screen.blit(rotated_spaceship, rotated_rect.topleft)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    dt = clock.tick(60) / 1000

pygame.quit()
