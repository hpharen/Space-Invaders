import pygame

# Laser speed (can be adjusted)
LASER_SPEED = 1000

# A list to store active lasers
active_lasers = []

class Laser:
    def __init__(self, x, y):
        self.x = x
        self.y = y - 20
        self.width = 4
        self.height = 60
        self.color = (200, 0, 0)  # Red color

    def move(self, dt):
        # Move the laser upwards
        self.y -= LASER_SPEED * dt

    def draw(self, screen):
        # Draw the laser as a rectangle
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

def fire_laser(x, y):
    """
    Fires a new laser from the given x, y position.
    """
    active_lasers.append(Laser(x, y))

def update_lasers(dt, screen, width, height):
    """
    Updates and draws all active lasers. Removes lasers that go off-screen.
    """
    for laser in active_lasers[:]:
        laser.move(dt)
        laser.draw(screen)
        # Remove laser if it goes off-screen
        if laser.y + laser.height < 0 or laser.y > height:
            active_lasers.remove(laser)
        if laser.x + laser.width < 0 or laser.x > width:
            active_lasers.remove(laser)
