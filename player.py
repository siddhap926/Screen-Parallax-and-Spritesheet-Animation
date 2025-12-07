import pygame

class Character(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()

        # Load the spritesheet
        self.sheet = pygame.image.load('Images/character.png').convert_alpha()
        
        # Define sprite clip size
        self.sheet.set_clip(pygame.Rect(0, 0, 52, 76))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rect = self.image.get_rect()
        self.rect.topleft = position

        self.frame = 0
        self.direction = 'stand_right'

        # Add these ↓↓↓
        self.animation_timer = 0
        self.animation_speed = 0.15  # Lower = slower animation

        # Frame coordinates for each direction
        self.left_states = {0: (0, 76, 52, 76), 1: (52, 76, 52, 76), 2: (156, 76, 52, 76)}
        self.right_states = {0: (0, 152, 52, 76), 1: (52, 152, 52, 76), 2: (156, 152, 52, 76)}
        self.up_states = {0: (0, 228, 52, 76), 1: (52, 228, 52, 76), 2: (156, 228, 52, 76)}
        self.down_states = {0: (0, 0, 52, 76), 1: (52, 0, 52, 76), 2: (156, 0, 52, 76)}

    def get_frame(self, frame_set):
        # Use timer to control animation speed
        self.animation_timer += self.animation_speed
        if self.animation_timer >= 1:
            self.animation_timer = 0
            self.frame += 1
            if self.frame >= len(frame_set):
                self.frame = 0
        return frame_set[self.frame]

    def clip(self, clipped_rect):
        if isinstance(clipped_rect, dict):
            self.sheet.set_clip(pygame.Rect(self.get_frame(clipped_rect)))
        else:
            self.sheet.set_clip(pygame.Rect(clipped_rect))
        return clipped_rect

    def update(self, direction):
        self.direction = direction
        if direction == 'left':
            self.clip(self.left_states)
            self.rect.x -= 3  # Slightly slower movement
        elif direction == 'right':
            self.clip(self.right_states)
            self.rect.x += 3
        elif direction == 'stand_left':
            self.clip(self.left_states[0])
        elif direction == 'stand_right':
            self.clip(self.right_states[0])
        self.image = self.sheet.subsurface(self.sheet.get_clip())

    def handle_keys(self, keys):
        if keys[pygame.K_LEFT]:
            self.update('left')
        elif keys[pygame.K_RIGHT]:
            self.update('right')
        else:
            # Standing still
            if self.direction.startswith('left'):
                self.update('stand_left')
            else:
                self.update('stand_right')
