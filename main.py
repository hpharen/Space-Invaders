import pygame
import random

# pygame setup
pygame.init()

# Fullscreen mode setup
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # 0, 0 auto-adjusts to full screen
WIDTH, HEIGHT = screen.get_width(), screen.get_height()  # Get the current screen size after fullscreen mode

# Set up clock, running, and other variables
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(WIDTH / 2, HEIGHT / 2)

# Load the spaceship images once (outside the loop for efficiency)
spaceship_image = pygame.image.load("spaceship.png")
spaceship_image = pygame.transform.scale(spaceship_image, (100, 100))
spaceship_fwd_image = pygame.image.load("spaceship_fwd.png")
spaceship_fwd_image = pygame.transform.scale(spaceship_fwd_image, (128, 128))

# Banking variables
bank_angle = 0  # Current bank angle
bank_speed = 300  # Speed of banking in degrees per second
max_bank_angle = 20  # Maximum tilt angle for banking

stars = []
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

    # Set the spaceship image depending on the W key
    if keys[pygame.K_w]:
        current_spaceship_image = spaceship_fwd_image  # Use forward-facing spaceship image when W is pressed
    else:
        current_spaceship_image = spaceship_image  # Use default spaceship image when W is not pressed


    # Determine movement direction, with boundary checks
    if keys[pygame.K_w]:
        if player_pos.y > 0:  # Prevent going off the top
            player_pos.y -= 525 * dt
    if keys[pygame.K_s]:
        if player_pos.y < HEIGHT:  # Prevent going off the bottom
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
        if player_pos.x > 0:  # Prevent going off the left edge
            player_pos.x -= 450 * dt
        bank_angle += bank_speed * dt
    elif keys[pygame.K_d]:
        # Bank right
        if player_pos.x < WIDTH:  # Prevent going off the right edge
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
    rotated_spaceship = pygame.transform.rotate(current_spaceship_image, bank_angle)


    # Adjust position to keep the rotation centered (avoid jitter)
    rotated_rect = rotated_spaceship.get_rect(center=(round(player_pos.x), round(player_pos.y)))

    # Ensure spaceship stays within screen boundaries
    # Prevent spaceship from going out of bounds
    if rotated_rect.left < 0:
        rotated_rect.left = 0
    if rotated_rect.right > WIDTH:
        rotated_rect.right = WIDTH
    if rotated_rect.top < 0:
        rotated_rect.top = 0
    if rotated_rect.bottom > HEIGHT:
        rotated_rect.bottom = HEIGHT

    # Draw the rotated spaceship
    screen.blit(rotated_spaceship, rotated_rect.topleft)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    dt = clock.tick(60) / 1000

pygame.quit()
