import pygame

class Fader:
    def __init__(self, width, height, fade_speed=100):
        self.width = width
        self.height = height
        self.fade_speed = fade_speed  # Slow down fade speed by increasing this value
        self.alpha = 255  # Start at fully opaque (black)
        self.fading_in = False
        self.fading_out = False

    def start_fade_in(self):
        """Start the fade-in effect."""
        self.alpha = 255  # Start opaque
        self.fading_in = True
        self.fading_out = False

    def start_fade_out(self):
        """Start the fade-out effect."""
        self.alpha = 0  # Start transparent
        self.fading_out = True
        self.fading_in = False

    def update(self, dt):
        """Update the fade effect based on delta time."""
        if self.fading_in:
            self.alpha -= self.fade_speed * dt
            if self.alpha <= 0:
                self.alpha = 0  # Prevent going below 0
                self.fading_in = False  # Stop fading in

        elif self.fading_out:
            self.alpha += self.fade_speed * dt
            if self.alpha >= 255:
                self.alpha = 255  # Prevent going above 255
                self.fading_out = False  # Stop fading out
        
        return self.fading_in or self.fading_out

    def draw(self, screen):
        """Draw the fade effect."""
        fade_surface = pygame.Surface((self.width, self.height))
        fade_surface.fill((0, 0, 0))  # Black overlay
        fade_surface.set_alpha(self.alpha)  # Apply transparency
        screen.blit(fade_surface, (0, 0))  # Draw the fade surface onto the screen
