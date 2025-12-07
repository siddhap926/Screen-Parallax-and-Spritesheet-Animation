import pygame
from player import Character

pygame.init()

# Logical render size
SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 500

# Create the window and set a title
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Midterm")

# Master timing
clock = pygame.time.Clock()
player = Character((300, 370))
FPS = 60

# -------------------------------------------------------------------
# SCROLL STATE
# -------------------------------------------------------------------
# Global horizontal camera scroll measured in pixels.
# Positive values mean "camera" moved to the right, so backgrounds
# slide to the left. You drive this with LEFT/RIGHT keys below.
scroll = 0

# -------------------------------------------------------------------
# ASSET LOADING (switched from BG1/* to Images/*, and 5 layers total)
# -------------------------------------------------------------------
ground_image = pygame.image.load("Images/ground.png").convert_alpha()

bg_images = []
for i in range(1, 6):  # plx-1 (nearest) ... plx-5 (farthest)
    img = pygame.image.load(f"Images/plx-{i}.png").convert_alpha()
    bg_images.append(img)

# Dimensions based on the first background image and ground
bg_width = bg_images[0].get_width()
ground_width = ground_image.get_width()
ground_height = ground_image.get_height()

# -------------------------------------------------------------------
# PARALLAX SPEEDS
# -------------------------------------------------------------------
# Speed multipliers for each background layer. Index 0 corresponds to
# plx-1 (nearest), index 4 to plx-5 (farthest). Bigger numbers move faster.
# Kept original four speeds and added one slower far layer.
layer_speeds = [0.25, 0.15, 0.09, 0.05, 0.03]

def crop_edges(surface, left=1, right=1, top=0, bottom=0):
    """
    Returns a copy of 'surface' cropped by the given number of pixels on
    each side. Use this when your art has a 1 px transparent border that
    can create a visible seam at tile joins.
    """
    w, h = surface.get_width(), surface.get_height()
    rect = pygame.Rect(left, top, max(1, w - left - right), max(1, h - top - bottom))
    return surface.subsurface(rect).copy()

# If your images include a 1 px transparent pad, this removes it to reduce seams.
# If your assets are already perfectly seamless, comment these lines out.
bg_images = [crop_edges(img, left=1, right=1) for img in bg_images]

# Scale background layers by height (preserve aspect ratio), not the ground
#missing

bg_width = bg_images[0].get_width()  # refresh width after cropping

ground_image = crop_edges(ground_image, left=1, right=1)
ground_width = ground_image.get_width()

# -------------------------------------------------------------------
# TILE OVERLAP
# -------------------------------------------------------------------
OVERLAP_X = 1

def draw_tiled_layer(img, speed, y, overlap=OVERLAP_X):
    """
    Tiles 'img' across the screen at vertical position 'y' while applying
    horizontal parallax based on global 'scroll' and the given 'speed'.
    """
    w = img.get_width()
    step = max(1, w - overlap)          # overlap tiling to hide seams
    offset = int((-scroll * speed) % step)
    start_x = -w + offset
    tiles = (SCREEN_WIDTH // step) + 3
    for i in range(tiles):
        x = start_x + i * step
        screen.blit(img, (x, y))

# -------------------------------------------------------------------
# DRAW ORDER AND PER-LAYER Y POSITIONS
# -------------------------------------------------------------------
# Draw one layer at a time (manual calls), following the original style.
def draw_bg():
    # New farthest layer: plx-5 (index 4)
    draw_tiled_layer(bg_images[0], layer_speeds[0], 0)

    # Farthest among the original four (now second-farthest overall)
    draw_tiled_layer(bg_images[1], layer_speeds[1],0)           # default 1 px overlap

    # Mid-far background
    draw_tiled_layer(bg_images[2], layer_speeds[2], 0)      # 0 overlap, try 1..3 if seams

    # Mid-near background
    draw_tiled_layer(bg_images[3], layer_speeds[3], 0)     # larger overlap if needed

    # Nearest background
    draw_tiled_layer(bg_images[4], layer_speeds[4], 0)      # 2 px overlap for safety

def draw_ground():
    """
    Optional separate ground draw helper in case you want to control when
    the ground is drawn relative to other sprites.
    """
    ground_speed = 2.2
    draw_tiled_layer(ground_image, ground_speed, 430)

# -------------------------------------------------------------------
# MAIN LOOP
# -------------------------------------------------------------------
run = True
while run:
    clock.tick(FPS)

    # Clear the screen.
    screen.fill((0, 0, 0))

    # Draw background layers from far to near (manual sequence)
    draw_bg()

    # Optional extra ground draw. (Kept from original)
    draw_ground()

    # Keyboard input for manual camera scrolling
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and scroll > 0:
        scroll -= 5  # move camera left
    if key[pygame.K_RIGHT] and scroll < 3000:
        scroll += 5  # move camera right
    
    player.handle_keys(key)
    screen.blit(player.image, player.rect)
    pygame.display.flip()

    # Basic window events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Present the frame
    pygame.display.update()

pygame.quit()
