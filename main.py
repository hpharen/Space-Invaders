import pygame
import random
import laser
import stars
import fade
import controls
import alien

# Initialize pygame
pygame.init()

# Fullscreen mode setup
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # 0, 0 auto-adjusts to full screen
WIDTH, HEIGHT = screen.get_width(), screen.get_height()  # Get the current screen size after fullscreen mode

# Initialize Fader
fader = fade.Fader(WIDTH, HEIGHT, fade_speed=90)
fader.start_fade_in()  # Trigger fade-in at the start of the game

# Initialize alien grid
alien_grid = alien.AlienGrid(WIDTH)

# Set up clock, running, delta time
clock = pygame.time.Clock()
running = True
dt = 0

# Player in game position
player_pos = pygame.Vector2(WIDTH / 2, HEIGHT / 2)

# Load the spaceship images once (outside of loop for efficiency)
spaceship_image = pygame.image.load("sprites/spaceship_shadow.png")
spaceship_fwd1 = pygame.image.load("sprites/spaceship_fwd1_shadow.png")
spaceship_fwd2 = pygame.image.load("sprites/spaceship_fwd2_shadow.png")
spaceship_fwd3 = pygame.image.load("sprites/spaceship_fwd3_shadow.png")

# Scale the images to match the desired size
spaceship_image = pygame.transform.scale(spaceship_image, (90, 90))
spaceship_fwd1 = pygame.transform.scale(spaceship_fwd1, (112, 112))
spaceship_fwd2 = pygame.transform.scale(spaceship_fwd2, (112, 112))
spaceship_fwd3 = pygame.transform.scale(spaceship_fwd3, (112, 112))

# Store them in a list for easier cycling
spaceship_fwd_images = [spaceship_fwd1, spaceship_fwd2, spaceship_fwd3]

# Banking variables
bank_angle = 0  # Current bank angle
bank_speed = 300  # Speed of banking in degrees per second
max_bank_angle = 10  # Maximum tilt angle for banking

# Animation control variables
fwd_index = 0  # Index to cycle through forward spaceship images
animation_timer = 0 # Timer to control the speed of animation change
animation_speed = 0.07  # Time in seconds between image swaps

# Initialize stars
star_manager = stars.StarManager(WIDTH, HEIGHT, num_stars=200, yspeed=12)

# Spacebar state
spacebar_pressed = False

# Initialize animation timer and spacebar state
animation_timer = 0  # Initialize timer for animation
spacebar_pressed = False  # Track spacebar press state

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # WASD for movement and other key events
    keys = pygame.key.get_pressed()

    # Escape key handling (quit the game)
    if keys[pygame.K_ESCAPE]:
        running = False

    # Handle controls and movement via the controls module
    player_pos, fwd_index, current_spaceship_image, bank_angle, spacebar_pressed, animation_timer = controls.handle_controls(
        keys, player_pos, dt, spaceship_image, spaceship_fwd_images, fwd_index, bank_angle, bank_speed, max_bank_angle, WIDTH, HEIGHT, spacebar_pressed, animation_timer
    )

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # Update and draw stars
    star_manager.update_and_draw(screen)

    # Update and draw lasers
    laser.update_lasers(dt, screen, WIDTH, HEIGHT)

    # Handle fade-in effect
    fader_active = fader.update(dt)  # Update fade and check if still active
    fader.draw(screen)  # Draw the fade effect on top of the screen

    # Draw the aliens
    alien_grid.draw(screen)

    # Draw the spaceship
    rotated_spaceship = pygame.transform.rotate(current_spaceship_image, bank_angle)
    rotated_rect = rotated_spaceship.get_rect(center=(round(player_pos.x), round(player_pos.y)))

    # Ensure spaceship stays within screen boundaries
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
