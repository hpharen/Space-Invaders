import pygame
import laser

def handle_controls(keys, player_pos, dt, spaceship_image, spaceship_fwd_images, spaceship_fwd_index, bank_angle, bank_speed, max_bank_angle, WIDTH, HEIGHT, spacebar_pressed):
    # Animation control variables
    fwd_index = spaceship_fwd_index  # Index to cycle through forward spaceship images
    animation_timer = 0  # Timer to control the speed of animation change
    animation_speed = 0.07  # Time in seconds between image swaps

    # Handle spacebar press for firing laser
    if keys[pygame.K_SPACE]:
        if not spacebar_pressed:  # Fire laser only if the spacebar was not already pressed
            laser.fire_laser(player_pos.x, player_pos.y - 50)
            spacebar_pressed = True  # Set flag to prevent further firing until released
    else:
        spacebar_pressed = False  # Reset flag when spacebar is released

    # Set the spaceship image depending on the W key
    if keys[pygame.K_w]:
        # Cycle through forward images while W is pressed
        animation_timer += dt
        if animation_timer >= animation_speed:
            fwd_index = (fwd_index + 1) % len(spaceship_fwd_images)
            animation_timer = 0
        current_spaceship_image = spaceship_fwd_images[fwd_index]  # Use forward-facing spaceship image
    else:
        current_spaceship_image = spaceship_image  # Use default spaceship image when W is not pressed

    # Determine movement direction, with boundary checks
    if keys[pygame.K_w]:
        if player_pos.y > 0:  # Prevent going off the top
            player_pos.y -= 625 * dt
    if keys[pygame.K_s]:
        if player_pos.y < HEIGHT:  # Prevent going off the bottom
            player_pos.y += 500 * dt

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
            player_pos.x -= 500 * dt
        bank_angle += bank_speed * dt
    elif keys[pygame.K_d]:
        # Bank right
        if player_pos.x < WIDTH:  # Prevent going off the right edge
            player_pos.x += 500 * dt
        bank_angle -= bank_speed * dt
    else:
        # Gradually return to neutral position when no A or D key is pressed
        if bank_angle > 0:
            bank_angle -= bank_speed * dt
            bank_angle = max(0, bank_angle)  # Avoid overshooting
        elif bank_angle < 0:
            bank_angle += bank_speed * dt
            bank_angle = min(0, bank_angle)  # Avoid overshooting

    # Clamp the bank angle to the maximum limits
    bank_angle = max(-max_bank_angle, min(max_bank_angle, bank_angle))

    return player_pos, fwd_index, current_spaceship_image, bank_angle, spacebar_pressed
